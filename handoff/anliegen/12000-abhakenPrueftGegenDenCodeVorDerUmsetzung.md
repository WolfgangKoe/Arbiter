# Abhaken prüft die Tests gegen den Code vor der Umsetzung

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Hält auf nach [Kritik](../../prozess/ablauf/kritik.md) (Hindernis
[11940](11940-hindernisKritikAnDenTestsZuItemLoslassen.md)): `grüneTests` in
[testsRot.py](../../prozess/pruefungen/standregeln/testsRot.py) lässt die Tests des Items im
Arbeitsbaum laufen. Nach [Technikphase 2](../../prozess/ablauf/technikphase.md) („der Rest
läuft weiter“) arbeitet dort der Implementierer schon am Code des Items. Sein Code macht 13
Tests zu AUF-28.1 und BEW-20.1 grün, und `grünVorDemCode` lehnt die Kritik des Architekten
ab, obwohl die Tests vor dem Code rot sind. Bestehende Regel ([Ich 4](../../prozess/praemissen/ich.md)):
[Standregeln, Zeile Retro 9 P1](../../prozess/regeln/standregeln.md); sie wird angepasst,
eine neue Regel entsteht nicht.

**Kosten.** Solange es bleibt, kann kein Kritiker die Tests eines Items abhaken, während
dessen Umsetzung läuft oder committet ist. Die Phase steht.

**Gegenvorschlag.** `grüneTests` prüft in einer Kopie in `/tmp`: Alles kommt aus dem
Arbeitsbaum (ohne `.git`, `.venv`, `node_modules`, `Arbiter-old`, `ArbiterMap`), nur
`technik/arbiter` und `technik/frontend` kommen aus dem Stand vor der Umsetzung
(`git archive <stand> technik/arbiter technik/frontend`). Dieser Stand ist `HEAD`. Steht in
`HEAD:handoff/plan.md` schon `- [x] Implementierer: Tests zu Item <k> grün`, ist es der
Vorgänger des jüngsten Commits, der diese Zeile hinzugefügt hat (`git log -S`). Die Zeile
Retro 9 P1 sagt dann „grün gegen den Code vor der Umsetzung“. Dazu kommt ein Scheiter-Test
in `abhakenTest.py`: Ein uncommitteter Produktcode, der einen Test grün macht, meldet kein
Hindernis.

Probe in `/tmp/probe11940` (`vorDemCode.py`, Ausgabe in `ergebnis.txt`):
- a, Arbeitsbaum jetzt, Stand `HEAD`: 7 von 39 grün. Es sind die sechs zu AUF-16.8 und
  `testAuf28_1DerDienstSetztAmPunktDerLetztenStelleWieDasBeispielImVertrag`; die beseitigten
  Hindernisse 11441 und 11260 nennen sie schon, Abhaken ginge durch.
- b, ein Klon mit dem Code des Implementierers, committet und mit Haken, Stand `<Commit>^`:
  dieselben 7 grün.
- c, bisher, derselbe Klon im Arbeitsbaum: 39 von 39 grün, Abhaken lehnt ab.

Der Server startet in der Kopie mit der `.venv` des Projekts (`sys.executable`).

Die Laufzeit bleibt bei rund 2,5 Minuten für dieses Item, dazu kommt die Kopie mit 24 MB.
Nicht erprobt ist, ob danach alle Rollen arbeiten und committen. Das gehört zur Umsetzung.
Rückweg: Revert deines Commits; `grüneTests` läuft dann wieder im Arbeitsbaum.

**Stellungnahme.** Angenommen und umgesetzt wie vorgeschlagen:
[standVorDerUmsetzung.py](../../prozess/pruefungen/standregeln/standVorDerUmsetzung.py) baut die
Kopie, `grüneTests` in [testsRot.py](../../prozess/pruefungen/standregeln/testsRot.py) läuft
darin. Fehlt ein Produktordner im Stand, wird er weggelassen. Scheiter-Tests in
[abhakenTest.py](../../prozess/pruefungen/standregeln/abhakenTest.py): uncommitteter und
committeter Produktcode (mit Haken des Implementierers) macht nichts grün. Zeile in
[Standregeln](../../prozess/regeln/standregeln.md) angepasst. Rückweg: Revert des Commits.
