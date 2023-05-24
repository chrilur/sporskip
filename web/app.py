from flask import Flask, request, render_template, send_from_directory, make_response
from skip import *
import re

app = Flask(__name__, static_folder='static')

@app.route('/', methods=['GET', 'POST'])

def home():
    if request.method == 'POST':
        imo = request.form.get('imo')
        startdato = request.form.get('startdato')
        starttid = request.form.get('starttid')
        stoppdato = request.form.get('stoppdato')
        stopptid = request.form.get('stopptid')

        skipsPos(imo, startdato, starttid, stoppdato, stopptid)
        #oppdater_index()
        response = make_response(render_template('index.html'))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return response
    else:
        #oppdater_index()
        response = make_response(render_template('index.html'))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return response

@app.route('../data/skipskart')
def skipskart():
    return send_from_directory('data', 'skipskart.html')

if __name__ == '__main__':
    app.run()
    
    