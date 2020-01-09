import os
import sys

def pickIndex(file):
    res = {}
    for root, dirs, files in os.walk(file):
        for d in dirs:
            fullpath  = os.path.join(root, d)
            split_res = d.split(".")
            idx       = int(split_res[0])
            res[idx] = fullpath
    return res

def pickSolution(file):
    res = {}
    for root, dirs, files in os.walk(file):
        for f in files:
            fullpath = os.path.join(root, f)
            if fullpath.endswith("md"):
                res["md"] = fullpath
            else:
                res["so"] = fullpath
    return res

def catFile(path):
    with open(path) as f:
        for line in f:
            print line.rstrip()

if __name__ == '__main__':
    idx     = int(sys.argv[1])
    all_res = pickIndex("solution_code")
    res     = all_res[idx]
    res     = pickSolution(res)
    res_md  = res["md"]
    res_so  = res["so"]
    catFile(res_md)
    catFile(res_so)
