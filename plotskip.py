import folium
import geopandas as gpd
from IPython.display import display, HTML
import pickle

# Funksjon som lager kart av geojson
def plotskip(filnavn):
    #filnavnmeta inneholder metadata som skal inn i endepunktene i grafen på kartet
    filnavnmeta = filnavn.replace('.geojson', '.pickle')

    #filnavnhtml skal huse HTML-filen som viser kartet
    filnavnhtml = filnavn.replace('.geojson', '.html')

    # Last inn data. Bruker geopandas.
    # Filnavnet er generert av skipsPos.
    gdf = gpd.read_file(filnavn)

    # Last inn metadata i form av en liste
    with open(filnavnmeta, 'rb') as f:
        meta = pickle.load(f)

    # Finn rammen til dataene
    startkoord = meta[3][::-1]  # Reverser punktene for å få lat/lon i rett rekkefølge
    stoppkoord = meta[4][::-1]
    starttid = meta[5]
    stopptid = meta[6]

    #Må finne sentrum av koordinatene slik at kartet gir rett visning
    sentrum = [(startkoord[0] + stoppkoord[0]) / 2, (startkoord[1] + stoppkoord[1]) / 2]

    #Opprett kart med folium
    kart = folium.Map(location=sentrum, zoom_start=8)

    # Legg geoJSON-data oppå
    folium.GeoJson(gdf).add_to(kart)

    # Legg på metadata
    folium.Marker(location=startkoord, popup=starttid).add_to(kart)
    folium.Marker(location=stoppkoord, popup=stopptid).add_to(kart)

    # Lag div som skal vise metadata over kartet
    txt = f"""
    <div style='font-family: monospace; font-size 20px; background-color:white; padding: 10px;'>
    <h1>{meta[0]}</h1>
    <p>IMO: {meta[1]} MMSI: {meta[2]} Tid: {meta[5]} - {meta[6]}</p>
    </div>
    """

    # Legg div over kartet med IPython.display
    display(HTML(txt + kart._repr_html_()))

    # Lagre kartet i to varianter:
    # En fil med konstant filnavn, som endres hver gang et nytt datasett lagres.
    # #En fil med unikt filnavn, som skaper en unik HTML-fil for hvert skipssøk
    # Dataene lagres i undermappen data, men stien kan selvsagt tilpasses.
    with open('data/skipskart.html', 'w') as f:
        f.write(txt + kart._repr_html_())
    with open(filnavnhtml, 'w') as f:
        f.write(txt + kart._repr_html_())