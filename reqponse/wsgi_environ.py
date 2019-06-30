import copy
import gzip
from wsgiref.util import is_hop_by_hop
import six
import requests


DEFAULT_PARAMS = {
    "timeout": 5,
    "allow_redirects": True
}


def environ2dict(environ, **kwargs):
    '''
    Convert wsgi environ to a dict object for requests
    to make a http request. 
    '''
    ret = copy.copy(DEFAULT_PARAMS)
    ret['method'] = environ['REQUEST_METHOD']
    url_handler = kwargs.pop('url_handler', None)
    if not url_handler:
        ret['url'] = "%s://%s%s" % (environ['wsgi.url_scheme'],
                                    environ['HTTP_HOST'],
                                    environ['PATH_INFO'])
    else:
        ret['url'] = url_handler(environ['wsgi.url_scheme'],
                                 environ['HTTP_HOST'],
                                 environ['PATH_INFO'])
    ret['headers'] = {}
    for k, v in environ.items():
        if k.startswith('HTTP_') and k != 'HTTP_HOST':
            ret['headers'][k[5:]] = v
    ret['params'] = environ['QUERY_STRING']
    if environ.get('CONTENT_LENGTH'):
        ret['data'] = environ['wsgi.input']\
                      .read(int(environ['CONTENT_LENGTH']))
    return ret


def get_response_dict(environ, **kwargs):
    '''
    Get a response dict from a wsgi environ.
    The following handlers in kwargs are supported:

    url_handler(scheme, host, path)
    For modifying the remote url, returns a string as the new url.

    request_handler(request_env_dict)
    For modifying the current request dict(headers and body), returns
    a new dict object with the same structure as input.

    get_response_dict function returns a dict object. 
    '''
    req_env_dict = environ2dict(environ, **kwargs)
    request_handler = kwargs.get('request_handler')
    if not request_handler:
        req_dict = req_env_dict
    else:
        req_dict = request_handler(req_env_dict)
    method = req_dict.pop('method')
    url = req_dict.pop('url')    
    resp = requests.request(method, url, **req_dict)
    resp_dict = {
        "status_code": resp.status_code,
        "headers": {},
        "original_headers": {k: v for k, v in resp.headers.items()}
    }

    # Filter out headers not needed
    filtered_headers = ['content-length']
    for k, v in resp.headers.items():
        if is_hop_by_hop(k) or k.lower() in filtered_headers:
            continue
        resp_dict['headers'][k.lower()] = v

    if 'gzip' in resp.headers.get('content-encoding', set()):
        fileobj = six.BytesIO()
        gzipper = gzip.GzipFile(fileobj=fileobj, mode='w')
        gzipper.write(resp.content)
        gzipper.flush()
        resp_dict['body'] = fileobj.getvalue()
    else:
        resp_dict['body'] = resp.content

    return resp_dict
