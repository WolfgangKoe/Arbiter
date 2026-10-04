# Freigabefeld nur im Abschnitt `## Freigabe` lesen

210 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von b232332 (Anliegen 167, Teil 3). `freigabeFormat.verstöße`
deckt die Scheiter-Tests aus 167 ab. `python3 -m pytest prozess/pruefungen` ist grün (578),
die Abdeckung reicht. Drei Punkte:

1. Stand und Formatprüfung lesen das Feld an verschiedenen Stellen.
   `freigabeKommentare.freigabeZuCommitten` (Zeile 59) sucht `Freigabe: ja` irgendwo in der
   Datei, `freigabeFormat.formatVerstoß` nur im Abschnitt `## Freigabe`. Probe: Unter
   `## Teil` steht `Freigabe: ja`, unter `## Freigabe` steht `Freigabe: offen`. Die
   Formatprüfung ist grün, der Stand meldet „Koordinator: Freigabe Plan 3 committen“.
2. `vorgehenVerstoß`, Zeilen 35 und 36 („steht nach `## Freigabe`“), kann nie greifen. Diese
   Zeilen deckt kein Test. `formatVerstoß` verlangt schon, dass `Freigabe` der letzte
   Schlüssel ist. `abschnitte` legt eine wiederholte Überschrift an ihrer ersten Stelle ab und
   verwirft deren Zeilen. Probe: `## Freigabe`, `## Danach`, `## Freigabe` mit Feld meldet
   „endet nicht mit `## Freigabe`“, obwohl die Datei so endet.
3. `ungeprüft` setzt den Pfad `handoff/retro.md` selbst zusammen, obwohl `artefakte` ihn
   kennt. Den Pfad `wurzel / "handoff" / artefakt.datei` bauen nun vier Stellen in zwei
   Modulen. `freigabeZuCommitten` schreibt den Betreff zweimal aus (Zeilen 61 und 62).

**Kosten.** Zu 1: Steht die Zeile außerhalb des Abschnitts, etwa als Zitat der Vorlage im
Review oder in der Retro, schickt der Stand den Koordinator zu einer Freigabe, die der
Stakeholder nicht gegeben hat. Zu 2: Toter Code und eine Meldung, die in die Irre führt.
Zu 3: Wer den Ort einer Datei ändert, muss mehrere Stellen finden.

**Gegenvorschlag.** Beide Module lesen die Datei über eine gemeinsame Funktion. Sie liefert
die Abschnitte als Liste von Paaren (Überschrift, Zeilen) und das Feld nur aus
`## Freigabe`; `abschnitte` zieht dafür nach `freigabeKommentare.py`, sonst entsteht ein
Ringimport. `freigabeZuCommitten` fragt nur dieses Feld ab. Die Prüfung auf die Reihenfolge
entfällt, oder sie wird mit der Liste echt prüfbar. Für den Pfad eine Funktion
`pfadDer(wurzel, artefakt)`; den Betreff einmal in eine Variable. Scheiter-Test in
`standTest.py`: `Freigabe: ja` außerhalb von `## Freigabe` und `Freigabe: offen` darin, der
Stand nennt den Koordinator nicht.

Erledigt, wenn der Scheiter-Test grün ist, kein Zweig von `freigabeFormat.py` ungedeckt bleibt,
`python3 -m pytest prozess/pruefungen` grün ist und der Reviewer den Commit geprüft hat.
