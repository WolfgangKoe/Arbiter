# Glossar: Grund nennt entfernten Code

Form: Kritik
Von: Reviewer
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [Glossar](../../domaene/glossar.md), Zeile *Grund*: In der Spalte Code steht
`Grund (überEineBase)`, die Definition sagt „‚über eine Base‘ nennt Arbiter bis zum Item
anhaltenAufDemWeg“. Mit diesem Item ist `Grund.überEineBase` aus `domaene/sperre.py`
entfernt (BEW-17 ersetzt die Sperre).

**Kosten.** Glossar → Code stimmt nicht mehr (DoD 2, [Wir 2](../../prozess/praemissen/wir.md));
„bis zum Item“ ist Historie in der Datei ([Wir 4](../../prozess/praemissen/wir.md)).

**Gegenvorschlag.** Als Beispiel im Code einen bestehenden *Grund* nennen, etwa
`Grund (baseÜberdeckt)`, und den Satz über ‚über eine Base‘ streichen.

**Stellungnahme.** Angenommen wie vorgeschlagen. [Glossar](../../domaene/glossar.md), Zeile
*Grund*: Code jetzt `Grund (baseÜberdeckt)` (steht in `technik/arbiter/domaene/sperre.py`),
der Satz über ‚über eine Base‘ samt seinen Fundstellen ist gestrichen.
`formregeln.glossar` grün. Dieselbe Änderung beantwortet [12042](12042-glossarBeispielUeberEineBase.md).
