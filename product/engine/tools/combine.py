#!/usr/bin/env python

import pandas as pd
import numpy  as np

from glob    import glob
from sys     import argv
from os.path import splitext
from os      import environ

video = f'{argv[1]}' if len(argv) > 1 else 'NcFVcihJHck'
stime = f'{argv[2]}' if len(argv) > 2 else '000'
etime = f'{argv[3]}' if len(argv) > 3 else '120'

tools = environ.get('tools', '/work/ActIQ/product/engine/tools')
cache = environ.get('cache', '/work/ActIQ/product/engine/cache')

df    = pd.DataFrame()
ranks = [f'rank{n}' for n in range(10)]

mmap  = \
{
    'mp' : 'MediaPipe',
    'sk' : 'SlowFastK',
    'sa' : 'SlowFastA',
    'st' : 'Subtitles'
}

row = \
{
    'video' : '',
    'index' : '',
    'model' : '',
    'rank'  : '',
    'prob'  : '',
    'text'  : ''
}

rows = []


for csv_file in glob(f'{cache}/{video}.classify.{stime}-{etime}.??.csv') :
    
    model       = csv_file.split(f'.classify.{stime}-{etime}.')[-1].split('.')[0]

    print(f'Combining : {csv_file} : {mmap[model]}')
    
    cf          = pd.read_csv(csv_file, names = ['micro'] + ranks).fillna('')
    cf['stamp'] = cf.micro.apply(lambda x : f'{int(x / 10 ** 6):03d}')
    cf['index'] = cf.stamp.apply(lambda x : f'{video}:{x}')
    cf          = cf.set_index('index')

    for index, row in cf.T.iteritems() :

        stamp = row['stamp']

        for n, rank in enumerate(ranks) :
            r     = (row[rank] + ':0.0').split(':')[:2]
            t     = r[0].replace('unknown','').replace('???', '').strip().lower()
            p     = f'{float(r[1]):4.2f}'

            if  t != '' :

                rows.append(
                {
                    'index' : index,
                    'video' : video,
                    'stamp' : stamp,
                    'model' : mmap[model],
                    'rank'  : n,
                    'prob'  : p,
                    'text'  : t
                })

    pd.DataFrame(rows).set_index('index').sort_index().to_csv(f'{cache}/{video}.combined.{stime}-{etime}.csv')
