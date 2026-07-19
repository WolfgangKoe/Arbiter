STATUS: NEEDS-DECISION

# Planning — S170 (2026-07-19)

**Priorität:** P1 (B-028c1 verifikations-Nacharbeiten + b3 abschließen)
**Scope:** S169-Retro-Maßnahmen in die Artefakte überführen, die 4 b2-UI-Nacharbeiten
(2 davon spec-first) umsetzen, P-16-Screenshots in In-Spec-Diagramme migrieren, b3
`auto_explode`-GO bauen — bis B-028c1 b1+b2 verifiziert abgehakt werden können.

> Token-Schätzungen tragen bereits den **Faktor ×1,5** (Retro-M2 S169). Kein Brief > Effort M.
> Entscheidungs-Tasks (T0) stehen bewusst zuerst; T2 ist ein Spec-first-Gate mit Stakeholder-
> Abnahme, das T4a/T4d blockiert.

---

## 0. Merkzeilen (kein Subagent-Task)

- **M3-Allowlist** (`S169_M3_ALLOWLIST.md`): Koordinator + Stakeholder tragen die zwei
  `.claude/settings.json`-Regeln **gemeinsam im Chat** ein (Classifier blockiert Claude-seitige
  Permission-Änderung). Danach Datei löschen. Kein Subagent, kein Umsetzungs-Task.
- **Stakeholder-Frage „NO in NO-GO":** „NO-GO" = „No-Go" (nicht freigegeben) — Standard-
  Reviewer-Vokabular, nicht vom Stakeholder eingeführt. Koordinator beantwortet im Chat.
- **§6-vs-§4.4-Interpretation** (s. T0): offene Bestätigung, kein Umsetzungsaufwand.

---

## 1. Task-Tabelle (ganze Session, Start → Commit)

