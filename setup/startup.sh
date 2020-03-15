#!/bin/bash

echo Starting Capstone RAPIDS Container

cd /work

source activate rapids

jupyter-lab --allow-root --ip=0.0.0.0 --no-browser --NotebookApp.token='capstone'

echo Bye
