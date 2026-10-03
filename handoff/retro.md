# Retro · Zyklus 1

Etappe 1 · Aufstellen, Item *Reihenfolge der Aufstellung*.
Grundlage: [Review 1](review.md), git, Anliegen, Rollenläufe.

## DoD und Abnahme
DoD nicht erreicht, keine Abnahme durch die Domäne. DoD 1 und 2 grün (45 und 290 Tests).
DoD 3: Das Item liegt; AUF-1.3 lässt den Zwischenzustand offen
([25](anliegen/25-auf1-an-der-reihe-zwischen-gewinner-und-zone.md), seit Plan 1 ohne Antwort,
im Review nicht genannt), die Zonennamen sind erfunden ([63](anliegen/63-zonenOhneErfundeneNamen.md)).
Ursache: Der Stand kennt Schritt 5 nicht (50), und der Koordinator kann `prozess/ablauf.md`
(9.800 Zeichen) nicht lesen (Lesegrenze 4.000). Lösbar mit P1 und P2.

## Befunde
1. Rollenläufe über der Schwelle: Technik 28/10, Prozess 23/5. 10 Technikläufe waren
   Prozessarbeit nach der Benennungsentscheidung im Zyklus. Nach Review 1 meldete der Stand
   die Prozessphase, die 18 Läufe danach waren Technik und Domäne.
2. 55 Anliegen angelegt, 26 offen. Dran: Regelumsetzer 10 (Phase lief nicht),
   Organisationsentwickler 5, Planer und Anforderungsautor 6, davon 09, 15, 16 nur als Ablage
   von Entscheidungen, Stakeholder 3: 21 und 28 tragen deine Antworten, Status `offen`.
3. Nummern doppelt vergeben: 40 und 42 in git, 60 beim parallelen Anlegen.
4. Ein Anliegen wurde per Bash geändert; dort greift `statusrecht.py` nicht.
5. Tote Links: 10 in Anliegen, 6 im Plan, alle auf gelöschte Anliegen (32 → 30).
6. `angenommen` vor dem weitergereichten Teil (50 → 56, 31): Der Stand meldet eine
   Nachprüfung ohne Gegenstand.
7. Ein Edit an einem Anliegen bringt rund 26.000 Zeichen Rechtschreibmeldungen in den Kontext
   (24, weiter offen).
8. Kritik des Entwicklers ([31](anliegen/31-kritikDesEntwicklersFuerRetro1.md)): Komplexität ohne
   Schwelle; das implizite Domänenmodell zeigt sich an 43, 58, 63.

## Geändert
- [Ablauf, Anliegen](../prozess/ablauf.md#anliegen): `Antwort: .` unter jeder Frage (20);
  `angenommen` erst nach dem weitergereichten Teil, sonst „wartet auf <nr>“.
- Planer liest git, bevor er eine Etappe ausformuliert (14);
  danach können 09, 15, 16 schließen.
- Koordinator: wer dran ist, steht im Kopf des Anliegens.
- [Kennzahlen](../prozess/kennzahlen.md): Bedeutung und Reaktion. [Backlog](../prozess/backlog.md):
  Zurückgestelltes aus 22, 31, 38.
- Domänenmodell (31, Punkt 4): Beziehungen im Glossar ([Domäne](../domaene/CLAUDE.md)).
- Nächster Lauf: Abschnitt Anliegen nach `prozess/anliegen.md`, für Koordinator und Rollen.

## Prozess-Items (Regelumsetzer, in dieser Reihenfolge)
- P1 Stand erkennt die Abnahme (56).
- P2 Stand nennt je offenem Anliegen, wer dran ist (ohne „wartet auf“), und fällige Kritik am
  Code; ein Hook `PostToolUse` auf `Agent` meldet ihn nach jedem Rollenlauf.
- P3 Nummer eindeutig: Write einer neuen Datei mit vergebener Nummer gesperrt, die Meldung
  nennt die nächste freie; Test aus 42.
- P4 `bashPositivliste.py` sperrt für Rollen Schreibbefehle auf `handoff/anliegen/`.
- P5 `erledigteLoeschen.py` ersetzt Links auf die gelöschte Datei durch „Anliegen <n>“.
- P6 `anliegen.py`: unter jeder Frage an den Stakeholder eine Zeile `Antwort:`.
- P7 complexipy (Schwelle 15, Verschachtelung) und ruff `PLR0912` (12, Zahl der Fälle) im
  Lauf der Prüfungen; der Architekt kritisiert.
- P8 `kennzahlen.py`: Rollenläufe je Phase und Rolle, offene Anliegen je Rolle mit Alter.
- P9 `glossar.py`: Klassen und Enum-Werte der Domäne stehen als Code-Bezeichner im Glossar
  oder als *Grund* in einer Anforderung (70), Enum-Werte in Klammern hinter ihrer Klasse;
  grün nach [75](anliegen/75-enumWerteDerAufstellungszone.md).
Danach seine Anliegen: 40, 57, 60, 62, 52, 24, 53.

## Empfehlung
1. Vor der Freigabe die Abnahme: Anforderungsautor 25; Testautor testet den Zwischenzustand,
   Fachkritiker prüft den Test; Implementierer 63; Fachkritiker nimmt ab; Planer löscht das
   Item; Reviewer ergänzt Review 1.
2. Moderation und Fragen an dich: Anliegen 65, umgesetzt als
   [Moderator](../.claude/agents/moderator.md), [Ablauf, Anliegen](../prozess/ablauf.md#anliegen)
   und [Prämisse](../prozess/praemissen/wir.md), Punkt 9.
3. `handoff/kritik-entwickler.md` ist ausgewertet; `VORGEHEN.md` löschbar nach
   [57](anliegen/57-pyprojectOhneVorgehen.md).
