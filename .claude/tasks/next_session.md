# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->

## ⚠️ Session-Regeln (immer beachten)

**Zu Beginn jeder Session lesen:**
- `CLAUDE.md` — Workflow, Freigabe-Pflicht, **Unklarheiten IMMER zuerst fragen**
- `docs/goals/ziel6.md` — Aufgabenliste, Checkboxen, **Session-Historie (Changelog)**

**Am Ende jeder Session:**
- Checkboxen in `docs/goals/ziel6.md` abhaken + eine Zeile in die Session-Historie ergänzen
- Diese Datei aktualisieren: Stand + nächster Schritt (ZUERST lesen, dann ergänzen)

> Die vollständige Session-Historie (S28–S45 + Audit-Queue) liegt jetzt in
> `docs/goals/ziel6.md ## Session-Historie` — hier nur noch der aktuelle Stand.

---

## Was ist Arbiter?

Digitaler Spielbegleiter für Warhammer 40.000 9. Edition, Streamlit (Python).
Start: `streamlit run src/app.py` (Port 8501). Branch `dev` (Entwicklung), `main` (nur per PR).

---

## Aktueller Stand (nach S49, 2026-06-15 — 819 Tests grün, 89 % Coverage)

- Ziel 1–5 vollständig; Ziel 6a–6n + Audit-Pläne 001–013 abgeschlossen (Details: ziel6.md).
- Plan 013 (einheitlicher Gruppen-Flow) live; B1–B5 post-013-Bugs gefixt (Commit `46e03f8`).
- **S45: Findings F1–F8 verifiziert** (Ergebnis unten). F8 war falsch, F6/F7 ungenau.
- **S46: Findings F2/F4/F6/F7 + Cover-Layout (Option B) implementiert** (Commit `44a29a5`).
- **S47: manuelle Verifikation → Findings G1–G5 ALLE umgesetzt.**
  G1/G4/G5 + Necron-Test-Roster (`e98d89d`); **G2 Silent King + per-Gruppe-Wunden** (`cb39cdd`).
- **S47b: Bracket-Follow-up + Menhir A2** (Commit `446c2b6`). Szarekh-Attacken folgen seinem
  eigenen Bracket; Menhirs fix A2.
- **S47c: Crash-Fix Silent-King-Gesundheitsbalken** (Commit `7ad42e6`). `st.progress(-0.125)` in
  `unitCard.py` (uniforme Frontmodell-Formel bei gemischten Wunden). Neuer Helfer
  `front_group_hp` (Option B) — Frontmodell aus der vordersten überlebenden Gruppe, geclampt [0,1].
