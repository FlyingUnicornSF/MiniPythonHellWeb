''' $ export FLASK_APP=dropdown.py
    $ FLASK_DEBUG=1 flask run
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
# Python doesn't have switch case??? 
@app.route('/', methods=['GET'])
def get_apps():
    resp = requests.post(_NarrativeMethodStore_url, data=json.dumps(payload))
    try:
        resp_json = resp.json()
    except ValueError as err:
        print(err)
    
    option = request.args.get('organize_by')
    organized_list = {}
    if option == None:
        organized_list = {
            'All Apps:' : resp_json['result'][0]
        }
        print("NONE")
    elif option == "Category":
        organized_list = {}
        # for app in resp_json['result'][0]:
            # print(app['categories'])
        for app in resp_json['result'][0]:
            if app.get('categories') is not None:
                # if categories exisit for an app, check if it's in the organized_list.
                categories = app.get('categories')
                for category in categories:
                    if category not in organized_list:
                        # if it is not alreay in the organized_list, then add category and the app associated. 
                        organized_list[category] = [app]
                    elif category and category in organized_list:
                        # if category is already exisiting in the dictionay, then add the app to the list.
                        arr = organized_list.get(category)
                        arr.append(app)
                        organized_list[category] = arr
                    else:
                        # This shouldn't happen.
                        pass

    elif option == "Module": 
        print(option)
    elif option == "Developer":
        print(option)
    else:
        print("this shouldn't happen!")
    
    return render_template('index.html', options=options, organized_list=organized_list )

