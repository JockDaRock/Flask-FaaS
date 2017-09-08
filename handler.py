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


if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    CGIHandler().run(app)
