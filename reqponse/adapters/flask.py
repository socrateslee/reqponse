'''
An adapter for flask to use reqponse.wsgi_environ
'''
import flask
from .. import wsgi_environ


def get_response(resp_dict=None, **kwargs):
    if resp_dict is None:
        resp_dict = wsgi_environ.get_response_dict(
            flask.request.environ,
            **kwargs)
    resp = flask.Response(resp_dict['body'])
    resp.status_code = resp_dict['status_code']
    for (k, v) in wsgi_environ\
                  .iter_response_headers(resp_dict['headers']):
        resp.headers.add_header(k, v)
    return resp
