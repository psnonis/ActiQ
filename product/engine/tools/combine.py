#!/usr/bin/env python

import pandas as pd
import numpy  as np

from glob    import glob
from sys     import argv, stderr
from os.path import splitext
from os      import environ

video = f'{argv[1]}' if len(argv) > 1 else 'NcFVcihJHck'
stime = f'{argv[2]}' if len(argv) > 2 else '000'
etime = f'{argv[3]}' if len(argv) > 3 else '120'

tools = environ.get('tools', '/engine/tools')
cache = environ.get('cache', '/engine/cache')

df    = pd.DataFrame()
ranks = [f'rank{n}' for n in range(10)]

mmap  = \
{
    'mp' : 'MediaPipe',
    'sk' : 'SlowFastK',
    'sa' : 'SlowFastA',
    'st' : 'Subtitles'
}

rows = []
flat = []

for csv_file in glob(f'{cache}/{video}.classify.{stime}-{etime}.??.csv') :

    with open(csv_file, 'r') as f: data = f.read()
    with open(csv_file, 'w') as f: f.write(data.replace(', ', ' ').replace(': ', ' '))
    
    model       = mmap[csv_file.split(f'.classify.{stime}-{etime}.')[-1].split('.')[0]]

    print(f'Combining : {csv_file} : {model}')
    
    cf          = pd.read_csv(csv_file, names = ['micro'] + ranks).fillna('unkown:0.00')
    cf['stamp'] = cf.micro.apply(lambda x : f'{int(x / 10 ** 6):03d}')
    cf['index'] = cf.stamp.apply(lambda x : f'{video}:{x}')
    cf          = cf.set_index('index')

    for index, row in cf.T.iteritems() :

        stamp = row['stamp']

        entry = \
        {
            'index' : index,
            'video' : video,
            'stamp' : stamp,
            'model' : model,

            'texts' : [],
            'probs' : []
        }

        for n, rank in enumerate(ranks) :

            r = row[rank].split(':')

            if  len(r) < 2 :
                stderr.write(f'{csv_file} {r}\n')
                continue
            
            t     = r[0].replace('unknown', '').replace('???', '').strip().lower()
            p     = f'{float(r[1]):4.2f}'

            if  t != '' :

                flat.append(
                {
                    'index' : index,
                    'video' : video,
                    'stamp' : stamp,
                    'model' : model,
                    'rank'  : n,
                    'prob'  : p,
                    'text'  : t
                })
                
                entry['texts'] += [t]
                entry['probs'] += [p]

            entry[f'rank{n}'] = n
            entry[f'prob{n}'] = p
            entry[f'text{n}'] = t

        entry['texts'] = ';'.join(entry['texts']).strip()
        entry['probs'] = ';'.join(entry['probs']).strip()

        rows.append(entry)

    if  flat : pd.DataFrame(flat).set_index('index').sort_index().to_csv(f'{cache}/{video}.combined.{stime}-{etime}.csv') # TODO : change to flatlist
    else     : raise Exception('Flat is Empty')

    if  rows : pd.DataFrame(rows).set_index('index').sort_index().to_csv(f'{cache}/{video}.collects.{stime}-{etime}.csv') # TODO : change to combined
    else     : raise Exception('Rows is Empty')
