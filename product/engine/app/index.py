
class Index(object):

    def __init__(self, folder):

        """
        initialize index
        > folder : string containg path to cache folder
        """

        self.folder = folder

        self.buildIndex()

    def buildIndex(self):

        """
        build index of video segments
        """

        pass

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

        result['clips'].append({ 'rank' : 1, 'video' : 'JH3iid1bZ1Q', 'start' :   0, 'end' : 30, 'model' : 'MediaPipe', 'match' : 'swimming, beach, kids', 'probability' : 0.97 })
        result['clips'].append({ 'rank' : 2, 'video' : 'btTKApmxrtk', 'start' :  40, 'end' : 35, 'model' : 'SlowFastK', 'match' : 'swimming, beach, girl', 'probability' : 0.94 })
        result['clips'].append({ 'rank' : 3, 'video' : 'JH3iid1bZ1Q', 'start' :  55, 'end' : 75, 'model' : 'MediaPipe', 'match' : 'swimming, rocks, kids', 'probability' : 0.92 })

      # Vinicio's Magic Here

        return result
