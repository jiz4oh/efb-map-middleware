import importlib
import pathlib
import sys
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module():
    for name in list(sys.modules):
        if name == "efb_map_middleware" or name.startswith("efb_map_middleware.") or name.startswith("ehforwarderbot"):
            sys.modules.pop(name, None)

    ehforwarderbot = types.ModuleType("ehforwarderbot")

    class Middleware:
        def __init__(self, instance_id=None):
            self.instance_id = instance_id

    class MsgType:
        Link = "Link"
        Location = "Location"
        Text = "Text"

    class Message:
        def __init__(self, *, type=None, text="", chat=None, author=None, deliver_to=None, attributes=None):
            self.type = type
            self.text = text
            self.chat = chat
            self.author = author
            self.deliver_to = deliver_to
            self.attributes = attributes

    ehforwarderbot.Middleware = Middleware
    ehforwarderbot.Message = Message
    ehforwarderbot.MsgType = MsgType
    sys.modules["ehforwarderbot"] = ehforwarderbot

    message_module = types.ModuleType("ehforwarderbot.message")

    class LocationAttribute:
        def __init__(self, latitude, longitude):
            self.latitude = latitude
            self.longitude = longitude

    message_module.LocationAttribute = LocationAttribute
    sys.modules["ehforwarderbot.message"] = message_module

    types_module = types.ModuleType("ehforwarderbot.types")
    types_module.ModuleID = str
    types_module.InstanceID = str
    sys.modules["ehforwarderbot.types"] = types_module

    requests_module = types.ModuleType("requests")
    requests_module.get = lambda *args, **kwargs: None
    sys.modules["requests"] = requests_module

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    return importlib.import_module("efb_map_middleware")


class TestMapMiddleware(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()
        self.middleware = self.mod.MapMiddleware()

    def test_process_message_preserves_message_context_when_replacing_link(self):
        original_attributes = types.SimpleNamespace(url="https://surl.amap.com/demo")
        message = self.mod.Message(
            type=self.mod.MsgType.Link,
            text="before",
            chat=object(),
            author=object(),
            deliver_to=object(),
            attributes=original_attributes,
        )

        location_message = self.mod.Message(type=self.mod.MsgType.Location, text="poi")
        location_message.attributes = self.mod.LocationAttribute(25.0, 121.0)
        self.middleware.parse_amap_url = lambda url: location_message

        result = self.middleware.process_message(message)

        self.assertIsNot(result, message)
        self.assertIs(result.chat, message.chat)
        self.assertIs(result.author, message.author)
        self.assertIs(result.deliver_to, message.deliver_to)
        self.assertEqual(result.type, self.mod.MsgType.Location)
        self.assertEqual(result.text, "poi")
        self.assertEqual(result.attributes.latitude, 25.0)
        self.assertEqual(result.attributes.longitude, 121.0)
        self.assertEqual(message.type, self.mod.MsgType.Link)
        self.assertEqual(message.text, "before")
        self.assertIs(message.attributes, original_attributes)

    def test_process_message_returns_original_when_link_has_no_attributes(self):
        message = self.mod.Message(type=self.mod.MsgType.Link, text="before", attributes=None)

        result = self.middleware.process_message(message)

        self.assertIs(result, message)


if __name__ == "__main__":
    unittest.main()
