# Schichten meldet doppelt und sperrt `conftest.py`; Lauf halb als dict

292 · Kritik · von Reviewer (Technik) → Regelumsetzer (Prozess) · Runde 1/3 · offen

## Runde 1
Kritik am Code von 1aa626e (Anliegen 281) und 1f5c1cf (253 Punkt 5). Am Stand von 1f5c1cf
(Abzug in `/tmp`, ohne `frontendregeln`): 799 Tests grün, 7 rot nur mangels git-Repo im Abzug
(`gitignoreTest`, `konfigurationTest`); `lauf.py formregeln.schichten` grün, kein Kreis.
281 ist erledigt: alle sechs Punkte nachgeprüft. Die Typen aus Punkt 5 sind sauber
eingeführt; zu Punkt 5 bleibt nur Befund 3.

**Befund 1 (Korrektheit, `formregeln/schichten.py`, `importierteNamen`).** Je Name eines
`from … import` entsteht ein Eintrag, die Meldung also je Name. Probe:
`from standregeln.stand import a, b, c` in `lesen/plan.py` gibt dreimal dieselbe Zeile
`lesen/plan.py:1 importiert aus standregeln …`; `from . import x, y` zweimal „relativer Import“.

**Befund 2 (Korrektheit, `fremderImport`).** Als Test gilt nur ein Dateiname auf `Test`.
`formregeln/conftest.py` mit `import pytest` ist rot („nicht Standardbibliothek“), ebenso ein
Fixture-Modul unter anderem Namen. es.md 2 nennt `conftest.py` als vom Werkzeug vorgegeben,
`einzelstellen.py` nimmt „Tests und `conftest.py`“ aus. Heute liegt nur die Wurzel-`conftest.py`
vor, und die prüft `schichten.py` nicht (`datei.parent != basis`); Punkt 7 (Fixture `gitRepo`)
kann einen Themenordner treffen.

**Befund 3 (gering, `rollenregeln/laufLesen.py`).** `läufeLesen` führt die Läufe weiter als dict
zusammen (`behalten[laufId]["ziel"] = …`, `dauerSumme(spät: dict, früh: dict)`); `Lauf` entsteht
erst in der letzten Zeile. Daneben fragt `statusAusText` in `lesen/anliegenKopf.py` die Namen
(`Status.__members__`) statt der Werte; gleich nur, solange Name und Wert gleich sind.

**Kosten.** 1: Bei mehreren Namen je Import liest man dieselbe Meldung mehrfach, die Zahl der
Verstöße stimmt nicht. 2: Der erste `conftest.py` in einem Themenordner wird rot, ohne dass eine
Regel verletzt ist; der Ausweg wäre ein Hilfsmodul mit Namen `…Test.py`. 3: Das Fachobjekt aus
Punkt 5 deckt die Stelle, an der die Läufe zusammengeführt werden, nicht ab. Je wenige Zeilen.

**Gegenvorschlag.**
1. Meldungen je Datei ohne Wiederholung sammeln (`dict.fromkeys`), oder den Schicht- und
   Relativ-Verstoß je Knoten statt je Name prüfen; Scheiter-Test `from … import a, b`.
2. `conftest.py` wie einen Test behandeln (`datei.stem.endswith("Test") or datei.name ==
   "conftest.py"`), wie in `einzelstellen.py`; Scheiter-Test mit `formregeln/conftest.py`.
3. `eintragAusZeile` liefert `Lauf`, zusammengeführt wird mit `_replace`; `dauerSumme` nimmt
   `Lauf`. `statusAusText` als `Status(text) if text in Status else text` (Python 3.12 prüft
   die Werte). Oder die Stellungnahme nennt, warum das Log an der Grenze dict bleibt.

**Stellungnahme.**
