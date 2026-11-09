# Mutationsregeln: Zeitpunkt des Laufs nach der DoD

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Mit P7 der [Retro 10](../retro.md) (Anliegen
[15960](15960-einMutationslaufJeZyklus.md)) läuft die Mutation einmal je Zyklus nach
`Freigabe Review`, bei erreichter Etappe voll; die Überlebenden schreibt der Reviewer als
Anliegen ([DoD, Mutationslauf](../../prozess/ablauf/dod.md#mutationslauf)). Die Zeile in den
[Mutationsregeln](../../prozess/regeln/mutationsregeln.md) sagt noch das Alte:
„Lücken gehen an den Testautor“, „der Lauf geschieht je Item vor dem Review“ und beim vollen
Lauf „nach der DoD über das Inkrement“.

**Kosten.** Eine Zeile Text, kein Code; `mutation.py` bleibt, wie es ist.

**Gegenvorschlag.** Die drei Stellen durch einen Link ersetzen: „der Lauf geschieht einmal
je Zyklus, nicht beim Commit; Zeitpunkt und Lücken:
[DoD](../ablauf/dod.md#mutationslauf) (Anliegen 15960)“; beim vollen Lauf entfällt „nach der
DoD über das Inkrement“.

**Stellungnahme.** Umgesetzt wie im Gegenvorschlag in den
[Mutationsregeln](../../prozess/regeln/mutationsregeln.md): „Lücken gehen an den Testautor“
entfällt, der Zeitpunkt ist „einmal je Zyklus, nicht beim Commit“ mit Link auf die DoD, beim
vollen Lauf entfällt „nach der DoD über das Inkrement“. Kein Code geändert.
