from elasticsearch import Elasticsearch
import pandas as pd

def most_prob(query):   
    pd_query = []
    dict_query = {}
    splits = query.split()
    for split in splits:
        search = es.search(index="ActiQ", body={"query": {"match" : {"text": split }}})
        for hit in search['hits']['hits']:
            if 'hit' not in dict_query:
                dict_query['hit'] = []
            dict_query['hit'].append(1)
            for key,val in hit["_source"].items():
                if key not in dict_query:
                    dict_query[key] = []
                dict_query[key].append(val)


    pd_search = pd.DataFrame.from_dict(dict_query)
    pd_search = pd_search.astype({'prob': 'float'})
    video = pd_search.groupby('video').agg('sum')['hit'].idxmax()
    stamp = pd_search.iloc[pd_search[pd_search['video'] == video]['prob'].idxmax()]['stamp']
    
    return video, stamp