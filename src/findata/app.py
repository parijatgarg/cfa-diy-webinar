# -*- coding: utf-8 -*-

import os

os.environ['TOFLER_CONF'] = '/home/ubuntu/scm/scm.conf'

from Screener import Screener
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def screener():
    if request.method == 'GET':
        default_dictionary = {}
        return render_template(
            'screener.html', **default_dictionary)
    elif request.method == 'POST':
        query = request.form.get('query')
        try:
            results = Screener().run_screen(query)
        except Exception as e:
            print(e)
            return '''Something was wrong with your query. Try again.'''

        output = {
            'query': query,
            'results': results
        }
        return render_template('screener.html', **output)


def GetParser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('port')
    return parser


if __name__ == "__main__":
    args = GetParser().parse_args()
    app.run(int(args.port))
