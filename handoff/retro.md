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
   verlangen, der Test fehlt (6241, Technikphase 9). „Kein Verhalten ohne Test“ steht in
   [Es 3](../prozess/praemissen/es.md) und beim [Implementierer](../.claude/agents/implementierer.md),
   darum kein Item. Im Frontend fängt es nur die Kritik am Code (6471, Prozessphase 9).
3. 572 neue Zeilen Prüfcode gegen 530 Produktcode: über der Schwelle. Prozesslast 13 von 93
   Anliegen: darunter. Darum beauftragt diese Retro keinen neuen Mechanismus außer auf deinen
   Wunsch, und 3960 (weitere Bash-Sperren) wartet auf Prozessphase 9.
4. Deine Frage nach den Kommentaren (6430): Im Produkt steht kein `#`, aber 71 Docstrings,
   38 mit Kennungen wie „(QUE-10.5)“; mit Tests und Prüfcode rund 500. Du hast in 6431 F1 A
   gewählt: Ein Docstring bleibt nur als Kopf einer Testdatei, die Überschrift ihrer
   Anforderung mit Kürzel (`"""AUF-7 · Einheit in Aufstellung."""`,
   [T1](../technik/architektur/tests.md), geprüft von `spiegel.py`), heute 31; alle übrigen
   fallen, was ein Modul tut, sagt sein Name. F1 gilt nur Docstrings: `# Warum:` in
   `pyproject.toml` und die Fundstellen in den Daten-YAML bleiben, Es 8 und `kommentare.py`
   erfassen sie nicht.
5. Das Dashboard verwirft deine Antwort, wenn unter der Frage keine Zeile `Antwort:` steht;
   die Prüfung der Anliegen verlangt „Ux“ statt „UX“ (6432 an den Regelumsetzer).

Nicht bestätigt: `.venv/bin/python -c` war in meinem Lauf gesperrt; der Befehl zum Abhaken
nimmt mit Absicht nur eigene Schritte. Ins [Backlog](../prozess/backlog.md): Abkürzungen in
zusammengesetzten Namen, tote Links, Formfehler erst beim Commit, Kommentare im Chat,
lange Läufe, `gleichwertig.json` für den Testautor.

## Prozess-Items
P1 gilt Befund 1; sonst deine Aufträge 6430, 6380, 4040, 3550, 6960.
- P1 Tests für jeden Fall (Organisationsentwickler): Nach deiner Antwort F2 A läuft der
  Testautor auf Opus (`model: opus` in seiner Definition); der Auslöser fällt aus
  [Rollen mit Auslöser](../prozess/ablauf/rollenMitAusloeser.md). Danach prüft ein Test eher
  gleich, was für beide Spieler oder jede Runde gilt; jeder Lauf des Testautors kostet je
  Token doppelt so viel. Nach deiner Antwort B in Anliegen 6640
  zeigt seine [Anleitung](../.claude/skills/akzeptanztest-schreiben/SKILL.md) zudem das
  Gegenbeispiel „nur Spieler 1“: ein Test, der nur einen Spieler prüft, mit Grund.
- P3 Prämissen nach deinen Antworten (Organisationsentwickler): Es 8 nach F1 A (Befund 4):
  Docstring nur als Kopf der Testdatei nach T1, sonst keiner; unter `technik/` rot ab der
  Technikphase 9 (Mechanismus P4). Es S: „sein Name nennt sie“. Die sechs Verschiebungen
  nach F3 A (6380): Ich 1 ohne „die Moderation listet … zuoberst“, dafür „Fragen an dich nur
  in einem Anliegen“ statt Ich 5 „als Datei in `handoff/`“; Ich 2 verlinkt die
  [Rollenregeln](../prozess/regeln/rollenregeln.md) statt Skripte und Lücken zu nennen; die
  Einordnung aus Ich 3 nach [Kritik](../prozess/ablauf/kritik.md); „Akzeptanztests entstehen
  vor dem Code“ aus der Root-CLAUDE.md nach Es; Es L und I ohne „Noch ohne Anlass“. Dazu das
  Kürzel je Phase in der Domäne (4620). Ich wird rund 1.000 Zeichen kürzer.
- P4 Docstrings im Prüfcode (Regelumsetzer), nach P3: `formregeln/kommentare.py` lässt einen
  Docstring nur noch als Modul-Docstring einer Akzeptanztestdatei zu
  (`technik/tests/akzeptanz/**/<name>Test.py`; den Wortlaut prüft weiter `spiegel.py`). Jeder
  andere, auch einzeilig, in Modul, Klasse oder Funktion, auch in `handgriffe.py` und
  `conftest.py`, ist rot: „Docstring nur als Spiegel der Anforderung (Es 8)“; die Prüfungen
  „einzeilig“ und „TODO im Docstring“ entfallen.
  1. Zuerst entfernt er die 282 Docstrings in `prozess/pruefungen/`, je Lauf unter 120.000
     Token ein `P4 Zwischenstand`; ist der Docstring die einzige Anweisung (`Umleitung` in
     `rollenregeln/bashSchreiben.py`), tritt `...` an seine Stelle. `standregeln/` erst nach
     4301, es ändert dieselben Dateien.
  2. Dann die Prüfung: außerhalb von `technik/` im Test mit Marke `stand`; unter `technik/` in
     einem eigenen Test ohne `stand`, erst ab `Freigabe Plan 9` (Schwelle wie
     `ersteGeprüfteTechnikphase` in `formregeln/technikphase.py`). So ist er in der DoD rot
     (`python3 -m pytest prozess/pruefungen`), hält aber keinen Commit auf. Scheiter-Tests:
     Docstring von Modul und Funktion im Prüfcode rot; Kopf einer Akzeptanztestdatei grün,
     eine Funktion darin mit Docstring rot; unter `technik/` vor Plan 9 grün, ab Plan 9 rot.
     Dazu die Zeile Kommentare in den [Formregeln](../prozess/regeln/formregeln.md).
  3. Je ein Anliegen mit `Wartet auf: Technikphase 9` an den Testautor (118 Docstrings in
     `technik/tests/akzeptanz/` außer den 31 Köpfen, sechs Fixtures bestehen nur aus ihm) und
     an den Implementierer (71 in `technik/arbiter/`, einer in `technik/tests/einheit/`).
