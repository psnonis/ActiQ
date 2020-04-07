"""Generate a MediaSequence metadata for MediaPipe input."""

from sys import path, argv
from os  import environ

tools = environ.get('tools', '/engine/tools')
cache = environ.get('cache', '/engine/cache')

path += [f'{tools}/mp']

from mediapipe.util.sequence    import media_sequence as ms
from tensorflow.compat.v1.train import SequenceExample
from os.path                    import abspath, basename
from six                        import ensure_binary

SECONDS_TO_MICROSECONDS = 1000000

if  __name__ == '__main__' :

    clip  = bytes(abspath(argv[1]), 'utf-8')
    meta  =       abspath(argv[2])
    stime =           int(argv[3])
    etime =           int(argv[4])

    start = stime * SECONDS_TO_MICROSECONDS
    end   = etime * SECONDS_TO_MICROSECONDS
  
    data  = SequenceExample()

    ms.set_clip_data_path(       clip, data)
    ms.set_clip_start_timestamp(start, data)
    ms.set_clip_end_timestamp(    end, data)

    with open(meta, 'wb') as writer :
        writer.write(ensure_binary(data.SerializeToString()))
