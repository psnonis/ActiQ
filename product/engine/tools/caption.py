#!/usr/bin/env python

from datetime import datetime
from sys      import stdin

time = ''
text = []
prev = ''

def is_time(line) : return line.count(':') == 2 and line.startswith('00')

for line in stdin.readlines() :

    if  is_time(line) and prev == 'text' and time != '' :

        text = text + [''] * (10 - len(text))
        usec = int((datetime.strptime(time, '%H:%M:%S.%f') - datetime(1900, 1, 1)).total_seconds() * 10 ** 6)
        print(f'{usec},{",".join(text)}')

        text = []
        time = ''

    if   is_time(line) : time  =  line.strip()
    elif time          : text += [line.strip().replace(',', ' ').replace(':', ' ').replace('.', '') + ':0.01']

    if   is_time(line) : prev = 'time'
    else               : prev = 'text'