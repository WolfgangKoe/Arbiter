# Mutation Zyklus 10: 67 Überlebende, 82 %

Form: Kritik
Von: Reviewer
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Der gezielte Lauf über die seit Commit „Freigabe Plan 10“ geänderten Zeilen der
Domänenmodule: 374 Mutanten, 82 % gefangen, Schwelle 95 % ([DoD](../../prozess/ablauf/dod.md),
Mutationsschwelle). Die Überlebenden, je Modul (Zeilen; Protokoll `/tmp/mutation10.log`):
- `messen.py`, 38: 13–15 (Konstanten von `wegInDieFreieFläche`: `_nenner`,
  `_abständeUmDenKandidaten`, `_richtungenUmDenKandidaten`), 24 und 31 (`frozen`), 215
  (`while schritt >= 0`), 247–271 (`_kreisMitKreis`, `_kreisMitGerade`, `_geradeMitGerade`),
  294, 297 (`_zulässig`), 321–324 (`_umDenKandidaten`), 333, 340 (`wegInDieFreieFläche`).
- `fliegen.py`, 12: 64, 76, 114, 124, 158, 160, 161.
- `anhaltenVorFremdenBases.py` 61, 101; `normaleBewegung.py` 15, 24, 30;
  `uebergehenBeimZiehen.py` 11, 16, 19; `anhaltenAnDerBewegungsweite.py` 29;
  `anhaltenAufDemWeg.py` 15, 21; `schlachtrunden.py` 149 (`raise` entfällt), 188;
  `setzen.py` 12; `spielobjekte.py` 37.
Viele `True wird False` stehen in `@dataclass(frozen=True)`; die sind wohl gleichwertig.

**Kosten.** Ohne Nachbessern hält die DoD über das Inkrement nicht, Review 10 ist nicht
freizugeben. Die Geometrie in `messen.py` (`wegInDieFreieFläche`, das Rücken an die nächste freie *Stelle*)
ist am Bildschirm am schwersten zu sehen; ein Fehler darin setzt ein *Modell* auf eine
falsche *Stelle*.

**Gegenvorschlag.** Je Überlebenden ein Test, der ihn fängt, oder eine Begründung in
[gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json) mit `bereich`;
Tests sagen kein Verhalten außerhalb einer Vorbedingung zu (Anliegen 1751). Erledigt, wenn
`.venv/bin/python prozess/pruefungen/gemeinsam/lauf.py mutationsregeln.mutation` 95 % meldet.

**Stellungnahme.** Umgesetzt; Anliegen 15680 ist erledigt
(38 Einträge in `gleichwertig.json`). Mutanten einzeln in einer Kopie geprüft, kein voller Lauf.
- `schlachtrunden.py` 188 (`False wird True`) ist nicht gleichwertig: Zieht jemand ein *Modell*
  des anderen *Spielers*, zeigt das *Spielfeld* nach BEW-10.1 keines bewegt, also hat AUF-29
  nichts angehalten (*gezeigt*, Glossar). Neu in
  [fremdeModelleTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fremdeModelleTest.py):
  `testBew10_1BeimZiehenZeigtDasSpielfeldKeinModellDesAnderenSpielersBewegtOderAngehalten`, für
  beide *Spieler* am Zug; fängt 188, ohne ihn überlebt 188.
- Offen beim Koordinator: `schlachtrunden.py` 149, Lücke im Plan (BEW-18.6, Etappe 7).
- Fangen jetzt: `anhaltenAnDerBewegungsweite.py` 29 (BEW-25.1), `anhaltenVorFremdenBases.py`
  61 (BEW-8.3), `fliegen.py` 76 (BEW-18.7); neu in
  [fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py): BEW-18.2 an
  jeder *Spielfeldkante*, die Spinne vor dem Overlord rückt entlang der Kante und innen am
  Overlord von ihr weg (`fliegen.py` 114, 124, 158, 160, 161; `messen.py` 262, 266, 267 `1 wird
  2`), BEW-18.2 schräg an der *Bewegungsweite*, nach Nordwesten und Südwesten (`messen.py` 247
  `0 wird 1`, 251, 253, 254).
- Gleichwertig, mit Grund an den Regelumsetzer in 15680: alle übrigen außer
  `schlachtrunden.py` 149, dort auch die Lücke im Plan (BEW-18.6, Etappe 7).
