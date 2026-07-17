STATUS: NEEDS-DECISION

# S158 — UI-Verifikation B-104 (Würfelsymbol statt nacktem ✕)

Render-Code (`diceCompose.py`/`diceHtml.py`) ist nicht von der Coverage-Messung erfasst
(CLAUDE.md „Warum Render-Code aus der Messung ausgeschlossen ist") — manuelle Prüfung
in der laufenden App PFLICHT, bevor B-104 endgültig als visuell bestätigt gilt.

## Testfall 1 — Auto-fail-✕ in der Wound-Zeile (Quantum Shielding)

**(a) Voraussetzungen:** Roster mit einer Necron-Einheit, die eine `wound_auto_fail`-Ability
mit Auto-fail-Slots trägt (z. B. Quantum Shielding, siehe S155-Beispiel); Kampfphase aktiv,
eine Attacke gegen diese Einheit ausgelöst bis zur Wound-Auflösung.

**(b) Klickpfad:** Angriff auflösen → Hit-Würfe bestätigen → Wound-Block öffnet sich; dort
die Auto-fail-Marker-Zeile unterhalb des Würfel-Grids betrachten (Slots, die durch die
Ability immer scheitern).

**(c) Erwartung inkl. Ausgangs-State:** Vorher (Ausgangs-State) zeigte jeder betroffene Slot
ein nacktes rotes/grünes „✕" als reinen Text-Glyph ohne Rahmen. Jetzt: jeder Auto-fail-Slot
zeigt ein umrandetes, würfelgroßes Kästchen (30×30px, abgerundete Ecken, Rahmenfarbe = Buff-
Grün oder Debuff-Rot je nach Perspektive) mit dem ✕ darin — visuell konsistent mit den
echten Miss-Würfeln im Grid darüber. Badge-Label links (z. B. „Quantum Shielding") bleibt
unverändert.

Befund: Statt einem "x" in der Mitte erscheint es wie die Fläche eines Würfels mit einem Auge. Es ist also noch nicht korrekt umgesetzt. Ich bitte dich noch einmal (schon das vierte Mal). Erstelle im Design-System bitte für jeden Fall das Schema eines Würfels. Wir haben eine Liste mit Symbolen unter §4. Und da können wir einfach eine Liste mit diesen Würfelsymbolen ergänzen. Dann ist alles standardisiert und enthält auch die Definitionen für die verschiedenen Farben. Dann tauchen natürlich alle Würfelflächen auf, aber eben auch die Effekte. Du kannst ja das System nach allen bisherigen Fällen durchsuchen und hier eine Liste anlegen. das sollte kein Problem sein. Und brauchen wir etwas Neues, ergänzen ein neues Symbol und bei Bedarf einen neuen Würfel.

## Testfall 2 — Reroll-↺-Marker (falls in dieser Session sichtbar verdrahtet)

**(a) Voraussetzungen:** Gleiche Kampfphase/Roster wie Testfall 1; ein Reroll-Marker
(`reroll_marker_row_html`) muss über einen Producer tatsächlich angezeigt werden — laut
Code-Kommentar (`diceCompose.py`, `reroll_marker_row_html`) ist dieser Baustein aktuell
„noch nicht in einen Roll-Block verdrahtet"; falls in der App kein Reroll-↺ sichtbar ist,
diesen Testfall als „nicht anwendbar (Baustein noch nicht produktiv verdrahtet)" markieren.

**(b) Klickpfad:** Falls verdrahtet: Attacke auflösen, bis eine Reroll-Situation angezeigt
wird (↺-Zeile unterhalb des betroffenen Würfel-Grids).

**(c) Erwartung inkl. Ausgangs-State:** Vorher nacktes gelb-oranges „↺" als Text-Glyph ohne
Rahmen. Jetzt: gleiches würfelgroßes Kästchen wie Testfall 1, Rahmenfarbe Reroll-Orange
(`#f59e0b`), ↺-Symbol zentriert darin.

Befund: Die Skorpekh Destroyers bzw. die Destroyers im Allgemeinen sollten so eine Fähigkeit beim Trefferwurf haben. Destroyer Lords erlauben das auch beim Verwundungswurf. Im Roster fehlt uns aber noch ein Destroyer Lord. Mit den Skorpekhs habe ich es gerade getestet. Scheinbar ist deren Fähigkeit nicht im Roster oder in der YAML verdrahtet.

**S158-Nachtrag:** Der Skorpekh/Destroyer-Lord-Befund ist als Backlog-Item
[B-113](../goals/backlog.md#b-113) überführt (Retro-Maßnahme 6); Testfall 1 (Sichtprüfung
des Würfelsymbols) bleibt hier offen.