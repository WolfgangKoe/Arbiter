# Gleichwertige Mutanten aus Zyklus 10 fehlen in gleichwertig.json

Form: Kritik
Von: Testautor
An: Regelumsetzer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Aus [15462](15462-mutationZyklus10Ueberlebende.md) bleiben Überlebende, die kein
Test fangen kann, weil sie nichts ändern, was ein Kriterium zusagt. In
[gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json) fehlen sie;
ohne sie bleibt der gezielte Lauf unter 95 %. Je Zeile: Datei, `bereich`, Fehler, Grund.
- `messen.py`, `Kreisrand` 24 und `Geradenrand` 31, `True wird False`;
  `anhaltenAufDemWeg.py` 15, 21; `normaleBewegung.py` 15, 24, 30;
  `uebergehenBeimZiehen.py` 11, 19; `querschnitt/setzen.py` 12 (jeweils die Klasse mit
  `@dataclass(frozen=True)`): kein Code ändert ein Feld nach dem Bau.
- `uebergehenBeimZiehen.py` 16, `spielobjekte.py` 37, `False wird True`: Standardwert, den
  jeder Aufrufer setzt.
- `fliegen.py` 64 (`Fliegen.nachDemLoslassen`) und `anhaltenVorFremdenBases.py` 101
  (`übergangen`), `False wird True`: gelesen wird nur `stellen`; in 101 ist `kurz` schon an der
  *Spielfeldkante* gekürzt, `anteilBisZurSpielfeldkante` gibt darauf 1.
- `schlachtrunden.py` 188, `False wird True`: bitte vom Implementierer begründen lassen; mein
  Stand aus Runde 1 von 15462.
- `messen.py`, `wegInDieFreieFläche`, `_umDenKandidaten`: 13–15 (Konstanten), 321 `2 wird 3`,
  323, 324 `Add wird Sub`: Die Suche um einen Kandidaten liegt immer innerhalb 1/250″ von ihm;
  323 und 324 spiegeln die 16 Richtungen auf dieselbe Menge, 321 und 13–15 ändern Punkte nur
  innerhalb der 1/100″, die BEW-18.2 erlaubt.
- `messen.py`, `anteilVorDerLetztenBerührung` 215 (`0 wird 1`, `GtE wird Gt`): Schritt 0 ist
  der Anfang, an dem kein Modell eine *Base* berührt.
- `messen.py`, `_kreisMitKreis` 247 und `_kreisMitGerade` 262 `Lt wird LtE`: ändert nur den
  Fall der bloßen Berührung (Wurzel aus 0, derselbe Punkt); 266, 267 `Add wird Sub`: tauscht die
  zwei Punkte; `_geradeMitGerade` 271 `Eq wird NotEq`: Die Ecke zweier *Geradenränder* ist nie
  die nächste freie *Stelle*, der Lotpunkt der näheren Gerade ist näher.
- `messen.py`, `_zulässig` 294 (`LtE wird Lt`, `GtE wird Gt`), 297 (`GtE wird Gt`),
  `wegInDieFreieFläche` 333, 340 (`LtE wird Lt`): unterscheiden sich nur bei Gleichheit von
  Gleitkommazahlen genau an der Toleranz von 1e-6.
- `messen.py`, `wegInDieFreieFläche` 340 `And wird Or`: `frei` prüft jeden Weg zuletzt; ein
  unzulässiger Kandidat liefert höchstens eine freie *Stelle* innerhalb 1/250″ von ihm, also
  innerhalb der 1/100″ von BEW-18.2; Kandidaten jenseits der Reichweite kommen nur zum Zug, wenn
  keiner in ihr frei ist (BEW-18.6, Etappe 7).

**Kosten.** Ohne die Einträge hält die DoD über das Inkrement nicht; Review 10 bleibt gesperrt.

**Gegenvorschlag.** Je Mutant ein Eintrag mit `datei`, `bereich`, `quelle`, `fehler` und dem
Grund oben; dann den gezielten Lauf
`.venv/bin/python prozess/pruefungen/gemeinsam/lauf.py mutationsregeln.mutation`. Bleibt
`schlachtrunden.py` 149 (`raise` entfällt, wirkt nur bei BEW-18.6, Etappe 7) darunter, gehört
es als Lücke im Plan an den Koordinator.

**Stellungnahme.** Meine Schreibgrenze erlaubt `gleichwertig.json`. 38 Einträge ergänzt.
Ausgenommen:
- `schlachtrunden.py` 188: nicht gleichwertig, `darstellung.stellenBeimLoslassen` gibt das
  Feld in die Antwort; ein Test darauf fängt ihn (Testautor).
- `schlachtrunden.py` 149: Lücke im Plan (BEW-18.6, Etappe 7), an den Koordinator.
- 247/262 `0 wird 1`, 266/267 `1 wird 2`: fängt laut 15462 jetzt der Test.
`pytest prozess/pruefungen/mutationsregeln` grün; gezielter Lauf nicht gestartet.

**Nachprüfung (Testautor).** Die 38 Einträge decken meine Liste aus dem Befund, je mit `bereich`
und Grund. `schlachtrunden.py` 188 fängt jetzt
`testBew10_1BeimZiehenZeigtDasSpielfeldKeinModellDesAnderenSpielersBewegtOderAngehalten` in
[fremdeModelleTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fremdeModelleTest.py),
geprüft an einer Kopie ([15462](15462-mutationZyklus10Ueberlebende.md)).
