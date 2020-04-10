mkdir -p /work/data/yt8m/frame ; cd /work/data/yt8m/frame

curl data.yt8m.org/download.py | partition=3/frame/validate mirror=us python3
curl data.yt8m.org/download.py | partition=3/frame/test     mirror=us python3

mkdir -p /work/data/yt8m/frame ; cd /work/data/yt8m/frame

curl data.yt8m.org/download.py | partition=2/frame/train    mirror=us python3
curl data.yt8m.org/download.py | partition=2/frame/validate mirror=us python3
curl data.yt8m.org/download.py | partition=2/frame/test     mirror=us python3

mkdir -p /work/data/yt8m/video ; cd /work/data/yt8m/video

curl data.yt8m.org/download.py | partition=2/video/train    mirror=us python3
curl data.yt8m.org/download.py | partition=2/video/validate mirror=us python3
curl data.yt8m.org/download.py | partition=2/video/test     mirror=us python3
