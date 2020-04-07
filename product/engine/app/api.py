#!/usr/bin/env python3

import   click as     cli
from      time import time
from      json import loads
from     flask import Flask, Response, jsonify, request
from  waitress import serve
from     index import Index
from     cache import Cache

CLS='\x1Bc'
PAD='\x1B[K'
SKY='\x1B[48;5;39m'
GRN='\x1B[48;5;42m'
PUR='\x1B[48;5;161m'
RED='\x1B[48;5;196m'

TXT='\x1B[38;5;190m'
RST='\x1B[0m'
EOL='\n'

def cache(app):

    if  cache.object is None:
        cache.object  = Cache(app.config['folder'])

    return cache.object

cache.object = None

def index(app):

    if  index.object is None:
        index.object  = Index(app.config['folder'])

    return index.object

index.object = None

app = Flask(__name__)

@app.route('/api/queueCache', methods = ['POST'])
def api_queueCache():

    print(f'{EOL}{SKY}{TXT} HNDLR > api_queueCache [{time()}] {PAD}{RST}')

    request.get_data()

    video = request.args.get('video')
    stime = request.args.get('stime')
    etime = request.args.get('etime')
    data  = request.data

    if  video :

        print(f'{PUR}{TXT} VIDEO > {video} {PAD}')
        print(f'{PUR}{TXT} STIME > {stime} {PAD}')
        print(f'{PUR}{TXT} ETIME > {etime} {PAD}{RST}{EOL}')

        response           = {}
        response['result'] = cache(app).queueCache(video, stime, etime)

        return reponse

    else :

        print(f'{RED}{TXT} ERROR > Invalid Request {PAD}{RST}{EOL}')

        return { 'error' : 'Invalid Request' }

@app.route('/api/queryIndex', methods = ['POST'])
def api_queryIndex():

    print(f'{EOL}{SKY}{TXT} HNDLR > api_queryIndex [{time()}] {PAD}{RST}')

    request.get_data()

    terms =       request.args.get('terms')
    knobs = loads(request.args.get('knobs'))

    data  = request.data

    if  terms :
        
        print(f'{PUR}{TXT} TERMS > {terms} {PAD}')
        print(f'{PUR}{TXT} KNOBS > {knobs} {PAD}{RST}{EOL}')

        response           = {}
        response['result'] = index(app).queryIndex(terms, knobs)

        return response

    else :

        print(f'{RED}{TXT} ERROR > Invalid Request {PAD}{RST}{EOL}')

        return { 'error' : 'Invalid Request' }

@app.route('/')
def hello():

    print(f'{EOL}{SKY}{TXT} HELLO {PAD}{RST}{EOL}')

    return f'ActIQ Engine Server Up and Running! : {time()}'

@cli.command()
@cli.option('--folder', default = '/engine/cache', type = str)
def main(folder):

    print(f'{CLS}{SKY}{TXT}ActIQ Engine : RESTful Application Programming Interface{PAD}{RST}{EOL}')

    app.config['folder'] = folder

    index(app)
    cache(app)

    serve(app, host = '0.0.0.0', port = 5000)

if  __name__ == '__main__':

    main()