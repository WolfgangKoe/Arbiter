# Retro 1, Befund 8: Erfundene Namen im Code findet eine Prüfung

70 · Kritik · von Architekt (Technik) → Organisationsentwickler · Runde 1/3 · angenommen

## Runde 1
**Befund.** Befund 8 bleibt ohne Folge; den fehlenden Empfänger auf der Seite der Domäne
nennt [68](68-domaenenmodellOhneEmpfaenger.md). Erfunden wurde aber im Code:
`Aufstellungszone.nord` und `.süd` ([63](63-zonenOhneErfundeneNamen.md)).
[Review 1](../review.md), DoD 2, prüfte „Glossar ↔ Code stimmt für alle kursiven Begriffe“,
also nur vom Glossar zum Code. Die Gegenrichtung (steht, was der Code einführt, im Glossar?)
prüft niemand, und die Domäne sieht den Code erst nach dem Bau. Der
[Backlog](../../prozess/backlog.md) stellt die Werkzeuge der DoD zurück, bis „Review oder
Kritik am Code findet, was das Werkzeug meldet“; mit 63 ist das eingetreten.

Wegwerf-Versuch (25 Zeilen mit `ast`, außerhalb des Repos): Jede Klasse und jeder Enum-Wert
in `technik/arbiter/domaene/` steht in der Spalte *Code-Bezeichner* des Glossars oder als
*Grund* ‚…‘ in einer Anforderung. Ergebnis heute: genau zwei Meldungen, `nord` und `süd`,
keine Fehlmeldung.

**Kosten.** Ohne Prüfung erfindet der nächste Implementierer den nächsten Namen (mit 64 kommen
*Spielfeld*, *Spielfeldkante*), und er wandert wie bei 63 in Karte, Protokoll und Oberfläche;
63 kostete vier Anliegen und zwei Runden beim Stakeholder. Die Prüfung kostet ein Skript in der
Art von `rueckverfolgung.py` mit Scheiter-Test.

**Gegenvorschlag.** Prozess-Item P9 an den Regelumsetzer, vor der nächsten Technikphase:
`glossar.py` im Lauf von `python3 -m pytest prozess/pruefungen`, Regel wie im Versuch;
Scheiter-Test: ein Enum-Wert `nord`. Die Meldung nennt den Weg (Anliegen an den
Anforderungsautor), nicht „ins Glossar schreiben“. Methoden und Variablen bleiben Urteil, ihre
Namen sind zusammengesetzt (`gewinnerWählen`). DoD 2 nennt dann „Code → Glossar“ mit
Mechanismus, „Glossar → Code“ bleibt nur Text. Der Architekt kritisiert. So steht ein Begriff
erst im Glossar, dann im Code: der prüfbare Teil von „Domänenmodell vor dem Code“, gleich wie
68 entschieden wird.

**Stellungnahme.** Angenommen. Der Auslöser im [Backlog](../../prozess/backlog.md) ist
eingetreten; [Retro 1](../retro.md), P9, verweist für Regel, Scheiter-Test und Meldung
hierher. Die Prüfung meldet heute `nord` und `süd`; grün wird sie mit 63, das Empfehlung 1 vor
der Freigabe einplant. Den Code der Prüfung kritisiert nach
[Ablauf, Kritik am Code](../../prozess/ablauf.md#kritik-am-code) der Reviewer; die Regel
prüfst du als Absender nach. DoD 2 nennt „Code → Glossar“ mit Mechanismus, sobald
`glossar.py` gebaut ist; bis dahin bleibt „Glossar ↔ Code“ nur Text.
