# UrbanAir data versions
from dataclasses import dataclass

@dataclass
class UrbanAirData:

    urls = { 
        "0.0": "http://exporter.nsc.liu.se/ff8ec3701cb946fc9ed09b34bbc94f01",
        "4": "http://exporter.nsc.liu.se/8a930c993fe54eedbdd7d4451b45ea57",
        "5.0": "http://exporter.nsc.liu.se/1c333ab5ee374ab2acb470b2870cc02e",
        "0.1": "http://exporter.nsc.liu.se/75e34a3e256a45c38b88bb3b6232f71a",
    }
    current_version = list(urls)[-1]
    base_url = urls[current_version]

    def __repr__(self):
        return("UrbanAirData")
    def __str__(self):
        txt = "Test data versions:\n"
        for k, v in self.urls.items():
            txt += f"  {k}: {v}\n"
        return(txt)

    def url_version(self, version=None):

        if version is None:
            version = self.current_version
        try:
            if not isinstance(version, str):
                version = str(version)
            url = self.urls[version]
        except KeyError:
            print(f"Version {version} is not available")
            print(f"Available versions are: {list(self.urls.keys())}")
            url = None

        return url
