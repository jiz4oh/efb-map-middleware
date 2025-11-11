from typing import Optional

from ehforwarderbot import Middleware, Message, MsgType
from ehforwarderbot.message import LocationAttribute
from ehforwarderbot.types import ModuleID, InstanceID
from urllib.parse import urlparse, parse_qs, unquote
import requests as requests
import copy


class MapMiddleware(Middleware):
    middleware_id: ModuleID = ModuleID("jiz4oh.map")
    middleware_name: str = "Map Middleware"
    __version__: str = "0.1.0"

    def __init__(self, instance_id: Optional[InstanceID] = None):
        super().__init__(instance_id)

    @staticmethod
    def parse_amap_url(url: str):
        if not url.startswith("https://surl.amap.com"):
            return None
        try:
            response = requests.get(url, allow_redirects=False)
            location = response.headers.get("Location")
            if location:
                parsed = urlparse(location)
                params = parse_qs(parsed.query)
                if "p" in params:
                    p_param = unquote(params["p"][0])
                    parts = p_param.split(",")

                    if len(parts) >= 5:
                        poiid, lat, lng, name, address = parts[:5]
                        msg = Message(type=MsgType.Location, text=name)
                        msg.attributes = LocationAttribute(
                            latitude=float(lat), longitude=float(lng)
                        )
                        return msg
        except Exception as e:
            return None
        return None

    def process_message(self, message: Message) -> Optional[Message]:
        if message.type == MsgType.Link:
            m = self.parse_amap_url(message.attributes.url)
            if m:
                msg = copy.deepcopy(message)
                msg.type = m.type
                msg.text = m.text
                msg.attributes = m.attributes
                return msg
        return message
