import requests
import json
import pickle
from plotskip import plotskip

#Sti til aktuelle API-er
#Bbox wer p.t. ikke i bruk av skriptet
rotPath = 'https://kystdatahuset.no/ws'
apis = {'mmsinr': '/api/ais/positions/for-mmsis-time', \
        'bbox': '/api/ais/positions/within-bbox-time',\
       'imonr': '/api/ship/data/nsr/for-mmsis-imos'}

#Generer URL til et API-endepunkt hos Kystdatahuset
def getURL(a):
    return rotPath + apis[a]

#Hent autentiseringsnøkkel
#Token må først skapes med skriptet auth.py
with open('token.txt', 'r') as f:
    token = f.read()

auth = 'Bearer '+ token

headers = {
    'accept': '*/*',
    'Content-Type': 'application/json',
    'Authorization': auth
}

# Hent data om et skip med IMO-nummer som variabel
def getShipInfoFromIMO(imo):
    url = getURL('imonr')

    inndata = {
        "mmsi": [],
        "imo": [int(imo)],
        "callsign": []
    }

    respons = requests.post(url, headers=headers, json=inndata).json()
    skipsdata = respons['data'][0]
    return skipsdata

#Hent ut MMSI-nummeret. Det trengs for å søke i AIS-dataene til Kystdatahuset.
def getMMSI(imo):
    skipsdata = getShipInfoFromIMO(imo)
    return skipsdata['mmsino']

#Hent navnet på båten.
def getNavn(imo):
    skipsdata = getShipInfoFromIMO(imo)
    return skipsdata['shipname']

# Finn posisjoner ved hjelp av IMO. Lagre som geoJSON.
def skipsPos(imo):
    mmsi = getMMSI(imo)
    skipsnavn = getNavn(imo)
    url = getURL('mmsinr')  # URL til endepunktet

    #Be brukeren om å definere tidsperioden det skal søkes i.
    startdato = input("Startdato (ÅÅÅÅ-MM-DD): ")
    starttid = input("Starttid (HHMM): ")
    stoppdato = input("Stoppdato (ÅÅÅÅ-MM-DD): ")
    stopptid = input("Stopptid (HHMM): ")

    #Få tidsdataene på formen ÅÅÅÅMMDDHHMM
    startdato = startdato.replace('-', '')
    stoppdato = stoppdato.replace('-', '')
    start = startdato + starttid
    stopp = stoppdato + stopptid

    #Lag dataene som API-et krever som input
    inndata = {
        'mmsiIds': [
            int(mmsi)
        ],
        'start': str(start),
        'end': str(stopp)
    }

    #API-kall. Returnerer fortegnelse. Geodataene ligger under key 'data'
    respons = requests.post(url, headers=headers, json=inndata).json()
    skipsdata = respons['data']

    # Hent ut koordinater og tidskoder fra skipsdata
    koordinater = []
    times = []
    for i in skipsdata:
        koord = [i[2], i[3]]
        koordinater.append(koord)
        times.append(i[1])
    print("Antall koordinater:", len(koordinater))

    #Generer en geojson-struktur av dataene
    #Skriptet trenger minst to koordinatpar.
    if len(koordinater) > 1:
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": koordinater
                    },
                    "properties": {
                        "times": times,
                        "mmsi": mmsi
                    }
                }
            ]
        }

        geojson_str = json.dumps(geojson)

        # Lag en liste som inneholder skipsnavn, imo og mmsi,
        # samt start- og sluttid og -koordinater.
        #Listen lagres som en picklefil og skal brukes i kartet
        # for å vise endepunkter.
        metadata = [skipsnavn, imo, mmsi]
        startkoord = koordinater[0]
        metadata.append(startkoord)
        stoppkoord = koordinater[-1]
        metadata.append(stoppkoord)
        tid1 = times[0]
        metadata.append(tid1)
        tid2 = times[-1]
        metadata.append(tid2)
        print(metadata)

        #Lage filnavn unikt for hvert søk
        #Dataene legges i undermappen 'data'
        filnavn = 'data/' + skipsnavn + '_' + str(imo) + '_' + startdato + '-' + stoppdato + '.geojson'
        filnavnmeta = 'data/' + skipsnavn + '_' + str(imo) + '_' + startdato + '-' + stoppdato + '.pickle'

        # Lagre geoJSON-data
        with open(filnavn, 'w') as f:
            f.write(geojson_str)
        print("Data lagret med filnavn", filnavn)

        # Lagre metadata
        with open(filnavnmeta, 'wb') as f:
            pickle.dump(metadata, f)
        print("Metadata lagret med filnavn", filnavnmeta)

        # Plotte dataene
        plotskip(filnavn)
    else:
        print("Fant ingen AIS-data i dette tidsrommet")
