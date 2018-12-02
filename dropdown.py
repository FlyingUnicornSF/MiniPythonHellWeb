''' $ export FLASK_APP=dropdown.py
    $ flask run
    https://stackoverflow.com/questions/22669342/passing-a-variable-into-python-from-jinja2-drop-down-menu
    https://stackoverflow.com/questions/11873576/how-to-get-value-from-dropdown-list
    
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
    'method': 'NarrativeMethodStore.list_methods',
    'version': '1.1',
    'params': [{}]
}
options = ['Organize by', 'Category', 'Module', 'Developer']

@app.route('/', methods=['GET'])
def get_apps():
    print('ARGS!', request.args)
    resp = requests.post(_NarrativeMethodStore_url, data=json.dumps(payload))
    try:
        resp_json = resp.json()
    except ValueError as err:
        print(err)
    #if 'error' in resp_json:
        #raise Exception('oh no!')
    print(resp_json['result'][0][10])
    return render_template('dropdown.html', resp_json=resp_json['result'][0][10], options=options)

@app.route('/organize_by_category', methods=['POST'])
# @app.route('/?organize_by=Category', methods=['GET'])
def organize_by_category():
    return 'oh nooooooo!'