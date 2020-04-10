import pandas  as     pd
import numpy   as     np

from   glob         import glob
from   time         import time, sleep
from   os.path      import basename, splitext
from   os           import environ, system
from elasticsearch  import Elasticsearch

class Index(object):

    def __init__(self, folder):

        """
        initialize index
        > folder : string containg path to cache folder
        """

        self.folder = folder

        self.combo  = pd.DataFrame()
        self.flats  = pd.DataFrame()

        self.blocks  = \
        [
            'El1_ENLEmKA', '_XmhBaUdges', '4rp2aLQl7vg'
        ]

        self.buildIndex()

    def buildIndex(self):

        """
        build index of video segments
        """

        self.combo = pd.concat([pd.read_csv(c, sep = '\t') for c in glob(f'{self.folder}/*.combined.*.tsv')]).fillna('').set_index('index') # 10 labels per row
        self.combo = self.combo[~self.combo.video.isin(self.blocks)]

        for c in glob(f'{self.folder}/*.combined.*.tsv'):
            x  = pd.read_csv(c,sep = '\t')
            if  x.shape[1] != 36 :
                print(splitext(basename(c))[0], '*' if x.shape[1] != 36 else ' ', x.shape[1], x.shape[0])

        print(f'Combined Index Contains {self.combo.shape[0]} Entries')

        self.flats = pd.concat([pd.read_csv(c, sep = '\t') for c in glob(f'{self.folder}/*.flatlist.*.tsv')]).fillna('').set_index('index') #  1 label  per row
        self.flats = self.flats[~self.flats.video.isin(self.blocks)]

        for c in glob(f'{self.folder}/*.flatlist.*.tsv'):
            x  = pd.read_csv(c,sep = '\t')
            if  x.shape[1] != 7 :
                print(splitext(basename(c))[0], '*' if x.shape[1] != 7 else ' ', x.shape[1], x.shape[0])

        print(f'FlatList Index Contains {self.flats.shape[0]} Entries')

    def queryIndex(self, terms, chips, knobs):

        """
        query index for video segment clips
        >  terms : string containing multiple search terms
        >  chips : string containing multiple search chips
        >  knobs : dictionary containig option knobs
        < result : dictionary contianig hits
        """



        result = \
        {
            'terms' : terms,
            'chips' : chips,
            'knobs' : knobs,
            'clips' :
            [

            ]
        }

      # result['clips'].extend(self.testSearch(terms, chips, knobs))
      # result['clips'].extend(self.dumbSearch(terms, chips, knobs))
        result['clips'].extend(self.bestSearch(terms, chips, knobs))

        print(result)

        return result

    def testSearch(self, terms, chips, knobs):

        clips = [{ 'rank' : 1, 'video' : 'JH3iid1bZ1Q', 'start' :   0, 'end' : 30, 'model' : 'MediaPipe', 'match' : 'swimming, beach, kids', 'probability' : 0.97 },
                 { 'rank' : 2, 'video' : 'btTKApmxrtk', 'start' :  40, 'end' : 35, 'model' : 'SlowFastK', 'match' : 'swimming, beach, girl', 'probability' : 0.94 },
                 { 'rank' : 3, 'video' : 'JH3iid1bZ1Q', 'start' :  55, 'end' : 75, 'model' : 'MediaPipe', 'match' : 'swimming, rocks, kids', 'probability' : 0.92 }]

        return clips

    def dumbSearch(self, terms, chips, knobs):

        clips = []

        frame = self.combo[self.combo.model != 'Subtitles'] if not knobs['subtitles'] else \
                self.combo

        terms = [term.lower().replace('_', ' ') for term in terms.strip().split()]
        chips = [chip['label'] for chip in chips]

        masks = [frame['texts'].str.contains(t) for t in terms] + \
                [frame['texts'].str.contains(c) for c in chips]

        hits  =  frame[np.logical_and.reduce(masks)] if knobs['all_terms'] else \
                 frame[ np.logical_or.reduce(masks)]

        first = hits.groupby('video').stamp.min()
        media = hits.groupby('video').stamp.median()

        model = hits.groupby('video').model.unique()

        print(model)

        for video, start in first.items():

            clips.append({ 'rank' : len(clips) + 1, 'video' : video, 'start' : start, 'end' : start + 30, 'model' : 'first', 'match' : '?', 'probability' : 0.95 })

        for video, start in media.items():

            clips.append({ 'rank' : len(clips) + 1, 'video' : video, 'start' : start, 'end' : start + 30, 'model' : 'media', 'match' : '?', 'probability' : 0.95 })

        return clips[:5]

    def bestSearch(self, terms, chips, knobs):

        es    = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        clips = []

        frame = self.combo[self.combo.model != 'Subtitles'] if not knobs['subtitles'] else \
                self.combo

        terms = [term.lower().replace('_', ' ') for term in terms.strip().split()]
        chips = [chip['label'] for chip in chips]

        query = {}

        for term in terms + chips :
            search = es.search(index = 'actiq', body = { 'query': { 'match' : { 'text' : term } } })
            for hit in search['hits']['hits'] :
                if 'hit' not in query :
                    query['hit'] = []
                query['hit'].append(1)
                for key,val in hit['_source'].items():
                    if  key not in query :
                        query[key] = []
                    query[key].append(val)

        panda = pd.DataFrame.from_dict(query).astype({ 'prob' : 'float' })

        video = panda.groupby('video').agg('sum')['hit'].idxmax()
        stamp = panda.iloc[panda[panda['video'] == video]['prob'].idxmax()]['stamp']
        prob  = panda.iloc[panda[panda['video'] == video]['prob'].idxmax()]['prob' ]
        
        clips.append({ 'rank' : 1, 'video' : video, 'start' : int(stamp), 'end' : int(stamp) + 30, 'model' : 'lucky', 'match' : '?', 'probability' : prob })

        print(clips)

        return clips
