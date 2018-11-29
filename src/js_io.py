"""
"""

from flask import Flask, render_template, request, redirect, Response
import random
import json

from split import Split

app = Flask(__name__)


@app.route("/")
def output():
    return render_template('index.html', name='Chris')


@app.route('/receiver', methods=['POST'])
def worker():
    # read json + reply
    data = request.get_json(force=True)
    split = Split(data)
    split.solve()
    results = split.get_results()
    split.output_results()
    return json.dumps(results)

if __name__ == "__main__":
    app.run()
