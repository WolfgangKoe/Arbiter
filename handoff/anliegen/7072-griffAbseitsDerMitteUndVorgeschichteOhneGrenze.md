# Griff abseits der Mitte doppelt, Vorgeschichte ohne eigene Grenze

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Kritik an den Tests zu 6241 (`git diff e1fb48b -- technik/tests/akzeptanz`).
Wartet nach [Kritik](../../prozess/ablauf/kritik.md) (Ablage und Namen von Hilfen, keine
Prüfung rot; `ruff`, `formregeln.benennung`, `.spiegel`, `.kommentare` grün).
1. Die beiden `testAuf8_7…` in
   [ziehenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ziehenTest.py) rechnen
   denselben Griff: Radius in Pixeln mal `0.8`, dazu `assert versatzDesGriffsInPixeln >
   zugschwelleInPixeln`. Die Zahl `0.8` steht zweimal ohne Namen ([Wir 3](../../prozess/praemissen/wir.md)).
2. `aufeinanderZuZiehen` in [schlacht.py](../../technik/tests/akzeptanz/schlacht.py) läuft,
   bis der Rest 0 ist. Hält Arbiter einen Schritt der Vorgeschichte an oder sperrt ihn,
   schrumpft der Rest nicht; die Schleife läuft bis zum Ende der *Schlacht*, dann tut
   `phaseBeenden` nichts mehr und `phaseBeendenBis` meldet „Die Phase bewegungsphase kam
   nicht in einem Zug“. Die Meldung zeigt nicht auf den Schritt, der scheiterte.
3. Schrittweite und Wächter nehmen `modell.bewegungsweite` aus dem Produkt, die
   Nachbartests `bewegungsweite("Warboss")` aus `ausgangslage.yaml` („nicht kopiert“).
   Zwei Quellen für denselben Wert; die aus dem Produkt prüft nichts gegen die Daten.

**Kosten.** Am Bildschirm nichts. Bleibt es, wächst die Kopie des Griffs mit jedem weiteren
Test zu AUF-8.7, und ein Fehler in der Vorgeschichte von BEW-6.2 kostet Suche statt einer
Zeile Meldung.

**Gegenvorschlag.**
1. Eine Hilfe in [ziehen.py](../../technik/tests/akzeptanz/ziehen.py), etwa
   `griffAbseitsDerMitte(seite, modell, mitte) -> Bildpunkt`, mit benanntem Anteil
   (`anteilDesRadius = 0.8`) und dem Wächter darin.
2. Nach jedem Schritt prüft `aufDasAndereZu`, dass das *Modell* an der *Stelle* steht, die
   es *setzen* wollte (`assert schlacht.stelle(modell) == ziel`), wie B1 es für
   `modellSetzen` will: Eine falsche Vorgeschichte scheitert an ihrem Schritt.
3. `bewegungsweite(einheitenname)` aus `schlacht.py`, wie die Nachbartests; oder, falls
   Item katalogwerteGliedern das ablöst, eine Quelle für alle.

**Stellungnahme.**
