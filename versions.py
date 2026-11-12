# UrbanAir data versions
from dataclasses import dataclass
import argparse
import json
import os
import sys


VERSIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json", "versions.json")


def load_versions(path=VERSIONS_FILE):
    with open(path, "r", encoding="utf-8") as f:
        content = json.load(f)
    data_info = content["data_info"]
    urls = {}
    for version, info in content["urls"].items():
        city = info.pop("city")
        if version not in data_info.get(city, {}):
            raise KeyError(f'{version} is not in data_info["{city}"] of {path}')
        info["metadata"] = data_info[city][version]
        urls[version] = info
    return data_info, urls


@dataclass
class UrbanAirData():
    data_info, urls = load_versions()
    current_version = list(urls)[-1]
    base_url = urls[current_version]["url"]

    def __repr__(self):
        return "UrbanAirData"

    def dict_print(self, d, indent=0, prefix=""):
        txt = ""
        for k, v in d.items():
            for i in range(0, indent):
                txt += " "
            if isinstance(v, dict):
                txt += f"{prefix}{k}:\n"
                txt += self.dict_print(v, indent + 1)
            else:
                txt += f"{k}: {v}\n"
        return txt

    def __str__(self):
        txt = "Available versions:\n"
        txt += self.dict_print(self.urls, 1, prefix="\n")

        return txt

    def expver(self, version=None):
        if version is None:
            version = self.current_version
        return self.urls[version]["metadata"].get("fdb", {}).get("expver")

    def list_versions(self, version=None):
        print(f"Current version: {self.current_version}\n")
        if version is not None and str(version) not in self.urls:
            print(f"KeyError: {version} is not listed")
            version = None
        for city, versions in self.data_info.items():
            rows = [
                (v, self.urls[v])
                for v in versions
                if v in self.urls and (version is None or v == str(version))
            ]
            if not rows:
                continue
            print(f"{city}:")
            print(f"  {'version':<8} {'expver':<8} {'modelName':<16} {'DxInMetres'}")
            for v, info in rows:
                expver = info["metadata"].get("fdb", {}).get("expver", "-")
                model = info["metadata"].get("modelName", "-")
                dx = info["metadata"].get("DxInMetres", "-")
                print(f"  {v:<8} {expver:<8} {model:<16} {dx}")
            print()

    def update_data_info(self, version, keys):
        city = next((c for c, v in self.data_info.items() if version in v), None)
        if city is None:
            return
        meta = self.data_info[city][version]
        new = {**keys, **meta}
        if new == meta and list(new) == list(meta):
            return
        meta.clear()
        meta.update(new)
        with open(VERSIONS_FILE, "r", encoding="utf-8") as f:
            content = json.load(f)
        content["data_info"][city][version] = {**keys, **content["data_info"][city][version]}
        with open(VERSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4)
            f.write("\n")

    def show(self, version=None, full=False):
        if version is None:
            version = self.current_version

        if version not in self.urls:
            print(f"KeyError: {version} is not listed")
            self.list_versions()
            return

        json_file = self.urls[version]["metadata"].get("json")
        toc = None
        if json_file is not None:
            path = json_file if os.path.exists(json_file) else os.path.join(os.path.dirname(VERSIONS_FILE), os.path.basename(json_file))
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    toc = json.load(f)
                meta_data = toc.get("meta_data", {})
                if meta_data:
                    self.update_data_info(version, meta_data)

        txt = self.dict_print(self.urls[version], 1, prefix="\n")
        print(txt)

        if not full:
            return

        import pydoc
        if json_file is None:
            print(f"No json content available for version {version}")
            return
        if toc is None:
            print(f"json file not found: {json_file}")
            return

        title = f'\t\t ---- Data available from polytope ( from {json_file} ) --- \n'
        formatted_json = title + json.dumps(toc, indent=4)
        pydoc.pager(formatted_json)


    def url_version(self, version=None):
        if version is None:
            version = self.current_version
        try:
            if not isinstance(version, str):
                version = str(version)
            url = self.urls[version]["url"]
            if 'liu.se' not in url:
                print(f"Version {version} does not have an lie.se url.")
                print(f"Run 'python download.py -l' for available versions")
                url = None
        except KeyError:
            print(f"KeyError: {version} is not listed")
            print(self)
            url = None

        return url

    def print_url_versions(self):
        import pprint
        print("\n\t\t -- Data versions available for direct (url) download  --\n")
        for url in self.urls:
            if 'exporter.nsc.liu.se' in self.urls[url]['url']:
                print(f"version : {url} \n")
                pprint.pprint(self.urls[url])

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Inspect the UrbanAir data versions")
    parser.add_argument(
        "-l",
        "--list",
        dest="list",
        action="store_true",
        help="List the available versions",
        required=False,
        default=False,
    )
    parser.add_argument(
        "-v",
        "--version",
        dest="version",
        help="Print the header information of a specific version",
        required=False,
        default=None,
    )
    parser.add_argument(
        "-f",
        "--full",
        dest="full",
        metavar="VERSION",
        help="Print the full information of a specific version, including the json content",
        required=False,
        default=None,
    )

    args = parser.parse_args()

    uad = UrbanAirData()
    if args.list:
        uad.list_versions(args.version)
        sys.exit()

    if args.full is not None:
        uad.show(args.full, full=True)
        sys.exit()

    uad.show(args.version)
