''' $ export FLASK_APP=FlaskHelloWeb.py
    $ flask run'''
from flask import Flask, url_for, request, render_template
import os
import requests
import json

app = Flask(__name__)

_kbase_url = os.environ.get('KBASE_ENDPOINT', 'https://ci.kbase.us/services')
_catalog_url = _kbase_url + '/catalog'
payload = {
    'id': 0,
    'method': 'Catalog.get_module_version',
    'version': '1.1',
    'params': [{   
                    'module_name': 'kb_ReadsUtilities',
                    'git_commit_hash' : '1b6d5c03cc5a96d867f1c1c061dc556bd2686ace',
                    'include_compilation_report': 1
                }]
}


@app.route('/', methods=['GET'])
def root():
    resp = requests.post(_catalog_url, data=json.dumps(payload))
    resp_json = resp.json()
    if 'error' in resp_json:
        raise Exception('oh no!')
    return render_template('simple.html', resp_json=resp_json)
