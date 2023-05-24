# Sporskip

En app for å spore skip med AIS-data

Skriptene ble skrevet som prosjektoppgave våren 2023 i UJO665, Programmering i Python.

Alle data skal krediteres [Kystverket](https://www.kystverket.no/) / [Kystdatahuset](https://kystdatahuset.no/).

Så langt hentes bare data fra sporingstjenesten av ett og ett skip fra API-et til Kystdatahuset. Det er [mange flere muligheter](https://kystdatahuset.no/ws/swagger/index.html), men jeg har ikke hatt tid til å utforske alle. Det kommer jeg antakelig tilbake til etter hvert.

Her følger en beskrivelse av hva filene gjør.

## auth.py
Et skript som fornyer tilgangen du trenger for å hente ned data fra API-ene. En tilgangsnøkkel lagres i filen "token.txt" som du senere kan hente inn når du skal gjøre en request.

## skip.py
Her gjøres request-en til API-et til Kystdatahuset. Jeg bruker IMO-nummer som variabel, da dette er unikt for hvert skip. Men Kystdatahusets API trenger MMSI-nummeret, som refererer til skipets AIS-sender. Derfor har jeg laget en liten funksjon getMMSI(imo) slik at jeg får hentet MMSI med IMO som input. 

Funksjonen getShipInfoFromIMO(imo) henter ut alle tilgjengelige metadata om fartøyet. Output er en fortegnelse.

skipsPos(imo) gjør selve spørringen mot API-endepunktet. Brukeren blir bedt om starttid og stopptid for søket. Kystdatahuset anbefaler ikke lengre enn en ukes tidsintervall, da datasettet kan bli svært stort.

Funksjonen genererer en geoJSON-fil av alle lokasjonsdataene den finner. Filen blir lagret med et unikt filnavn i mappen data. Det blir også generert en liste med noen få metadata som blir lagret som en .pickle. Disse dataene er til å markere endepunktene for skipets kurs i kartet når det plottes.

## plotskip.py
Her plottes dataene, som skipsPos akkurat lagret, i et folium-kart. Det genereres også en HTML-fil med en 'div' over kartet som viser navn på fartøy, tidsperiode, IMO- og MMSI-nummer. Se bildeeksempler i bildemappen.

## web
Jeg ville lage en app som kunne tas i bruk også av andre som ikke har Python-kompetanse. Jeg har derfor laget en flask-app som benytter de samme skriptene, men som gjør det mulig å gi input i et web-grensesnitt. Se bildeeksempel i bildemappen.