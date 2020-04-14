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
            'El1_ENLEmKA', '_XmhBaUdges', '4rp2aLQl7vg', '3smpofL8uPM',
           #'wxMrtK-kYnE'
        ]

        self.buildIndex()
        self.sanityTest()

    def buildIndex(self):

        """
        build index of video segments
        """

        self.combo = pd.concat([pd.read_csv(c, sep = '\t') for c in glob(f'{self.folder}/*.combined.*.tsv')]).fillna('').set_index('index') # 10 labels per row
        self.combo = self.combo[~self.combo.video.isin(self.blocks)]

        clist = glob(f'{self.folder}/*.combined.*.tsv')
        flist = glob(f'{self.folder}/*.flatlist.*.tsv')

        for t in clist:
            x  = pd.read_csv(t, sep = '\t')
            if  x.shape[1] != 28 :
                print(splitext(basename(t))[0], '*' if x.shape[1] != 28 else ' ', x.shape[1], x.shape[0])

        print(f'Combined Index Contains {self.combo.shape[0]:06d} Entries in {len(clist)} Videos')

        self.flats = pd.concat([pd.read_csv(c, sep = '\t') for c in glob(f'{self.folder}/*.flatlist.*.tsv')]).fillna('').set_index('index') #  1 label  per row
        self.flats = self.flats[~self.flats.video.isin(self.blocks)]

        for t in flist:
            x  = pd.read_csv(t, sep = '\t')
            if  x.shape[1] != 9 :
                print(splitext(basename(t))[0], '*' if x.shape[1] != 9 else ' ', x.shape[1], x.shape[0])

        print(f'FlatList Index Contains {self.flats.shape[0]:06d} Entries in {len(flist)} Videos')

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

      # print(result)

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

        return clips[:3]

    def sanityTest(self):

        return
        try :

            self.bestSearch(terms = 'swimming',
                            chips = [],
                            knobs = {'subtitles' : True})

            self.bestSearch(terms = 'solving_for_x_and_y',
                            chips = [],
                            knobs = {'subtitles' : True})

            self.bestSearch(terms = 'solving for x and y',
                            chips = [],
                            knobs = {'subtitles' : True})        

            self.bestSearch(terms = '',
                            chips = [{'label' : 'crouch or kneel'},{'label' : 'carry or hold (an object)'}, {'label' : 'ripping paper'}],
                            knobs = {'subtitles' : False})

        except :

            print('\n *** EXCEPTION *** \n')

            raise

            exit()

    def bestSearch(self, terms, chips, knobs):

        clips = []

      # frame = self.flats[self.flats.model != 'Subtitles'] if not knobs['subtitles'] else \
      #         self.flats

        frame = self.flats

        terms = [term.lower().replace('_', ' ') for term in terms.strip().split()]
        chips = [chip['label'] for chip in chips]

        print('\n' + '-' * 80)
        print('|'.join(terms + chips))
        print('-' * 80 + '\n')

        hits  = []

        for term in terms + chips :
            if  knobs['subtitles']:

                mask = frame['text'].str.match(term)
                print(f'matching : "{term}" : {sum(mask)} hits')
                mask = frame['text'].str.contains(term)
                print(f'contains : "{term}" : {sum(mask)} hits')

                hits.append(frame[mask])
            else                  :
                hits.append(frame[frame['text'].eq(       term)])

        hits   = pd.concat(hits)

        print(f'\nhits : {type(hits)} =\n{hits}\n')

        videos = hits.groupby('video').agg('sum').sort_values(
            by = 'prob', ascending = False).iloc[:3].index.values

        for video in videos :

            bucket    = frame[frame['video'].eq(video)]
            length    = int(bucket.sort_values(by = 'stamp', ascending = False).iloc[0]['stamp'])
            n_buckets = length // 30

            query = {
                'bucket': [],
                'prob'  : []
                }

            for i in range(n_buckets) :

                for term in terms + chips :

                    aux = 0

                    if  knobs['subtitles'] :

                        aux += bucket[(bucket['stamp'] >= 30*(i+0)) & 
                                      (bucket['stamp']  < 30*(i+1)) & 
                                      (bucket['text' ].str.contains(term))]['prob'].sum()
                    else :

                        aux += bucket[(bucket['stamp'] >= 30*(i+0)) & 
                                      (bucket['stamp']  < 30*(i+1)) & 
                                      (bucket['text' ] == term)]['prob'].sum()
                        
                query['bucket'].append(i)
                query['prob'  ].append(aux)
            
            query_dict = pd.DataFrame.from_dict(query)
            max_bucket = query_dict['prob'].idxmax()
            
            max_stamp_loc = []

            for term in terms + chips :

                if  knobs['subtitles'] :
                    if  bucket[(bucket['stamp'] >= 30*(max_bucket+0)) & 
                                                (bucket['stamp']  < 30*(max_bucket+1)) & 
                                                (bucket['text' ].str.contains(     term))].empty:
                        next
                    else :
                        max_stamp_loc.append(bucket[(bucket['stamp'] >= 30*(max_bucket+0)) & 
                                                (bucket['stamp']  < 30*(max_bucket+1)) & 
                                                (bucket['text' ].str.contains(     term))].iloc[0][['stamp','prob']])
                else :
                    if  bucket[(bucket['stamp'] >= 30*(max_bucket+0)) & 
                                                (bucket['stamp']  < 30*(max_bucket+1)) & 
                                                (bucket['text' ].eq(            term))].empty:
                        next

                    else :
                        max_stamp_loc.append(bucket[(bucket['stamp'] >= 30*(max_bucket+0)) & 
                                                (bucket['stamp']  < 30*(max_bucket+1)) & 
                                                (bucket['text' ].eq(            term))].iloc[0][['stamp', 'prob']])
                        
            print(f'max_stamp_loc : {type(max_stamp_loc)} = \n{max_stamp_loc}\n')

            max_stamp_loc_df = pd.DataFrame(max_stamp_loc)
            stamp            = max_stamp_loc_df.loc[max_stamp_loc_df['prob'].idxmax()]['stamp']
            
            # if ~isinstance(stamp, np.float64) :
            #     stamp = stamp[0]

            print(f'stamp : {type(stamp)} = \n{stamp}\n')

            clips.append(
            {
                'rank'   : len(clips) + 1,
                'video'  : video, 
                'length' : length,
                'start'  : int(stamp),
                'end'    : int(stamp) + 30,
            })

        for c in clips :
            print('clip :', c)

        return clips
