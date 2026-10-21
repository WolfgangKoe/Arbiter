# Code ohne gesperrtes Modell

1443 · Kritik · von Architekt → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Hält auf ([Ich 3](../../prozess/praemissen/ich.md): Code verletzt den Vertrag, Prüfungen
rot). Der Vertrag kennt kein *gesperrtes* *Modell* mehr ([V1](../../technik/architektur/vertrag.md),
[V5 bis V7](../../technik/architektur/handlungen.md)), die Beispiele `spielstand.json` und
`ebene.json` haben weder `gesperrt` noch `gründeDerGesperrten`. Zehn Tests in `auswahlTest.py`,
`modellPerKlickTest.py` und `blockAlsGanzesTest.py` sind darum rot: Der Dienst schreibt die
Schlüssel noch, die Seite bricht ohne `gründeDerGesperrten` ab. Dies ersetzt Schritt 3 in
[1440](1440-kritikAmCodeAnhaltenAnBases.md), Punkt 5; was dort steht, gilt mit dieser Liste.
1. Domäne: `gesperrtesModell.py`, `Gesperrtes`, `zurücknehmen`, `_gesperrte`, `gesperrt`,
   `stelleDesGesperrten`, `gründeDesGesperrten`, `_prüfenDassNichtsGesperrtIst` samt seinen drei
   Aufrufen, `Grund.modellGesperrt`.
2. `_loslassen`: Bleibt nach dem Anhalten ein *Grund* gegen eine *Stelle*, wirft es `Sperre`
   mit jedem *Grund* aller *Modelle* des Loslassens und *setzt* keines (V5, D2, AUF-12.5).
3. `zurück()` ändert nichts (AUF-17.1); `PUT /api/zurück` bleibt (V5).
4. `darstellung.py`: Feld `gesperrt`, `_gründeDerGesperrten`, der Rückgriff auf
   `stelleDesGesperrten` in der Liste der *Modelle*.
5. Seite: Kreis `gesperrt` in `seite.js` und `.modell.gesperrt` in `komponenten.css`,
   `gründeDerGesperrten` in der `sperrmeldung` (nur noch die `gründe` der letzten 409) und der
   Knopf „zurück“ in der `knopfGruppe` (V7).

**Kosten.** Ohne 1 bis 5 bleiben die zehn Tests rot, und [1430](1430-restDesGesperrtenModellsInDenKriterien.md)
kann AUF-12.1 und die Glossarzeilen nicht löschen, ohne Spiegel und Glossar rot zu machen.

**Gegenvorschlag.** Wie 1 bis 5, nachdem der Testautor 1442 umgesetzt hat; danach sind unter
`technik/tests` nur noch die vier Tests aus [1460](1460-vierTestsVerlangenWasDerCodeNichtLiefernKann.md)
rot. `seite.js` wird dabei kleiner ([1440](1440-kritikAmCodeAnhaltenAnBases.md), Punkt 4).

**Stellungnahme.** Angenommen und umgesetzt, Punkte 1 bis 5.
1. `gesperrtesModell.py`, `Gesperrtes`, `zurücknehmen`, `_gesperrte`, `gesperrt`, `stelleDesGesperrten`,
   `gründeDesGesperrten`, `_prüfenDassNichtsGesperrtIst` mit den Aufrufen und `Grund.modellGesperrt` sind weg;
   dazu `einheitInAufstellungNach`, das nur `zurück` brauchte.
2. `_loslassen` sammelt die *Gründe* aller *Modelle*, wirft `Sperre` mit allen und *setzt* sonst alle.
3. `zurück()` ändert nichts, `PUT /api/zurück` bleibt.
4. `darstellung.py` ohne `gesperrt` und `gründeDerGesperrten`.
5. `seite.js` ohne Kreis `gesperrt`, Knopf „zurück“ und `gründeDerGesperrten`; `komponenten.css` ohne `.modell.gesperrt`.
Lauf über `technik/tests`: vorher 12 rot, 669 grün; nachher 681 grün. `prozess/pruefungen`:
729 grün (formregeln, Glossar, Spiegel). `ruff check` und `ruff format --check` grün.
