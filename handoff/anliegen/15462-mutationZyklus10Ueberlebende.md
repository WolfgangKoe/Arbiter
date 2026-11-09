# Mutation Zyklus 10: 67 Überlebende, 82 %

Form: Kritik
Von: Reviewer
An: Testautor
Runde: 1/3
Status: offen

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

**Stellungnahme.** In Arbeit, Status bleibt offen: Der Lauf des Testautors endete an der
Belegungsgrenze vor den Tests. Zwischenstand, Mutanten einzeln gegen `fliegenTest.py` in einer
Kopie geprüft (`/tmp/mutwerk.py`, `/tmp/mutlab`):
- Tests, die fangen sollen (BEW-18.2, Kante parametrisiert über alle vier *Spielfeldkanten*):
  `fliegen.py` 114, 158, 160, 161; `messen.py` 262 (`< 1`), 266/267 (`1 wird 2`) und 247 (`< 1`),
  251–254 mit Mitten, die nicht achsparallel liegen, und gespiegelt (die heutigen Tests liegen auf
  einer Achse, darum überleben sie). BEW-18.7: `fliegen.py` 76, wenn der Warboss neben dem Punkt
  steht (in *Nahkampfreichweite* am Punkt, nicht beim doppelten Weg). BEW-25.1: 
  `anhaltenAnDerBewegungsweite.py` 29 mit genau 1″ zurück in x und in y. BEW-8: 
  `anhaltenVorFremdenBases.py` 61 (nach Anhalten auf dem Weg kein Angebot ohne Grenze).
- Gleichwertig, Einträge an den Regelumsetzer (Schreibpfad `prozess/pruefungen/`): `frozen` in
  `messen.py` 24, 31, `anhaltenAufDemWeg.py` 15, 21, `normaleBewegung.py` 15, 24, 30,
  `uebergehenBeimZiehen.py` 11, 19, `setzen.py` 12; Standardwerte, die kein Aufrufer nutzt:
  `uebergehenBeimZiehen.py` 16, `spielobjekte.py` 37 (zu prüfen); `fliegen.py` 64 (die Schlacht
  liest nach dem Loslassen nur `stellen`); `schlachtrunden.py` 188 (ohne Stellen wertet kein
  Aufrufer `angehaltenAufDemWeg` aus); `messen.py` 215 (bei Schritt 0 ist das Ergebnis in beiden
  Fällen 0), 271 (für eine *Stelle* im *Spielfeld* ist eine Ecke nie die nächste); 13–15
  (innerhalb der Zusage „höchstens 1/100″ weiter“); `anhaltenAufDemWeg`/`anhaltenVorFremdenBases.py`
  101 (zu prüfen: Kante auf schon gekürztem Weg).
- Lücke ohne Test im Plan: `schlachtrunden.py` 149 (`raise`) wirkt nur, wenn 18.2 keine *Stelle*
  findet, das ist BEW-18.6 (Etappe 7).
- Offen: `fliegen.py` 124; `messen.py` 294, 297, 321–324, 333, 340.