- **S48: Findings H1–H7** (Commit `3e508bb`, 815 Tests grün):
  - H3 Living-Metal-Bug (gruppen-bewusste `unit_max_hp`); H2 Silent-King-Waffen korrekt verteilt;
    H1 Big-Mek-MA-Wargear modelliert; H4a Szarekhan-Code = **Uncanny Artificers** (NICHT „beide
    Direktiven" — das war erfunden; Silent King als DYNASTIC AGENT bekommt gar keinen Code);
    H4b Roster-Standard `dynasty:`+`protocol_order` (SK-Roster = szarekhan); H5 MWBD 2× bei PHAERON;
    H7 Badge-Farben in `_common.py` an `design_colors.md` angeglichen (MOVED blau, Buff grün).
- **S49 (2026-06-15):** Architektur-Gate + Artefakt-Konsolidierung + Logo
  (Commits `bd9cbe7` / `bbf0a61` / `fc1dd74`). Manuelle UI-Verifikation der G-/H-Fixes
  durchgeführt → **neue Findings 1–9** (Abschnitt „S49 — UI-Findings" unten).
- **S50 (2026-06-16):** Freier Lauf durch die S49-Findings. Erledigt + committet:
  Logo (`79e96ee`), Finding 5 Skorpekh-Header (`1544ecc`), H2 Silent-King-Caps (`a989b1c`),
  H4a Dynastie-Badge (`59dda19`), Finding 7 Protokoll-Buff-Badge + Kurzlabel (`4f8089f`),
  Finding 8 6.-Protokoll-Dropdown im Setup (`6eb26dd`). **Verifiziert ohne Code-Änderung:**
  Finding 1 (Choppa-Extra ist bereits korrekt choppa-gebunden, PK cappt bei 4), Finding 2
  (S = User×2+1 = 11 regelkonform, Multiplikation vor Addition, generisch), H1 (Loader
  add/replace korrekt; **es gibt keine Wargear-Picker-UI** → nichts zu rendern).
  **OFFEN:** nur noch **Finding 9 (Würfelanzeige)** — braucht Layout-Abstimmung (s.u.).
- **OFFEN (alt):** Findings 1–9 abarbeiten (erst Plan je Punkt, Freigabe) + neues Logo integrieren. ✅ bis auf Finding 9.

### 🟢 Architektur-Gate (seit 2026-06-15)

Neben der Coverage gibt es jetzt ein **Architektur-Gate**: `tests/architecture/` setzt 4
Invarianten durch (gameObjects Streamlit-frei, YAML nur über Loader, Layer-Richtung,
Generic-src). Status + Schulden-Ledger: [docs/spec/architecture_invariants.md](../../docs/spec/architecture_invariants.md).
Schnellmessung: `pytest tests/architecture/ --no-cov -q`. Läuft im normalen `pytest` mit.

---

## S49 — UI-Findings (manuelle Verifikation, NOCH NICHTS UMGESETZT)

### ▶ Start nächste Session (bei „Der Plan ist freigegeben")

Die „Freigabe" deckt hier **das Starten + die Regel-Recherche** ab, NICHT das stille Umsetzen:
diese Liste ist ein Findings-Backlog, kein fertiger Ausführungsplan. Konkret:
1. Zuerst **neues Logo integrieren** kurz bestätigen lassen (freistellen → Assets ersetzen).
2. **Regel-Recherche** zu Findings 1 (Boss Nob), 4 (Veil/Retreated), 8 (Protocol-Wechsel/Silent King) —
   lokal in `docs/work/wahapedia_*`, dann Ergebnis vorlegen.
3. Pro Finding **kurzen Plan / UI-Mockup** zeigen und auf „ja" warten, bevor Code geändert wird
   (Findings 7/9 sind UI-Design → Mockup-Pflicht).

Reihenfolge sonst offen; Regelfragen recherchiere ich lokal.

1. **Boss-Nob-Attacken (Regel-Recherche):** zeigt 4 auf Power Klaw. Prüfen: korrekte Gesamtzahl
   (Basis A3 + WAAAGH +1 + Choppa-Extra?), darf Choppa **neben** Power Klaw geführt werden, und
   darf die **Choppa-Extra-Attacke nicht** auf die Power Klaw gelegt werden (extra_attacks-Cap).
2. **S11 generisch (Investigation):** S-Berechnung (User×2+1) bei ALLEN Einheiten gegenprüfen,
   nicht nur Boss Nob.
3. **Cover Option B:** ✅ bestätigt, nichts offen.
4. **Veil of Darkness (Regel-Recherche):** Träger steht nach Teleport korrekt nicht mehr „IN MELEE".
   OFFEN: Gelten die Einheiten danach als **„Retreated"** (kein Schießen/Kämpfen)? RAW prüfen.
5. **Skorpekh Attacken-Summe (Bug):** linke Zahl „assigned" bleibt **0**, obwohl Nahkampf-Attacken
   unten zugewiesen sind. Soll = Summe der tatsächlich zugewiesenen Attacken sein.
6. **S48 H1–H7:** aufgeschlüsselt + verifiziert — Detailstatus in H1/H2/H4a unten.
7. **Command-Protocol-Buff (Bug + UI):** Buff wird **weder in unitCard noch in den Phasen** angezeigt.
   Soll als **grüne Buff-Badge** bei jeder betroffenen Einheit + im Phasen-Block erscheinen (wie MWBD).
   Badge **kürzen**: armyCard ohne „Protocol of the …"-Präfix (→ „Undying Legion"); unitCard noch kürzer.
8. **Command-Protocol-Setup (UI + Regel-Recherche):** das **permanent-aktive (6.) Protokoll** soll
   **oben ebenfalls als Dropdown** erscheinen (wie die rundenbasierten); Default bleibt; Auswahl tauscht.
   Festlegung beim Setup gemäß Regeln. NICHT eingeplant (Plan 016 = nur Effekte). Wechsel-Regeln inkl.
   **Silent King** recherchieren (Wechsel im Spiel nur mit SK + Fähigkeit?).
9. **Würfelanzeige Attackenabfolge (UI-Spec):** Spec/Mockup ggf. veraltet → mit Nutzer abstimmen.
   - 9.1 Randfälle: der Ergebnis-Würfel muss **unter seiner Wert-Spalte** stehen (Bsp.: 5 stand unter 1).
     „x" soll ein **Würfel-Icon = generelles Miss-Icon** sein (auch im normalen HIT/WOUND/SAVE-Block),
     rechts neben der 6 platziert (analog 1 links neben 2). **Alle** Fälle abbilden, in denen AP den
     Standardfall verschiebt. Wiederholungswürfel bisher nie gesehen.
   - 9.2 Standardfall: Würfel nicht spaltenkonform ausgerichtet; AP-Pfeile nicht entsprechend länger.
   - Vorgehen: `dice_html.py` + Spec (`ziel6.md §6n D5`) studieren → korrigiertes Layout-Mockup vorlegen.
   - **S50-Analyse (Root Cause gefunden, noch NICHT umgesetzt — wartet auf Layout-Abstimmung):**
     `threshold_header_html` rendert 6 feste `_DIE_SLOT`-Spalten **ohne** Boundary-Gap;
     `dice_row_html` schiebt aber zwischen Miss- und Erfolgs-Würfel einen **vollen** die-slot
     breiten `_boundary_gap_html` (34px) ein. Dadurch sind die gerahmten Erfolgswürfel (inkl.
     Ergebnis-/Eff.-Würfel) um ~1 Spalte gegen den Header verschoben → „5 stand unter 1" (9.2).
     Fix-Optionen: (a) den Boundary-Gap auch in `threshold_header_html` einsetzen, ODER (b) die
     Trennlinie ohne eigene Spaltenbreite zwischen Würfel `t-1` und `t` zeichnen. **(b) bevorzugt**
     (hält 6 Spalten = 6 Würfel), aber visuell zu bestätigen.
     9.1 Miss-Icon: `dice_face_svg(1)` zeigt schon ein ×; gewünscht ist ein **Würfel-Icon als
     generelles Miss-Symbol rechts neben der 6** in verschobenen/AP-Fällen (analog 1 links neben 2)
     statt des Text-`×` (`save_modifier_die_pair_html` right_raw>6 und `dice_row_html` threshold>6).
     **Offen an den Nutzer:** Soll Fix (b) gelten? Soll das Miss-Würfel-Icon das Text-× überall
     ersetzen? Spec `§6n D5` ggf. veraltet — aktuelles Wunschlayout bestätigen, bevor ich `dice_html.py` ändere.

### S48-Detailstatus (aus S49-Verifikation)

- **H1 (UI-Bug):** YAML korrekt — `tellyport_blasta` ist als optionales `add` modelliert
  (`orks/units.yaml` big_mek_mega_armour). Die Wargear-UI rendert optionale `add`-Items aber nicht
  → Render-Pfad prüfen.
- **H2 (Regel/Daten):** Silent-King-Waffen korrekt, aber **Nahkampf-Verteilung** muss die feste
  Max-Attackenzahl je Waffe respektieren (max_attacks/extra_attacks).
- **H3/H5/H7:** ✅ bestätigt.
- **H4a (Feature, generisch!):** Dynastie liegt im State (`p1_dynasty`/`p2_dynasty`,
  `game_state.py:294-295`), wird aber **nirgends angezeigt**. Dynastiebonus muss in armyCard +
  unitCard-Badge + relevanten Phasen sichtbar werden — **keine Fraktionslogik in `src/`** (Arch-Gate!).
- **H4b:** Roster `dynasty:`/`protocol_order` → Loader (`loader.py:907-908`) → State
  (`game_state.py:66-67`); Tausch bei `:254`/`:359`.

### Logo — neues GPT-Bild (bereit, Integration ausstehend)

Neues Logo unter `Fotos/ChatGPT Image 15. Juni 2026, 19_47_45.png` — Waffen gerade, Gold/Rot passt.
**Wichtig:** Bild ist komplett opak (GPT hat ein Karomuster als Hintergrund gemalt). Freistellen via
neutral-hell-Flood-Fill von den Rändern + 1px-Erosion (wie in S49 erprobt) → dann
`tools/process_logo.py`-Trim/Square/Icon. Ergebnis sah sauber aus. Aktuell in der App noch die
Soft-Gold-Variante des **alten** Logos (Commit `fc1dd74`). Nächster Schritt: neues Logo freistellen,
`assets/arbiter_logo.png` + `arbiter_icon.png` ersetzen, committen.

---

## Findings G1–G5 (S47 — aus manueller Verifikation)

- **G1 ✅** Granaten-Cap pro **Einheit** (1/Phase, über alle Gruppen geteilt), nicht pro Gruppe.
  `_render_group_declaration` zieht in anderen Gruppen zugewiesene Granaten ab.
- **G4 ✅ (gehärtet, RE-VERIFIZIEREN)** Warbikers-Schussphase zeigte vorausgewähltes Ziel.
  `group_targets` wird nur per Klick/Reset gesetzt → Ursache vermutlich stale `decl_*`-Widget-Keys.
  `reset_group_declaration_state` löscht jetzt `decl_m_*`/`decl_a_*`/`decl_p_*`/`group_autosel_done_*`.
  **Bitte im echten Spiel gegenprüfen, ob behoben.**
- **G5 ✅** Reanimation Protocols **einmal pro Verteidiger-Einheit**, nachdem die angreifende
  Einheit ALLE Waffen-Tabs abgehandelt hat (vorher pro Tab). `_render_unit_rp` summiert
  Modellverluste pro `def_uid`. Generisch (Gate `reanimationProtocols`-Rule).
- **G3 ✅ (teilweise)** `necrons_test.yaml` deckt Skorpekh-Reap / Lychguard-Swap / Lokhust-Enmitic
  ab. **Silent-King-Variante fehlt → hängt an G2.**

### G2 ✅ — The Silent King als 3-Modell-Einheit (per-Gruppe-Wunden)

Umgesetzt (Commit `cb39cdd`): Szarekh (1 Modell, W16, Bracket) + Triarchal Menhirs (2 Modelle, W7,
WS5+/BS3+, **sterben zuerst**). Generisches per-Gruppe-HP-Subsystem:
- `ModelGroup.stats["wounds"]` + `Unit.has_per_group_wounds()`/`group_wound_value()`.
- `game_state._unit_state`: `group_wounds`-Pool pro Gruppe; `current_wounds` = Summe. Uniforme
  Einheiten behalten den alten flachen Pfad (kein Test-Bruch).
- `unit_mutations.apply_damage`/`heal_unit`/`flee_models`: Allokation nach `priority` (Menhirs
  zuerst, Spillover auf Szarekh; Heilung/RP füllt Menhirs zuerst). Gegated auf `group_wounds` —
  keine Fraktionslogik.
- UI-Damage-Block: Einheiten mit gemischten Wunden bekommen ein „Total damage"-Feld (Verluste
  werden per Gruppe verteilt); `models_lost` wird nach Apply als Delta berechnet.

