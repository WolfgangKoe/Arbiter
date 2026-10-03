# Doppelte Kennung eines Kriteriums fällt nicht auf

60 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Aus [Anliegen 45](45-kennungBleibtStabil.md), Nr. 2; der Anforderungsautor hat
Nr. 1 angenommen (eine Kennung bleibt, eine gelöschte wird nicht neu vergeben; Text:
[Anliegen 59](59-kennungInDomaeneClaude.md)). `kriterien()` in
[`rueckverfolgung.py`](../../prozess/pruefungen/rueckverfolgung.py) sammelt die Kennungen in
eine Menge. Steht `- AUF-1.1` zweimal in einer Anforderungsdatei, zählt ein Test
`testAuf1_1…` für beide; `verstöße()` meldet nichts. Wegwerf-Versuch in 45.

**Kosten.** Ein Kriterium geht ohne Test durch die DoD (Nr. 2), und keiner sieht es: Die
Prüfung ist grün.

**Gegenvorschlag.**
1. `rueckverfolgung.py` meldet jede Kennung, die in einer Anforderungsdatei mehr als einmal
   als Kriterium steht, auch ohne Testdatei: „`<anforderung>`: AUF-1.1 steht zweimal“.
2. Scheiter-Test: eine Anforderungsdatei mit zweimal `- AUF-1.1` ergibt genau diesen Verstoß.
3. Die Kennung einer Anforderung (`### AUF-1 · …`) gleich mit: zweimal `AUF-1` ist derselbe
   Fehler.
4. Wandernde Nummern (45, Fall 1) bleiben Text; eine Prüfung über die git-Historie lohnt
   erst, wenn es vorkommt.

**Stellungnahme.** Umgesetzt in `rueckverfolgung.py`: Jede doppelte Kriteriums- oder Anforderungskennung einer Datei ist ein Verstoß, auch ohne Testdatei. Scheiter-Tests: `testDoppeltesKriteriumIstAuchOhneTestdateiRot`, `testDoppelteAnforderungIstRot`. Punkt 4 bleibt Text.
