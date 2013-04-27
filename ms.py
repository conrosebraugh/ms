#!/usr/bin/python

import os
import glob
import re
from pprint import pprint

def find_sys_stats():
    f = open('/proc/meminfo','r')

    memtotal = re.findall('MemTotal:\s+(\d+)', f.read())[0]
    f.seek(0)
    memfree = re.findall('MemFree:\s+(\d+)', f.read())[0]
    f.seek(0)
    shmem = re.findall('Shmem:\s+(\d+)',f.read())[0]
    inuse = repr(int(memtotal) - int(memfree))
    nonshared = repr(int(inuse) - int(shmem))

    return [('Total',memtotal), ('In-Use',inuse), ('Free',memfree),
            ('Shared',shmem), ('Nonshared',nonshared)]

sys_stats = find_sys_stats()

for key, value in sys_stats:
    print (key + ":").ljust(12), (value + ' kB').ljust(0)

print '--'

running_dir = os.getcwd()

os.chdir('/proc')

list_of_pids = glob.glob('[0-9]*')

process_dict = {}

process_dict['0'] = {}
process_dict['0']['PID'] = 'PID'
process_dict['0']['USS'] = 'USS'
process_dict['0']['PSS'] = 'PSS'
process_dict['0']['SWAP'] = 'SWAP'
process_dict['0']['RES'] = 'RES'
process_dict['0']['SHR'] = 'SHR'
process_dict['0']['CMD'] = 'CMD'


for i in list_of_pids:
	process_dict[i] = {}
	process_dict[i]['PID'] = i
	os.chdir('/proc/'+i)
	f = open('statm', 'r')
	process_dict[i]['RES'] = f.readline().split()[1]
	process_dict[i]['USS'] = repr(int(l[2]) - int(l[1]))
	process_dict[i]['SHR'] = l[2]
	f.close()
	f = open('cmdline', 'r')
	process_dict[i]['CMD'] = f.readline().split('\x00')[0]
	f.close()
	f = open('status', 'r')
	process_dict[i]['SWAP'] = re.findall('VmSwap:\s+(\d+)', f.read())[0]
	f.close()
	f = open('smaps', 'r')
	process_dict[i]['PSS'] = repr(sum([int(x) for x in re.findall('^Pss:\s+(\d+)', fp.read(), re.M)]))
	f.close()
	
	os.chdir('/proc')
