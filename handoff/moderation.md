# Moderation

Stand: Zyklus 3, Prozessphase, 38 offene Anliegen; nächster Schritt Retro 3.

## Befund: bestätigt
- Offen: 38 von 38 in der Perspektive Prozess; Domäne 0, Technik 0 (294, 286 prüfen
  Frontend und web, ändern aber nur Prüfskripte). Empfänger: Regelumsetzer 33,
  Organisationsentwickler 5 (107, 138, 150, 219, 289); alle anderen Rollen 0.
- Absender: Reviewer 19, Organisationsentwickler 12, Architekt 4, Stakeholder 3. Also
  gut die Hälfte ist Kritik am Code der Prüfskripte, die selbst Kritik erzeugt (Nachschliff
  202 bis 206 stammt von Kritik an Nachschliff).
- Zufluss gegen Abfluss seit Freigabe Retro 2: 129 angelegt, 112 gelöscht, 243 Commits.
  Der Abfluss hält kaum mit; 22 der 38 sind älter als 250. Die Last liegt auf einer Rolle.
- Arbeit seit Freigabe Retro 2 (Dateien): prozess und .claude 499, technik 57, domaene 38.
  Prozesslast ([Kennzahlen](../prozess/kennzahlen.md)): nahe 100 % gegen Schwelle ein Drittel.
- Fehlt: ein Anliegen mit Frage zu dieser Lage. Die alten Fragen (279, 280) sind erledigt.

## Dran
Blockiert Plan 4 (Komponentenseite): Anliegen 286,
Anliegen 294; Prüfung vor dem Frontend, sonst nichts.
- Regelumsetzer: 33 an ihn, Kette siehe unten.
- Organisationsentwickler: Retro 3; 107, 138, 150, 219, 289.
- Reviewer, Architekt: Nachprüfungen, die fällig werden. Domäne, Technik-Rollen: frei.

## Vorschläge
Vor Plan 4 (Regelumsetzer): 286, 294, 287, 290, 295; danach Plan 4 starten, Rest parallel.
Schließen (Organisationsentwickler, Absender): [107](anliegen/107-kritikAnDenPruefungen.md)
(253 erledigt), 219 mit 220, 138 mit 215.
Bündeln, ein Lauf des Regelumsetzers:
- 215, 288, 138: Bash-Umgehung; 215 ist der Versuch, in den Backlog (139 steht dort).
- 289 mit 290; 278 mit 287 (Hook-Meldung, Bilanz); 272 mit 292 (Schichten).
- 228, 229, 230, 231, 232 (Starter, Wurzel, Unterordner); 247 mit 249 (Importvertrag).
- 274, 275 mit 246 (Dashboard, Anliegenformen); 273, 276, 284, 240 einzeln, klein.
Backlog (Reviewer als Absender, kein Fehlverhalten, Nachschliff): 202 bis 206, 221, 295.
  Auslöser: Fund in einem Lauf. Behalten, weil Stakeholder oder Plan es trägt:
  [150](anliegen/150-sonarlintAbdeckungUndToterCode.md) mit 216, 246, 275.
Regel (Organisationsentwickler, Retro 3, Kennzahl greift): Kritik am Code der Prüfskripte nur
bei Fehlverhalten, Rest als Sammelanliegen je Datei und Zyklus; höchstens 10 offen an den
Regelumsetzer. Bestehende Regel: Prozesslast, Reaktion „mindestens einen Mechanismus löschen“.
Arbeitsteilung: Zyklus Domäne, Technik im Wechsel; Prozessphase nur Kette der Blocker.
Stränge nach [Ablauf](../prozess/ablauf.md#gleichzeitige-läufe): Hook-Code (272, 278, 287,
289, 290) höchstens ein Lauf; Linter (294) und Prüfskript-Werkzeug (228 bis 232, 247, 249)
daneben.

## Fragen an dich
Offen ist keine; kein Anliegen stellt sie. Der Organisationsentwickler legt sie an, wenn du
unten zustimmst:
- Backlog und Deckel (höchstens 10 offene Anliegen an den Regelumsetzer) wie oben?
- Plan 4 vor der restlichen Kette, nur 286, 294 vorab?
- Kritik am Code der Prüfskripte nur bei Fehlverhalten?
Kommentar:
