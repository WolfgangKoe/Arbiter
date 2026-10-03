# Index auf eine Einheit im Test des gemeinsamen Modells

140 · Kritik · von Reviewer (Technik) → Implementierer · Runde 1/3 · angenommen

## Runde 1
Gegenstand: e817638 (Kritik am Code). Tests grün (150), Prüfungen grün (419), `ruff` sauber.
Sonst keine Befunde: Vorbedingung, Meldung, Katalog und `MappingProxyType` sind korrekt und
lesbar.

**Befund.** `technik/tests/einheit/domaene/phasen/aufstellenTest.py:79`:
`modell, *_ = spielerMitEinerEinheit().armee.einheiten[0].modelle`. Das widerspricht
`prozess/praemissen/wir.md`, Regel 6: „Keine Indizes auf Fachobjekte (`einheiten[0]`):
benennen oder entpacken.“

**Kosten.** Klein. Regel 6 prüft nur der Text, der Index fällt keiner Prüfung auf; einmal
geduldet, wird er zum Vorbild für weitere Tests. Die Zeile darüber im selben Modul entpackt
schon: `eigene, *_ = spielerMitEinerEinheit().armee.einheiten`.

**Gegenvorschlag.** Entpacken wie dort:
`einheit, *_ = spielerMitEinerEinheit().armee.einheiten`, dann
`modell, *_ = einheit.modelle`.

Erledigt, wenn die Zeile ohne Index auskommt und `python3 -m pytest technik/tests` grün ist.

**Stellung (Implementierer).** Angenommen und umgesetzt wie vorgeschlagen.
