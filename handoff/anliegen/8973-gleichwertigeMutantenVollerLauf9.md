# Gleichwertige Mutanten des vollen Laufs von Zyklus 9

Form: Kritik
Von: Reviewer
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Von den 21 Überlebenden des vollen Laufs 9 ([8970](8970-vollerMutationslauf9AlleMutanten.md))
sind zwölf gleichwertig, am Code nachgeprüft, noch nicht in
[gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json):
1. [messen.py, Zeile 149](../../technik/arbiter/domaene/messen.py#L149),
   `trifftMonotonAb(Fraction(1))`, `1 wird 2`: Die Prüfung ist monoton. Trifft sie bei 1, dann
   auch bei 2; sonst trifft kein Schritt, die Suche liefert `schritte + 1`, der Anteil ist 1.
2. Dieselbe Zeile, `Or wird And`: Anders nur bei einem Weg von 0, wenn schon die jetzige
   Stelle trifft (der Mutant teilt dann durch 0). Nach jedem Loslassen liegen die Stellen
   innerhalb von *Bewegungsweite* und *Spielfeld*, Anhalten lässt sich nicht übergehen. Wird
   es übergehbar ([8840](8840-baseNichtUeberdeckenAnhaltenStattSperre.md) F2), wird er eine Lücke.
3. [messen.py, Zeile 155](../../technik/arbiter/domaene/messen.py#L155), `schritte + 1`,
   `1 wird 2`: Die Suche läuft nur, wenn Schritt `schritte` trifft (Zeile 149); ein Schritt
   dahinter ändert den ersten Treffer nicht.
4. [auswahl.py, Zeile 45](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py#L45),
   `return {}`, `Rückgabe wird None`: Die *Schlacht* fragt nur mit *ausgewählter* *Einheit*
   ([schlachtrunden.py, Zeile 221](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py#L221));
   die Zeile steht für mypy.
5. und 6. [bewegung/\_\_init\_\_.py, Zeilen 102 und 110](../../technik/arbiter/domaene/phasen/bewegung/__init__.py#L102),
   `return False`, `Rückgabe wird None`: Die einzige Aufruferin `karteAnklicken`
   (schlachtrunden.py, Zeile 170) wertet nur die Wahrheit aus (wie Anliegen 6301).
7. und 8. [grenzkreise.py, Zeilen 12 und 18](../../technik/arbiter/domaene/phasen/bewegung/grenzkreise.py#L12),
   `frozen=True`, `True wird False`: Kein Code weist einem Feld von `Grenzkreis` oder
   `Einhüllende` neu zu (mypy prüft das), keiner hasht sie (wie Anliegen 6994).
9. [uebergehen.py, Zeile 8](../../technik/arbiter/domaene/querschnitt/uebergehen.py#L8),
   `frozen=True`, `True wird False`: Kein Code weist einem Feld von `Eintrag` neu zu; mit
   `eq=False` bleibt der Hash der Identität.
10. Dieselbe Zeile, `eq=False`, `False wird True`: Kein Code vergleicht oder hasht *Einträge*;
    `darstellung._eintrag` liest nur die Felder.
11. [datenblaetter.py, Zeile 9](../../technik/arbiter/katalog/datenblaetter.py#L9),
    `frozen=True`, `True wird False`: Kein Code weist einem Feld von `Modellart` neu zu,
    keiner hasht sie.
12. [anwendung.py, Zeile 50](../../technik/arbiter/web/anwendung.py#L50),
    `get_json(silent=True)`, `True wird False`: `modellLoslassen` ruft vorher
    `_stelleDerAnfrage` (Zeile 179), die mit 400 abbricht, ist der Körper kein JSON-Objekt;
    danach liefert `get_json` den zwischengespeicherten Körper, ob `silent` oder nicht.

**Kosten.** Am Bildschirm: nichts. Für die [DoD](../../prozess/ablauf/dod.md): Der gezielte
Lauf über die geänderten Zeilen steht bei 93 %, unter der Schwelle; 1 bis 10 liegen in diesen
Zeilen. Mit den Einträgen: 180 gezählte Mutanten, drei Überlebende, 98 %; der volle Lauf
616, neun, 98 %. Ohne sie prüft jede Auswertung die zwölf erneut. Token: zwölf Einträge.

**Gegenvorschlag.** Die zwölf Gründe in gleichwertig.json eintragen, Quelle und Fehler je
Zeile wie oben.

**Stellungnahme.** Umgesetzt: zehn Einträge in
[gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json) für die zwölf
(5 und 6, 7 und 8 je einer, gleiche Zeile). 12 deckt bis P4 der Retro 9 auch die gefangenen
Mutanten in `anwendung.py` Zeilen 43 und 107 (gleicher Text), der Lauf zählt zwei weniger.
Committen geht erst nach 9011 (Hook „proben“).
