clear

docker rm -f rapids > /dev/null 2>&1

docker pull rapidsai/rapidsai-dev:0.11-cuda10.1-devel-ubuntu18.04-py3.7 > /dev/null 2>&1

docker run -d \
--name rapids \
--gpus all \
--shm-size="8g" \
--entrypoint /work/ActIQ/setup/startup.sh \
-p 8888:8888 -p 8787:8787 -p 8786:8786 \
-v /work:/work \
rapidsai/rapidsai-dev:0.11-cuda10.1-devel-ubuntu18.04-py3.7
