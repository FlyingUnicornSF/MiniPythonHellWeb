import requests
import json


class GenericClient(object):
    def __init__(self, module=None, url=None, token=None):
        if module is None:
            raise ValueError('The "module" argument is required')
        if url is None:
            raise ValueError('The "url" argument is required')

        self.module = module
        self.token = token
        self.url = url

    def call_func(self, func_name, params):
        if not isinstance(func_name, str):
            raise ValueError('"func_name" must be a string')
        if not isinstance(params, list):
            raise ValueError('"params" must be an array')

        call_params = {
            'id': 'uniquestring',
            'method': self.module + '.' + func_name,
            'version': '1.1',
            'params': params
        }
        header = {
            'Content-Type': 'application/json'
        }
        if self.token:
            header['Authorization'] = self.token

        r = requests.post(self.url, headers=header, data=json.dumps(call_params), timeout=60)
        if r.headers.get('content-type', '').startswith('application/json'):
            try:
                response = r.json()
            except Exception as err:
                #TODO: Gave error: instance of Exception has no message number
                #raise ValueError('Invalid response; claiming to be json, but not: %s' % err.message)
                raise ValueError('Invalid response; claiming to be json')

            result = response.get('result')
            error = response.get('error')
            if error:
                # Better be a JSON RPC 2.0 Error structure
                raise ValueError('temp error - TODO: AKIYO')

            if not (isinstance(result, list) or result is None):
                raise ValueError('Expected result to be list, is ' + type(result).__name__)
                
            return result

        r.raise_for_status()
        raise ValueError('Invalid response; not json, not an error status')