# Abdeckung der Prüfskripte lehnt sich an den Stand

172 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
Kritik am Code zu Commit `6dfe473` (P1 der [Retro 2](../retro.md)). Was
[170](170-abdeckungMeldetFalschGruen.md) und [171](171-abdeckungLaufzeitUndZuschnitt.md)
nennen, wiederhole ich nicht.

**Befund.**
1. Die 96 % für `prozess/pruefungen` zählen auch Zeilen, die nur die Prüfungen über das echte
   Repo erreichen, keine Probe: 17 Testfunktionen, die die Wurzel des Repos lesen
   (`testDasRepoHält…`, `testDateiHältIhrHöchstmaß`, `testJedesAnliegenHatEinenGültigenKopf`
   usw.). Wegwerf-Messung ohne sie: 94 %, unter der Schwelle. Betroffen sind etwa
   `kommentare.py` `verstöße` (Zeilen 57 bis 65; nur der Lauf über das Repo ruft sie, die
   Meldung in Zeile 64 erreicht kein Test), `bashPositivliste.py` (158, 181, 198, 218 bis
   225) und `benennung.py` 45. Ein Lauf über einen sauberen Stand probt nur den grünen Weg;
   ob die Funktion einen Verstoß meldet, zeigt er nicht. Zudem hängt die Zahl am Stand:
   Dieselben Prüfskripte und Tests ergeben eine andere Quote, sobald das Repo einen Verstoß
   enthält.
2. `abdeckungTest.py` importiert `wurzel` aus `konfigurationTest.py`, ein Testmodul dient als
   Bibliothek. Dieselbe Zeile `wurzel = Path(__file__).resolve().parents[2]` steht in zwölf
   Testmodulen; `pfade.py` ist der Ort für „Ordner des Repos, die mehrere Prüfungen kennen“.

**Kosten.** 1: Die Schwelle aus Anliegen 157 soll
zeigen, dass jeder Mechanismus an Proben geprüft ist (Scheiter-Test,
[Ablauf, Prozessphase](../../prozess/ablauf.md#prozessphase) 2). Heute verdeckt sie gerade
die Stellen, an denen ein Mechanismus falsch grün melden kann, dieselbe Fehlerart wie 170,
Befund 1. 2: Wer `konfigurationTest.py` aufräumt, bricht `abdeckungTest.py`; die Wurzel
steht zwölfmal.

**Gegenvorschlag.**
1. Die Prüfungen über das echte Repo tragen eine Marke (etwa `@pytest.mark.stand`). Die
   Messung der Prüfskripte läuft mit `-m "not stand"`; die markierten Prüfungen laufen
   weiter im normalen Lauf. Mit 171, Gegenvorschlag 1, verträgt sich das, wenn der eigene
   Hook nur misst und den normalen Lauf nicht ersetzt. Die fehlenden Proben (etwa
   `kommentare.verstöße` an einer Probe mit einem Verstoß) schreibt der Regelumsetzer.
   Erledigt, wenn die Quote ohne die markierten Tests mindestens 95 % ist.
   Billiger, aber schwächer: die Quote mit Stand lassen und beim Regelumsetzer nennen, dass
   sie Läufe über das Repo mitzählt. Ich empfehle die Marke; es fehlen rund 20 Zeilen Proben.
2. `wurzel` steht in `pfade.py`; `abdeckungTest.py` und die übrigen Testmodule importieren es
   von dort. Das passt zu [114](114-pruefskripteOrdnenUndLesbarMachen.md).

**Stellungnahme (Regelumsetzer).** Angenommen, umgesetzt.
1. Die Prüfungen über das echte Repo tragen `@pytest.mark.stand` (registriert in
   `pyproject.toml`), auch die Messung von `technik/arbiter`. Die Messung der Prüfskripte läuft
   mit `-m "not stand"`; der normale Lauf führt alle aus. Neue Proben, die die Lücken
   schließen: `kommentare.verstöße`, `glossar.verstöße`, `plan.py` (neu `planTest.py`),
   `statusrecht`, `lesegrenze`, `anliegennummer`, `hookProtokoll`, `schreibpfade`,
   `schlussantwort`. Ohne die markierten Tests: Zeilen 98,2 %, Zweige 96,7 %.
   Noch ohne Probe: Zeilen in `bashPositivliste.py`, `belegung.py`, `benennung.py`,
   `phasenfolge.py`, `rueckverfolgung.py` (Kommandozeile), `agenten.py` 22 und 41.
2. `wurzel` steht in `pfade.py`; alle Testmodule und `abdeckungTest.py` importieren sie dort.
