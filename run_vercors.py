#!/usr/bin/env python

import subprocess, sys, threading, time, os, re, random, datetime
# from __future__ import print_function

vct_home = os.path.expandvars('${VCT_HOME}/')

if os.name == 'nt':
    vct_bin = os.path.expandvars(vct_home + '/windows/bin/vct.cmd')
else:
    vct_bin = os.path.expandvars(vct_home + '/unix/bin/vct')

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def last_line(res, n=1):
    return str([i for i in res.splitlines() if i][-n])
    
def total_time(res):
    # return last_line(res).split(" ")[3]
    ret = re.search(r'entire run took (\d+) ms', str(res))
    return -1 if ret is None else ret.group(1)
    
def backend_time(res):
    # return last_line(res, 2).split(" ")[2]
    ret = re.search(r'task Viper verification took (\d+) ms', str(res))
    return 0 if ret is None else ret.group(1)
    
def parsing_time(res):
    ret = re.search(r'Parsed \d+ file\(s\) in: (\d+)ms', str(res))
    return 0 if ret is None else ret.group(1)

    
# TODO: fix
def triggers_time(res):
    raw = str(res)
    reg = 'Applying simple_triggers([ \.\n\r$^]+)pass took (\d+) ms'
    reg = r'Applying simple_triggers([ .\.\r\n$^]*)pass took ([\d]+) ms'
    ret = re.findall(reg, raw, re.MULTILINE)
    # ret = re.findall('Applying simple_triggers(.)', str(res), re.MULTILINE)
    # print(str(ret))
    return 0 if len(ret) == 0 else ret[0][1]

def verdict(res):
    ret = re.search(r'The final verdict is (\w+)', str(res))
    return "None" if ret is None else ret.group(1)

def run_vct(opts, input_files):
    # eprint('[%s]\nRunning %s...' % (datetime.datetime.now(), args[-1]))
    args = opts+input_files
    eprint('[%s]\n%s' % (datetime.datetime.now(), ' '.join(args)))
    ar = [vct_bin, '--progress']+args
    popen = subprocess.Popen(ar, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
    result, err = popen.communicate(input=None)
    return [' '.join(input_files).replace(vct_home, ''), verdict(result), total_time(result), backend_time(err), parsing_time(err), triggers_time(err)]

def print_result_csv(resultlist):
    print('File, Verdict,Total time,Back-end time, Parse time, Trigger time')
    for result in resultlist:
        # print('%s, %s, %s, %s' % result)
        print(', '.join([str(r) for r in result]))

def extra_options(fpath):
    result = []
    for fp in fpath.split(' '):
        f = open(fp, 'r')
        opts = re.findall(r'//::\s+option\s+(.+)\n', f.read())
        if opts:
            for match in opts:
                result += match.split()
    return result

def expandfiles(files):
    return ' '.join([os.path.join(vct_home, f) for f in files.split()])

def run_vercors(sys_argv):
    input_file = sys_argv[1]
    f = open(input_file, 'r')
    srcs = [expandfiles(x.strip()) for x in f.readlines()]
    # random.shuffle(srcs)
    opts = sys_argv[2:]
    commandlist = [(opts + extra_options(src), src.split(' ')) for src in srcs]
    resultlist = [run_vct(*command) for command in commandlist]
    return resultlist
    
def print_run_vercors(sys_argv):
    resultlist = run_vercors(sys_argv)
    args = sys_argv[2:]
    print("Options: %s" %(" ".join(args)))
    print_result_csv(resultlist)

if __name__ == '__main__':
    print_run_vercors(sys.argv)