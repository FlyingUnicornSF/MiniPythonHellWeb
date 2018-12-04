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

''' sort_app takes in an array, organize_by, which is derived from drop down menu and decoded response. 
        organize_by is an array of either categories, modules, or developers. 
        app_list is an array of all apps.
    It returns a dictionary of {key = category/developer/module : value = app }.
'''
def sort_app(organize_by, app_list):
    organized_app_list = {}
    for app in app_list:
        if app.get(organize_by) is not None:
            # check if it already exisits in the organized_app_list dictionary.
            items = app.get(organize_by)
            # Modules are not in an array. Any option that are no in an array and a string, store in an array to avoid string iteration.
            if isinstance(items, str):
                items = [items]

            for item in items:
                if item not in organized_app_list:
                    # if it is not alreay in the organized_app_list, then add category and the app associated. 
                    organized_app_list[item] = [app]
                elif item in organized_app_list:
                    # if category is already exisiting in the dictionay, then add the app to the list.
                    arr = organized_app_list.get(item)
                    arr.append(app)
                    organized_app_list[item] = arr
                else:
                    # This shouldn't happen.
                    pass
        else:
            # If the organized by item does not exisit in app information, then simply pass. 
            pass
    return organized_app_list

@app.route('/', methods=['GET'])
def get_apps():
    resp = requests.post(_NarrativeMethodStore_url, data=json.dumps(payload))
    try:
        resp_json = resp.json()
        # Apps are stored in the first element of the result array.
        app_list = resp_json['result'][0]
    except ValueError as err:
        #TODO: Find document on set ValueError
        print(err)

    # Get value from dropdown menue from url parameter
    option = request.args.get('organize_by')

    if option == None:
        # When the page loads and drop down menue has not been used, return all of the apps non-sorted.
        organized_list = {
            'All Apps:' : app_list
        }

    elif option == "Category":
        sorted_list = sort_app('categories', app_list)
        #TODO: shape sorted_list. need to get GetCategoryParams for each from narrative method store
        # for category in sorted_list:
        #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', category)
        #     category_info = requests.post(_NarrativeMethodStore_url, data=json.dumps({
        #                                                                                 'id': 0,
        #                                                                                 'method': 'NarrativeMethodStore.get_category',
        #                                                                                 'version': '1.1',
        #                                                                                 'params': [{'ids': [category]}]
        #                                                                             }))
        #     print(category_info.json())
        category_info = requests.post(_NarrativeMethodStore_url, data=json.dumps({
                                                                                    'id': 0,
                                                                                    'method': 'NarrativeMethodStore.get_category',
                                                                                    'version': '1.1',
                                                                                    'params': [{'ids': ['sequence']}]
                                                                                }))
        print(category_info.json())
        organized_list = sort_app('categories', app_list)    
    elif option == "Module":
        organized_list = sort_app('module_name', app_list)
    elif option == "Developer":
        #TODO: shape sorted_list. need to get developer names for each from ??
        organized_list = sort_app('authors', app_list)
    else:
        print("this shouldn't happen!")
    
    return render_template('index.html', options=options, organized_list=organized_list )

