### AUF-25 · Modell per Klick auswählen

Zweck: Ein Klick auf ein *Modell* der *ausgewählten* *Einheit* macht es zu ihrer *Ebene*, ein weiterer Klick darauf wieder die ganze *Einheit*; ohne Knopf (Anliegen 980, Vorbild `ArbiterMap/frontend/static/js/model_selection.js:336`).
Am Bildschirm: ein *gesetztes* *Modell* der *ausgewählten* *Einheit* anklicken.

- AUF-25.1 **Gegeben** eine *ausgewählte* *Einheit*, **wenn** jemand eines ihrer *gesetzten* *Modelle* anklickt, das nicht ihre *Ebene* ist, **dann** ist ihre *Ebene* dieses *Modell*, gleich ob davor die ganze *Einheit* oder ein anderes ihrer *Modelle* (Vorbild `:350`).
- AUF-25.2 **Gegeben** eine *ausgewählte* *Einheit*, deren *Ebene* ein *Modell* ist, **wenn** jemand dieses *Modell* anklickt, **dann** ist ihre *Ebene* die ganze *Einheit* (Vorbild `:347`).
- AUF-25.3 **Wenn** AUF-25.1 oder 25.2 greift, **dann** bleiben *Auswahl*, *Modelle*, *Einheit in Aufstellung* und *an der Reihe* gleich.
- AUF-25.4 **Gegeben** eine *ausgewählte* *Einheit*, deren *Ebene* ein *Modell* ist, **dann** kennzeichnet die *Karte* statt nach AUF-5.7 nur dieses *Modell* (Anliegen 980).
