# Alte Kopfzeile der Anliegen und doppelte Prüfung der Kommentare im Frontend

Form: Kritik
Von: Reviewer
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Im Auftrag des Stakeholders: Er hat [Review 7](../review.md) mit der Empfehlung
freigegeben, Rundgang 1 und 2 dir zu geben (Punkt 3 ist schon
[2460](2460-hindernisAbhakenUndCommitBeiLaeufen.md)). Nach [Ich 3](../../prozess/praemissen/ich.md):
keine Prüfung rot, wartet auf die Prozessphase.
1. Alte Kopfzeile: `lesen/anliegenKopf.py` liest sie noch (`alteKopfzeile` Zeile 24,
   `alterKopfAusZeile` Zeile 83 und 111), `anliegenregeln/kopfUmschreiben.py` schreibt sie
   um. Kein Anliegen trägt sie mehr, auch nicht im Commit „Freigabe Plan 7“ (`git grep`).
   Dazu der Rest `die ` vor der Phase: `anliegenKopf.py:107` setzt ihn in `wartetAuf`,
   `anliegenregeln/anliegenDran.py:9` und `rollenregeln/dashboardAnliegen.py:13` definieren
   je eine eigene Konstante `phasenanfang`, um ihn wieder zu erkennen.
2. Kommentare im Frontend: `frontendregeln/eslintKommentare.mjs` prüft ihre Form in
   `technik/frontend/**/*.js`, `formregeln/kommentare.py` (`geprüfteQuelltexte`, Zeile 76)
   dieselben Dateien noch einmal. Ein Kommentar dort wird zweimal gemeldet, die Form steht als
   regulärer Ausdruck in zwei Sprachen ([Regeln](../../prozess/regeln.md#formregeln), Zeile
   „Kommentare“).

**Kosten.** Rund 100 Zeilen Prüfcode ohne Anlass gegen die
[Kennzahl](../../prozess/kennzahlen.md#kennzahlen); wer die Kommentarregel ändert, ändert zwei
Stellen, die auseinanderlaufen können (die Python-Prüfung sieht in JavaScript nur
Zeilenkommentare am Zeilenanfang, eslint auch Block- und angehängte Kommentare).

**Gegenvorschlag.** Bestehende Regel: [Regeln](../../prozess/regeln.md#anliegenregeln), Zeile
„Anliegen“ (Kopf) und Zeile „Kommentare“; beide werden kürzer, keine neue.
1. `alteKopfzeile`, `alterKopfAusZeile`, `kopfUmschreiben.py` und seinen Test entfernen; der
   Test für den Befehl `freieNummer` in `kopfUmschreibenTest.py` zieht nach `anliegenTest.py`.
   `wartetAuf` trägt die Phase ohne `die `, `phasenanfang` entfällt.
2. Die Form der Kommentare im Frontend prüft nur eslint; `kommentare.py` zählt dort weiter
   die TODOs für Höchstzahl und Alter. Hältst du die umgekehrte Lösung für einfacher, nenne
   sie.

Erledigt, wenn keine Prüfung die alte Kopfzeile kennt, `die ` nur noch im Text steht und ein
Prosa-Kommentar im Frontend genau einmal rot ist.

**Stellungnahme.**
