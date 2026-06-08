# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->

## ⚠️ Session-Regeln (immer beachten)

**Zu Beginn jeder Session lesen:**
- `CLAUDE.md` — Workflow, Freigabe-Pflicht, **Unklarheiten IMMER zuerst fragen**
- `docs/goals/ziel6.md` — vollständige Aufgabenliste mit allen Checkboxen

**Am Ende jeder Session:**
- Checkboxen in `docs/goals/ziel6.md` abhaken
- Diese Datei aktualisieren: Stand + nächster Schritt + neue Erkenntnisse (ZUERST lesen, dann ergänzen)

---

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Start: `streamlit run src/app.py` (Port 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Aktueller Stand (nach Session 28, 2026-06-08)

- Ziel 1–5 vollständig abgeschlossen
- Ziel 6a–6k vollständig committed (inkl. 6j YAML-Konsolidierung)
- 6d-v3 Würfel-UI vollständig (Treffer/Verwundung/Save-Blöcke mit SVG-Würfeln, Modifier-Paaren, 7+-Handling)
- Cover: 3 phasengebundene Checkboxen (Dense → HIT, Light/Heavy → SAVE)
- Fight Phase: beide Spieler alternieren korrekt; CHARGED-Priorität; inaktiver Spieler startet
- Heroic Intervention: Step-2-Timing, CHARACTER-Check, Badge, Feind-Zielauswahl
- 6k: `persistent_effects` Interpreter; `wargear_ids`/`wargear_keywords` auf Unit; Resurrection Orb via Wargear-ID
- 6j: `weapon_abilities.yaml` + `wargear_abilities.yaml` gelöscht; alle YAML-Header vereinheitlicht
- Session 27: Fix A+D (wargear_used generisch, Bearer via session key); Fix B (WAAAGH!-UI generisch); Fix C (Protokoll-Keys auf faction_dir-Scope)
- **Session 28 neu:** CLAUDE.md Generic-src/-Regel ✅; WAAAGH! Advance+Charge (ORKS CORE/CHARACTER, Stage 1) ✅; WAAAGH! +1 Attacks in Melee-Deklaration (Stage 1+2) ✅; Nahkampf-Deklaration: per-weapon atk_counter, kein Multiselect im Melee-Pfad ✅
- 485 Tests grün

---

## Nächste Schritte (priorisiert)

1. **6l Relic-Effekt-Interpreter** — Schema noch nicht spezifiziert; zuerst alle Necron + Ork Relics in `docs/work/` lesen, dann Schema vorschlagen, Freigabe einholen
2. **GOs in gameActionArea** — kontextuelle GO-Buttons für aktiven + inaktiven Spieler
3. **Necron Command Phase** — Protokoll-Effekte auf Living Metal / RP-Verbesserungen; Dynastiebonus; Anzeigereihenfolge
4. **6h Fix B** — WAAAGH!-UI vollständig generisch (armyCard.py); **Fix C** — Protokoll-Keys per Fraktion (bereits committed, ggf. Nacharbeit)
5. **WAAAGH! Gretchin Cowardly** — Moralphase: −1 Attrition wenn kein RUNTHERD in 6"

---

## Offene Tasks

### 🟡 MITTEL — GOs in gameActionArea

- [ ] GO-Buttons kontextuell direkt in gameActionArea (aktiver + inaktiver Spieler), nicht als Liste
- [ ] Overwatch als reaktive GO in Charge Phase
- [ ] Counterattack GO in Fight Phase (reaktive Unterbrechung) — Teil von 6e
- [ ] GOs die Non-CHARACTER HI erlauben (z.B. `enslaved_protectors`) → HI-Eligibility erweiterbar

### 🟡 MITTEL — Necron Command Phase

- [x] Living Metal: einmalig pro Phase ✅ (2026-06-08)
- [ ] Protokoll-Effekte auf Living Metal / RP-Verbesserungen abbilden
- [ ] Dynastiebonus: wenn Direktive durch Dynastiezugehörigkeit gilt → Effekt anzeigen
- [ ] Anzeigereihenfolge: Regelkasten immer ganz oben in allen Phasen

### 🟡 MITTEL — WAAAGH!

- [x] WAAAGH!-Badge auf unitCards ✅ (2026-06-08)
- [x] **Advance & Charge:** `chargephase.py` — WAAAGH! Stage 1 + ORKS CORE/CHARACTER → advanced-Block überspringen ✅ (2026-06-08)
- [x] **+1 Attacks:** `render_attack_declaration` → `_total_attacks_int()`: +1 auf `unit.attacks` wenn WAAAGH! aktiv + ORKS-Keyword; gilt für Stage 1 und Stage 2 ✅ (2026-06-08)

### ✅ Nahkampf-Deklaration regelkonform — ERLEDIGT (2026-06-08)

Melee-Pfad auf per-weapon `atk_counter` umgestellt. Jede Waffe bekommt eigenen Counter pro Ziel (kein Multiselect mehr). Summe aller Counters = Gesamtattacken. 15 neue Tests.

### 🟡 MITTEL — Fähigkeit + AP kombiniert (SAVE-Block)

- [ ] `Enslaved AP-1` o.ä. als kombinierte Badge darstellen — erfordert 6j/6l YAML-Erweiterung

### 🟢 NIEDRIG

- [ ] Gretchin Cowardly: −1 auf Combat Attrition Tests wenn kein RUNTHERD in 6" (Ld 4)
- [ ] Nach Reset keine alten Einträge im Battle Log (6g)
- [ ] CP-Doppelvergabe-Fix + `collect_modifiers_for_phase()` (6e)
- [ ] Hardcoded Fraktionslogik herauslösen (6h)

---

## Wichtige Constraints (unveränderlich)

- **Freigabe vor Umsetzung** — Plan + Dateiliste zeigen, auf „ja" warten
- **Planergänzung ≠ Freigabe** — Plan neu zeigen, nochmal warten
- **Kein Memory/Subagent/Skill ohne Freigabe**
- dev-Branch, kein direktes Committen auf main
- Seitenleisten: `first_player` links, `second_player` rechts (unveränderlich)
- Keywords immer `UPPERCASE` in YAML
- `_parse_strength()` für Waffenstärke, nie `int(strength)` direkt
- Regelreferenz: Immer erst lokal nachschlagen (`docs/work/wahapedia_*/`), nie Nutzer fragen

---

## Regelerkenntnisse (nicht-offensichtlich)

- **WAAAGH! Stage 1:** Nur ORKS CORE und ORKS CHARACTER dürfen nach Advance chargen (nicht alle ORKS). +1 Strength und +1 Attacks gilt für ALLE ORKS-Modelle. GRETCHIN-Ausnahme gilt nur für Waaagh! Energy-Zählung.
- **WAAAGH! Aktivierung:** Erfordert, dass der WARLORD ein WARBOSS ist (nicht nur irgendein WARBOSS auf dem Feld). Aktuell prüft die App nur ob irgendeine Einheit das WARBOSS-Keyword hat — streng genommen müsste der WARLORD-Status geprüft werden (noch nicht implementiert, pragmatische Näherung akzeptiert).
- **Resurrection Orb**: Keine KERN-Einschränkung — gilt für alle `<DYNASTY>`-Einheiten.
- **FNP**: Gilt für alle Wunden — normale UND tödliche. Pro Wunde nur eine Ignore-Regel verwendbar.
- **Fight Phase**: Startet mit dem **inaktiven** Spieler. CHARGED-Einheiten aller Spieler kämpfen zuerst, dann abwechselnd.
- **Heroic Intervention**: Schritt 2 der Charge Phase (nach allen Charges). Nur CHARACTER. ≤3" Bewegung, muss näher zum nächsten Feind enden.
