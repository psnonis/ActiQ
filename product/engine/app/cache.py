import whoosh  as     wh
import pandas  as     pd
import numpy   as     np

from   glob    import glob
from   time    import time, sleep
from   os.path import basename, splitext
from   os      import environ, system
from   pymongo import MongoClient

# from   locale             import getpreferredencoding
# from   asyncio            import get_event_loop, run, run_coroutine_threadsafe, create_subprocess_shell
# from   asyncio.subprocess import PIPE

from subprocess import Popen, PIPE

class Cache(object) :

    def __init__(self, folder) :

        """
        initialize index
        > folder : string containg path to cache folder
        """

        self.folder = folder
        self.worker = {}
        self.client = MongoClient(f'mongodb://127.0.0.1:81/meteor')
        self.queue  = MongoClient(f'mongodb://127.0.0.1:81/meteor')['meteor']['queue']

        print(self.client.list_database_names())

    def queueCache(self, video, stime, etime) :

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

        def monitor() :

            command = f'cd /engine ; process {video}'
            workdir = f'/engine'

            try                 :

                process = Popen(command, cwd = workdir, stdout = PIPE, shell = True, universal_newlines = True)

            except OSError as e :

                print(f'process failed to start : {e}')

                result['grade'] = 'FAIL'

                return

            for line in process.stdout :
                line  = line.strip()

                if  line.count('[ACQUIRE]') > 0 : self.queue.update({'_id' : video}, {'$set' : {'stage' : '[ACQUIRE]', 'progress' :  10}}, upsert = True)
                if  line.count('[PREDICT]') > 0 : self.queue.update({'_id' : video}, {'$set' : {'stage' : '[PREDICT]', 'progress' :  20}}, upsert = True)
                if  line.count('[OVERLAY]') > 0 : self.queue.update({'_id' : video}, {'$set' : {'stage' : '[OVERLAY]', 'progress' :  30}}, upsert = True)
                if  line.count('[CAPTION]') > 0 : self.queue.update({'_id' : video}, {'$set' : {'stage' : '[CAPTION]', 'progress' :  80}}, upsert = True)
                if  line.count('[COMBINE]') > 0 : self.queue.update({'_id' : video}, {'$set' : {'stage' : '[COMBINE]', 'progress' :  90}}, upsert = True)

                if  line.count('[FAILURE]') > 0 : self.queue.update({'_id' : video}, {'$set' : {'stage' : '[FAILURE]', 'progress' : 100}}, upsert = True)
                if  line.count('[SUCCESS]') > 0 : self.queue.update({'_id' : video}, {'$set' : {'stage' : '[SUCCESS]', 'progress' : 100}}, upsert = True)

                if  line :

                    print(f'OUT > {line}', flush = True)

            process.kill()

            print(f'RET > {process.returncode}')

            return process.wait()

        if  video not in self.worker :

            self.worker[video] = time()

            tlimit = 10 * 60

            monitor()

            print('bye')


            # try                       :

            #     yields = future.result(tlimit)

            # except TimeoutError  as e :

            #     print('timeout')
            #     future.cancel()

            # except Exception     as e :

            #     print(f'exception : {e}')

            # print(f'yields = {yields}')
            # print(f'finish = {self.worker.pop(video) - time()}')

            # if  system(f'(cd /engine && process {video} {int(stime):03d} {int(etime):03d})&') == 0 :
            #     result['grade'] = 'PASS'
            # else:
            #     result['grade'] = 'FAIL'

        return result
