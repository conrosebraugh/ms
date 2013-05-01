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

pd = {}

pd['0'] = {}
pd['0']['PID'] = 'PID'
pd['0']['USS'] = 'USS'
pd['0']['PSS'] = 'PSS'
pd['0']['SWAP'] = 'SWAP'
pd['0']['RES'] = 'RES'
pd['0']['SHR'] = 'SHR'
pd['0']['CMD'] = 'CMD'

#
#
#
#
#
#
#
#

for i in list_of_pids:
    os.chdir('/proc/'+i)
    f = open('status', 'r')
    try:
        temp = re.findall('VmSwap:\s+(\d+)', f.read())[0]
        pd[i] = {}
        pd[i]['PID'] = int(i)
        pd[i]['SWAP'] = int(temp)
    except IndexError:
        continue
    # print i
    f.close()
    f = open('statm', 'r')
    l = f.readline().split()
    pd[i]['RES'] = int(l[1])
    pd[i]['USS'] = (int(l[1]) - int(l[2]))
    pd[i]['SHR'] = int(l[2])
    f.close()
    f = open('cmdline', 'r')
    # pd[i]['CMD'] = f.readline().split('\x00')[0]
    pd[i]['CMD'] = re.split('(\x00|\s+)', f.readline())[0]
    f.close()
    f = open('smaps', 'r')
    pd[i]['PSS'] = sum([int(x) for x in re.findall('^Pss:\s+(\d+)', f.read(), re.M)])
    f.close()
    
    os.chdir('/proc')

print " "

ordered = sorted(pd.items(), key=lambda x: x[1]['RES'], reverse=True)

print (pd['0']['PID']).ljust(8), (pd['0']['USS']).ljust(8), (pd['0']['PSS']).ljust(8),
print (pd['0']['SWAP']).ljust(8), (pd['0']['RES']).ljust(8), (pd['0']['SHR']).ljust(8), 
print (pd['0']['CMD']).ljust(8) 

# for i in pd:
#     if i == '0':
#         continue
#     print (repr(pd[i]['PID'])).ljust(8), (repr(pd[i]['USS'])).ljust(8), (repr(pd[i]['PSS'])).ljust(8),
#     print (repr(pd[i]['SWAP'])).ljust(8), (repr(pd[i]['RES'])).ljust(8), (repr(pd[i]['SHR'])).ljust(8), 
#     print (pd[i]['CMD']).ljust(8) 


for i in ordered:
    if i[1]['PID'] == 'PID':
        continue
    print (repr(i[1]['PID'])).ljust(8), (repr(i[1]['USS'])).ljust(8), (repr(i[1]['PSS'])).ljust(8),
    print (repr(i[1]['SWAP'])).ljust(8), (repr(i[1]['RES'])).ljust(8), (repr(i[1]['SHR'])).ljust(8), 
    print (i[1]['CMD']).ljust(8) 

#items = ((pid, uss, pss, swap, res, shr, cmd) for pid in pd for blah, val in pd[pid].items())


#pprint(ordered)
