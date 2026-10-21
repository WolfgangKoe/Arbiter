# Loslassen ohne Antwort bleibt in der Vorschau stehen

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase

## Runde 1
**Befund.** Kritik am Code (Lesbarkeit) zu Anliegen 1640,
`ziehenBeenden` in [seite.js](../../technik/frontend/seite.js):
1. Antwortet der Server beim Loslassen nicht (Arbiter beendet, `fetch` scheitert), wirft
   `handlungSenden`, und keiner zeichnet neu. Die Kreise bleiben dann an der Vorschau stehen,
   obwohl nichts *gesetzt* ist. Vorher sprangen sie in diesem Fall an den Anfang zurück, wie
   bei `ziehenAbbrechen`. ArbiterMap nimmt sie bei einem Fehler zurück
   (`ArbiterMap/frontend/static/js/model_drag.js:1609`).
2. Der Kommentar „Warum: Die Kreise bleiben bis zur Antwort … sonst blitzen sie am Anfang auf“
   steht über der Zeile zum Klick und erklärt einen Aufruf, den es nicht mehr gibt. Das ist
   Historie ([Wir](../../prozess/praemissen/wir.md) 4) und gehört zu keiner Zeile.

Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet auf die Technikphase. 1 ist
ein Randfall abseits des Happy Path, kein Kriterium regelt ihn. 2 ist ein Kommentar, und
`formregeln/kommentare.py` ist grün.

**Kosten.** Bei 1 zeigt die *Karte* einen Stand, den es nicht gibt, bis zum nächsten
Zeichnen. Bei 2 sucht der Leser die Zeile, die der Kommentar meint.

**Gegenvorschlag.**
1. Scheitert `modellLoslassen` oder `modellAufAblageLoslassen`, zeichnet die Seite
   `letzterSpielstand`, wie ohne Ziel. Am einfachsten fängt `handlungSenden` den Fehler von
   `senden` ab und zeichnet dann `letzterSpielstand`.
2. Den Kommentar löschen. Wer wissen will, warum nichts zurückgenommen wird, findet die
   Antwort in git (Anliegen 1640).

Erledigt: 1 und 2 umgesetzt, Bildschirmtests grün.

**Stellungnahme.**
