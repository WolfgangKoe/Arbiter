# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planning vorlegen** (Prioritäten + Token-Schätzung), erst nach
  Freigabe los; Shortcut „Plan ist freigegeben" = direkt los. **Lesen:** `CLAUDE.md` +
  `docs/goals/ziel6.md` + `docs/goals/backlog.md`. Einstieg `LEITSTAND.md`; Rollen/Tier/Modi:
  `docs/governance/operating_model.md`.
- **Ende:** Review → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) → Abschluss: **diese
  Datei** aktualisieren (ZUERST lesen, dann ergänzen) + ggf. ziel6-Checkboxen.
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70** kürzen —
  Erledigtes → `backlog.md`/`session_archive.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten =
  stehende Freigabe (proaktiv, ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).

---

## Aktueller Stand (nach S97, 2026-06-25)

**S97 — nur Planung/Scoping + Doku, KEIN Code geschrieben.** Step 2 (Hungry Void) gescoped; dabei
**zwei strukturelle Befunde** + Konsens-Entscheide (alle in Plan 025 „Update S97" + backlog §0/§2):
1. **Combat ist zähl-basiert** (`resolve_attack(... wounds_rolled: int ...)`, kennt keine einzelnen
   Würfelaugen) → `ap_on_unmod_wound_6` ist **nicht** als A-Effekt machbar. **Konsens: D1 Hungry +
   Vengeful A → B** (Tisch-Hinweis). Pro-Würfel-Umbau = eigener großer Plan, vorerst nicht gewollt.
2. **Latente Drift:** `strength_modifier`/`ap_bonus` sind engine-gemappt + getestet, aber in
   `_collect_atk_modifiers`/`_collect_def_save_modifiers` **nie konsumiert** → Hungry-S/Vengeful-S
   wirken im Kampf gar nicht. backlog-§0-„Engine ✅" war zu optimistisch.

**Stakeholder-Kritik S97 (ernst nehmen):** Ich habe Anzeige-Anforderungen wiederholt auf „später"
geschoben statt zu fragen → Schuld türmt sich. **Neue verbindliche Regel: Anzeige ist Pflichtteil
JEDES 025-Steps** (in Plan 025 DoD verankert). Daraus: **Step 2b = generischer Direktiv-Hinweisblock**
(YAML-Feld `enforcement: app|table`, pure Fn `directive_hints`, Caption `✓ angewandt` / `⚠ am Tisch`),
der die aufgelaufenen 🔲-Anzeige-Lücken (Reroll-Save-Hinweis, S+1-WOUND, AP-im-SAVE, Sudden-Storm-B)
Schritt für Schritt ablöst.

**Vom Stakeholder gemeldete offene Bugs (S97, in backlog dokumentiert):** (a) Reroll-of-1-Save-Hinweis
fehlt in der UI (Soll: ⟳-Caption im SAVE-Block, Plan 024); (b) Dynastie-Affinität „beide Direktiven"
greift nicht beim rundenzugewiesenen Protokoll (war als S96-Notiz da, jetzt als Bug geführt).

**Vorher (S96):** Plan 025 Step 1 erledigt (Sudden Storm D2 + Undying-Legions-Tausch → alle 6
Protokolle Primary=9E-D1). 1135 grün / 93,11 %. Detail → `session_archive.md` / git.

### Nächster Schritt
**Plan 025 Step 2 (Logik) — Freigabe-Punkt 1:** Hungry D1 → `ap_on_unmod_wound_6` (melee, **B**),
D2 → `strength_if_charged` (melee, **A**, value 1). Neues `was_charged`-Flag (`set_charged` markiert
nur Charger; turn_flags-Init + Reset in game_state). Pure Fn `get_active_round_choice_strength_if_charged`;
Konsum in `_common.py` Strength-Berechnung. Test-Migrationen (hungry_void primary/secondary, strength_modifier)
+ neue Tests + **Vollsuite**.
**Dann Step 2b (Anzeige) — Freigabe-Punkt 2:** generischer Hinweisblock (s. o.).
Reihenfolge gesamt: 025(Rest, je Step mit Anzeige) → 016(Rest) → 018 → 015 → 017.

### ⚠️ Carry-over (offen)
0. **Kontext-Engineering / Regel-Kuratierung (eigene Session, Maßnahme C).** Quelle:
   `docs/reference/context-engineering-slides.md`. (a) SessionStart-Regel-Injektion (relevante Regeln je
   Ziel verbatim in den Kontext) — behebt Tiering-/Regel-Lücken. (b) Subagent-Ergebnis → `docs/handoff/`-
   Datei statt in Orchestrator-Kontext. (c) Handoff-Lebenszyklus (lesen→arbeiten→auslagern→löschen).
   (d) governance-Doc `context_engineering.md`; `docs/handoff/context-audit-S91.md` verarbeiten + löschen.
   **S95-Beleg (warum Kern):** Die Regelprüfung griff nur, weil sie *expliziter Plan-Schritt* war — nicht
   aus zuverlässiger Gewohnheit. Assurance braucht **Injektion oder Gate**, nicht „zufällig im Kontext".
1. **Plan 025** = aktive Hauptlinie (s. o.). Bug 3 (Zweitspieler-Direktiv-Wahl, armyCard.py:296/307) +
   INV-4b-Restschuld (`dynasty`/`gloom`/`prism`/`necrons`-Defaults) laufen nebenher, je eigene Freigabe.
2. **Manuelle UI-Verifikation (offen, PFLICHT, Render-Code):** (a) S91 Mirror-Protokoll — Necron-vs-Necron
   Befehlsphase: Spieler-1-Wahl lässt Spieler-2-Karte unverändert. (b) Bug 5: Runde-2-Fernkampf-Zielwahl.
   (Eternal-Guardian-Save / Undying-Legions-RP / Living-Metal-S waren S93 ✅.)

### Offene Fragen / Vormerke
- **Design-System-Crew (eigene Session):** Subagenten-Gespann Designsystem + Buff-/Direktiv-Hinweis-
  Komponente (RP-Hint deutlicher, konsistent mit MWBD/SAVE). Greift, sobald 025 die Effekte festlegt.
- **S95-Prozess-Vormerk (nicht entschieden):** Regelkonformität evtl. schon **beim YAML-Modellieren**
  prüfen, nicht erst bei Anzeige — als DoD-#1-Ergänzung erwägen.
- **Lehren:** „Engine oder Verdrahtung?" → erst prüfen, welche State-Klassen der Resolver liest (S93);
  Repro-zuerst (S92); Branch-Check (aktiv = `feature/016`).
- **Kleine Doku-Vormerke:** backlog #2 / ziel6 6e um Bug-3-Step + „Reset kampfrunden-weit" (S90);
  Freigabe-Gate Re-Arm nur bei echtem SessionStart prüfen; `CLAUDE.md` um ADR-0006-Verweis ergänzen.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor 90 %, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report:** `python tools/token_report.py --write`. **History:** `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
