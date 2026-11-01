# Retro 9: ein wartendes Anliegen fehlt, Items lassen Fälle offen

Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Hält auf: Die Items werden gebaut, wie sie in der [Retro 9](../retro.md) stehen.
Die 19 genannten sind eingeplant, 6361 ist erledigt.
1. Es fehlt [7031](7031-commitHookRotWegenTestsDesPlans.md): wartet auf 7030 (P3), dein F2
   „Ja“ will C. Ohne C ist der Commit-Hook nach `Freigabe Plan 10` rot, bis jeder Test
   steht; in Zyklus 9 lagen so 71 Dateien nur auf der Platte.
2. P1: „dessen Tests“ und „begründet“ sind offen; zu Recht grün ist ein Test, wenn Bestand
   das Kriterium schon erfüllt. Der Lauf liest den Arbeitsbaum, auf dem ein Implementierer
   schreibt; P2 verlangt dann einen Abzug, rund 6 Minuten je Abhaken. „Nie grün“ (7640,
   8280) fängt P1 nicht.
3. P4: „Alle Kerne belegt“ hängt an Last und Zahl der Mutanten, kein Test prüft das
   verlässlich. „Nur für seine Klasse“: Die Einträge in
   [gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json) liegen
   meist in Funktionen; ohne Umschreiben zählen die 23 als Überlebende.
4. P8 (7380): Plan 9 hatte 3.907 von 4.000 Zeichen; 24 Anliegen warten auf Technikphase 10,
   als Links rund 1.300 Zeichen. „Nennt“ plant nicht ein: Kein Schritt der
   [Technikphase](../../prozess/ablauf/technikphase.md) hat sie. 7380 gilt für jede Phase;
   8 warten auf Domänenphase 10, und [Prozessphase](../../prozess/ablauf/prozessphase.md) 1
   („höchstens zwei“, „übrige im Backlog“) widerspricht dem Einplanen aller.
5. [Ich 5](../../prozess/praemissen/ich.md): Nur P1 nennt Probe und Rückweg, P3 bis P7 ändern
   Prüfungen und Hooks; ein falsches Muster in P5 sperrt `python3 -m pytest` für alle. Die
   Folgen nennen den Prüfcode nicht: P1, P3 bis P7 zählen in Zyklus 10, Abstand heute 250
   Zeilen, Zyklus 10 räumt vor allem auf (8880).
6. P6 lässt 6988 Punkt 4 fallen: Ein Test sucht den Text `classList.toggle`, statt den Klick
   zu prüfen ([Absicht 1](../../prozess/praemissen/absicht.md)).
7. P7 nennt keine Schwelle. Playwright für Python hat meines Wissens kein `page.coverage`;
   es braucht das Chrome-Protokoll und eine Umrechnung in Zeilen, wohl ein npm-Paket.

**Kosten.** Ohne 1 ruht jeder Commit von Plan 10 bis zum letzten Test; sonst rät der
Regelumsetzer, ohne 5 entscheidest du ohne die Folgen. Ändern: Text der Retro.

**Gegenvorschlag.** Bestehende Regeln zuerst ([Ich 4](../../prozess/praemissen/ich.md)).
1. 7031 C in P3: eine Funktion in `lesen/plan.py` liefert die Items des Plans samt
   Kriterien; Fortschritt, Hook und P1 nutzen sie.
2. P1: nur die Testfunktionen zu den Kriterien des Items ([Es 4](../../prozess/praemissen/es.md)),
   am Arbeitsbaum; er meldet kein „grün“, darum kein Abzug. Ist einer grün, meldet der
   Befehl ein Hindernis an den Testautor; seine Stellungnahme begründet, Fachkritiker und
   Architekt prüfen sie. „Nie grün“ bleibt bei der Kritik an den Tests.
3. P4: Ein Test, dass sich Mutanten zweier Module zeitlich überschneiden (8990, 6). Ein
   Eintrag gilt für seine umschließende Klasse oder Funktion, sonst das Modul; P4 schreibt
   die 23 Einträge um.
4. P8: Der [Fortschritt](../../prozess/ablauf/fortschritt.md) jeder Phase bekommt je
   wartendem Anliegen `- [ ] <Rolle aus An:>: Anliegen <nr>`, Fakt: `angenommen` oder
   `erledigt`. Er zählt nicht zum Höchstmaß; ein Mechanismus für alle drei Phasen
   (Regelumsetzer, Text: du), Prozessphase 1 angepasst.
5. Je Item Probe oder „nicht erprobt“ und Rückweg; P5 erprobt an einer Kopie, dass jede
   Rolle Tests, `lauf.py` und Commits weiter ausführt. In den Folgen geschätzte Zeilen.
6. P6 ersetzt den Test durch einen Klick im Browser oder streicht ihn.
7. P7: Zeilen wie DoD 1, Zweige nur, wenn der Versuch sie vergleichbar misst; ein neues
   Paket kritisiere ich vor dem Einbau.

**Stellungnahme.**
