# Vertrag: Aufstellen · Ziehen

Abschnitt der *Aufstellung*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt.md).

Nach V10 (AUF-24.3, 26.5; 28.2, 29.1 und 29.3 nur für das erste Weiterrücken, Rest:
Anliegen 2180): `stellenBeimLoslassen(modell, stelle)` → *Modell* → *Stelle* nennt jedes
*Modell*, das `modellLoslassen` *setzen* würde (das gezogene oder jedes *gesetzte* der
*Einheit*, [V3](auswahl.md)), an seiner *Stelle* nach AUF-8.2, 21.1, 21.2, 26.1 und 29.1,
ohne zu *setzen*, Wächter wie dort. `modellLoslassen` *setzt* genau diese, so steht nach dem
Loslassen alles, wo die *Karte* es zeigte (AUF-28.2). Der Weg beginnt an der *gesetzten*
*Stelle*, nicht an der zuletzt gezeigten. Angehalten wird nur, wenn die *Stelle* am Ende
eine *Base* *überdecken* würde, an der ersten, an die eine *Base* auf der geraden Strecke
stößt (AUF-29, [S3](../../domaene.md#stelle-und-rechnen)); bis AUF-27 *überdeckt* am Anfang
des Wegs keine *Base* eine, gegen die angehalten wird. Beispiel
[stelleBeimLoslassen.json](../stelleBeimLoslassen.json): Stand von V1, `x=35&y=28` für
*Modell* 1, AUF-21.2 rückt den Block hinein.

*Neben der Karte* loslassen (V10, Seite): AUF-28.1 mit dem Punkt der letzten 200; ein
*Modell* einer *aufgestellten* *Einheit* bekommt in V10 nur 409, also keine Anfrage und
keine `sperrmeldung` (AUF-16.8). Ist das gezogene *Modell* nicht *gesetzt* (eine zweite Seite
zeigt es noch, AUF-16.7), geben vor jedem Wächter `stellenBeimLoslassen` `{}` (V10 200 mit
leerem `modelle[]`) und `modellLoslassen` nichts zurück, ohne `Sperre`, Stand unverändert.
Warum vor den Wächtern: Kein *Grund* nach AUF-16.7, auch wenn inzwischen eine andere
*Einheit in Aufstellung* ist. Beispiele: [losgelassen.json](../losgelassen.json), V5 200:
Stand von `stelleBeimLoslassen.json`, dann `PUT …/modelle/1/stelle` mit `{"x": 35, "y": 28}`,
also neben der *Karte* nach dieser 200 losgelassen.
[keineStelleBeimLoslassen.json](../keineStelleBeimLoslassen.json), V10 200: Stand von
`zurueckgelegt.json`, dann dieselbe Abfrage wie `stelleBeimLoslassen.json`; V5 danach an
jedem Punkt 200 gleich `zurueckgelegt.json`. Eine 409 in V10 liefert die Seite wie
[sperre.json](../sperre.json), ihr Inhalt zählt dort nicht (V10).

Prüft wie im Querschnitt: AUF-29.1 mit einem Weiterrücken ab der *gesetzten* *Stelle*, an
der *Stelle* nach dem Loslassen (28.2): auf der Strecke zur *Stelle*, wie `web/` sie liest
(S2, exakt kollinear), keine *Base* *überdeckt*, zur ersten angestoßenen `abstandHöchstens`
1/100″; den Raster prüfen nur Unit-Tests. AUF-24.3, 26.5 und 28.1 am Bildschirm nach V10.
AUF-28.1 mit `page.route`: Der Körper von V5 gleicht dem Punkt der letzten 200, auch wenn
danach eine 409 kam; die Kreise stehen wie `losgelassen.json`. Am Dienst: die Antworten
gleich den Beispielen. Am echten Server: über die *Spielfeldkante* auf eine *Armeeliste* und daneben
loslassen, die *Stellen* gleich den zuletzt gelesenen `cx`, `cy` (B3). AUF-16.8: keine
Anfrage nach V5, Kreise wie vor dem Ziehen, keine `sperrmeldung`. AUF-16.7: mit einer Seite
von vor `PUT /api/zurücklegen`, auf und neben der *Karte* losgelassen, danach kein *Modell*
der *Einheit* auf der *Karte* (die Seite zeichnet die Antwort, V6) und keine `sperrmeldung`.
