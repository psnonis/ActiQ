import whoosh as     wh
import pandas as     pd
import numpy  as     np

from   glob   import glob
from   time   import time, sleep
from   os     import environ, system

class Index(object):

    def __init__(self, folder):

        """
        initialize index
        > folder : string containg path to cache folder
        """

        self.folder = folder

        self.dbase  = pd.DataFrame()
        self.fbase  = pd.DataFrame()

        self.count  = 0

        self.buildIndex()

    def buildIndex(self):

        """
        build index of video segments
        """

        self.dbase = pd.concat([pd.read_csv(c) for c in glob(f'{self.folder}/*.collects.*.csv')]).fillna('').set_index('index') # 10 labels per row - aggregate
        self.fbase = pd.concat([pd.read_csv(c) for c in glob(f'{self.folder}/*.combined.*.csv')]).fillna('').set_index('index') #  1 label  per row - flat list

        self.count = self.dbase.shape[0]

        print(f'Index Contains {self.count} Entries')

    def queryIndex(self, terms, knobs):

        """
        query index for video segment clips
        >  terms : string containing multiple search terms
        >  knobs : dictionary containig option knobs
        < result : dictionary contianig hits
        """

        result = \
        {
            'terms' : terms,
            'knobs' : knobs,
            'clips' :
            [

            ]
        }

      # result['clips'].extend(self.testSearch(terms, knobs))
        result['clips'].extend(self.dumbSearch(terms, knobs))
        result['clips'].extend(self.viniSearch(terms, knobs)) # Vinicio's Magic Here

        return result

    def testSearch(self, terms, knobs):

        clips = [{ 'rank' : 1, 'video' : 'JH3iid1bZ1Q', 'start' :   0, 'end' : 30, 'model' : 'MediaPipe', 'match' : 'swimming, beach, kids', 'probability' : 0.97 },
                 { 'rank' : 2, 'video' : 'btTKApmxrtk', 'start' :  40, 'end' : 35, 'model' : 'SlowFastK', 'match' : 'swimming, beach, girl', 'probability' : 0.94 },
                 { 'rank' : 3, 'video' : 'JH3iid1bZ1Q', 'start' :  55, 'end' : 75, 'model' : 'MediaPipe', 'match' : 'swimming, rocks, kids', 'probability' : 0.92 }]

        return clips

    def dumbSearch(self, terms, knobs):

        clips = []

        masks = [self.dbase['texts'].str.contains(term) for term in terms.split()]
        hits  =  self.dbase[np.logical_and.reduce(masks)]

        first = hits.groupby('video').stamp.min()

        print(first)

        for n, (video, start) in enumerate(first.items(), 1):

            clips.append({'rank' : n, 'video' : video, 'start' : start, 'end' : start + 30, 'model' : '?', 'match' : '?', 'probability' : 0.95 })

        return clips

    def viniSearch(self, terms, knobs):

        clips = []


        return clips
