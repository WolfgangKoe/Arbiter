STATUS: ANSWERED — S155-Review nachgeholt (R3), Urteil GO, durchgereicht S156; behalten bis Retro-Maßnahmen-Entscheid (S157), dann löschbar

# S156 — DoD-Review des S155-Stands (nachgeholt, R3-Regel)

**Prüfumfang:** 6 Commits `ab36b80`…`8a69281` (21 Dateien, +618/-476).
**Reviewer:** Reviewer-Subagent (Opus), read-only. **Datum:** 2026-07-17.
**Gesamturteil:** ✅ **GO** — alle harten Gates grün, keine Blocker; zwei kosmetische
Doku-Notizen (siehe P7) und eine offene Stakeholder-Entscheidung (P6, begründet n/a).

---

## Prüfpunkte (CLAUDE.md 7-Punkte-Katalog)

### 1. Regelkonform — ✅
E1-Fix in `ab36b80` (`src/gameMechanic/fightPhase.py`): `_any_unit_fought` → `_enemy_has_fought`.
Regeltext `docs/work/wahapedia_core_rules/core_rules.txt` (COUNTER-OFFENSIVE, 2CP, Zone Z. 3256 ff.):

> „Use this Stratagem **after an enemy unit has fought in this turn**. Select one of your own
> eligible units and fight with it next."

