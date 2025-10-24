# UrbanAir data versions
from dataclasses import dataclass

@dataclass
class UrbanAirData:

    urls = { 
            "4": { "url" : "http://exporter.nsc.liu.se/28e80f79cad547988e7a0b64809e0dc3", "doc": "Antwerpen test"},
            "5.0": { "url": "http://exporter.nsc.liu.se/1c333ab5ee374ab2acb470b2870cc02e", "doc": "Antwerpen"},
            "6.1": { "url": "http://exporter.nsc.liu.se/284818358def438b8c142f4223c96936", "doc": "Paris" },
    }
    current_version = list(urls)[-1]
    base_url = urls[current_version]["url"]

    def __repr__(self):
        return("UrbanAirData")
    def __str__(self):
        txt = "Available versions:\n"
        for k, v in self.urls.items():
            txt += f"  {k}: {v}\n"
        return(txt)

    def url_version(self, version=None):

        if version is None:
            version = self.current_version
        try:
            if not isinstance(version, str):
                version = str(version)
            url = self.urls[version]["url"]
        except KeyError:
            print(f"Version {version} is not available")
            print(self)
            url = None

        return url
