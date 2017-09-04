#!/usr/bin/python
from wsgiref.handlers import CGIHandler
from flask import render_template
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/testing')
def hello_again(name=None):
    return render_template('hello.html', name=name)


class ProxyFix(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['SERVER_NAME'] = "localhost"
        environ['SERVER_PORT'] = "8080"
        environ['REQUEST_METHOD'] = "GET"
        environ['SCRIPT_NAME'] = ""
        environ['PATH_INFO'] = "/"
        environ['QUERY_STRING'] = ""
        environ['SERVER_PROTOCOL'] = "HTTP/1.1"
        return self.app(environ, start_response)

    
class HeaderRewriterFix(object):

    def __init__(self, app, remove_headers=None, add_headers=None):
        self.app = app
        self.remove_headers = set(x.lower() for x in (remove_headers or ()))
        self.add_headers = list(add_headers or ())

    def __call__(self, environ, start_response):
        def rewriting_start_response(status, headers, exc_info=None):
            new_headers = []
            return start_response(status, new_headers, exc_info)
        return self.app(environ, rewriting_start_response)

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.wsgi_app = HeaderRewriteFix(app.wsgi_app)
    CGIHandler().run(app)
