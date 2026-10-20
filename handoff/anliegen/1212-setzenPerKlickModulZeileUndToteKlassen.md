# Setzen per Klick: Modulname, zu lange Zeile, tote Klassen

1212 · Kritik · von Architekt → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code zu Item [setzenPerKlick](../../domaene/items/setzenPerKlick.md)
nach `git diff`. Die Akzeptanztests des Items sind grün, rot sind nur die Tests zu den Items 2
und 3. eslint, stylelint, Import-Vertrag, Spiegel und Glossar sind grün. Alle drei Befunde
halten auf ([Ich 3](../../prozess/praemissen/ich.md)):
1. Eine Prüfung ist rot. `ruff` meldet E501 in
   [`aufstellen/__init__.py`](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py),
   Zeile 123: Der Kommentar `# Regel: AUF-18.2 … AUF-18.5 sonst nichts` hat 104 Zeichen,
   erlaubt sind 100.
2. Der Code liegt im falschen Modul. Laut seinem Docstring enthält
   [`ziehen.py`](../../technik/arbiter/domaene/phasen/aufstellen/ziehen.py) jetzt nur noch das
   Setzen per Klick (AUF-18.2, 18.3). Der
   [Grundschnitt](../../technik/architektur.md#grundschnitt-der-domäne) verlangt für die Regeln
   einer Anforderung ein Modul mit ihrem Namen, hier also `setzenPerKlick.md` →
   `setzenPerKlick.py`. Zu AUF-8 ([ziehen.md](../../domaene/anforderungen/phasen/aufstellen/ziehen.md))
   steht nichts mehr darin. `spiegel.py` bleibt trotzdem grün, weil `ziehen.md` noch existiert.
   Wer AUF-18 sucht, findet es daher nicht. Wer AUF-8 sucht, findet eine *Formation*.
3. Es gibt tote Klassen ([O3](../../technik/architektur/oberflaeche.md)). Das Abzeichen
   „in Aufstellung“ entfällt, das hat der Stakeholder im Plan 6 entschieden, siehe
   [1191](1191-abzeichenInAufstellungOhneQuelle.md). Seitdem hat
   `.einheitenKarte.inAufstellung` und `.einheitenKartenAbzeichen` kein Template mehr.
   Beide stehen noch in [komponenten.css](../../technik/frontend/komponenten.css) (Zeilen
   128, 140) und in [komponenten.html](../../technik/frontend/komponenten.html) (Zeilen 27, 29).

Nachgeprüft und in Ordnung: Das Ziehen der *Einheitenkarte* ist vollständig entfernt
([1090](1090-knopfWaechterOhneFallUndZiehenDerKarte.md)), V8 ist umgesetzt
(`preventDefault`, `user-select: none`), und `Grund.modelleFehlen` ist aus dem Produktcode
verschwunden ([1170](1170-grundModelleFehlenOhneKriterium.md)).

**Kosten.** Zu 1: Solange ruff rot ist, scheitert der Commit des Items. Zu 2: Mit Item 2
kommen AUF-21 und das Rücken des Blocks hinzu. Steht die *Formation* dann noch in
`ziehen.py`, sucht man sie dort, wo die Anforderung zum Ziehen liegt. Ein Umbenennen ist
jetzt am billigsten, denn zwei Dateien importieren das Modul. Zu 3: Die Komponentenseite
zeigt ein Abzeichen, das es in Arbiter nicht gibt.

**Gegenvorschlag.**
1. Den Kommentar kürzen, zum Beispiel
   `# Regel: AUF-18.2 setzt die Formation, AUF-18.5 mit gesetzten Modellen nichts`.
2. Mit `mv` umbenennen: `ziehen.py` → `setzenPerKlick.py` und
   `tests/einheit/domaene/phasen/aufstellen/ziehenTest.py` → `setzenPerKlickTest.py`.
   Dazu die Importe in `aufstellen/__init__.py` und im Unit-Test anpassen. S3 in der
   [Architektur](../../technik/architektur.md) nennt noch `ziehen.py`; das ziehe ich bei der
   Nachprüfung nach.
3. Aus `komponenten.css` die Regeln für `.einheitenKarte.inAufstellung` und
   `.einheitenKartenAbzeichen` streichen, aus `komponenten.html` die Klasse `inAufstellung`
   und den `span` mit dem Abzeichen. Für `vorschlag.css` ist UX zuständig
   ([1213](1213-abzeichenAusVorschlagCss.md)).

Erledigt, wenn `ruff check technik/arbiter` grün ist, `ziehen.py` nicht mehr existiert,
`python3 -m pytest technik/tests/akzeptanz/phasen/aufstellen/setzenPerKlickTest.py technik/tests/einheit`
grün ist und `grep -rn "inAufstellung\|einheitenKartenAbzeichen" technik/frontend` nichts
findet. Verhalten unverändert.

**Stellungnahme.** Angenommen, alle drei Punkte wie vorgeschlagen umgesetzt: Kommentar
gekürzt, `ziehen.py` und `ziehenTest.py` zu `setzenPerKlick.py` und `setzenPerKlickTest.py`
umbenannt (Importe angepasst, Importreihenfolge für ruff), Klassen `inAufstellung` und
`einheitenKartenAbzeichen` aus `komponenten.css` und `komponenten.html` gestrichen. `ruff check
technik/arbiter` grün, 94 Tests grün, grep leer.
