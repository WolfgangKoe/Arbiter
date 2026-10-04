# Niemand darf technik/frontend/ schreiben

233 · Kritik · von Architekt (Technik) → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
**Befund.** [Plan 3](../plan.md) bringt die erste Oberfläche. Ihr Ort ist nach
[architektur.md](../../technik/architektur.md) (Schichten) `technik/frontend/`: HTML, CSS und
JavaScript, getrennt von `technik/arbiter/web/` (Aufbau aus
[153](153-frontendBackendUndDatenbank.md)). Keine Rolle hat diesen Pfad in `schreibpfade`:
Der Implementierer schreibt `technik/arbiter/` und `technik/tests/einheit/`, der Testautor
`technik/tests/akzeptanz/`, ich nur die Architektur. `schreibgrenze.py` liest
`schreibpfade` und sperrt damit jede Datei unter `technik/frontend/`, also auch die
Komponentenseite und das übernommene Markup der Mockups (Anliegen 151).

**Kosten.** Ohne Änderung bleibt der Implementierer beim ersten roten Bildschirmtest stehen:
Er darf `web/` bauen, aber nicht die Seite, die es ausliefert. Der Ausweg, das Frontend nach
`technik/arbiter/web/` zu legen, verwischt die Trennung, die der Stakeholder verlangt hat
(Beispiel ArbiterMap: `routes/map.py` füllt Vorlagen, 40.000 Zeichen).

**Gegenvorschlag.** `technik/frontend/` in die `schreibpfade` des Implementierers, vor dem
ersten Lauf des Implementierers in Zyklus 3. Der Auslöser für einen eigenen
Frontend-Implementierer (Ablauf, Rollen mit Auslöser) bleibt, wie er ist. Erledigt, wenn
`schreibgrenze.py` dem Implementierer eine Datei unter `technik/frontend/` erlaubt.

**Stellungnahme.** Berechtigt, Gegenvorschlag übernommen; der Stakeholder hat mit der
Freigabe von Plan 3 Antwort A gegeben (Anliegen 238, git). Umgesetzt:
`.claude/agents/implementierer.md` hat `technik/frontend/` in `schreibpfade` und einen Satz
unter „Was du tust“; `schreibgrenze.py` erlaubt ihm damit `technik/frontend/komponenten.html`,
dem Testautor nicht. In [Kritik am Code](../../prozess/ablauf.md#kritik-am-code) prüft der
Reviewer den Pfad; den Mechanismus dafür baut der Regelumsetzer
([240](240-codekritikFuerFrontend.md)).
