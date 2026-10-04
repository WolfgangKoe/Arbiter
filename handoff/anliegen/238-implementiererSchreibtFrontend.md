# Der Implementierer schreibt auch technik/frontend/

238 · Anliegen · von Organisationsentwickler → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Der Architekt meldet in [233](233-frontendOhneAutor.md): Keine Rolle darf
`technik/frontend/` schreiben, `schreibgrenze.py` sperrt dort jede Datei. Plan 3 bringt aber
die erste Oberfläche, und nach [Ablauf](../../prozess/ablauf.md#technikphase) Schritt 3
übernimmt der Implementierer Markup und CSS der Mockups (Anliegen 151). Ein Recht zu ändern
ist deine Entscheidung.

**Kosten.** Ohne Änderung bleibt der Implementierer beim ersten roten Bildschirmtest stehen,
oder er legt die Seite nach `technik/arbiter/web/` und verwischt die Trennung von Frontend
und Backend aus [153](153-frontendBackendUndDatenbank.md).

**Gegenvorschlag.** Siehe F1.

**F1 · Wer schreibt `technik/frontend/`?**
- A: Der Implementierer, zusätzlich zu `technik/arbiter/` und `technik/tests/einheit/`.
  Der Auslöser für einen eigenen Frontend-Implementierer
  ([Rollen mit Auslöser](../../prozess/ablauf.md#rollen-mit-auslöser)) bleibt, wie er ist.
- B: Schon jetzt ein eigener Frontend-Implementierer.
Empfehlung: A. Eine Rolle entsteht erst bei beobachtetem Bedarf; der Auslöser für B
(wiederholt umgeschriebene Mockups) ist noch nie eingetreten, und ein Inkrement aus
`web/` und Seite bliebe bei einer Rolle. Umgesetzt wird nach der Freigabe von Plan 3,
vor dem ersten Lauf des Implementierers: `schreibpfade` in
`.claude/agents/implementierer.md`, dazu ein Satz unter „Was du tust“. Erledigt, wenn
`schreibgrenze.py` dem Implementierer eine Datei unter `technik/frontend/` erlaubt.
Antwort: .

**Stellungnahme.**
