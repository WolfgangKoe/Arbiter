# Pfad der alten Spezifikationen in domaene/CLAUDE.md

164 · Kritik · von Architekt (Technik) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
Kritik am Code zu Commit 6a64835.

**Befund.** Der Commit stellt laut Betreff „alle Verweise“ auf `Arbiter-old/` um. Diesen hat er
übersehen: `domaene/CLAUDE.md`, Zeile 22, nennt als Quelle noch `Arbiter/Arbiter_Specs/*.pdf`.
Die Dateien liegen jetzt in `Arbiter-old/Arbiter_Specs/`. `domaene/CLAUDE.md` gehört zu deinen
Schreibpfaden (`*/CLAUDE.md`).

**Kosten.** Gering, aber es trifft die Quellen: Anforderungsautor und Planer finden die
Spezifikationen des Stakeholders unter dem genannten Pfad nicht. Dann fragen sie entweder
nach oder verzichten auf die Quelle.

**Gegenvorschlag.** In `domaene/CLAUDE.md`, Zeile 22, `Arbiter/` durch `Arbiter-old/` ersetzen.
Den Code betreffen [163](163-altbestandEinmalNennen.md) und
[165](165-umbenennungPerTestBemerken.md). Tote Pfade in Markdown findet keiner von beiden. Für
eine einzelne Zeile lohnt sich ein solcher Test nicht.

Erledigt, wenn `git grep -n "Arbiter/" -- domaene` nichts mehr findet.

**Stellungnahme.**