| # | Aufgabe | Effort | Token ×1,5 | Modus | Subagent + Tier | Scope / Dateien |
|---|---------|--------|-----------|-------|-----------------|-----------------|
| **T0** | **Entscheidungs-Block** (früh, voller Headroom): (a) §6-vs-§4.4 bestätigen; (b) Spec-first-Abnahme T2 einholen; (c) Sequenz/Cut-Line dieser Session bestätigen | XS | — (Chat/Mailbox) | **Konsens** | Koordinator | `S169_RETRO.md`, dieses Planning |
| **T1** | Retro **M1** (Lösch-Whitelist-Standardsatz: Pflicht-Grep Voll- UND Kurzname über `docs/`+`src/`, alle Dateitypen) + **M2** (Token-Schätzfaktor ×1,5, Selbst-Stopp 2×, Split > 250k) in `agent_scopes.md` verankern | XS | ~45k | Konsent | Executor + **Haiku** | `docs/reference/agent_scopes.md` (Standardsatz Doku-Briefs §M3-S158-Block + Auftragsgrößen-Gate) |
| **T2** | **Spec-first-Vorlage** für Nacharbeit **a** (Layout: Binärwurf-Kachel + Info-Kasten nur über die `playerArea` des besitzenden Spielers, nicht ganze `gameActionsArea`) und **d** (Direkt-Apply beim Zuweisen + Reset-Rückgängig + Rückkehr-in-State nach Confirm; Sort-to-top ist in §1.7 Z.203 bereits spezifiziert) → `processes.md` P-16 Schritt 5/6 + `design_system.md` §1.7/§1.9 anpassen, **dem Stakeholder zur Abnahme vorlegen** | S | ~60k | **Konsens** (NEEDS-DECISION) | Executor + **Sonnet** | `docs/spec/processes.md` (P-16), `docs/spec/design_system.md` (§1.7, §1.9) |
| **T3** | **Screenshot→Diagramm-Migration P-16:** die **5** `Bildschirmfoto…png`-Referenzen in `processes.md` in korrigierbare ASCII/Markdown-Diagramme direkt in der Spec übertragen, dann Referenz-Block + die 5 PNG-Dateien entfernen (Lösch-Whitelist nach T1-M1: Grep Voll+Kurzname vor Löschung) | S | ~60k | Konsent | Executor + **Sonnet** | `docs/spec/processes.md` (§Screenshot-Referenzen Z.784–795), `docs/handoff/*.png`, `agent_scopes.md` §e (Screenshot-Konvention-Verweis prüfen) |
| **T4-bc** | b2-Nacharbeit **b** (Hinweis-Block „► … zuerst vollständig zerstören." entfernen, `_common.py:2188`) + **c** (fehlende Reset-Buttons: Explosionswurf-Karte bei Erfolg UND Misserfolg, sowie nach Confirm des verteilten Schadens) | S | ~110k | Gate | Executor + **Sonnet** | `src/uiLayout/_common.py` (`_render_explode_roll`, `_render_explode_outcome`, `_render_explode_target_panel`, Z.2188) |
| **T4-a** | b2-Nacharbeit **a** — Layout-Constrain (blockiert durch T2-Abnahme) | S | ~90k | Gate | Executor + **Sonnet** | `src/uiLayout/_common.py` (`render_explode_tiles_for_destroyed`, `_render_explode_tile`), `design_system.md` §1.9 |
| **T4-d** | b2-Nacharbeit **d** — Verhaltensänderung: Schaden direkt beim Zuweisen je Einheit anwenden (LP live, auch bei Zerstörung), gewählte Einheit in ihrer armyList nach oben sortieren, „Reset" macht Zuweisungen rückgängig, nach „Confirm" Rückkehr in denselben Vor-Bestätigungs-State (Korrektur möglich). **Blockiert durch T2-Abnahme.** Core+UI+State-Mix → ggf. splitten | M | ~190k | Gate | Executor + **Sonnet** | `src/uiLayout/_common.py` (`_render_explode_target_panel`, `_render_explode_tile`), `src/gameMechanic/unitMutations.py` (`apply_damage`), `gameState.py` |
| **T5** | **b3 `auto_explode`-GO** — echte GO (Standard-GO-Karte §6.1) an der Kachel-Gruppe (Baustein ②), CP 1/3 (TITANIC), `[Use]` ersetzt den Binär-Wurf; `on_destroy`/`phase_reactive`-Anker | M | ~190k | Gate | Executor + **Sonnet** | `src/uiLayout/_common.py`, `src/gameMechanic/abilityEngine.py`, `data/wh40k_9e/necrons/stratagems.yaml`, `processes.md` P-16 §`auto_explode` |
| **T6** | **Manuelle UI-Verifikation** (Prüfpunkte s. §2) — nach T4/T5, Handoff-Datei `AWAITING-VERIFICATION` | S | ~60k | Gate | Executor + **Sonnet** | App :8501, Rosters (s. §2) |
| **T7** | **Artefakt-Nachzug** (s. §3) | XS | ~45k | Konsent | Executor + **Haiku** | `backlog.md`, `briefing.md`, Handoff-Lifecycle |
| **T8** | **Abschluss-Dreiklang** Review → Retro → Commit (stehend freigegeben) + `token_report.py --write` + `rotate_history.py` | S | ~120k | Gate/stehend | Reviewer **Opus** + Koordinator | ganze Session |

**Session-Realismus / Cut-Line-Vorschlag (T0c bestätigen):** T1 + T2 + T3 + T4-bc + (T4-a) sind
ein realistischer erster Session-Block. **T4-d (M) und T5 (M)** sind je ein eigener M-Brief und
sprengen zusammen mit dem Rest die ~150k-Korridor-Grenze des Koordinators → Empfehlung: **T4-d
und T5 in eine Folge-Session** ziehen, sonst kein sauberes Abschluss-Fenster. Verifikation (T6)
läuft über das, was in dieser Session wirklich committet ist.

---

## 2. Manuelle UI-Verifikation — konkrete Prüfpunkte (T6)

Voraussetzungen (Roster-Bestand per `ls data/rosters/` verifiziert):
- **Silent King** (Pflicht-Trigger 4+): `necrons_1500pts_silent_king.yaml` ✓ vorhanden.
- **Gunwagon** (2. Pflicht-Trigger-Träger, Single-Model, explodes on 6): `orks_transport.yaml` ✓ —
  deckt den Stakeholder-Wunsch „auch andere Einheiten testen" für den **Pflicht-Trigger-Pfad** ab.
- **Canoptek Spyder** (`necrons_beta.yaml`) ist **Mehrmodell** → eigenes Konzept nötig (briefing),
  **nicht** in dieser Verifikation.
- **`auto_explode`-GO (Curse of the Phaeron)** ist regeltextlich **NECRONS VEHICLE**-only → Gunwagon
  (Ork) kann sie NICHT auslösen. **OFFEN/PREP:** Für die T5-Verifikation muss zuerst ein Roster mit
  einem NECRONS-VEHICLE-Explodes-Träger (Night Scythe / Annihilation Barge) bestätigt/angelegt
  werden (Retro-M2-S160-Pflicht: Testfall-Voraussetzung vor Einplanung prüfen). → Vorbereitungs-Task
  falls kein passendes Roster existiert.
 

Prüfpunkte:
1. **(a-Fix)** Binärwurf-Kachel + Info-Kasten erstrecken sich NUR über die `playerArea` des
   besitzenden Spielers, nicht über die ganze `gameActionsArea`. Multi-Unit-Panel bleibt korrekt
   (war schon ok).
2. **(b-Fix)** Hinweis-Block „► … zuerst vollständig zerstören." erscheint NICHT mehr.
3. **(c-Fix)** Reset-Button ist sichtbar auf der Explosionswurf-Karte bei **Erfolg** UND
   **Misserfolg**, und erneut **nach** Confirm des verteilten Schadens.
4. **(d-Fix)** Zuweisen im Multi-Unit-Panel: LP der gewählten Einheit sinkt **direkt** (auch bis
   zur Zerstörung); die unitCard springt in ihrer armyList nach oben; „Reset" macht die
   Zuweisungen rückgängig; nach „Confirm" kann man in denselben State direkt vor der Bestätigung
   zurückkehren und Fehl-Zuweisungen korrigieren.
5. **(T5)** `auto_explode`-GO-Karte erscheint bei einem NECRONS-VEHICLE-Explodes-Träger; `[Use]`
   (1 CP, 3 CP bei TITANIC) ersetzt den Binär-Wurf, Explosion gilt automatisch → direkt Info-Kasten
   + Multi-Unit-Panel.
6. **Regelkonformität:** App würfelt selbst nicht, Reichweite wird nicht nachgezählt (P-16).

 Das mit dem Gunwaggon war gut. Die entsprechende Go der Orks ist "Careen!", wenn sie keinen auto-Explode GO haben. Es explodiert zwar nicht zwangsläufig, aber es muss vor der Explosion ausgeführt werden.
  Ich habe es auch mit der Spyder getestet und es sieht aktuell gut aus. Es scheint also richtig verdrahtet worden zu sein. Die bisherigen Kommentare gelten immer noch. Es gibt eine weitere Ergänzung. Die Hinweis-Felder nach der explosion (und vielleicht auch, wenn die Explosion nicht erfolgt) werden in darauffolgenden Phasen und Runden permanent angezeigt. Das sollte so nicht sein. Nach der Explosion, sollte beim Phasenwechsel auch der Hinweis-Kachel nicht mehr zu sehen sein. Lediglich im Protokoll sollte es stehen.

---

## 3. Artefakt-Nachzug (T7) + Handoff-Lifecycle

- **B-028c1** bleibt **In Progress**, bis alle Verifikations-Nacharbeiten (a–d) + b3 verifiziert
  sind — b1+b2 sind committet (`40c29a9`), aber die UI-Verifikation ergab Teil-GO mit 4
  Nacharbeiten ⇒ NICHT abhaken.
- `briefing.md`: Stand auf S170, nächsten Schritt fortschreiben (offene M-Tasks T4-d/T5 falls
  vertagt; auto_explode-Roster-Prep).
- **Handoff-Lifecycle:**
  - `S169_PLANNING.md` → nach Sichtung **löschen**.
  - `S169_REVIEW.md` → nur Sichtung (NO-GO bereits in S169 ausgeräumt), dann löschen.
  - `S169_RETRO.md` → nach Überführung M1/M2 in `agent_scopes.md` **löschen** (M3 = Merkzeile).
  - `S169_M3_ALLOWLIST.md` → löschen, sobald Stakeholder die Regeln eingetragen hat (§0).
  - `S169_b2_ui_verifikation.md` → offen halten bis a–d verifiziert, dann durch neue S170-
    Verifikationsdatei ablösen.
  - `Stakeholder_Beobachtungen.md` → STANDING, bleibt.
- Backlog: `B-028c1`-Zeile Fachlichkeits-Kommentar auf „b1+b2 committet S169; b2-Nacharbeiten
  a–d + b3 in S170" aktualisieren.

---

## 4. Backlog-Reihenfolge — Empfehlung (NICHT selbst geändert)

Der Planner hat **kein** Schreibrecht auf `backlog.md`. Empfehlung an den Koordinator, die
offenen Zeilen so zu sortieren, dass die S170-Items oben stehen:
1. **B-028c1** (bereits Zeile 1) — bleibt oben, In Progress.
2. **B-124** (Design-System-Ratchet) — direkt darunter, weil T2/T4 die §1-Registrierung berühren.
3. Rest unverändert. Keine Item-Archivierung in dieser Runde (B-028c1 noch offen).

---

## 5. Offene Entscheidungen / NEEDS-DECISION (T0)

1. **§6-vs-§4.4-Bestätigung** (aus S169): T2 hat statt des wörtlich genannten „§6" den
   Würfel-Abschnitt §4.4 nach P-08 migriert (§6 = GO-Karten, hat keine Würfeldarstellung).
   → Stakeholder: bestätigen oder korrigieren. - Bestätigt.
2. **Spec-first-Abnahme T2** (Layout-Constrain a + Verhalten d): Bauform-/Verhaltensänderung →
   erst Spec-Update (`design_system.md` §1.7/§1.9, `processes.md` P-16) abnehmen, DANN T4-a/T4-d
   codieren. Ohne Abnahme sind T4-a und T4-d blockiert. - Bitte in einer Handoff-Datei zeigen bzw. darauf verlinken, dann kann ich es abnehmen.
3. **Session-Cut-Line:** T4-d (M) + T5 (M) in dieser Session ODER Folge-Session? Empfehlung:
   vertagen (Korridor). → Stakeholder bestätigt Umfang. - Vertagen wir es.
4. **`auto_explode`-Test-Roster:** existiert kein NECRONS-VEHICLE-Explodes-Roster, wird ein
   Vorbereitungs-Task nötig (Night Scythe / Annihilation Barge ins Roster). → vor T5-Verifikation. - Diese Entscheidung verstehe ich nicht. Annihilation Barge ist im Roster. Das können wir so lassen. Die auto-explode-GO scheint einfahc noch nicht implementiert oder verdrahtet zu sein. Ich kann diese jedenfalls nicht sehen.

---

## 6. Zähl-Belege (grep/wc)

- **Screenshot-Referenzen in `processes.md` (T3-Scope):** `grep -rn "Bildschirmfoto" docs/spec/`
  → **5** PNG-Referenzen (Z. 791–795) + 1 Header (Z. 784) + 1 Tabellenkopf (Z. 789). Zusätzlich
  2 Screenshot-Erwähnungen in `design_colors.md` (Z. 23/88) — **außerhalb P-16-Scope**, nicht
  anfassen.
- **Explode-Kachel-Aufrufstellen:**
  `grep -rn "render_explode_tiles_for_destroyed" src/gameMechanic/*Phase.py` → **5** Call-Sites
  (chargePhase:46, shootingPhase:89, psychicPhase:43, movementPhase:73, fightPhase:389), je mit
  Import — alle 5 Phasen verdrahtet.
- **Render-Funktionen (Nacharbeits-Ziele) in `_common.py`:** `_render_explode_roll` (Z.519),
  `_render_explode_target_panel` (Z.548), `_render_explode_outcome` (Z.621), `_render_explode_tile`
  (Z.639), `render_explode_tiles_for_destroyed` (Z.688).
- **Menhir-Hinweis-Block (T4-b):** `_common.py:2188`
  `dmg_col.warning(f"► **{locked.name_en}** zuerst vollständig zerstören.")` — genau 1 Stelle.
- **Sort-to-top bereits spezifiziert:** `design_system.md:203` „Ausgewählte Einheit springt in
  ihrer armyList-Sidebar (§1.9) an die erste Position" — d-Teil „nach oben sortieren" ist in der
  Spec bereits vorhanden, nur Code fehlt (kein Spec-Neuland für diesen Teilpunkt).
- **Explodes-Träger in Rosters:** Silent King (`necrons_1500pts_silent_king.yaml`), Gunwagon
  (`orks_transport.yaml`, Single-Model Pflicht-Trigger), Canoptek Spyder (`necrons_beta.yaml`,
  Mehrmodell → out of scope).
- **Git-Abgleich:** `40c29a9 Close S169` enthält b1+b2 → als committet bestätigt; keine stale
  Checkbox für B-028c1 (Item steht korrekt „In Progress", nicht abgehakt).

**Nächster Schritt:** T0-Entscheidungen einholen → T1 (Haiku) parallel zu T2 (Sonnet, Spec-first-
Abnahme) → nach Abnahme T3/T4.
