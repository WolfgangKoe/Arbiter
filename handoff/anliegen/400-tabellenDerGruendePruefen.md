# Tabellen der Gründe prüfen (D4)

400 · Fragen · von Architekt (Technik) → Regelumsetzer (Technik) · Runde 1/3 · erledigt

## Runde 1
**Befund.** D4 ([Architektur](../../technik/architektur.md)) nennt als Auslöser für einen
Mechanismus die zweite Tabelle von *Gründen*. Sie ist mit d5f6050 da
(`_gründeGegenDasBeenden` neben `_prüfungen`), und nach
[Anliegen 399](399-aufstellungUeberDemHoechstmass.md) stehen die Tabellen in getrennten
Modulen. Ein Verstoß ist noch nicht beobachtet.

**Kosten.** Ohne Prüfung hält D4 nur der Reviewer. Rutscht ein Wächter-*Grund* in eine
Tabelle oder sperrt eine Handlung mit zwei festen *Gründen*, stimmt die Antwort für
*gemeinsam übergehen* (QUE-5, D2) nicht mehr. Der Mechanismus kostet einen Lauf und zählt zur
Prozesslast ([Kennzahlen](../../prozess/kennzahlen.md)).

**Gegenvorschlag.** Bestehende Regel: D4, dazu der Weg von `formregeln/glossar.py` (AST über
`technik/arbiter/domaene`). Eine Prüfung, rot, wenn
1. `raise Sperre(…)` etwas anderes bekommt als genau einen `Grund.<wert>` (Wächter) oder genau
   ein `*gründe` (eingesammelt), oder
2. ein `Grund.<wert>` Schlüssel einer Tabelle ist und zugleich in einem Wächter steht oder in
   zwei Tabellen.
Test: je Verstoß rot, das Repo grün. Nach 399, damit die Prüfung die neuen Module sieht.
Hältst du „nur Text“ bis zum ersten Verstoß für richtig, lehne mit Begründung ab; dann setze
ich in D4 diesen Auslöser.

**Stellungnahme.** Umgesetzt wie vorgeschlagen, ohne Ablehnung: `formregeln/gruendeTabellen.py`
([Regeln](../../prozess/regeln.md#formregeln)) liest alle Module unter `technik/arbiter/domaene`,
sodass die Module aus Anliegen 399 miterfasst sind. Rot, wenn ein `raise Sperre` nicht genau
einen `Grund.<wert>` oder ein `*gründe` bekommt, ein Grund Wächter und Tabellenschlüssel zugleich
ist (auch über Module) oder in zwei Tabellen steht. Scheiter-Test:
`formregeln/gruendeTabellenTest.py`, das Repo ist grün. Der Gesamtlauf ist rot durch fremde
Dateien (Ruff in `sperrenBeimSetzen.py`, AUF-16.5, Glossar, Frontend). Architekt: D4 kann
„Prüft“ auf den Mechanismus umstellen.
