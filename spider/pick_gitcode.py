import os
import sys

def pickIndex(file):
    res = {}
    for root, dirs, files in os.walk(file):
        for d in dirs:
            fullpath  = os.path.join(root, d)
            split_res = d.split(".")
            idx       = int(split_res[0])
            res[idx]  = fullpath
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

def catFile(path, printflag=False):
    res = []
    with open(path) as f:
        for line in f:
            res.append(line.rstrip())
            if printflag:
                print line.rstrip()
    return res

def pick_solution(all_res, idx, printflag=False):
    res_list = []
    res     = all_res.get(idx, {})
    if len(res) == 0:
        return
    res     = pickSolution(res)
    res_md  = res["md"]
    res_so  = res["so"]
    #print "***"*40
    res_md_list = catFile(res_md, printflag)
    #print "***"*40
    #print "\n"
    res_so_list = catFile(res_so, printflag)
    #print "\n"
    #res_list.extend(res_md_list)
    #res_list.append("")
    res_list.extend(res_so_list)
    return res_list

def build_idx():
    res = {}
    all_res = pickIndex("../solution_code")
    for idx in range(1, 668):
        #print idx
        item_res = pick_solution(all_res, idx, printflag=False)
        if item_res == None:
            continue
        res[idx] = "\n".join(item_res)
        print res[idx]
    return res

if __name__ == '__main__':
    build_idx()
    print ""
