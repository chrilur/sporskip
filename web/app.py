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

        # Les det genererte kart-HTML-innholdet fra filen
        with open('data/skipskart.html', 'r') as f:
            skipskart_html = f.read()

        #Les tekstfilen
        with open('static/text.js', 'r') as f:
            tekstinnhold = f.read()

        return render_template('index.html', skipskart_html=skipskart_html, tekstinnhold=tekstinnhold)
    else:
        return render_template('index.html')

@app.route('/data/skipskart')
def skipskart():
    return send_from_directory('data', 'skipskart.html')

if __name__ == '__main__':
    app.run()
    
    