#!/usr/bin/env python

import pandas as pd

from glob import glob
from sys  import argv

video = argv[1] if len(argv) > 1 else 'NcFVcihJHck'
stime = argv[2] if len(argv) > 1 else '000'
etime = argv[3] if len(argv) > 1 else '120'

tools = '/work/ActIQ/product/engine/tools'
cache = '/work/ActIQ/product/engine/cache'

cf    = pd.DataFrame()
print(f'{cache}/{video}')

for csv_file in glob(f'{cache}/{video}.classify.??.{stime}-{etime}.csv'):
    
    print(f'Combining : {csv_file}')
    
    df          = pd.read_csv(csv_file, header = None)
    df['model'] = csv_file.split('.classify.')[-1].split('.')[0]
    df['video'] = video
    df['start'] = stime
    df['end'  ] = etime
    
    cf          = pd.concat(cf, df)

cf = cf.sort_index()

cf.to_csv(f'cache/{video}.combined.csv')
