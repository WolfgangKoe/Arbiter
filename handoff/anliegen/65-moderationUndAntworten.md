# Moderation, der Weg deiner Antworten, eine Prämisse

65 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** [Retro 1](../retro.md), Befund 2: 26 offene Anliegen, der Auslöser der Moderation
(mehr als 5, [Ablauf](../../prozess/ablauf.md#rollen-mit-auslöser)) ist erreicht. Wer dran ist
und seit wann, kann ein Skript sagen (Retro 1, P2 und P8). Nicht berechnen lässt sich, welche
Anliegen dasselbe Thema tragen (43, 58, 63), welche nur noch Entscheidungen ablegen (09, 15,
16) und welche zu schließen sind.

**Kosten.** Ein Lauf vor jeder Freigabe, rund 15.000 Token zum Lesen der Anliegen. Ohne ihn
sortierst du die Anliegen selbst, oder sie wachsen weiter.

**F1 · Moderation einsetzen?** A: Rolle `moderator` (Prozess, prüfend, Sonnet). Läuft vor jeder
Freigabe und auf Auftrag des Koordinators, liest alle offenen Anliegen und schreibt nur
`handoff/moderation.md` (höchstens 4.000 Zeichen, auch für den Koordinator lesbar): je Rolle,
was dran ist und was davon das Inkrement blockiert; was zusammengehört oder geschlossen werden
kann; deine offenen Fragen gesammelt. Status setzt sie nicht, sie entscheidet nichts. B: erst
nur das Skript; die Rolle, wenn es nicht reicht.
Empfehlung A: Das Sortieren ist Urteil; die Rollen sehen jeweils nur ihre eigenen Anliegen.

Antwort: .

**F2 · Gilt deine Freigabe „.“ auch für deine offenen Fragen?** 21 und 28 tragen deine
Antworten, ihr Status ist noch `offen`; `beantwortet` setzt heute nur du.
A: Die Freigabe beantwortet jede Frage an dich, die in der Freigabevorlage steht: mit deiner
Zeile `Antwort:`, sonst mit der Empfehlung. Danach setzt der Absender `beantwortet`.
B: Du setzt den Status weiter selbst.
Empfehlung A: Keine Frage hängt mehr am Status, und „.“ gilt schon heute als Zustimmung.

Antwort: .

**F3 · Prämisse „Abstraktion nach Verständlichkeit“?** Aus der
[Kritik des Entwicklers](../kritik-entwickler.md) ([31](31-kritikDesEntwicklersFuerRetro1.md)).
A: in `prozess/praemissen/wir.md`: „Die Form folgt der Verständlichkeit: wenige Fälle als
`if` mit frühem `return`; viele, die sich nur in Daten unterscheiden, als Tabelle oder
Katalogdaten; viele mit eigenem Verhalten als eigene Typen. Es urteilt der Reviewer.“
B: keine Prämisse, nur die Schwellen.
Empfehlung A: complexipy sperrt Verschachtelung, ruff `PLR0912` die Zahl der Fälle (Retro 1,
P7; ein `match` zählt bei complexipy nur einmal, [69](69-schwelleZaehltKeineFaelle.md)); der
Satz sagt, wohin umgebaut wird.

Antwort: .

**Stellungnahme.**