Der neue Trigger ermittelt `enemy = second if faction == first else first` und prüft
ausschließlich die `turn_flags.fought`-Flags der **gegnerischen** Einheiten
(`fightPhase.py`, `_enemy_has_fought`). Das deckt sich exakt mit dem Regelwortlaut
„an **enemy** unit has fought". Die alte Version prüfte „irgendeine Einheit beider Seiten"
und bot die Box fälschlich schon nach dem **eigenen** Fight an — Regelbruch behoben.
Der ergänzte Caption-Hinweis („Counter-Offensive becomes available once an enemy unit has
fought.") ist rein informativ und ändert die Regellogik nicht.
Regressionstests in `tests/gameMechanic/test_fight_turn_advance.py`:
`test_enemy_has_fought_false_when_only_own_side_fought` (eigener Fight ⇒ kein Trigger) und
`test_enemy_has_fought_true_when_opponent_fought` (Gegner-Fight ⇒ Trigger) — belegen genau
den Regelfall. Belegt zusätzlich in `rules_appendix.txt` Z. 2570 ff.

### 2. Generisch — ✅
B-027-Wiring in `316240f`:
- `src/gameMechanic/chargePhase.py:181` — nur `unit_key_for_modifier=uid` an bestehenden
  GO-Box-Aufruf durchgereicht.
- `src/gameMechanic/movementPhase.py:335,347,357` — `_spend_callback` erhält zusätzliches
  `unit_key`-Argument, das an `spend_stratagem` weitergegeben wird.

Keine neuen Fraktions-Strings/-Checks in `src/`. Das Architektur-Gate INV-4b meldet
unverändert 6 Tokens / 16 Fundstellen / 3 Dateien (bestehender Ratchet-Ledger, **nicht**
erhöht) — d. h. das Wiring hat kein Fraktions-Vokabular eingeschleppt. ✅

### 3. Tests grün — ✅ (mit Zähl-Notiz)
`pytest --tb=short`: **1881 passed** in 235,72 s, **TOTAL coverage 99,14 %**
(„Required test coverage of 99.0% reached."). Floor 99 % gehalten.
Coverage stimmt exakt mit der Briefing-Zahl (99,14 %). Testzahl **1881** statt der im
Briefing notierten **1880** — Abweichung +1, Gate unberührt (grün). Vermutlich Briefing-Zahl
vor dem letzten hinzugefügten Test notiert; kein Befund, nur Doku-Zahl nachziehen.

### 4. Architektur-Gate — ✅
`pytest tests/architecture/ tests/docs/ tests/acceptance/ --no-cov -q`: **31 passed** in 4,44 s.
Ledger „impl. ohne Test" = 0 (leer), alle getestet-Refs existieren, alle AC-IDs gepinnt.

### 5. Clean Code — ✅
- `ruff check`, `black --check`, `isort --check` über die drei geänderten `src/`-Dateien:
  alle sauber („All checks passed!", „3 files would be left unchanged").
- Namensqualität: `_enemy_has_fought` benennt die Bedingung präziser als das alte
  `_any_unit_fought`; Testnamen beschreiben Verhalten. Keine toten Pfade in den Diffs.
- Kommentar-Konvention: die neuen Erklär-Kommentare (fightPhase-Caption-Block,
  movementPhase-Docstrings) sind durchweg **Warum-Kommentare mit Quellenangabe**
  (`core_rules.txt Z. 3256-3259`) bzw. begründen nicht offensichtliche Entscheidungen
  (Closure-Capture, warum `unit_key` hier immer bekannt ist) — konventionskonform.
  ⓘ Kosmetik (kein Befund): die `movementPhase._spend_callback`/`_advance_reroll_state`-
  Docstrings sind recht ausführlich; inhaltlich zulässig (Warum), stilistisch grenzwertig
  lang — bei nächster Modulberührung ggf. straffen.

### 6. UI manuell verifiziert — ✅ begründet n/a (wartet auf Stakeholder)
Render-Code (`fightPhase.py`-Caption, GO-Box-Suffixe) ist nicht test-gedeckt.
`docs/handoff/S155_ui_verifikationen.md` steht auf **NEEDS-DECISION** (4 Prüfblöcke:
Counter-Offensive-Hinweis, used-on-Suffix Advance-Reroll + Overwatch, Silent-King-Defaults,
PSI-Flow) — Stakeholder-Antwort steht aus. Damit **begründet n/a**, **kein Blocker** fürs
Urteil (Handoff sauber ausgelagert nach neuer Ablaufregel).

### 7. Artefakte aktuell — ✅ (mit 1 anstehender Löschaktion)
- Handoff-Marker-Lifecycle:
  - `S155_planning.md` → **ANSWERED** ✅ (Freigabe + Empfehlungen dokumentiert).
  - `S155_ui_verifikationen.md` → **NEEDS-DECISION** ✅ (korrekt, s. P6).
  - `S152_offene_ui_verifikationen.md` → **gelöscht** ✅ (142 Zeilen entfernt, durch
    S155-Version ersetzt gemäß neuer „UI-Verifikationen immer als Handoff"-Regel).
  - ⚠️ **`S154_planning.md` existiert noch** — Briefing markiert es als „löschbar nach
    S155-Review". **Anstehende Löschaktion für den Koordinator** (Datei
    `docs/handoff/S154_planning.md`), sobald dieses Review durch ist.
- Backlog-Archivierung inkl. Details-Abschnitt:
  - `aeae746`: B-036 / B-053 / B-079 → `backlog_archive.md`, Details aus
    `backlog_details.md` entfernt ✅ (B-079 war stale seit S118); B-025 umformuliert.
  - `ee6eb15`: B-027 / B-060 / B-087 → `backlog_archive.md`, Details entfernt ✅.
  - Kein archiviertes Item als aktive Zeile doppelt: B-031 (Anker `backlog_details.md:632`
    existiert weiter) und B-087 erscheinen in `backlog.md` nur als **Querverweis/Narrativ**,
    nicht als Duplikat-Row — konsistent.
  - ⓘ Kosmetik (kein Befund): `backlog.md:20` enthält eine datierte S152-„Abgleich"-
    Notiz „B-009+B-087 Nacharbeit → ToDo"; B-087 ist inzwischen archiviert. Es ist ein
    historischer Log-Eintrag (kein aktiver Status), daher zulässig — bei nächster
    Backlog-Bereinigung ggf. datieren/kürzen.
  - **B-102 neu** angelegt (`backlog.md:113`, E1-Zusatzbefund: Counter-Offensive-Box in
    einfachen 1-gegen-1-Sequenzen selten erreichbar, `_enemy_has_fought` selbst korrekt) ✅.
- `gretchin_mob`-Relikt (`aeae746`) aus `data/wh40k_9e/orks/unit_abilities.yaml` entfernt;
  `grep` über `src/` + `data/` findet keine verbliebene Referenz ✅.
- Briefing (`8a69281`) + `session_archive.md`/`.json` rotiert, Stand S155 konsistent ✅.

---

## Gesamturteil: ✅ GO

Alle harten Gates grün (1881 passed / 99,14 % / 31 Arch+Doku+Acceptance), E1-Fix
nachweislich regelkonform, B-027-Wiring generisch, Artefakte konsistent archiviert.
Keine Blocker. Offen bleibt nur die Stakeholder-UI-Verifikation (P6, außerhalb des
Review-Scopes) und — als reine Aufräumaktion — die Löschung von `S154_planning.md`.

---

## Retro-Input (Beobachtungen, keine Maßnahmen)

1. **R3-Regel hat funktioniert:** Das nachgeholte Review deckt einen sauber
   abgeschlossenen Stand auf — kein Nacharbeitsstau. Die Regel „Review verpasst ⇒ Punkt 0
   nächste Session" verhinderte, dass unreviewte Commits sich weiter stapeln. Positiv.
2. **Fix + Folgebefund + Backlog-Item als Kette:** E1 wurde nicht nur gefixt, sondern der
   Zusatzbefund (Box-Erreichbarkeit) direkt als B-102 verankert statt im Chat zu versanden —
   gutes Muster (Befund → kanonischer Ort).
3. **Briefing-Testzahl driftet leicht (1880 vs. 1881):** Kleine, aber wiederkehrbare
   Reibung — die im Briefing eingefrorene Kennzahl war schon beim Schreiben eine Momentaufnahme.
   Muster: manuell notierte Gate-Zahlen altern; Verlass sollte auf dem Live-Gate liegen.
4. **Doku-Konventions-Grauzone bei Docstrings:** Die verbosen movementPhase-Docstrings zeigen,
   dass „Warum erlaubt / Spec nacherzählen verboten" in der Praxis eine unscharfe Grenze hat —
   die Autoren wählen im Zweifel Ausführlichkeit. Kein Fehler, aber ein wiederkehrender
   Entscheidungspunkt.
5. **Handoff-Lifecycle sauber, aber Löschungen hängen nach:** `S152_offene…` korrekt gelöscht,
   `S154_planning.md` aber trotz „löschbar"-Marke noch da. Muster: das *Markieren* als löschbar
   und das *tatsächliche* Löschen fallen auseinander — Aufräumaktionen brauchen einen festen
   Auslöser, sonst sammeln sich ANSWERED/löschbar-Dateien an.
