# Freigabesperre: Umgehung in zwei Schritten über die Zyklusnummer

218 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von 1bc5648 (Anliegen 210, 213). `python3 -m pytest prozess/pruefungen`
ist grün (631). `freigabeFormat.py` und `freigabeKommentare.py` sind zu 100 % abgedeckt, die
Scheiter-Tests aus 213 gehen so aus wie gefordert. Folgendes habe ich mit Proben auf
`freigabeVerstoß` geprüft:

1. `freigabeKommentare.py`, `freigabeVerstoß` (Bedingung `alt is None or …`): Wer nur die
   Nummer entfernt, wird nicht gesperrt (`Zyklus 3` → `Zyklus`, sonst nichts geändert:
   `None`). Danach ist `alt` gleich `None`, und der nächste Edit löscht `Kommentar: warum so?`
   frei. Dasselbe in zwei anderen Schritten: `Zyklus 3` → `Zyklus 4`, dabei den Kommentar
   löschen (abgelöst, frei), dann `Zyklus 4` → `Zyklus 3` (keine geschützte Zeile ändert sich,
   frei). Am Ende steht Plan 3 ohne den Kommentar des Stakeholders. Die Tests
   `testZyklusnummerEntfernenLöstNichtAb` und `…SenkenLöstNichtAb` prüfen nur den Fall in
   einem Schritt.
2. `prozess/regeln.md` (Zeile „Freigabe und Kommentare“, Anliegen 213) schreibt: „Nummer
   entfernt oder gesenkt sind gesperrt“. Das stimmt nicht: Gesperrt ist nur, was dabei eine
   geschützte Zeile ändert. Senken oder Entfernen allein ist frei (Probe 5: `Zyklus 3` →
   `Zyklus 2`: `None`).
3. `freigegebenerZyklus` liest die Datei zweimal, über `zeilenDer` und über
   `zyklus(pfadDer(…))`. Das doppelte Lesen nannte 213, Punkt 6, und es ist geblieben.

**Kosten.** Zu 1: Die Rolle, die aufräumt, löscht den Kommentar mit einem Edit mehr, und der
Stand meldet den Autor nicht mehr als dran. Damit bleibt die Lücke aus 213, Punkt 1 offen.
Zu 2: Die Tabelle verspricht eine Sperre, die es nicht gibt. Zu 3: Bei jedem Stand und jedem
Commit des Koordinators wird die Datei doppelt gelesen.

**Gegenvorschlag.**
1. Eine Nummer, die fehlt oder kleiner ist als die bisherige, ist selbst ein Verstoß:
   „senkt oder entfernt die Zyklusnummer; die Datei löst nur eine höhere Nummer ab.“ Das passt
   zum [Ablauf](../../prozess/ablauf.md#freigabe-und-kommentare) („bis der Autor die Datei im
   nächsten Zyklus neu schreibt“). Abgelöst wird nur bei `alt is None` (neue Datei) oder
   `neu > alt`. Damit sperrt auch der Rückweg 4 → 3.
   Scheiter-Tests: Nummer entfernen ohne andere Änderung rot, 3 → 2 ohne andere Änderung rot.
2. Die Zeile in `regeln.md` danach so fassen: „Nummer entfernt oder gesenkt rot“.
3. `freigegebenerZyklus` liest die Zeilen einmal und nimmt die Nummer aus der ersten Zeile
   (`zyklusAusText`).

Erledigt, wenn die Scheiter-Tests grün sind, `python3 -m pytest prozess/pruefungen` grün ist
und der Reviewer den Commit geprüft hat.

**Stellungnahme.**

Stellungnahme: Entfällt mit dem Rückbau.
