# UrbanAir data versions
from dataclasses import dataclass


@dataclass
class UrbanAirData:
    data_info = {
        "Antwerpen": {"nx": 139, "ny": 139, "dx": 500},
        "Paris": {"nx": 989, "ny": 989, "dx": 500},
        "Paris_7.1": {
            "nx": 989,
            "ny": 989,
            "dx": 500,
            "date": "2023-08-20T00:00:00Z",
            "forecast_range": "PT36H",
            "output_frequency": "PT15M",
            "fdb": {
                "expver": "aabg",
                "georef": "u09tvk",
             },
            "polytope": {
                "collection": "deode",
                "url": "polytope-test.ecmwf.int",
            },
        },
        "Paris_8.0": {
            "nx": 989,
            "ny": 989,
            "dx": 500,
            "date": "2023-08-20T00:00:00Z",
            "forecast_range": "PT48H",
            "output_frequency": "PT15M",
            "fdb": {
                "expver": "aad4",
                "georef": "u09tvk",
             },
            "polytope": {
                "collection": "deode",
                "url": "polytope-test.ecmwf.int",
            },
        },
    }
    urls = {
        "4": {
            "name": "Antwerpen test",
            "url": "http://exporter.nsc.liu.se/28e80f79cad547988e7a0b64809e0dc3",
            "metadata": data_info["Antwerpen"],
        },
        "5.0": {
            "name": "Antwerpen",
            "url": "http://exporter.nsc.liu.se/1c333ab5ee374ab2acb470b2870cc02e",
            "metadata": data_info["Antwerpen"],
        },
        "6.1": {
            "name": "Paris",
            "url": "http://exporter.nsc.liu.se/284818358def438b8c142f4223c96936",
            "metadata": data_info["Paris"],
        },
        "7.1": {
            "name": "Paris 7.1",
            "url": "http://exporter.nsc.liu.se/f1559d3fb24e47b5b9b3f77905a8bcba",
            "metadata": data_info["Paris_7.1"],
        },
        "8.0": {
            "name": "Paris 8.0",
            "url": None,
            "metadata": data_info["Paris_8.0"],
        },
    }
    current_version = list(urls)[-1]
    base_url = urls[current_version]["url"]

    def __repr__(self):
        return "UrbanAirData"

    def __str__(self):
        txt = "Available versions:\n"
        for k, v in self.urls.items():
            txt += f"  v{k}:\n"
            for x, y in v.items():
                if isinstance(y,dict):
                    for z, u in y.items():
                        txt += f"     {z}: {u}\n"
                else:
                    txt += f"    {x}: {y}\n"
        return txt

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
