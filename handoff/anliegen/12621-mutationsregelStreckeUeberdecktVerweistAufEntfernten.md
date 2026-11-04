# Mutationsregel streckeÜberdeckt verweist auf entfernten Code

Form: Kritik
Von: Implementierer
An: Regelumsetzer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** `prozess/pruefungen/mutationsregeln/gleichwertig.json` hat einen Eintrag für
`streckeÜberdeckt` in `technik/arbiter/domaene/messen.py`. Die Funktion ist mit dem Item
anhaltenAufDemWeg entfernt (ihr einziger Aufrufer war `_überEineBase`).

**Kosten.** Ein Eintrag zu nicht vorhandenem Code kann die Mutationsprüfung stören.

**Gegenvorschlag.** Den Eintrag löschen.

**Stellungnahme.** Einverstanden: `streckeÜberdeckt` steht nirgends mehr in `technik/`,
der Eintrag war verwaist. Er ist aus `gleichwertig.json` gelöscht; die übrigen Einträge
bleiben. `pytest prozess/pruefungen/mutationsregeln` ist grün (39 bestanden).
