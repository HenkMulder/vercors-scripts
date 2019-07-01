#!/usr/bin/env python

import sys
from statistics import mean, pstdev

def transpose(mat):
    return [list(i) for i in zip(*mat)]

def matrix_to_int(matrix):
    return list(map(lambda x: list(map(lambda y: int(y), x)), matrix))

def mean_stdev(vals):
    return {'mean': mean(vals), 
        'stdev': pstdev(vals)}

def sum_distinct_file(file, results):
    # verdicts = set([res[1] for res in results])
    # return [" ".join(verdicts)] + list(map(lambda x: mean_stdev(x), transpose(matrix_to_int([res[2:] for res in results]))))
    return {'file': file,
        'verdicts': '/'.join(set([res[1] for res in results])),
        'runs': len(results),
        'results': list(map(lambda x: mean_stdev(x), transpose(matrix_to_int([res[2:] for res in results]))))}

def sum_all_files(results):
    distinct_files = list(set([res[0] for res in results]))
    return [(sum_distinct_file(file, list(filter(lambda x: x[0]==file, results)))) for file in distinct_files]

def print_single_result(headers, result):
    # print(str(result))
    print('%s, %d, %s, %s, %d, %d' % (result['file'], result['runs'], result['verdicts'], headers[0], result['results'][0]['mean'], result['results'][0]['stdev']))
    for i in range(1, len(headers)):
        print(' , , , %s, %d, %d' % (headers[i], result['results'][i]['mean'], result['results'][i]['stdev']))

def print_summary(csv):
    print('File, Verdict, runs, pass, mean, stdev')
    headers = csv[0].split(",")
    vals = [val.split(',') for val in csv[1:]]
    results = sum_all_files(vals)
    print_summary_vals(headers, results)
    
def print_summary_vals(headers, results):
    for result in results:
        print_single_result(headers[2:], result)

if __name__ == '__main__':
    input_file = sys.argv[1]
    f = open(input_file, 'r')
    res = [x.strip() for x in f.readlines()]
    if len(res) > 2:
        print_summary(res[1:])
    else:
        print("Invalid input.")
    