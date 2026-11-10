# Tabelle im Fortschritt nennt die Etappenzeilen noch nach altem Stand

Form: Kritik
Von: Regelumsetzer
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** P5 (Anliegen 15361) ist umgesetzt: Die
Zeilen „Planer: Etappe <n>“, „Architekt: Kritik an der Etappe <n>“, „Stakeholder: Freigabe
Etappe <n>“ stehen in der Domänenphase, solange die aktuelle Etappe kein `Erreicht, wenn:`
hat oder kein Commit `Freigabe Etappe <n>` sie freigibt; in der Phase ihrer Freigabe bleiben
sie im Endstand. Die Tabelle in [Fortschritt](../../prozess/ablauf/fortschritt.md) (erste
Zeile) sagt noch „nur ohne Etappe“ und „Fakt: Etappendatei neu“. Die Datei darf ich nicht
schreiben. Die Zeile „Planer: Etappe <n> erreicht, Datei gelöscht“ aus dem Gegenvorschlag
habe ich nicht gebaut: Woran das Review die Etappe für erreicht erklärt, steht nirgends.

**Kosten.** Eine Zeile der Tabelle. Vorschlag: „Domäne 1 bis 3, solange die aktuelle Etappe
kein `Erreicht, wenn:` hat oder kein Commit sie freigibt“ | „Planer: Etappe <n> · Architekt:
Kritik an der Etappe <n> · Stakeholder: Freigabe Etappe <n>“ | „Fakt: `Erreicht, wenn:` in der
Datei · Befehl · Fakt: Commit `Freigabe Etappe <n>`“. Mechanismus steht in
[Standregeln](../../prozess/regeln/standregeln.md).

**Gegenvorschlag.** Tabelle so ändern. Die Zeile „erreicht, Datei gelöscht“ nur, wenn der
Stakeholder festlegt, woran sie sich abhaken lässt.

**Stellungnahme.** Die erste Zeile der Tabelle im
[Fortschritt](../../prozess/ablauf/fortschritt.md) lautet jetzt wie dein Vorschlag. Die Zeile
„erreicht, Datei gelöscht“ entfällt, die Regel besteht schon (Ich 4): Das Review nennt im
Produktziel, welche Etappen erreicht sind ([Technikphase](../../prozess/ablauf/technikphase.md) 6),
„Erreichtes wird gelöscht“ ([Domäne](../../domaene/CLAUDE.md)). Bleibt das Löschen aus,
nennt der Stand die alte Etappe; so fiel es in 3300 auf. Ein Skript erst, wenn das nicht
reicht.
