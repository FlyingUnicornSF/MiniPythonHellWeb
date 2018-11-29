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
    'method': 'Catalog.list_basic_module_info',
    'version': '1.1',
    'params': [{'include_released': 1,
                'include_unreleased': 1,
                'include_disabled': 0}]
}


@app.route('/', methods=['GET'])
def root():
    resp = requests.post(_catalog_url, data=json.dumps(payload))
    resp_json = resp.json()
    if 'error' in resp_json:
        raise Exception('oh no!')
    return render_template('index.html', resp_json=resp_json)
