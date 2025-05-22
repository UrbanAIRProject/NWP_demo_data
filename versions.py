# UrbanAir data versions
class UrbanAirData:
    urls = { 4: "http://exporter.nsc.liu.se/8a930c993fe54eedbdd7d4451b45ea57" }
    current_version = 4
    base_url = urls[current_version]

def url_version(version):

    try:
       url = UrbanAirData.urls[version]
    except KeyError:
       print(f"Version {version} is not available")
       print(f"Available versions are: {list(UrbanAirData.urls.keys())}")
       url = None

    return url
