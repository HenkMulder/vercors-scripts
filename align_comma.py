#! /usr/bin/env python

import sys

def transpose(mat):
    return [list(i) for i in zip(*mat)]

def fmt(l):
    return '%%-%ds' % (l)

def align(cells):
    cells = [[str(c).strip() for c in line] for line in cells]
    lengths = [list(map(lambda x: len(x), l)) for l in cells]
    maxlengths = list(map(lambda x: max(x), transpose(lengths)))
    return [list(map(lambda s, l: fmt(l) % (s), line, maxlengths)) for line in cells]

def sep_cells(cells, sep=', '):
    return '\n'.join([sep.join(line) for line in cells])

if __name__ == '__main__':
    input_file = sys.argv[1]
    f = open(input_file, 'r')
    lines = f.readlines()
    f.close()
    cells = [l.split(',') for l in lines]
    resized = align(cells)
    
    print(sep_cells(resized), end='')
    