- P5 Ablauf schlanker (Organisationsentwickler): Streichungen 1 bis 6 aus
  Anliegen 4040; an einer Kopie in `/tmp`
  arbeiten und committen alle Rollen wie vorher.
- P6 Regeln schlanker (Regelumsetzer): Punkt 7 aus 4040, das Format `Hindernis:` einmal
  (4120), dazu 3780, Punkt 1.
- P7 Belegte Kriterien je Etappe (Regelumsetzer): Stand und Dashboard zeigen „Etappe 2: x von
  y Kriterien belegt“ neben allen (3550, A). Ein Kriterium zählt zur Etappe aus `(Etappe <n>)`
  am Satzende, sonst aus `Etappe: <n>` seiner Anforderung, ohne beides nur unter allen
  (Annahme bis zur Antwort des Anforderungsautors, [6500](anliegen/6500-etappeEinesKriteriums.md)).
- P8 Mutationslauf früher (Organisationsentwickler), nach deinen Antworten in
  [6960](anliegen/6960-mutationslaufFrueherStarten.md): Ab Technikphase 9 startet der
  Koordinator den vollen Lauf, sobald die DoD über das Inkrement grün ist, nicht erst mit der
  Prozessphase; ändert sich `technik/` danach, startet er neu ([DoD](../prozess/ablauf/dod.md)).
- P9 Mutationslauf zeigt und merkt je Modul (Regelumsetzer), nach P8: `mutation.py` schreibt
  je fertigem Modul sofort eine Zeile ins Protokoll (Modul, Mutanten, Überlebende) und das
  Ergebnis in `.git/arbiter/mutation.json`; ein unterbrochener Lauf beim gleichen Stand
  übernimmt die fertigen Module. Scheiter-Tests in `mutationTest.py`: nach dem ersten Modul
  steht seine Zeile, bevor das zweite fertig ist; ein nach dem ersten Modul abgebrochener Lauf
  prüft es beim nächsten nicht neu. Dazu die Zeile in den
  [Mutationsregeln](../prozess/regeln/mutationsregeln.md), `--voll` „nach der DoD über das
  Inkrement“ statt „für die Retro“.

## Empfehlung
Für dich ist nichts zu tun. Der Regelumsetzer arbeitet nach deiner Entscheidung in dieser
Reihenfolge: die Hook-Zeile aus Anliegen 6760; 3780
Punkt 4, ob `Wartet auf` eine Phase oder eine Nummer nennt, an einer Stelle statt an vier
([3780](anliegen/3780-restePruefcodeNach3301.md)); keine Testzeilen im Fortschritt für ein
Item ohne Kriterium ([4301](anliegen/4301-fortschrittFuerItemOhneKriterium.md)); P4 nach 4301,
ohne Teilung um `standregeln/`, weil beide dort ändern; P9 nach P4, es wirkt ab der
Technikphase 9 (6960, F3); zuletzt der Reiter Architektur
([4140](anliegen/4140-architekturAlsReiterBisZuDenDateien.md)): erst Bestand abbauen, dann
Neues (306).

## Fortschritt
- [x] Organisationsentwickler: Retro geschrieben
- [x] Fachkritiker: Kritik an der Retro
  Hindernis: Fachkritiker → Organisationsentwickler: P2 nähme die von BEW-1.5 und QUE-1.3 verlangte Sperre ‚Nahkampfreichweite‘ weg; P7 nennt einen falschen Stand zu Etappe: (Anliegen 6450); beseitigt: Commit „Nachkorrektur Retro 8, Rückfrage des Stakeholders zu 6431“
- [x] Architekt: Kritik an der Retro
  Hindernis: Architekt → Organisationsentwickler: F1 widerspricht T1, P2 steht schon, P7 zählt ungeregelt (Anliegen 6470); beseitigt: Commit „Nachkorrektur Retro 8, Rückfrage des Stakeholders zu 6431“
- [x] Organisationsentwickler: Nachkorrektur
- [x] Stakeholder: Freigabe Retro 8
- [x] Organisationsentwickler: P1
- [x] Organisationsentwickler: P3
- [ ] Regelumsetzer: P4
- [x] Organisationsentwickler: P5
- [x] Regelumsetzer: P6
- [x] Regelumsetzer: P7
- [ ] Organisationsentwickler: P8
- [ ] Regelumsetzer: P9
- [ ] Koordinator: nach dev gepusht

## Freigabe
Freigabe: ja
Kommentar: Zu P1, bitte nochmal erläutern, was esmit dem Gegenbeispiel auf sich hatte. Viellicht habe ich etwas missverstanden.
Stellungnahme: Erläutert in Anliegen 6640, dort F1 mit Empfehlung; P1 im Abschnitt Prozess-Items verweist darauf.