**Menhir-Stats-Quelle:** Wahapedia-9e-Datasheet (zweites Profil). Die lokale `units_all.txt`
hatte nur Szarekhs Statline (Scraper schnitt das zweite Profil ab). Verwendete Werte: Menhirs
**W7, WS5+, BS3+, T7, Sv3+** (Inv4+ via Transtemporal Force Field). **Falls eine Zahl abweicht:
`data/wh40k_9e/necrons/units.yaml` → `triarchal_menhirs.stats` anpassen.**

**Mini-Follow-up ✅ (Commit `446c2b6`):** `_group_effective_attacks` — Gruppen mit eigenem
`attacks`-Stat sind fix (Menhirs A2); Gruppen ohne (Szarekh, nutzt Unit-Attacks) werden über das
Bracket anhand der **eigenen** Gruppen-Wunden reduziert (A6→A4→A2). In Deklaration + Owner-Budget
genutzt. Menhirs `attacks: 2` korrigiert.

**Boss Nob W2 — bewusst NICHT umgesetzt:** Das per-Gruppe-Wunden-System würde den Boss Nob (W2)
zwar korrekt abbilden, aber dann nutzt die ganze Boyz-Einheit den „Total damage"-Eingabepfad statt
„Models lost" — für einen 30-Modell-Mob schlechtere UX. Boss Nob bleibt vorerst effektiv W1 (nur
relevant, wenn er als letztes Modell übrig ist). Falls gewünscht: per-Gruppe-Wunden-UI um eine
Modell-Counter-Variante erweitern, dann Boss Nob W2/Warbike W4 nachziehen.

