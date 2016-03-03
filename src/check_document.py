#!/bin/env python3
#-*- coding:utf-8 -*-

import json,logging,os,elasticsearch,sys,datetime

from json_diff import json_struct_patch

def get_matches(hostname, es, query_size, indices, debug=False, numdays=14):
    query = {
         "filter": {
             "term": {
                "hostname": hostname
             }
         }
    }
    index_list = []
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
    for date in date_list:
        index_value = "logstash-%s" %(str(date).split(' ')[0].replace('-','.'))
        if indices.exists(index_value):
            index_list.append(index_value)

    matches = es.search(index_list, body=query, size=query_size, explain=True)
    logger.debug("Matches for: query: %s | index:  %s |  query_size: %s" %(query, index_list, query_size))
        #print matches
    logger.debug('-'*80)
    return matches

def validate_documents(matches, differ):
    if matches['hits']['total'] == 0:
        return;
    hits = [x['_source'] for x in  matches['hits']['hits']]
    #logger.debug("the source is %s"%(hits))
    #diff = json_struct_patch.JsonStructPatch(template)
    return differ.compare_series(hits)

def main():

    es_server = os.getenv('ELASTICSEARCH_SERVER')
    es = elasticsearch.Elasticsearch([es_server])
    indices = elasticsearch.client.IndicesClient(es)
    logger.info("----Starting document validation----")
    with open(sys.argv[1]) as json_file:
        json_template = json.load(json_file)

    query_size = int(os.getenv('QUERY_SIZE'))
    num_days = int(os.getenv('NUM_DAYS'))
    index_out = os.getenv('JOBS_INDEX_NAME')
    debug = os.getenv('DEBUG')
    hostname = sys.argv[2]

    differ = json_struct_patch.JsonStructPatch(json_template['mappings']['_default_']['properties'])
    base_matches = get_matches(hostname, es, query_size, indices, debug, num_days)
    #logger.debug("Search result is %s",base_matches)
    diff = validate_documents(base_matches, differ)
    differ.print_diff(diff)
    #logger.info("the difference with template is %s", diff)

if __name__ == '__main__':
    logger = logging.getLogger("templatevalidator")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    _stdlog = logging.StreamHandler()
    _stdlog.setLevel(logging.DEBUG)
    _stdlog.setFormatter(formatter)

    logger.addHandler(_stdlog)
    main()
