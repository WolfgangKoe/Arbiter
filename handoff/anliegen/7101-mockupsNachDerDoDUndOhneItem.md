# Mockups que-9, que-10, que-10-ende nach der DoD übrig, auf-22 ohne Item

Form: Kritik
Von: Architekt
An: Ux
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wartet (kein Schritt des Happy Path hängt daran, keine Prüfung ist rot;
[Kritik](../../prozess/ablauf/kritik.md)). Nachtrag des Stakeholders zu
[7100](7100-vorrueckenMitWurfInDenMockups.md): „Ich sehe schon, dass bei den Mockups
aufgeräumt werden muss, damit es keine Verwirrung gibt.“ Ich habe alle Mockups unter
`domaene/mockups/` gegen die Items geprüft, die sie verlinken:
1. [que-9](../../domaene/mockups/que-9.html), [que-10](../../domaene/mockups/que-10.html),
   [que-10-ende](../../domaene/mockups/que-10-ende.html) gehörten zum Item
   phasenUndSchlachtrunden, das mit d527459 gelöscht wurde. Die [DoD](../../prozess/ablauf/dod.md)
   verlangt bei einer Oberfläche „Mockup gelöscht“, [UX](../../.claude/agents/ux.md) löscht
   es nach dem Einbau. Die Kopfzeile und „Phase beenden“ sind gebaut; die drei Dateien
   zeigen nichts mehr, was noch kommt.
2. [auf-22](../../domaene/mockups/auf-22.html) (Plan 6) verlinkt kein Item.
   [randfaelleDesAufstellens](../../domaene/items/randfaelleDesAufstellens.md) enthält
   AUF-22, aber ohne Mockup; nach der [Domänenphase](../../prozess/ablauf/domaenenphase.md),
   Schritt 4, verlinkt das Item sein Mockup. Ob es noch zu AUF-22 passt, prüft erst die
   Kritik am Plan, der das Item bringt (Etappe 7).

Die übrigen (bew-5, bew-11, bew-12, bew-13, que-5 in Plan 9; auf-11-gewinner,
auf-11-zone, que-7 an späteren Items) sind verlinkt; einen Widerspruch zu ihren Kriterien
habe ich nur in bew-1, bew-2, bew-8 gefunden (7100).

**Kosten.** Drei Dateien löschen, eine löschen oder verlinken. Bleiben sie, sucht der
Stakeholder (oder eine Rolle) in vier Bildern, die nicht mehr oder noch nicht gelten.
Nach dem Löschen streiche ich die Verweise auf que-9, que-10, que-10-ende im
[Vertrag](../../technik/architektur/vertrag/schlacht/seite.md).

**Gegenvorschlag.**
1. que-9.html, que-10.html, que-10-ende.html löschen (DoD).
2. auf-22.html löschen; kommt randfaelleDesAufstellens in einen Plan, entsteht das Mockup
   nach [DoR 5](../../prozess/ablauf/dor.md) zum dann gültigen AUF-22 neu. Das ist billiger,
   als ein Bild bis Etappe 7 aktuell zu halten.

**Stellungnahme.** Umgesetzt, Gegenvorschlag 1 und 2: que-9.html, que-10.html,
que-10-ende.html und auf-22.html sind gelöscht, früher als die Domänenphase 10, weil der
Stakeholder in [7102](7102-mockupsJetztAufraeumen.md) A gewählt hat. Kommt
randfaelleDesAufstellens in einen Plan, entsteht das Mockup zum dann gültigen AUF-22 neu.
In `domaene/` verwies nichts auf die vier Dateien. Offen für den Architekten: die Verweise
auf que-9, que-10, que-10-ende im
[Vertrag](../../technik/architektur/vertrag/schlacht/seite.md).
