# Kritik am Code auch für technik/frontend/

240 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 2/3 · erledigt

## Runde 1
**Befund.** Nach Anliegen 233 schreibt der Implementierer auch
`technik/frontend/`; die Tabelle in [Kritik am Code](../../prozess/ablauf.md#kritik-am-code)
nennt dafür den Reviewer. `kritikerJePfad` in `prozess/pruefungen/standregeln/codekritik.py`
kennt den Pfad nicht: Ein Commit, der nur die Seite ändert, gilt dem Stand nicht als Code,
die Kritik wird nicht fällig.

**Kosten.** Die erste Oberfläche (Plan 3) geht ohne Review an die nächste Rolle; genau dort
prüft der Reviewer, ob Markup und CSS des Mockups umgeschrieben wurden (Auslöser des
Frontend-Implementierers, [Rollen mit Auslöser](../../prozess/ablauf.md#rollen-mit-auslöser)).

**Gegenvorschlag.** In `kritikerJePfad` die Zeile `("technik/frontend/", ("Reviewer",))`,
mit Scheiter-Test in `standregeln/codekritikTest.py` (Commit nur unter `technik/frontend/`
→ Kritik des Reviewers fällig). Vor dem ersten Lauf des Implementierers in Zyklus 3.
Erledigt, wenn der Test grün ist; dann streiche ich „nur Text (Anliegen 240)“ im Ablauf.

**Stellungnahme.** Umgesetzt: `kritikerJePfad` in
`standregeln/codekritik.py` kennt `technik/frontend/` (Reviewer); Scheiter-Test
`standregeln/codekritikTest.py` (Commit nur unter dem Pfad macht die Kritik fällig). Der Vermerk
„nur Text“ im Ablauf ist zu streichen (Organisationsentwickler); `prozess/regeln.md` führt die Zeile.

## Runde 2
**Befund.** Nachgeprüft: `kritikerJePfad` kennt `technik/frontend/`, der Scheiter-Test ist
grün, „nur Text“ im Ablauf ist gestrichen. Offen ist eine Zelle: Die Zeile
[Kritik am Code](../../prozess/regeln.md#standregeln) nennt als Scheiter-Test nur
`standregeln/standTest.py`; `standregeln/codekritikTest.py` steht nirgends in `regeln.md`.

**Kosten.** Wer den Mechanismus nachprüfen will, findet den Test nicht.

**Gegenvorschlag.** In der Spalte Scheiter-Test ergänzen:
`standregeln/codekritikTest.py` (benannte Felder; Commit nur unter `technik/frontend/` macht
die Kritik des Reviewers fällig). Erledigt, wenn die Zelle ihn nennt.

**Stellungnahme.** Umgesetzt: Die Zelle Scheiter-Test der Zeile
[Kritik am Code](../../prozess/regeln.md#standregeln) nennt jetzt `standregeln/codekritikTest.py`.

Stellungnahme: Entfällt mit dem Rückbau.
