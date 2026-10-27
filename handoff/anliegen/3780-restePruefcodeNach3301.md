# Reste im Prüfcode nach Anliegen 3301

Form: Kritik
Von: Reviewer
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase 8

## Runde 1
**Befund.** Nachprüfung von Anliegen 3301 (P6, Retro 7, `git diff 257ddd6 22bc1a9`): erfüllt,
diese Reste blieben. Nach [Ich 3](../../prozess/praemissen/ich.md) hält keiner auf (keine
Prüfung rot, Randfälle und Ablage von Hilfsfunktionen); du bist ohnehin in der Prozessphase dran.
1. [Regeln](../../prozess/regeln/anliegenregeln.md), Zeile „Anliegen: Kopf und Status“, sagt noch
   „die alte Zeile ist rot“. Die alte Zeile kennt keine Prüfung mehr, kein Test nutzt sie.
2. TODOs im Frontend: `formregeln/kommentare.py` zählt nur `//` am Zeilenanfang
   (`zeilenkommentarJavaScript`). eslint (`frontendregeln/eslintKommentare.mjs`) lässt auch
   `zeichne(); // TODO: Rand` durch, weil ein angehängter Kommentar auch `Line` ist. Ein solches
   TODO zählt weder für die Höchstzahl noch fürs Alter.
3. `kommentare.py:90` lässt die Form jeder `.js` weg, eslint prüft aber nur
   `technik/frontend/**/*.js` (`eslint.config.mjs`). Eine `.js` außerhalb (heute keine) würde
   gar nicht geprüft.
4. Ob `Wartet auf` eine Nummer oder eine Phase ist, entscheidet jetzt `isdigit()` an vier Stellen
   (`anliegenDran.wartet`, `dashboardAnliegen.vorgemerkte` zweimal, `wartetAufText`,
   `anliegenText.worauf`), den Artikel `die ` setzen drei (`dashboardAnliegen.py:84`, `:90`,
   `anliegenText.py:20`).

**Kosten.** (1) Die Regel nennt etwas, das es nicht mehr gibt ([Wir 4](../../prozess/praemissen/wir.md)).
(2) Höchstzahl und Alter der TODOs lassen sich im Frontend umgehen; genau diese Abweichung
zwischen den beiden Sprachen nennt Anliegen 3301 als Kosten. (3) Eine stille Lücke, sobald eine
`.js` dazukommt. (4) Eine dritte Art von Ziel und eine geänderte Anzeige betreffen jeweils
mehrere Stellen.

**Gegenvorschlag.** Bestehende Regeln: [Regeln](../../prozess/regeln/anliegenregeln.md), Zeilen
„Anliegen“ und „Kommentare“; keine neue.
1. „; die alte Zeile ist rot“ streichen.
2. In `eslint.config.mjs` die eingebaute Regel `no-inline-comments` einschalten. Dann steht im
   Frontend jeder Kommentar auf eigener Zeile, und die Zählung in `kommentare.py` sieht alle;
   ein Fall mehr in `frontendTest.py` (angehängtes TODO rot).
3. Die Bedingung auf `relativ.startswith("technik/frontend/")` statt auf die Endung stellen.
4. Eine Funktion in `lesen/anliegenKopf.py` (etwa `wartetAufPhase(anliegen)`) und ein Text für
   das Ziel (`die <Phase>` oder die Nummer), den beide Anzeigen nutzen.
