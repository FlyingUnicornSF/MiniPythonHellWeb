''' $ export FLASK_APP=NarrativeMethodStoreAppList.py
    $ flask run'''
from flask import Flask, url_for, request, render_template, jsonify, Markup
import os
import requests
import json

app = Flask(__name__)

_kbase_url = os.environ.get('KBASE_ENDPOINT', 'https://ci.kbase.us/services')
_NarrativeMethodStore_url = _kbase_url + '/narrative_method_store/rpc'
payload = {
    'id': 0,
    'method': 'NarrativeMethodStore.list_methods',
    'version': '1.1',
    'params': [{}]
}


@app.route('/', methods=['GET'])
def root():
    resp = requests.post(_NarrativeMethodStore_url, data=json.dumps(payload))
    try:
        resp_json = resp.json()
    except ValueError as err:
        print(err)
    #if 'error' in resp_json:
        #raise Exception('oh no!')
    
    print(resp_json['result'][0][10])
    return render_template('index.html', resp_json=resp_json['result'][0])

