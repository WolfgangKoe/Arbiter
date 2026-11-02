# Rote Probe der Prüfskripte bei teilweise gestagedem Commit

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Commit-Hook `proben` (`python3 -m pytest prozess/pruefungen -q -m "not stand"`,
[Commits](../../prozess/ablauf/commits.md)) war rot, als nur `prozess/ablauf/dod.md` und
`prozess/pruefungen/mutationsregeln/gleichwertig.json` gestaged waren; mit allen Dateien
grün. Nachgestellt in einem Klon unter `/tmp` (Stand vor dem Commit `Plan 10 geschrieben`,
nur diese zwei Dateien eingespielt, dazu die uncommittete `wartendeSchritte.py`): 877 Proben
grün, ebenso der volle Lauf im Repo (980 grün, SonarLint ohne Funde). Ein Fehler in einem
Prüfskript ist es danach nicht; einen Scheiter-Test kann ich nicht schreiben, weil nichts rot
wird. Die Meldung des Hooks liegt nicht vor. Wahrscheinlichste Ursachen: pre-commit stasht die
nicht gestageten Änderungen und stellt sie nach dem Lauf wieder her; liefen dabei zugleich
Architekt und Fachkritiker oder griffen Tests auf das echte Repo zu (Anliegen, Handoff), sah ein
Test ein halbes Arbeitsverzeichnis. Dazu laufen die Proben über 100 Sekunden und teilen sich
das Repo mit anderen Läufen.

**Kosten.** Ohne Meldung des Hooks lässt sich nichts beheben; weiter nachforschen kostet
einen Lauf.

**Gegenvorschlag.** Tritt es wieder auf, nennt der Koordinator die rote Probe (Testname aus
der Hook-Ausgabe) in einem Anliegen an den Regelumsetzer; dann entsteht der Scheiter-Test.

**F1 · Wie gehen wir mit der nicht nachvollziehbaren roten Probe um?**
A: Abwarten; beim nächsten Auftreten den Testnamen festhalten (Gegenvorschlag; neu).
B: Hook so ändern, dass seine Ausgabe in `.git/arbiter/` bleibt (neu).
Empfehlung: A, ein einzelner Fall ohne Meldung rechtfertigt keinen Mechanismus ([Absicht 2](../../prozess/praemissen/absicht.md)).
Antwort: A

**Stellungnahme.**
