#!/usr/bin/env python

from analyze_results import *
from align_comma import align, sep_cells

def results_from_file(input_file):
    f = open(input_file, 'r')
    res = [x.strip() for x in f.readlines()]
    res = res[1:]
    vals = [val.split(',') for val in res[1:]]
    return sum_all_files(vals)

def get_or_default(name, list, default):
    for result in list:
        if result['file'] == name:
            return result
    return default

result_none = {'file': '-',
    'results': [{'mean': -1}] }

def timeof(res):
    return int(res['results'][0]['mean'])

def pass_only(lst):
    return list(filter(lambda x: x['verdicts'].strip() == 'Pass', lst))

def result_only(lst):
    return list(filter(lambda x: not 'None' in x['verdicts'], lst))

def sort_files(filelist, cmp1=1, cmp2=-1):
    rs = [results_from_file(r) for r in filelist]
    rs = [pass_only(r) for r in rs]
    files = set()
    for r in rs:
        files = files.union({s['file'] for s in r})
    res = []
    for f in files:
        res.append([f] + [timeof(get_or_default(f, s1, result_none)) for s1 in rs])
    if len(sys.argv) > 2:
        res = sorted(res, key=lambda x: abs(x[cmp2])/x[cmp1])
    else:
        res = sorted(res, key=lambda x: x[1])        
    return res

if __name__ == '__main__':
    c1 = 1
    c2 = -1
    result = sort_files(sys.argv[1:], c1, c2)
    result = [r+[int(r[c2]*100/r[c1])] for r in result]
    fastcount = [0]*len(sys.argv)
    ftime = 0
    for r in result:
        fastest = 'None'
        ftime = 1000000000000
        fi = 0
        for i in range(1, len(sys.argv)):
            if ((r[i] > 0) & (r[i] < ftime)):
                fastest = sys.argv[i]
                ftime = r[i]
                fi = i
        r.append(fastest)
        fastcount[fi] = fastcount[fi]+1
    result = align(result)
    print(sep_cells(result))
    fi = fastcount.index(max(fastcount))
    print('Most fastest: %s' %(sys.argv[fi]), end='')
