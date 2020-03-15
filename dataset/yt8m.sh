mkdir -p /work/data/yt8m/3/frame
mkdir -p /work/data/yt8m/3/frame/validate ; cd /work/data/yt8m/3/frame/validate
curl data.yt8m.org/download.py | partition=3/frame/validate mirror=us python3

mkdir -p /work/data/yt8m/3/frame/test ; cd /work/data/yt8m/3/frame/test 
curl data.yt8m.org/download.py | partition=3/frame/test     mirror=us python3


mkdir -p /work/data/yt8m/2/frame
mkdir -p /work/data/yt8m/2/frame/train ; cd /work/data/yt8m/2/frame/train 
curl data.yt8m.org/download.py | partition=2/frame/train    mirror=us python3

mkdir -p /work/data/yt8m/2/frame/validate ; cd /work/data/yt8m/2/frame/validate
curl data.yt8m.org/download.py | partition=2/frame/validate mirror=us python3

mkdir -p /work/data/yt8m/2/frame/test ; cd /work/data/yt8m/2/frame/test
curl data.yt8m.org/download.py | partition=2/frame/test     mirror=us python3


mkdir -p /work/data/yt8m/video
mkdir -p /work/data/yt8m/video/train ; cd /work/data/yt8m/video/train 
curl data.yt8m.org/download.py | partition=2/video/train    mirror=us python3

mkdir -p /work/data/yt8m/video/validate ; cd /work/data/yt8m/video/validate
curl data.yt8m.org/download.py | partition=2/video/validate mirror=us python3

mkdir -p /work/data/yt8m/video/test ; cd /work/data/yt8m/video/test
curl data.yt8m.org/download.py | partition=2/video/test     mirror=us python3