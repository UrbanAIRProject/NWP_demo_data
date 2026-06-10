import copy
import os
import sys
import re
import json

os.environ["FDB5_HOME"] = os.environ["ECMWF_TOOLBOX_DIR"]
os.environ["FDB_HOME"] = "/home/fdbtest"
USER = os.environ["USER"]

import pyfdb
import shutil


def get_data(request):
    levtype = request["levtype"]
    if levtype in ("sfc"):
        ret = {}
    elif levtype in ("hl", "pl", "ml"):
        ret = {}

    j = 0
    for x in pyfdb.list(request, keys=True):
        y = x["keys"]
        if levtype == "sfc":
            step, param = y["step"], y["param"]
            if step not in ret:
                ret[step] = []
            if param not in ret[step]:
                ret[step].append(param)
            else:
                print("Warning:", param)
                print(y)
        else:
            step, param, levelist = y["step"], y["param"], y["levelist"]
            if step not in ret:
                ret[step] = {}
            if levelist not in ret[step]:
                ret[step][levelist] = []
            if param in ret[step][levelist]:
                print(param)
                sys.exit()
            ret[step][levelist].append(param)

    return ret


def reduce_one(ret, match_key, append_key, reduce_single=True):
    _ret = copy.deepcopy(ret)
    x, param = _ret.popitem()
    regret = [{append_key: [x], match_key: param}]
    i = 0
    for x, y in _ret.items():
        found = False
        for j in range(0, i + 1):
            if set(regret[j][match_key]) == set(y):
                found = True
                regret[j][append_key].append(x)
        if not found:
            i += 1
            regret.append({append_key: [x], match_key: y})

    if len(regret) == 1 and reduce_single:
        regret = regret[0]
    return regret


def print_ret(ret):
    for x, y in ret.items():
        print("\nX:", x)
        try:
         for z,w in y.items():
          print("\nY:", z)
          print("  ", w, "\n")
        except:
          print("\nY:", y)


def sort_ret(ret):

    newret = copy.deepcopy(ret)
    for i in range(0,len(newret)):
        newret[i]["param"].sort(key=int)
        newret[i]["step"].sort(key=to_minutes)
        if "levelist" in newret[i]:
          newret[i]["levelist"].sort(key=int)
        
    return newret

def to_minutes(s):

    if "h" in s and "m" in s:
      h, m = re.match(r"(\d+)h(\d+)m", s).groups()
    elif "m" in s:
      h, m = (0, re.match(r"(\d+)m", s).groups()[0])
    else:
      h, m = (s,"0")
    return int(h) * 60 + int(m)


request = {
        "class": "d1",
        "dataset": "on-demand-extremes-dt",
        "date": 20230820,
        "expver": "aagp",
        "georef": "u09tvk",
}
ret_all = {}
for levtype in ["hl", "pl", "ml", "sfc"]:
    print("Process:", levtype)

    request.update({ "levtype": levtype})
    ret = get_data(request)
    if levtype == "sfc":
      ret_x = reduce_one(ret, "param", "step")
      ret_all[levtype] = sort_ret(ret_x)
    else:
      ret_lev = reduce_one(ret, "levelist", "step", reduce_single=False)
      append_key, match_key  = ("levelist", "param")
      ret_x = [
        reduce_one(item[append_key], match_key, append_key, reduce_single=True)
        for item in ret_lev
      ]
      for i, item in enumerate(ret_lev):
        ret_x[i]["step"] = item["step"]

      ret_all[levtype] = sort_ret(ret_x)

json_object = json.dumps(ret_all, indent=4)
filename =  f"{request['expver']}.json"
with open(filename, "w", encoding="utf8") as f_h:
                    f_h.write(json_object)

