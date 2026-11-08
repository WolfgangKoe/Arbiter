### AUF-25 · Modell per Klick auswählen

Zweck: Ein Klick auf ein *Modell* der *ausgewählten* *Einheit* macht seine *Modellebene* zu ihrer *Ebene*, ein weiterer Klick darauf wieder die *Einheitenebene*; ohne Knopf (Anliegen 980, Vorbild `ArbiterMap/frontend/static/js/model_selection.js:336`).
Am Bildschirm: ein *gesetztes* *Modell* der *ausgewählten* *Einheit* anklicken.

- AUF-25.1 **Gegeben** eine *ausgewählte* *Einheit*, **wenn** jemand eines ihrer *gesetzten* *Modelle* anklickt, dessen *Modellebene* nicht ihre *Ebene* ist, **dann** ist ihre *Ebene* die *Modellebene* dieses *Modells*, gleich welche davor (Vorbild `:350`).
- AUF-25.2 **Gegeben** eine *ausgewählte* *Einheit* mit der *Modellebene* eines *Modells*, **wenn** jemand dieses anklickt, **dann** ist ihre *Ebene* die *Einheitenebene* (Vorbild `:347`).
- AUF-25.3 **Wenn** AUF-25.1 oder 25.2 greift, **dann** bleiben *Auswahl*, *Modelle*, *Einheit in Aufstellung* und *an der Reihe* gleich.
- AUF-25.4 **Gegeben** eine *ausgewählte* *Einheit* mit der *Modellebene* eines *Modells*, **dann** kennzeichnet das *Spielfeld* statt nach AUF-5.7 nur dieses (Anliegen 980).
