#!/usr/bin/env python3

import sys
import sh
import collections
import re
import string
import math
import datetime
import time
from pygtail import Pygtail
import os


def parse_line(line, state_vec={'time': '', 'from': '', 'to': '', 'message': ''}):
    if line[0]=='\t':
        state_vec['message'] = line.strip()
    else:
        time, rest = line.split(maxsplit=1)
        state_vec['time'] = time.strip()
        _, rest = rest.split(maxsplit=1)
        fr, rest = rest.split("to", maxsplit=1)
        state_vec['from'] = fr.strip()
        to, message = rest.split(":", maxsplit=1)
        state_vec['to'] = to.strip()
        state_vec['message'] = message.strip()
    #return {'time': time, 'from': fr, 'to': to, 'message': message}
    return state_vec



alphanum_pattern = re.compile('[\W_]+')
def concentrate(x):
    '''Removes all punctuation and whitespace, and then deduplicates'''
    s = set(alphanum_pattern.sub('', x.lower()))
    return "".join(s)

def confusion_by_punc(x):
    '''Measures confusion by taking the log of the number of question marks'''
    s = collections.Counter(x)
    return math.log2(s['?']+1)

def minute_from_time(x):
    '''Gets minute from the time of chat'''
    broken = x.split(":", maxsplit=2)
    hour = int(broken[0])
    minute = int(broken[1])
    return int(60*hour + minute)

def curr_m():
    '''Gets current minute'''
    now = datetime.datetime.now()
    return int(60*now.hour + now.minute)


type_spec = "bar"
database = {}
conf_data = collections.defaultdict(lambda: 0, {})
if __name__ == "__main__":
    #tail = sh.tail("-f", "-n", "+1", sys.argv[1], _iter=True)
    #for line in tail:
    try:
        os.remove(sys.argv[1] + ".offset")
    except OSError:
        pass
    p = {'time': '', 'from': '', 'to': ''}
    while True:
        time.sleep(2)
        for line in Pygtail(sys.argv[1]):
            try:
                p = parse_line(line, p)
                print(p)
                if p['from'] == "Yun William Yu":
                    if p['message'].startswith("/bar"):
                        type_spec = "bar"
                    if p['message'].startswith("/pie"):
                        type_spec = "pie"
                    if p['message'].startswith("/reset"):
                        database = {}
                if True:
                    conc = concentrate(p['message'])
                    if conc == "a":
                        database[p['from']] = "a"
                    if conc == "b":
                        database[p['from']] = "b"
                    if conc == "c":
                        database[p['from']] = "c"
                    if conc == "d":
                        database[p['from']] = "d"
                    if conc == "e":
                        database[p['from']] = "e"
                C = collections.Counter(database.values())
                if True:
                    conf = confusion_by_punc(p['message'])
                    conf_data[minute_from_time(p['time'])] = conf_data[minute_from_time(p['time'])] + conf
            except:
                pass
        with open('data.js', 'w') as f:
            print("type_spec = '{}'; data_points = [{}, {}, {}, {}, {}];".format(type_spec, C['a'], C['b'], C['c'], C['d'], C['e']) +
                  " confuse_points = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]; ".format(
                      conf_data[curr_m()-10],
                      conf_data[curr_m()-9],
                      conf_data[curr_m()-8],
                      conf_data[curr_m()-7],
                      conf_data[curr_m()-6],
                      conf_data[curr_m()-5],
                      conf_data[curr_m()-4],
                      conf_data[curr_m()-3],
                      conf_data[curr_m()-2],
                      conf_data[curr_m()-1],
                      conf_data[curr_m()]
                  ), file=f)





