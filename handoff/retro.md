# Retro · Zyklus 8

Dashboard: im Projektordner
`python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer` starten,
`http://127.0.0.1:8765/` öffnen, Strg+C beendet.

Etappe 2 von 10 (Phasen und Bewegungsphase) läuft ([Review 8](review.md)); 95 von 123
Kriterien belegt (Zyklus 7: 78 von 108). Neu am Bildschirm: „Erster Zug“, *Schlachtrunden*
mit „Phase beenden“, in der *Bewegungsphase* ein Zug bis zur *Bewegungsweite*, Sperre über
eine fremde *Base* und in *Nahkampfreichweite*, ‚keine Kohärenz‘ beim Phasenende,
Schlachtende nach Runde 5.

## Was geklappt hat
Alle drei Items abgenommen, DoD erfüllt, 17 Kriterien mehr belegt. Die Kritik am Review fand
vor deiner Freigabe, was der Klickpfad ausließ (6335, 6360).

## Was nicht geklappt hat
1. 6 der 12 Hindernisse gingen an den Testautor: Tests prüften nur einen Fall (nur Spieler 1,
   nur Runde 1, nur auf den Achsen); die Mutation fing zuerst 84 %. Damit trat der Auslöser
   „Testautor auf Opus“ ein ([Rollen mit Auslöser](../prozess/ablauf/rollenMitAusloeser.md)).
2. Zwei Verhalten kamen ohne Test: Das Greifen am Rand (AUF-8.7) fand die Kritik am Code
   (6101). ‚Nahkampfreichweite‘ sperrt in der *Bewegungsphase*, wie BEW-1.5 und QUE-1.3
   verlangen, der Test fehlt (6241, Technikphase 9). „Kein Verhalten ohne Test“ steht in der
   [Root-CLAUDE.md](../CLAUDE.md) und beim [Implementierer](../.claude/agents/implementierer.md),
   darum kein Item. Im Frontend fängt es nur die Kritik am Code (6471, Prozessphase 9).
3. 572 neue Zeilen Prüfcode gegen 530 Produktcode: über der Schwelle. Prozesslast 13 von 93
   Anliegen: darunter. Darum beauftragt diese Retro keinen neuen Mechanismus außer auf deinen
   Wunsch, und 3960 (weitere Bash-Sperren) wartet auf Prozessphase 9.
4. Deine Frage nach den Kommentaren (6430): Im Produkt steht kein `#`, aber 71 Docstrings,
   38 mit Kennungen wie „(QUE-10.5)“; dazu Tests und Prüfcode. Deine Wahl:
   [Anliegen 6431](anliegen/6431-fragenDerRetro8.md), F1. Bei A bleibt im Docstring jeder
   Testdatei die Überschrift ihrer Anforderung mit Kürzel (`"""AUF-7 · Einheit in Aufstellung."""`,
   [T1](../technik/architektur/tests.md), geprüft von `spiegel.py`); B streicht auch T1 (1),
   Es S und diese Prüfung. F1 gilt nur Docstrings: `# Warum:` in `pyproject.toml` und die
   Fundstellen in den Daten-YAML bleiben, Es 8 und `kommentare.py` erfassen sie nicht.
5. Das Dashboard verwirft deine Antwort, wenn unter der Frage keine Zeile `Antwort:` steht;
   die Prüfung der Anliegen verlangt „Ux“ statt „UX“ (6432 an den Regelumsetzer).

Nicht bestätigt: `.venv/bin/python -c` war in meinem Lauf gesperrt; der Befehl zum Abhaken
nimmt mit Absicht nur eigene Schritte. Ins [Backlog](../prozess/backlog.md): Abkürzungen in
zusammengesetzten Namen, tote Links, Formfehler erst beim Commit, Kommentare im Chat,
lange Läufe, `gleichwertig.json` für den Testautor.

## Prozess-Items
P1 gilt Befund 1; sonst deine Aufträge 6430, 6380, 4040, 3550.
- P1 Tests für jeden Fall (Organisationsentwickler): Nach F2 läuft der Testautor auf Opus,
  der Skill `akzeptanztest-schreiben` bekommt das Gegenbeispiel „nur Spieler 1“. Danach
  prüft ein Test, was für beide Spieler oder jede Runde gilt, mit mehr als einem Wert.
- P3 Prämissen nach deinen Antworten (Organisationsentwickler): Es 8 nach F1 (Befund 4), die
  sechs Verschiebungen nach F3 (6380), das Kürzel je Phase in der Domäne (4620).
- P4 Docstrings im Prüfcode (Regelumsetzer): `formregeln/kommentare.py` nach Es 8 neu, der
  Prüfcode danach ohne verbotene Docstrings. Produkt und Tests räumen Implementierer und
  Testautor in Technikphase 9; rot erst in deren DoD.
- P5 Ablauf schlanker (Organisationsentwickler): Streichungen 1 bis 6 aus
  [Anliegen 4040](anliegen/4040-ablaufUndRegelnVerschlanken.md); an einer Kopie in `/tmp`
  arbeiten und committen alle Rollen wie vorher.
- P6 Regeln schlanker (Regelumsetzer): Punkt 7 aus 4040, das Format `Hindernis:` einmal
  (4120), dazu 3780, Punkt 1.
- P7 Belegte Kriterien je Etappe (Regelumsetzer): Stand und Dashboard zeigen „Etappe 2: x von
  y Kriterien belegt“ neben allen (3550, A). Ein Kriterium zählt zur Etappe aus `(Etappe <n>)`
  am Satzende, sonst aus `Etappe: <n>` seiner Anforderung, ohne beides nur unter allen
  (Annahme bis zur Antwort des Anforderungsautors, [6500](anliegen/6500-etappeEinesKriteriums.md)).

## Empfehlung
Beantworte 6431 und gib die Retro frei. Der Reiter Architektur (4140) kommt nach P6: erst
Bestand abbauen, dann Neues (306).

## Fortschritt
- [x] Organisationsentwickler: Retro geschrieben
- [x] Fachkritiker: Kritik an der Retro
  Hindernis: Fachkritiker → Organisationsentwickler: P2 nähme die von BEW-1.5 und QUE-1.3 verlangte Sperre ‚Nahkampfreichweite‘ weg; P7 nennt einen falschen Stand zu Etappe: (Anliegen 6450); beseitigt: Commit „Nachkorrektur Retro 8, Rückfrage des Stakeholders zu 6431“
- [x] Architekt: Kritik an der Retro
  Hindernis: Architekt → Organisationsentwickler: F1 widerspricht T1, P2 steht schon, P7 zählt ungeregelt (Anliegen 6470); beseitigt: Commit „Nachkorrektur Retro 8, Rückfrage des Stakeholders zu 6431“
- [x] Organisationsentwickler: Nachkorrektur
- [ ] Stakeholder: Freigabe Retro 8
- [ ] Organisationsentwickler: P1
- [ ] Organisationsentwickler: P3
- [ ] Regelumsetzer: P4
- [ ] Organisationsentwickler: P5
- [ ] Regelumsetzer: P6
- [ ] Regelumsetzer: P7
- [ ] Koordinator: nach dev gepusht

## Freigabe
Freigabe: offen
Kommentar: .
