"""
"""

from flask import Flask, render_template, request, redirect, Response
import random
import json

app = Flask(__name__)


@app.route("/output")
def output():
    return render_template('index.html', name='Joe')


@app.route('/receiver', methods=['POST'])
def worker():
    # read json + reply
    data = request.get_json(force=True)
    result = ''
    for item in data:
        # loop over every row
        result += str(item['make']) + '\n'
    print("AHDLJNFKJNDFKJN")
    return result

if __name__ == "__main__":
    app.run()
