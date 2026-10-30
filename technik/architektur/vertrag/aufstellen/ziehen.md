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
*Modell* 1, AUF-21.2 rückt den Block hinein. Neben dem *Spielfeld*: AUF-28.1, mit Item
loslassenNebenDerKarte; eine *aufgestellte* *Einheit* bekommt nur 409 (AUF-16.8).

Prüft wie im Querschnitt: AUF-29.1 mit einem Weiterrücken ab der *gesetzten* *Stelle*, an
der *Stelle* nach dem Loslassen (28.2): auf der Strecke zur *Stelle*, wie `web/` sie liest
(S2, exakt kollinear), keine *Base* *überdeckt*, zur ersten angestoßenen `abstandHöchstens`
1/100″; den Raster prüfen nur Unit-Tests. AUF-24.3, 26.5 und 28.1 am Bildschirm nach V10.