---

## Verifizierte Analyse F1–F8 (S45 — korrigiert die alte Doku)

> Geprüft gegen `_common.py`, `dice_html.py`, `ability_engine.py`, Ork-/Necron-YAML,
> `movementPhase.py` und die Core Rules. Mehrere alte F-Befunde waren ungenau.

### WAAAGH (F2 / F4 / F8) — Sichtbarkeit ist da, Architektur fehlt

- **F8 war falsch.** `+1 Strength` wird als blau umrandete S-Badge gerendert
  (`dice_html.py:300`), `str_bonus` korrekt **nach** `_parse_strength` addiert (`_common.py:687`).
  Der WAAAGH-Invuln ist verdrahtet: `ability_invuln_save` → `resolve_save` → eigene „Inv N+"-Zeile
  (`_common.py:748`, `dice_html.py:381`). **Keine UI-Arbeit nötig.**
- **F2 (echter Bug):** `model_groups` tragen keine eigenen Stats. Budget = `alive × (atk_unit.attacks + atk_bonus)`
  (`_common.py:1134/1193`). Boss Nob (real A=3) erbt Boyz `attacks: 2` → mit WAAAGH 3 statt 4
  → „4. Attacke nicht auf Power Klaw legbar".
- **F4 = vermutlich gleicher Root Cause wie F2.** `buff_stat_bonus` matcht `ORK` (Warbikers haben es),
  der +1 greift. **Offene Restfrage:** Bleibt `activated_abilities` über den Zugwechsel hinaus
  erhalten (Invuln „bis Beginn deines nächsten Zuges" im Verteidigerpfad)? → reproduzieren.

### Cover (F1 / F3 / F5)

- Cover wird einmal **oberhalb der Tabs** gerendert (`_common.py:1346`), im Tab unterdrückt.
- **F1/F3 = Layout-Entscheidung getroffen → Option B:** Dense in HIT-Block, Light/Heavy in SAVE-Block.
- **F5 vermutlich kein Bug:** Key-Konsistenz stimmt (`rsplit`); Heavy-Cover-Checkbox erscheint nur
  wenn Verteidiger **nicht selbst gechargt** hat (`_common.py:1358`) = regelkonform. Erst reproduzieren.

### Skorpekh (F6) — Doku-Annahme ungenau

- Einheit **hat** `model_groups` mit `reap_blade_swap`, `limit: per_3` (`necrons/units.yaml:244`),
  aber als **optionaler** Swap. Datasheet verlangt **feste Komposition** (1 Reap-Blade je 3 Modelle).
  → Fix: fester Sub-Gruppen-Split (analog Boss Nob) + Roster prüfen. `src/` unberührt.

### Veil of Darkness (F7) — Root Cause korrekt, Flag-Name falsch

- Flag heißt `movement_locked` (nicht `veil_moved`). Teleport-Confirm setzt `moved`+`movement_locked`
  (`movementPhase.py:223`), **cleart `in_melee` nicht** → „MOVED"+„IN MELEE" gleichzeitig.
  → Fix: `in_melee=False` für Träger + optionale CORE-Einheit beim Confirm; im `_undo_teleport` zurück.

---

## Freigegebener Plan (S45) — Reihenfolge: Doku-Cleanup ✅, dann Findings

**Entscheidungen des Nutzers:**
- Cover-Layout: **Option B** (Cover in die jeweiligen Blöcke einbetten)
- Per-Gruppe-Stats: **volles Override-Schema** (`attacks`/`strength`/`wounds`/`ws`/`bs`)
- Reihenfolge: erst Doku-Cleanup (erledigt), dann Findings, dann Roster-Audit

**Block A — Per-Gruppe-Statarchitektur (F2 + F4) ✅ S46:** `ModelGroupSpec`/`ModelGroup.stats`
+ `.stat()`-Helper; Loader parst `stats` und propagiert (inkl. Sub-Gruppen/Merge); `_common.py`
Budget + Resolution lesen Gruppen-`attacks`/`strength`/`ws`/`bs` (Fallback Unit); Boss-Nob-Daten
(A3/S5/WS2+) in `orks/units.yaml`. Power Klaw mit WAAAGH = S 5×2+1 = 11 ✓.

**Block B — WAAAGH-Persistenz ✅ verifiziert, KEIN Bug:** `_reset_turn_state` löscht
`activated_abilities` nicht, schaltet nur bei neuer Runde Stage 1 → Stage 2. Stage-1-Invuln steht
den Orks im Gegnerzug defensiv zur Verfügung.

**Block C — Veil of Darkness (F7) ✅ S46:** `_lock_teleport_movement` cleart `in_melee` für Träger
+ CORE-Einheit und merkt den Vorwert; `_undo_teleport` stellt ihn wieder her. 3 Tests.

**Block D — Skorpekh (F6) ✅ S46:** `units.yaml` ist RAW-korrekt (optionaler `per_3`-Swap);
`necrons_alpha` + `zarekhan_sol_kampf_2` opten in den Standard-Build (1 Reap-Blade je 3).

**Block E — Cover Option B (F1/F3) ✅ S46:** Cover-Checkboxen in HIT-(Dense)/SAVE-(Light/Heavy)
-Block, per-Tab-Key; Block oberhalb der Tabs entfernt; `show_cover_controls`-Param weg.

**F5 / F8 — nichts zu tun:** F8 (Strength-Badge/Invuln) war bereits verdrahtet. F5 (Heavy Cover
nicht setzbar) = vermutlich korrektes Verhalten (Checkbox nur wenn Verteidiger nicht gechargt) →
beim manuellen Test an einer nicht-gechargten Einheit gegenprüfen.

### 🔲 Manuelle UI-Verifikation (S46 — Render-Code, PFLICHT vor „fertig")

- Boss Nob (Boyz/Warbike) mit WAAAGH: **4** Attacken auf Power Klaw legbar; Wound-Block zeigt **S 11**.
- Cover: Dense-Checkbox erscheint im HIT-Block, Light/Heavy im SAVE-Block, **je Tab**; Toggle wirkt.
- F5: Heavy Cover an nicht-gechargter Melee-Einheit lässt sich aktivieren.
- Veil aus dem Nahkampf: danach **kein** „IN MELEE"-Badge; Undo stellt Melee wieder her.
- Skorpekh-Roster (`necrons_alpha`): 2× Threshers + 1× Reap-Blade als getrennte Gruppen.
- **S48 (H1–H7):** Big Mek MA zeigt nur noch mega-blasta + power klaw (bzw. gewählte Swap-Option);
  Silent King: Szarekh hat Sceptre/Staff/Scythe, Menhirs nur Beam; **Living Metal erscheint NICHT
  bei voller HP**; MWBD bei Szarekh **2×** nutzbar (PHAERON); Badges MOVED **blau** / Buffs **grün**
  auch im Silent-King-Roster; RP einmal pro Verteidiger nach „All done".

### 🔲 Roster-Audit (nächster Schritt) — Abweichungsliste VOR Änderung vorlegen

Alle 6 Rosters in `data/rosters/` gegen Datasheets prüfen (Modellzahl, Pflicht-/Wahlwaffen,
Komposition). Nur YAML, `src/` unberührt. Skorpekh (F6) ist bereits erledigt.

---

## Plan-Queue (Executor) — nach den Findings

| Plan | Titel | Prio | Status |
|------|-------|------|--------|
| 014 | P17: Verteidiger-Korrektur Schadenszuweisung (±-Counter pro Gruppe, Snapshot, Waffen-Wegfall) | HOCH | TODO |
| 015 | Reaktive Stratagems: Overwatch, Counter-Offensive, HI-Hook, once_per_battle | MITTEL | TODO |
| 016 | Protokoll-Effekte auf RP (`rp_reroll`/`rp_bonus`) + Dynastiebonus-Anzeige | MITTEL | TODO |
| 017 | SAVE-Block: Fähigkeits-AP kombinierte Badge (`ap_modifier`-Schema) | MITTEL | TODO |
| 018 | Kleinkram: CP-Doppelvergabe (Bug!), Battle-Log-Reset, Gretchin Cowardly, Modifier-Konsolidierung | NIEDRIG | TODO |

Empfohlene Reihenfolge: **014 → 016 → 018 → 015 → 017** (Begründung in `docs/audit/plans/README.md`).
Pläne 014/015 enthalten **Mockup-Stopps** — UI-Layout erst vorlegen, dann implementieren.

---

## Offene Tasks (Backlog, nach Prio)

### 🟡 MITTEL — GOs in gameActionArea
- GO-Buttons kontextuell in gameActionArea (aktiver + inaktiver Spieler), nicht als Liste
- Overwatch (Charge Phase) + Counter-Offensive (Fight Phase) als reaktive GOs
- GOs die Non-CHARACTER-HI erlauben (`enslaved_protectors`) → HI-Eligibility erweiterbar

### 🟡 MITTEL — Necron Command Phase
- Protokoll-Effekte auf Living Metal / RP-Verbesserungen
- Dynastiebonus anzeigen wenn Direktive durch Dynastiezugehörigkeit gilt
- Regelkasten immer ganz oben (alle Phasen prüfen)

### 🟡 MITTEL — SAVE-Block
- Fähigkeit + AP kombiniert als eine Badge (`Enslaved AP-1`) — erfordert YAML-Erweiterung (6j/6l)

### 🟢 NIEDRIG
- Gretchin Cowardly: −1 Attrition wenn kein RUNTHERD in 6" (Ld 4)
- Nach Reset keine alten Einträge im Battle Log (6g)
- CP-Doppelvergabe-Fix + `collect_modifiers_for_phase()` (6e)

---

## Wichtige Constraints (unveränderlich)

- **Freigabe vor Umsetzung** — Plan + Dateiliste zeigen, auf „ja" warten
- **Planergänzung ≠ Freigabe** — Plan neu zeigen, nochmal warten
- **Kein Memory/Subagent/Skill ohne Freigabe**
- dev-Branch, kein direktes Committen auf main
- Seitenleisten: `first_player` links, `second_player` rechts (unveränderlich)
- Keywords immer `UPPERCASE` in YAML
- `_parse_strength(raw: int|str, unit_strength)` für Waffenstärke — akzeptiert native YAML-Typen;
  nie `int(strength)`/`str(strength)` direkt. `User×N`/`User+N`/`User-N` werden akzeptiert.
- Weapon strength in YAML: plain int = fest, `"+N"` = User+N, `"×N"` = User×N, `"User"` = User
- Regelreferenz: Immer erst lokal (`docs/work/wahapedia_*/`), nie Nutzer fragen
- **Generisch:** keine Fraktions-Checks in `src/` — alle Fraktions-Entscheidungen über YAML

---

## Architekturmuster

### ModelGroup-Pattern (6m)

Einheiten mit strukturell verschiedenen Modellen (z.B. Boyz: 9 Boys + 1 Boss Nob) via `model_groups`
in `units.yaml`. Drei Typen:
- **Homogen:** synthetische Einzelgruppe im Loader (Plan 013)
- **Strukturell gemischt:** `count: 1` / `count: remainder`; Roster-Swap aufgelöst
- **Per-Model:** `scope: per_model`; Loader splittet in Sub-Gruppen

State: `unit_state["group_models"]: dict[str,int]`; `models` = Summe. Tod: `apply_damage()` reduziert
nach `priority` (1 = stirbt zuerst). UI: subUnitCard pro Gruppe, Gruppe-für-Gruppe-Deklaration.
**Offen (Block A):** per-Gruppe-Stat-Overrides (`attacks`/`strength`/`wounds`/`ws`/`bs`).

### Reset-Button-Pattern für Fähigkeits-gesetzte Zustände

Setzt eine Fähigkeit/ein Relikt einen Zustand (z.B. `turn_flags`), MUSS es eine Undo-Möglichkeit
geben solange der Zug läuft:
- `turn_flags["<ability>_locked"] = True` beim Aktivieren (Unterscheidung zu normalem Zug)
- Phase-UI: bei `_locked` Buttons deaktivieren + Undo-Button zeigen
- Undo löscht `_locked` und setzt betroffene Felder zurück
- Nach Zugwechsel (`reset_turn_flags`): `_locked`-Flags weg → State „fest"
- Beispiel: Veil of Darkness (`movement_locked`) in `movementPhase.py`

---

## Regelerkenntnisse (nicht-offensichtlich)

- **WAAAGH! Stage 1:** Nur ORKS CORE/CHARACTER dürfen nach Advance chargen; +1 S/+1 A für ALLE ORKS.
  Aktivierung erfordert WARBOSS-WARLORD (App prüft pragmatisch nur WARBOSS-Keyword).
- **Cover:** Dense (−1 Hit) + Light (+1 Save) NUR Shooting; Heavy (+1 Save) NUR Melee, außer der
  Verteidiger hat selbst gechargt.
- **Veil of Darkness:** „remove & set up 9"+ weg" — laut RAW auch aus Engagement Range nutzbar;
  danach `in_melee` clearen (F7).
- **Resurrection Orb / RP:** keine KERN-Einschränkung; gilt für `<DYNASTY>`-Einheiten. RP-Gate über
  `unit.rules` (nicht `keywords`).
- **FNP:** gilt für normale UND tödliche Wunden; pro Wunde nur eine Ignore-Regel.
- **Fight Phase:** startet mit **inaktivem** Spieler; CHARGED zuerst, dann abwechselnd.
- **Heroic Intervention:** Schritt 2 der Charge Phase, nur CHARACTER, ≤3", näher zum Feind enden.
- **extra_attacks — zwei Klassen:** „+N additional" → `unit.attacks + N`; „+N AND no more than N"
  → fester Cap N (`max_attacks`): attack_squig (2), squighog_jaws (2), squigosaur's_jaws (3),
  grabbin_klaw (1), wreckin_ball (1), butcha_boyz (4), savage_horns_and_hooves (4).
- **Boss-Nob-Waffen:** nur der Boss Nob trägt Spezialwaffen (power klaw, big choppa, killsaw) — bei
  boyz, warbikers, stormboyz, kommandos. Nobz/meganobz/squighog: alle Modelle gleich.
- **Skorpekh Destroyers:** feste Komposition 1 Reap-Blade je 3 Modelle (Rest Threshers) — kein Wahl-Wargear (F6).
