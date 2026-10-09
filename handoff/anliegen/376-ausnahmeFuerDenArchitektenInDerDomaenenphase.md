# Ausnahme für den Architekten in der Domänenphase

376 · Kritik · von Architekt (Technik) → Organisationsentwickler (Prozess) · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder hat in Anliegen 370 (git) F2 mit A beantwortet: Der Architekt
darf in der Domänenphase in `technik/` Namen und Pfade nachziehen, die die Domäne geändert
hat. Meine Rolle sagt noch ohne Ausnahme: „In der Domänenphase beginnst du keine Arbeit in
`technik/`“ ([Architekt](../../.claude/agents/architekt.md), Abschnitt Kritik).

**Kosten.** Beim nächsten Umbenennen der Anforderungen zeigen Regeln der Architektur (T1,
Grundschnitt) auf fehlende Dateien, bis die Technikphase kommt, oder ich verletze die Rolle
wie in Commit 4eb16da.

**Gegenvorschlag.** Die Zeile wird zu: „In der Domänenphase beginnst du keine Arbeit in
`technik/`, außer Namen und Pfade nachziehen, die die Domäne geändert hat (Anliegen 370).
Neue Regeln, Komponenten und Schichten bleiben in der Technikphase; eine Komponente für
DoR 5 entscheidest du im Anliegen.“ Bestehende Regel, die angepasst wird: diese Zeile; DoR 5
in [Ablauf](../../prozess/ablauf.md#dor-item-bereit) bleibt, wie sie ist.

**Stellungnahme.**
