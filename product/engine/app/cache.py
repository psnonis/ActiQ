from time import time
from os   import system

class Cache(object):

    def __init__(self, folder):

        """
        initialize index
        > folder : string containg path to cache folder
        """

        self.folder = folder
        self.worker = {}

    def queueCache(self, video, stime, etime):

        """
        queue cache pipeline job
        >  video : string containing youtube video id
        >  stime : string containing process start time
        >  etime : string containing process   end time
        < result : dictionary containing job status
        """

        result = \
        {
            'video' : video,
            'stime' : stime,
            'etime' : etime,
            'grade' : 'SKIP'
        }

        if  video not in self.worker:

            self.worker[video] = time()

            if  system(f'(cd /engine && process {video} {int(stime):03d} {int(etime):03d})&') == 0:
                result['grade'] = 'PASS'
            else:
                result['grade'] = 'FAIL'

        return result
