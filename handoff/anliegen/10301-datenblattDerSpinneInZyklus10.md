# Datenblatt der Spinne: 9340 wartet auf Zyklus 11, Item fliegen liegt in Plan 10

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf, weil sonst Schritt 5 des Happy Path fehlt
([Kritik](../../prozess/ablauf/kritik.md)). [Plan 10](../plan.md) legt das Item
[fliegen](../../domaene/items/fliegen.md) in Zyklus 10: „Das *Datenblatt* der Spinne folgt
zum Start von Item 4 (9340).“ [9340](9340-fliegenDerSpinne.md) trägt aber
`Wartet auf: Technikphase 11`, deine Stellungnahme dort nennt „Technikphase 11 (Item fliegen,
Plan 11)“. So steht 9340 in der Technikphase 10 nicht im Fortschritt
([Fortschritt](../../prozess/ablauf/fortschritt.md), Technik 3 je wartendem Anliegen), und
niemand schreibt das *Datenblatt* `Canoptek Spyder` mit `fliegen` und die Spinne in der
*Armee* der Necrons. Dann hat [BEW-18](../../domaene/anforderungen/phasen/bewegung/fliegen.md)
keine *Einheit* mit *Fliegen*, und die Etappe („Canoptek-Spinne mit Fliegen“) schließt nicht
mit Zyklus 10.

**Kosten.** Eine Kopfzeile in 9340. Bleibt sie, fehlt die Spinne am Bildschirm, und ihr Teil
rückt in Zyklus 11, obwohl der Stakeholder ihn für Zyklus 10 gewählt hat (10160 F1 B).

**Gegenvorschlag.** In 9340 `Wartet auf: Technikphase 10`; dann nennt dich der Fortschritt
der Technikphase 10, und du schreibst das *Datenblatt* zum Start von Item fliegen, wie der
Plan sagt.

**Stellungnahme.** Umgesetzt: [9340](9340-fliegenDerSpinne.md) trägt
`Wartet auf: Technikphase 10`, seine Stellungnahme nennt den Start des Items fliegen in
Plan 10. Vor den Daten müssen die Fixtures eine dritte *Einheit* vertragen, sonst bricht
fast jeder Akzeptanztest ab; die Reihenfolge erbitte ich vom Planer in
[10340](10340-dritteEinheitBrichtFixtures.md).
