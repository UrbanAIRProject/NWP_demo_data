import os
import pyfdb

fdb_rules = {
  "grib_set": {
   "centre": "98",
   "class": "d1",
   "dataset": "on-demand-extremes-dt",
   # Don't change expver!
   "expver": "test",
   "grib2LocalSectionNumber": "1",
   "productionStatusOfProcessedData": "12",
   "setLocalDefinition": "1",
   "stream": "oper",
   "tablesVersion": "34",
   "type": "fc",
   # Update date and time to match your data
   "date": "20261003",
   "time": "0000",
    },
  "negative_rules": {
      "levtype": ["unknown"],
      "param": ["0"],
      "productDefinitionTemplateNumber": ["113", "114"],
      "typeOfLevel": ["unknown", "not_found"],
    },
  }


class FDB():

    def __init__(self):
        self.fdb_rules = fdb_rules
        self.fdb = pyfdb.FDB()
        self.request = {k:self.fdb_rules["grib_set"][k] for k in ("class","expver","dataset","stream","date","time")}

    def prepare_data(self, filename):
        rules = self.fdb_rules.get("negative_rules", {})
        grib_set = { x:y for x, y in self.fdb_rules.get("grib_set").items() }
        temp1 = f"{filename}_temp1.grib"
        self.temp2 = f"{filename}_temp2.grib"
        rules_file = "temp_rules"
        self._write_rules_file(rules_file, rules, neg="!")
        cmd_filter = f"grib_filter {rules_file} {filename} -o {temp1}"
        #print(f"\nFilter file with command: {cmd_filter}")
        os.system(cmd_filter)
        set_values = ",".join(
                [f"{key}={value}" for key, value in grib_set.items() if value]
        )
        cmd_for_grib = "grib_set -s " + set_values + f" {temp1} {self.temp2}"
        #print(f"\nSet grib parameters with command: {cmd_for_grib}")
        os.system(cmd_for_grib)

    def archive(self):

        with open(self.temp2, "rb") as infile:
                self.fdb.archive(infile.read())
        self.fdb.flush()

    def _write_rules_file(self, filename, rules, neg="", oper=" && "):
        if bool(rules):
            x = [
                f'{neg}({name} is "{value}")'
                for name, values in rules.items()
                for value in values
            ]
            rule = "if (" + oper.join(x) + ") { append; }\n"
        else:
            rule = "append;\n"
        with open(filename, "w") as outfile:
            outfile.write("set edition = 2;\n")
            outfile.write(rule)

    def wipe_fdb(self):
      # Remove the new data from fdb
      fdb_sel = ",".join(
          [f"{key}={value}" for key, value in self.request.items()]
      )
      cmd = f"fdb wipe {fdb_sel} --doit"
      print(f"\nClean FDB with command: {cmd}")
      os.system(cmd)

    def check_fdb(self):
        recorded_dates = {}
        for entry in pyfdb.list(self.request, keys=True):
          date = entry["keys"]["date"]
          if date not in recorded_dates:
            recorded_dates[date] = []
            for key in ("stream", "type", "expver", "georef", "param", "levtype"):
              x = entry["keys"][key]
              if x not in recorded_dates[date]:
                recorded_dates[date].append({key:x})

        print("Found:", recorded_dates)



def compute_georef(domain_config):
    """Computes georef from domain_config."""
    lat_center = domain_config["xlatcen"]
    lon_center = domain_config["xloncen"]

    return geohash.encode(longitude=lon_center, latitude=lat_center, precision=6)

def check_fdb_env():
    # Set FDB environment for atos
    os.environ["FDB_HOME"] = "/home/fdbtest"
    try:
        os.environ["FDB5_HOME"] = os.environ["ECMWF_TOOLBOX_DIR"]
    except:
        raise KeyError("Make sure to load ecmwf-toolbox before your start")

def main():

    check_fdb_env()

    filename = "examples/t2m.grib2"
    fdb = FDB()
    # Update grib records
    fdb.prepare_data(filename)
    # Push to fdb
    fdb.archive()
    # Check for the data
    fdb.check_fdb()
    # Clean fdb again, as this is a test
    fdb.wipe_fdb()


if __name__=='__main__':
    main()

