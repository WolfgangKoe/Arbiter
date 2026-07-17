STATUS: NEEDS-APPROVAL

# S161 — Planning-Entwurf

Grundlage: `.claude/tasks/briefing.md` (Stand nach S160), `docs/reference/agent_scopes.md`,
`docs/governance/operating_model.md` (Event 1 §ev1), `docs/goals/backlog.md` (B-109/B-105/
B-119), `docs/handoff/README.md` (Status-Marker-Tabelle), `docs/handoff/S159_planning.md`
(Task 3/Task 4 — B-109-/B-105-Briefe), `tests/docs/test_handoff_hygiene.py`, Ist-Code
`src/uiLayout/diceCompose.py`, `src/gameMechanic/abilityEngine.py`.

**Stakeholder-Korrektur zum Auftrag (Grundannahme dieser Fassung):** Der Retro-Entscheid „M1
übernommen" ist **Input** für die Planung, nicht ihr alleiniger Gegenstand — S161 wird
**ganz normal** entlang der Backlog-Prioritäten aus `briefing.md` geplant. M2 und M3 gelten
durch Nicht-Nennung als **verworfen** (keine offene Frage mehr, keine Rückfrage nötig).

---

## 0. Checkbox-Sync (Pflicht)

Aktive Zieldatei laut Backlog: `docs/goals/ziel7.md`. Tasks 1, 4 und 5 sind reine Prozess-/
Doku-Items, in `ziel7.md` nicht als Checkbox geführt — kein Abgleich nötig. Task 2 (B-109) und
Task 3 (B-105) sind ebenfalls nicht dort dupliziert (leben ausschließlich in `backlog.md`, wie
bereits in `S159_planning.md` §0 festgestellt).

