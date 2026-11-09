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

**Stellungnahme.** In Arbeit, Status bleibt offen; Lauf 2 endete an der Belegungsgrenze.
Mutanten einzeln in `/tmp/mutlab` geprüft (`/tmp/mutwerk.py`).
- Fangen jetzt: `anhaltenAnDerBewegungsweite.py` 29 (BEW-25.1, 1″ zurück nach Osten, Süden),
  `anhaltenVorFremdenBases.py` 61 (BEW-8.3, nach Anhalten auf dem Weg ohne Grenze kein
  Angebot), `fliegen.py` 76 (BEW-18.7, Warboss hinter und neben dem Punkt).
- Test fehlt, Entwurf steht: BEW-18.2 an jeder *Spielfeldkante* (`fliegen.py` 114, 158, 160,
  161; `messen.py` 262, 266, 267): Overlord und Spinne per Übergehen an die Kante, zwei Züge
  weiter (die Weite zählt ab Beginn der *Bewegungsphase*), Lage je Kante um 90° gedreht, Overlord
  1,6″ von der Linie der Mitten. BEW-18.2 an der *Bewegungsweite*, Warrior 7,5″ schräg,
  gespiegelt (`messen.py` 247, 251, 253, 254).
- Gleichwertig, Einträge an den Regelumsetzer: `frozen` in `messen.py` 24, 31,
  `anhaltenAufDemWeg.py` 15, 21, `normaleBewegung.py` 15, 24, 30, `uebergehenBeimZiehen.py` 11,
  19, `setzen.py` 12; ungenutzte Standardwerte `uebergehenBeimZiehen.py` 16, `spielobjekte.py` 37;
  `fliegen.py` 64 (gelesen wird nur `stellen`); `schlachtrunden.py` 188; `messen.py` 215
  (Schritt 0), 271 (Ecke nie die nächste), 13–15 (innerhalb 1/100″), 247 und 262 `Lt wird LtE`
  (nur bei Berührung), 266, 267 `Add wird Sub` (dieselben Punkte); zu prüfen
  `anhaltenVorFremdenBases.py` 101.
- Lücke im Plan: `schlachtrunden.py` 149 wirkt nur, wenn 18.2 keine *Stelle* findet (BEW-18.6,
  Etappe 7).
- Offen: `fliegen.py` 124; `messen.py` 294, 297, 321–324, 333, 340.
