# Wie nennt ein Kriterium seine Etappe?

Form: Fragen
Von: Organisationsentwickler
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 9

## Runde 1
**Befund.** P7 der [Retro 8](../retro.md) zählt „Etappe 2: x von y Kriterien belegt“; wie ein
Kriterium seine Etappe nennt, legen Planer und Anforderungsautor fest (Anliegen 3550, A).
Heute haben 15 von 39 Anforderungen die Zeile `Etappe: <n>`, 11 davon `Etappe: 2`. Einzelne
Kriterien tragen `(Etappe <n>)` am Satzende, auch abweichend von der Zeile: AUF-8.7, AUF-12.8,
AUF-20.6 „(Etappe 2)“ in Anforderungen ohne `Etappe:`, AUF-28.2 „(Etappe 3)“ unter
`Etappe: 2`. 24 Anforderungen nennen keine Etappe, darunter
[QUE-1](../../domaene/anforderungen/querschnitt/setzen.md), das die *Bewegungsphase* braucht.
Die [Domäne](../../domaene/CLAUDE.md) nennt das Format nicht (Anliegen 6450, 6470).

**Kosten.** Fehlt einem Kriterium der laufenden Etappe die Kennzeichnung, zählt „Etappe 2“ es
nicht mit; die Zahl, an der der Stakeholder den Fortschritt der Etappe abliest, wird zu klein.

**Gegenvorschlag.**
1. Das Format, wie es heute steht: `Etappe: <n>` unter der Überschrift der Anforderung,
   `(Etappe <n>)` am Satzende eines Kriteriums, das davon abweicht; das Kriterium geht vor.
   Nach deiner Antwort trage ich es in die [Domäne](../../domaene/CLAUDE.md) ein (Prozessphase 9).
2. Ein Kriterium ohne beides zählt nur unter allen, nicht zur laufenden Etappe; Etappe 1 ist
   erreicht, ihre Datei gelöscht (Domäne: Erreichtes wird gelöscht).
3. Anforderungen, deren Kriterien die laufende Etappe braucht, etwa QUE-1, bekommen mit dem
   Planer `Etappe: <n>` oder `(Etappe <n>)`.

Annahme: P7 zählt nach 1 und 2, bis du antwortest.

**Stellungnahme.**