| Item | Backlog-Status | Beleg (diese Session neu verifiziert) | Ergebnis |
|---|---|---|---|
| B-109 | `ToDo` | `always_fail_marker_row_html` (`src/uiLayout/diceCompose.py:444–462`) hat weiterhin `badge = _badge_chip(label or "Auto-fail", color)` — Fallback-String unverändert seit S159-Planung. `unit_wound_auto_fail_label()` (`src/gameMechanic/abilityEngine.py:567–577`) existiert bereits (liest `badge_label or name_en`), der Loader-Guard gegen fehlendes Label fehlt weiterhin. | **kein Stale-Check** — echt offen |
| B-105 | `ToDo` | `grep -rn "go_source_chip" src/` → kein Treffer. `_strength_source_badge_html` (`src/uiLayout/diceHtml.py`) ist weiterhin nicht generalisiert. | **kein Stale-Check** — echt offen |
| B-119 | `ToDo` | Zeile am Ende von `backlog.md` (vor der Legende), keine Prio zugewiesen — Beschreibung („Deny-Quellen-Anzeige … Canoptek Spyder nicht") unverändert seit S160-Aufnahme. | **kein Stale-Check** — echt offen, nur Prio-Position fehlt |

Kein Doku-Drift bei B-109/B-105/B-119 gefunden, bis auf eine veraltete Zeilenangabe in
`backlog_details.md#b-109` (~Zeile 286/425 statt 444) — kosmetisch, wird im Task-2-Commit
mitkorrigiert, kein eigener Task nötig.

**Marker-Bestandsaufnahme (`ls docs/handoff/`):** aktuell keine offenen Handoff-Dateien außer
`README.md` (Referenz), `S159_planning.md` (Brief-Quelle für Task 2/3, bleibt bis beide
abgeschlossen sind) und `Stakeholder_Beobachtungen.md` (`STATUS: STANDING`, dauerhaft). Keine
UI-Verifikations-Handoffs vorhanden, die auf den neuen Marker (Task 1) migriert werden müssten.

---

## 1. Task 1 — Retro-M1: Handoff-Marker `AWAITING-VERIFICATION` (Executor, Sonnet)

### Root Cause (Anlass S160)

UI-Verifikations-Handoffs (Pflicht seit S155, `agent_scopes.md` „UI-Verifikations-Pflicht")
missbrauchten bisher `STATUS: NEEDS-DECISION` für reine Sichtprüfungen — belegt an den zuletzt
gelöschten Dateien `S158_B104_ui_verifikation.md` und `S159_B028b_ui_verifikation.md` (beide
`STATUS: NEEDS-DECISION`, Commits `cf41cc8`/`0eee7a1`). Das ist der exakte Auslöser der
S160-Stakeholder-Verwirrung („was soll ich hier entscheiden?") — eine Sichtprüfung ist keine
Entscheidungsfrage. `NEEDS-DECISION` bleibt echten Entscheidungsfragen vorbehalten (Kanal-Pflicht,
`agent_scopes.md` Zeile 288–289 bleibt unverändert gültig).

### Kanonischer Ort

`docs/handoff/README.md` — dort steht bereits die vollständige Status-Marker-Tabelle
(Zeile 13–31) inkl. Wächter-Referenz auf `tests/docs/test_handoff_hygiene.py`. Kein neuer Ort,
keine Duplikate: `AWAITING-VERIFICATION` wird als **neue Tabellenzeile** ergänzt, exakt wie
`NEEDS-APPROVAL` in einer früheren Session ergänzt wurde.

### Lifecycle-Semantik (neue Tabellenzeile, Formulierungsvorschlag)

| Marker | Bedeutung | Wer handelt als Nächstes |
|---|---|---|
| `STATUS: AWAITING-VERIFICATION` | Ergebnis fertig, aber Render-Code ist nicht von der Coverage erfasst (`CLAUDE.md`) → wartet auf die manuelle Stakeholder-Sichtprüfung des UI-Effekts (DoD Punkt 6). Keine Entscheidungsfrage. | Stakeholder führt den in der Datei genannten Klickpfad aus, trägt Ergebnis ein → Koordinator setzt `ANSWERED` (bei Nacharbeit) oder direkt `DONE` (bei reiner Bestätigung) und löscht im selben Abschluss (bestehende ANSWERED/DONE-Konvention, keine neue Lösch-Regel nötig) |

- **Gesetzt:** vom Executor beim Anlegen der UI-Verifikations-Handoff-Datei (Pflicht seit S155,
  Template-Felder Voraussetzungen/Klickpfad/Erwartung bleiben unverändert) — ersetzt die
  bisherige Fehlnutzung von `NEEDS-DECISION` für diesen Fall.
- **Aufgelöst:** Stakeholder trägt sein Prüfergebnis in dieselbe Datei ein (Bestätigung oder
  Befund) → Koordinator wandelt genau wie beim bestehenden `NEEDS-DECISION`→`ANSWERED`-Pattern
  um, kein neuer Übergangsmechanismus.
- **Wer löscht:** wer den Folgemarker (`ANSWERED`/`DONE`) setzt, löscht im selben Schritt —
  identische Regel wie für alle anderen Durchgangs-Marker (README Zeile 19/22).
- **Nicht stale-pflichtig wie `DONE`/`ANSWERED`:** `AWAITING-VERIFICATION` darf über Sessions
  hinweg liegen bleiben (wartet auf den Stakeholder, analog `NEEDS-DECISION`) — nicht in
  `_STALE_MARKERS` aufnehmen.

### Hygiene-Test-Nachzug

`tests/docs/test_handoff_hygiene.py`:
- `_VALID_MARKERS`-Tupel (Zeile 18–28) um `"AWAITING-VERIFICATION"` erweitern, mit Kommentar
  nach demselben Muster wie `NEEDS-APPROVAL`/`STANDING` (kurze Begründung + Anlass „Retro-M1,
  S160/S161").
- **Nicht** in `_STALE_MARKERS` (Zeile 54) aufnehmen — sonst würde der Wächter jede offene
  Verifikation fälschlich als „liegen geblieben" markieren.
- Neue Regressionstests (Stil wie bestehende Datei — direkte Assertions auf Modul-Konstanten,
  kein neues Fixture-Setup nötig):
  - `test_awaiting_verification_is_a_valid_marker` — `"AWAITING-VERIFICATION" in _VALID_MARKERS`.
  - `test_awaiting_verification_is_not_treated_as_stale` — `"AWAITING-VERIFICATION" not in
    _STALE_MARKERS`.

### Begleit-Korrekturen in `agent_scopes.md` (selbe Ursache, sonst bleibt die Verwechslung bestehen)

1. **Selbstprüf-Checkliste** (Zeile 200–202): Aufzählung `` `STATUS: NEEDS-DECISION|ANSWERED|DONE` ``
   um `AWAITING-VERIFICATION` erweitern.
2. **UI-Verifikations-Pflicht-Bullet** (Zeile 173–182): Satz ergänzen, der `AWAITING-VERIFICATION`
   für diese Handoff-Art explizit vorschreibt (statt `NEEDS-DECISION`).

**Betroffene Dateien:** `docs/handoff/README.md`, `tests/docs/test_handoff_hygiene.py`,
`docs/reference/agent_scopes.md`.

**Testansatz:** `pytest tests/docs/ --no-cov -q` (neue Tests grün, bestehende unverändert grün),
Vollsuite am Ende (Standard-Gate-Netz).

**Akzeptanzkriterien:** neue UI-Verifikations-Handoffs nutzen künftig `AWAITING-VERIFICATION`
statt `NEEDS-DECISION`; Wächter akzeptiert den Marker, stuft ihn nicht als stale ein;
Selbstprüf-Checkliste nennt ihn korrekt.

**Token-Budget:** ~10k (S), Selbst-Stopp bei ~15k. **Tier:** Sonnet — reine Doku-/Test-Erweiterung,
kein Produktivcode/UI-Render-Pfad betroffen.

---

## 2. Task 2 — B-109: Auto-Fail-Badge-Label verpflichtend aus YAML (Executor, Sonnet)

Vollständiger Brief bereits vorhanden in `docs/handoff/S159_planning.md` Task 3 (Zeile 201–221) —
hier referenziert, nicht neu ausgeplant.

- **Scope:** `label or "Auto-fail"`-Fallback in `always_fail_marker_row_html`
  (`diceCompose.py:462` — Zeile bei Umsetzung neu verifizieren, S159-Brief nannte 425) entfernen;
  Loader-Guard für fehlendes `badge_label`/`name_en` bei `wound_auto_fail`-Effekten einführen
  (Ladefehler statt stillem Fallback, nennt Fraktion+Ability-ID).
- **Betroffene Dateien:** `src/uiLayout/diceCompose.py` (`always_fail_marker_row_html`),
  `src/gameMechanic/abilityEngine.py` (`unit_wound_auto_fail_label`), `src/gameObjects/loader.py`
  (neuer Guard), `tests/gameObjects/test_loader.py`, `tests/uiLayout/test_dice_html.py`;
  zusätzlich `docs/goals/backlog_details.md#b-109` (Zeilenangabe 286→444 korrigieren, siehe §0).
- **Testansatz:** Unit-Test für den Loader-Guard (fehlendes Label → Ladefehler), Regressionstest,
  dass bestehende `wound_auto_fail`-Effekte (Quantum Shielding) weiter laden. Kein manueller
  UI-Verifikationspunkt nötig (reine Guard-/Fallback-Logik, keine neue Optik).
- **Akzeptanzkriterien:** kein stiller Fallback mehr möglich, Ladefehler ist aussagekräftig.

**Token-Budget:** ~10–15k (S), Selbst-Stopp bei ~20k. **Tier:** Sonnet.

---

## 3. Task 3 — B-105 Variante A: generischer GO-Quellen-Chip (Executor, Sonnet)

Vollständiger Brief bereits vorhanden in `docs/handoff/S159_planning.md` Task 4 (Zeile 224–257) —
hier referenziert, nicht neu ausgeplant. Deckt den Stakeholder-Wunsch „Badge am
Quantum-Deflection-Rettungswurf".

- **Scope:** Nach Task 2 (gleiche Datei-Nachbarschaft `diceCompose.py`/`diceHtml.py`, sequenziell
  wegen Datei-Overlap). `_strength_source_badge_html` (diceHtml.py) zu
  `go_source_chip(label, color)` in `diceCompose.py` generalisieren — Farbe über
  `_modifier_color`/`color_hint` statt hart `_BUFF_COLOR_HEX`. Aufrufstellen: (a) bestehender
  Strength-Buff-Call (Rewire, keine Verhaltensänderung), (b) neu: Invuln-Row in
  `_render_dice_save_block` — GO-Name neben `Inv N+`, sofern der Ability-Badge-Label-Pfad
  (`ability_badge_label`, analog B-103/B-109-Muster) für Invuln-Quellen existiert; falls nicht,
  als Scope-Erweiterung im Bericht melden statt improvisiert zu verdrahten.
- **Wrap-Schutz:** `go_source_chip` nutzt denselben Wrap-fähigen `_badge_chip`-Unterbau — braucht
  mindestens dieselbe `title`-Tooltip-Absicherung wie B-111, damit lange GO-Namen nicht denselben
  Truncation-Bug reproduzieren.
- **Betroffene Dateien:** `src/uiLayout/diceCompose.py` (neue Funktion `go_source_chip`),
  `src/uiLayout/diceHtml.py` (`_render_dice_wound_block` Rewire, `_render_dice_save_block`
  Invuln-Zeile), `tests/uiLayout/test_dice_html.py`.
- **Namenswahl vorab gegen INV-4b-Vokabular prüfen** (`tests/architecture/test_generic_src_vocab.py`).
- **Testansatz:** HTML-Output-Test für `go_source_chip` (Buff-Grün/Debuff-Rot), Test für den neuen
  Invuln-Aufrufer, Regressionstest für den bestehenden Strength-Buff-Aufrufer (bytegleich).
  **Manuelle UI-Verifikation PFLICHT** — eigene Handoff-Datei, jetzt korrekt mit
  `STATUS: AWAITING-VERIFICATION` (Task 1 muss dafür vorher gelandet sein): Necron-Roster mit
  Quantum Deflection, Save-Block zeigt „Inv 4+ [Quantum Deflection]" statt nacktem „Inv 4+".
- **Akzeptanzkriterien:** ein Baustein für beide bisherigen Ad-hoc-Lösungen, Invuln-Lücke aus
  S155-Befund geschlossen, kein zweites visuelles Muster.

**Token-Budget:** ~15–20k (S/M), Selbst-Stopp bei ~28k. **Tier:** Sonnet.
**Abhängigkeit:** Task 1 vor Task 3 landen lassen (Marker-Konvention für den PFLICHT-UI-Verifikations-Handoff).

---

## 4. Task 4 — B-119 priorisieren (Backlog-Hygiene, Executor, Sonnet)

Kein Implementierungs-Task — reine Einordnung in `docs/goals/backlog.md`. B-119 steht aktuell
ohne Prio am Listenende (Zeile 129, „neu am Listenende, ohne Prio" laut `briefing.md`).

**Einordnungsvorschlag:** direkt nach B-028b (Zeile 31) einsortieren — B-119 ist ein direkter
Sub-Befund der B-028b-Testfall-3-Verifikation (Deny-Quellen-Anzeige beim Canoptek Spyder,
`gloom_prism`) und teilt denselben Deny-/GO-Infrastruktur-Kontext. Reihenfolge danach:
B-028b → **B-119** → B-109 → B-105 → B-028c1…c5 (unverändert). Vor der Umsetzung dem
Stakeholder als Teil dieses Plans zur Freigabe vorgelegt (Positionsänderung ist eine reine
Reihenfolge-Frage, kein Entscheidungsmodus `Konsens` nötig).

**Betroffene Dateien:** `docs/goals/backlog.md` (Zeile verschieben).

**Testansatz:** `pytest tests/docs/test_backlog_structure.py --no-cov -q` (Tabellenstruktur bleibt
gültig), Vollsuite am Ende.

**Token-Budget:** ~5k (XS), Selbst-Stopp bei ~8k. **Tier:** Sonnet.

---

## 5. Task 5 — Prozess-Verankerung: Retro-Entscheid ist Input, nicht Planungsgegenstand (Executor, Sonnet)

**Anlass:** Der ursprüngliche S161-Auftrag las sich so, als sei „M1 übernommen" der alleinige
Planungsgegenstand der Session — Stakeholder-Korrektur: der Entscheid zu Retro-Maßnahmen-
Kandidaten aus der Vorsession ist **Input** für die normale Session-Planung, ersetzt sie aber
nicht. Nicht genannte Maßnahmen (hier: M2/M3) gelten als **verworfen**, ohne dass eine
Rückfrage nötig ist. Diese Regel fehlt bisher als geschriebene Konvention — Anlass für den
Prozess-Task.

**Kanonischer Ort:** `docs/governance/operating_model.md`, Event 1 „Planning (Session-Start)"
(§ev1, Zeile 136–148) — dort steht bereits die Default-Planning-Beschreibung inkl.
„Reihenfolge-Pflicht" und „Ausstehendes Review/Retro = Punkt 0"-Bullets; neue Regel als weiterer
Bullet in derselben Liste, kein neuer Ort, keine Duplikate.

**Formulierungsvorschlag (neuer Bullet, nach „Ausstehendes Review/Retro = Punkt 0"):**

> **Retro-Maßnahmen-Entscheid = Input, nicht Planungsgegenstand (Anlass S161):** Kündigt der
> Stakeholder zu Session-Start einen Entscheid zu Retro-Maßnahmen-Kandidaten der Vorsession an
> (übernommen/verworfen), fließt dieser Entscheid als Input in die normale Session-Planung ein
> — er ersetzt sie nicht. Nicht genannte Maßnahmen gelten als verworfen, keine Rückfrage nötig.
> Der Planner plant weiterhin die volle Session entlang der Backlog-Prioritäten; übernommene
> Maßnahmen reiht er als regulären Task in diesen Plan ein.

**Kurzer Hinweis in `.claude/tasks/briefing.md`:** Abschnitt „Session-Routine — nur Verweise"
(Zeile 18–24) bekommt eine weitere reine Verweis-Zeile (kein Duplikat der Regel selbst, gleicher
Stil wie die vier bestehenden Zeilen dort):
`- **Retro-Maßnahmen-Entscheid am Session-Start:** docs/governance/operating_model.md Event 1 (§ev1)`

**Betroffene Dateien:** `docs/governance/operating_model.md`, `.claude/tasks/briefing.md`.

**Testansatz:** `pytest tests/docs/ --no-cov -q` (Doku-Gate, falls ein Struktur-Test die Datei
prüft — sonst reine Sichtprüfung), Vollsuite am Ende.

**Akzeptanzkriterien:** Regel steht genau einmal, kanonisch in `operating_model.md`; Verweis in
`briefing.md` ist reiner Pointer ohne Textduplikat.

**Token-Budget:** ~5k (XS), Selbst-Stopp bei ~8k. **Tier:** Sonnet.

---

## 6. Ausführungsreihenfolge

```
Task 1 (Handoff-Marker) ──▶ Task 2 (B-109) ──▶ Task 3 (B-105)
   sequenziell, gleiche Dateien (diceCompose.py/diceHtml.py) +
   Task 3 braucht den in Task 1 definierten Marker für seinen UI-Verifikations-Handoff

Task 4 (B-119-Prio)  ─┐  unabhängig, disjunkte Dateien (backlog.md)
Task 5 (Prozess-Doku) ─┘  unabhängig, disjunkte Dateien (operating_model.md/briefing.md)
```

Reihenfolge im Plan: 1 → 2 → 3 → 4 → 5 (Reihenfolge folgt der Backlog-Priorität aus
`briefing.md`: Retro-Maßnahme zuerst gelandet, weil Task 3 sie als Marker braucht; danach die
Fachlichkeits-Kette B-109→B-105; die beiden günstigen, unabhängigen Doku-Tasks 4/5 zuletzt).

---

## 7. Token-Budget-Gesamtschätzung und empfohlener Session-Schnitt

| Task | Budget | Selbst-Stopp | Kumulativ (Budget) | Modus | Tier |
|---|---|---|---|---|---|
| 1 — Retro-M1 (Handoff-Marker) | ~10k | ~15k | ~10k | Gate | Sonnet |
| 2 — B-109 (Label-Guard) | ~10–15k | ~20k | ~25k | Gate | Sonnet |
| 3 — B-105 (go_source_chip) | ~15–20k | ~28k | ~45k | Gate | Sonnet |
| 4 — B-119 priorisieren | ~5k | ~8k | ~50k | Gate | Sonnet |
| 5 — Prozess-Verankerung | ~5k | ~8k | ~55k | Gate | Sonnet |

**Gesamtschätzung:** ~55k reine Task-Budgets (Executor-Subagenten-Kontext) + Review/Retro-Budget
~45k (Event 6, zählt zur laufenden Session mit) ≈ **~100k** — bleibt unter dem
Wind-down-Schwellwert (~120k), Korridor <150k eingehalten, **wenn** die Selbst-Stopp-Schwellen
halten. Erfahrungswert aus S159 (dieselbe Dice-Cluster-Dateinachbarschaft, `diceCompose.py`/
`diceHtml.py`): dort lag der Ist-Verbrauch nach nur zwei vergleichbaren Tasks bereits bei ~90k
gegen ein ähnliches Budget — reale Executor-Läufe überschreiten Schätzungen in dieser Dateizone
öfter als in reinen Doku-Tasks.

**Empfohlener Session-Schnitt:** Tasks 1–3 (Handoff-Marker + Dice-Cluster B-109/B-105,
sequenziell wegen Datei-Overlap und Marker-Abhängigkeit) bilden den Kern dieser Session —
danach **Zwischen-Checkpoint**: Kontextstand gegen die Ist-Werte aus `docs/metrics/overview.md`
prüfen (nicht nur die Budget-Tabelle), bevor Task 4/5 gestartet werden. Tasks 4 und 5 sind klein,
unabhängig und günstig (~10k zusammen) — bei Headroom nach dem Checkpoint direkt anhängen; ist
der Korridor nach Task 3 bereits über ~100k Ist-Verbrauch, werden Task 4/5 **nicht** mehr
begonnen, sondern als Punkt 0 der nächsten Session eingeplant (Event 1, „Ausstehendes
Review/Retro = Punkt 0"-Regel gilt analog für angebrochene, aber nicht gestartete Restarbeit).

**Nächster Schritt:** Plan dem Stakeholder zur Freigabe vorlegen (Gate, Event 2), danach Task 1
starten.

**Entscheidungsmodus je Task:** alle fünf Tasks sind `Gate` (Freigabe vor Umsetzung) — keine
`Konsens`-Punkte in diesem Plan, da M2/M3 bereits entschieden (verworfen) sind und alle übrigen
Tasks rein mechanisch/fachlich sind.
