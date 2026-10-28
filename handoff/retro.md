# Retro · Zyklus 8

Dashboard: im Projektordner
`python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer` starten,
`http://127.0.0.1:8765/` öffnen, Strg+C beendet.

Etappe 2 von 10 (Phasen und Bewegungsphase) läuft ([Review 8](review.md)); 95 von 123
Kriterien belegt (Zyklus 7: 78 von 108). Neu am Bildschirm: „Erster Zug“, *Schlachtrunden*
mit „Phase beenden“, in der *Bewegungsphase* ein Zug bis zur *Bewegungsweite*, Sperre über
eine fremde *Base*, ‚keine Kohärenz‘ beim Phasenende, Schlachtende nach Runde 5.

## Was geklappt hat
Alle drei Items abgenommen, DoD erfüllt, 17 Kriterien mehr belegt. Die Kritik am Review fand
vor deiner Freigabe, was der Klickpfad ausließ (6335, 6360).

## Was nicht geklappt hat
1. 6 der 12 Hindernisse gingen an den Testautor: Tests prüften nur einen Fall (nur Spieler 1,
   nur Runde 1, nur auf den Achsen); die Mutation fing zuerst 84 %. Damit trat der Auslöser
   „Testautor auf Opus“ ein ([Rollen mit Auslöser](../prozess/ablauf/rollenMitAusloeser.md)).
2. Code vor dem Test: Das Greifen am Rand (AUF-8.7) kam ohne Test (6101), ‚Nahkampfreichweite‘
   sperrt ohne Test, obwohl Plan 8 sie unter „Noch nicht“ nennt (6241). Die Regel steht nur als
   Text in der [Root-CLAUDE.md](../CLAUDE.md).
3. 572 neue Zeilen Prüfcode gegen 530 Produktcode: über der Schwelle. Prozesslast 13 von 93
   Anliegen: darunter. Darum beauftragt diese Retro keinen neuen Mechanismus außer auf deinen
   Wunsch, und 3960 (weitere Bash-Sperren) wartet auf Prozessphase 9.
4. Deine Frage nach den Kommentaren (6430): Im Produkt steht kein `#`, aber 71 Docstrings,
   38 mit Kennungen wie „(QUE-10.5)“; dazu Tests, Prüfcode und `pyproject.toml`. Deine Wahl:
   [Anliegen 6431](anliegen/6431-fragenDerRetro8.md), F1.
5. Das Dashboard verwirft deine Antwort, wenn unter der Frage keine Zeile `Antwort:` steht;
   die Prüfung der Anliegen verlangt „Ux“ statt „UX“ (6432 an den Regelumsetzer).

Nicht bestätigt: `.venv/bin/python -c` war in meinem Lauf gesperrt; der Befehl zum Abhaken
nimmt mit Absicht nur eigene Schritte. Ins [Backlog](../prozess/backlog.md): Abkürzungen in
zusammengesetzten Namen, tote Links, Formfehler erst beim Commit, Kommentare im Chat,
lange Läufe, `gleichwertig.json` für den Testautor.

## Prozess-Items
P1 gilt Befund 1, P2 Befund 2; sonst deine Aufträge 6430, 6380, 4040, 3550.
- P1 Tests für jeden Fall (Organisationsentwickler): Nach F2 läuft der Testautor auf Opus,
  der Skill `akzeptanztest-schreiben` bekommt das Gegenbeispiel „nur Spieler 1“. Danach
  prüft ein Test, was für beide Spieler oder jede Runde gilt, mit mehr als einem Wert.
- P2 Kein Verhalten ohne Test (Organisationsentwickler): Verlangt kein Test ein Verhalten,
  baut der Implementierer es nicht, sondern schreibt ein Anliegen an den Testautor; der
  Architekt prüft es in der Kritik am Code. Danach sperrt Arbiter nichts, was der Plan unter
  „Noch nicht“ nennt.
- P3 Prämissen nach deinen Antworten (Organisationsentwickler): Es 8 nach F1, die sechs
  Verschiebungen nach F3 (6380), das Kürzel je Phase in der Domäne (4620).
- P4 Docstrings im Prüfcode (Regelumsetzer): `formregeln/kommentare.py` nach Es 8 neu, der
  Prüfcode danach ohne verbotene Docstrings. Produkt und Tests räumen Implementierer und
  Testautor in Technikphase 9; rot erst in deren DoD.
- P5 Ablauf schlanker (Organisationsentwickler): Streichungen 1 bis 6 aus
  [Anliegen 4040](anliegen/4040-ablaufUndRegelnVerschlanken.md); an einer Kopie in `/tmp`
  arbeiten und committen alle Rollen wie vorher.
- P6 Regeln schlanker (Regelumsetzer): Punkt 7 aus 4040, das Format `Hindernis:` einmal
  (4120), dazu 3780, Punkt 1.
- P7 Belegte Kriterien je Etappe (Regelumsetzer): Stand und Dashboard zeigen „Etappe 2: x von
  y Kriterien belegt“ neben allen (3550, A); jede Anforderung nennt jetzt `Etappe:`.

## Empfehlung
Beantworte 6431 und gib die Retro frei. Der Reiter Architektur (4140) kommt nach P6: erst
Bestand abbauen, dann Neues (306).

## Fortschritt
- [x] Organisationsentwickler: Retro geschrieben
- [ ] Fachkritiker: Kritik an der Retro
- [ ] Architekt: Kritik an der Retro
- [ ] Organisationsentwickler: Nachkorrektur
- [ ] Stakeholder: Freigabe Retro 8
- [ ] Organisationsentwickler: P1
- [ ] Organisationsentwickler: P2
- [ ] Organisationsentwickler: P3
- [ ] Regelumsetzer: P4
- [ ] Organisationsentwickler: P5
- [ ] Regelumsetzer: P6
- [ ] Regelumsetzer: P7
- [x] Koordinator: nach dev gepusht

## Freigabe
Freigabe: offen
Kommentar: .
