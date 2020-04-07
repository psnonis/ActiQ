import csv
import sys
import os
import re
import json
import requests
from elasticsearch import Elasticsearch

dataFilePath = '/engine/cache/'

class ElasticSearchImporter(object):
    def importToDb(self, fileName, indexDbName, indexType="default"):
        csv.field_size_limit(sys.maxsize)
        if max_rows is None:
            max_rows_disp = "all"
        else:
            max_rows_disp = max_rows
            
        es = Elasticsearch()
        print("")
        print(" ----- CSV to ElasticSearch ----- ")
        print("Importing %s rows into `%s` from '%s'" % (max_rows_disp,indexDbName, dataFilePath))
        print("")

        count = 0
        headers = []
        headers_position = {}
        to_elastic_string = ""
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter, quotechar='"')
            for row in reader:
                if count == 0:
                    for iterator, col in enumerate(row):
                        headers.append(col)
                        headers_position[col] = iterator
                elif max_rows is not None and count >= max_rows:
                    print('Max rows imported - exit')
                    break
                elif len(row[0]) == 0:    # Empty rows on the end of document
                    print("Found empty rows at the end of document")
                    break
                else:
                    pos = 0
                    if os.name == 'nt':
                        _data = json_struct.replace("^", '"')
                    else:
                        _data = json_struct.replace("'", '"')
                    _data = _data.replace('\n','').replace('\r','')
                    for header in headers:
                        if header == datetime_field:
                            datetime_type = dateutil.parser.parse(row[pos])
                            _data = _data.replace('"%' + header + '%"', '"{:%Y-%m-%dT%H:%M}"'.format(datetime_type))
                        if header == "rank":
                            row[pos] = str(int(row[pos])+1)
                            _data = _data.replace('"%' + header + '%"', row[pos])
                        if header == "stamp":
                             _data = _data.replace('"%' + header + '%"', str(int(row[pos])))
                        else:
                            try:
                                int(row[pos])
                                _data = _data.replace('"%' + header + '%"', row[pos])
                            except ValueError:
                                _data = _data.replace('%' + header + '%', row[pos])
                        
                        es.index(index=indexDbName, doc_type=indexType, body=obj)
                        pos += 1
                    # Send the request
                    if id_column is not None:
                        index_row = {"index": {"_index": indexDbName,
                                               '_id': row[headers_position[id_column]]}}
                    else:
                        index_row = {"index": {"_index": elastic_index, "_type": elastic_type}}
                    json_string = json.dumps(index_row) + "\n" + _data + "\n"
                    to_elastic_string += json_string
                count += 1
                if count % 10000 == 0:
                    send_to_elastic(elastic_address, endpoint, ssl, username, password, to_elastic_string, count)
                    to_elastic_string = ""

        print('Reached end of CSV - sending to Elastic')
        
importer = ElasticSearchImporter()
importer.importToDb("result.csv", "testIndex", indexType="default")