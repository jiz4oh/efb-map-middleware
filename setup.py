from setuptools import setup, find_packages

setup(
    name="efb-map-middleware",
    packages=find_packages(),
    version="0.1.1",
    description="parse amap url",
    author="jiz4oh",
    author_email="me@jiz4oh.com",
    url="https://github.com/jiz4oh/efb-map-middleware.git",
    include_package_data=True,
    install_requires=[
        "ehforwarderbot>=2.0.0",
        "requests"
    ],
    entry_points={
        "ehforwarderbot.middleware": "jiz4oh.map=efb_map_middleware:MapMiddleware",
    },
)
