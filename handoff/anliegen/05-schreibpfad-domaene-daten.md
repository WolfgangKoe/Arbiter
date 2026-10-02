# Schreibpfad für `domaene/daten/` fehlt

05 · Kritik · von Planer (Domäne) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** Etappe 1 verlangt eine feste Ausgangslage als Datei in `domaene/daten/`, die auch
den Akzeptanztests als Ausgangsstand dient (Anliegen 01); dazu kommen die vorgezogenen
Katalogeinheiten mit deutschen Schlüsseln. Keine Rolle in `.claude/agents/` hat
`domaene/daten/` in ihren `schreibpfade`; die Schreibgrenze sperrt die Datei.

**Kosten.** Ohne Schreibpfad bleibt Etappe 1 nach der Domänenphase ohne Ausgangsstand; die
Testautoren der Technikphase hätten keine gemeinsame Quelle.

**Gegenvorschlag.** `domaene/daten/` in die `schreibpfade` des Anforderungsautors: Katalogwerte
sind Regelfakten mit Fundstelle, die Ausgangslage folgt den Kriterien der Etappe.

**Stellungnahme.**
