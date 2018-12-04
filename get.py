''' $ export FLASK_APP=get.py
    $ FLASK_DEBUG=1 flask run 
    '''
from flask import Flask, url_for, request, render_template, jsonify, Markup, g
import os
import requests
import json
app = Flask(__name__)

_kbase_url = os.environ.get('KBASE_ENDPOINT', 'https://ci.kbase.us/services')
# Narrative Method Store URL needs rpc at the end. 
# ref L43/44 https://github.com/kbase/narrative_method_store/blob/master/scripts/nms-listmethods.pl 
_NarrativeMethodStore_url = _kbase_url + '/narrative_method_store/rpc'
payload = {
    'id': 0,
    'method': 'NarrativeMethodStore.list_categories',
    'version': '1.1',
    'params': [{
        'load_methods': 1,
        'load_apps': 0,
        'load_types': 0,
        'tag': 'release'
    }]
}

@app.route('/', methods=['GET'])
def get_apps():
    resp = requests.post(_NarrativeMethodStore_url, data=json.dumps(payload))
    try:
        resp_json = resp.json()
    except ValueError as err:
        print(err)
   
    return render_template('get.html',  resp_json=resp_json['result'][1])

