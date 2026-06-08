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

## Aktueller Stand (nach Session 27, 2026-06-08)

- Ziel 1–5 vollständig abgeschlossen
- Ziel 6a–6k vollständig committed (inkl. 6j YAML-Konsolidierung)
- 6d-v3 Würfel-UI vollständig (Treffer/Verwundung/Save-Blöcke mit SVG-Würfeln, Modifier-Paaren, 7+-Handling)
- Cover: 3 phasengebundene Checkboxen (Dense → HIT, Light/Heavy → SAVE)
- Fight Phase: beide Spieler alternieren korrekt; CHARGED-Priorität; inaktiver Spieler startet
- Heroic Intervention: Step-2-Timing, CHARACTER-Check, Badge, Feind-Zielauswahl
- 6k: `persistent_effects` Interpreter; `wargear_ids`/`wargear_keywords` auf Unit; Resurrection Orb via Wargear-ID
- 6j: `weapon_abilities.yaml` + `wargear_abilities.yaml` gelöscht; alle YAML-Header vereinheitlicht
- Session 26: Living Metal einmalig pro Phase; WAAAGH!-Badge auf unitCards; Attack-Splitting Single-Modell; `"*"`-Bug gefixt
- **Session 27 neu:** Fix A+D (wargear_used generisch, Bearer via session key) ✅; Fix B (WAAAGH!-UI: once_per_battle, check_conditions, active_text) ✅; Fix C (Protokoll-Keys auf faction_dir-Scope) ✅
- 470 Tests grün

---

## Nächste Schritte (priorisiert)

1. **WAAAGH! Advance+Charge** — `chargephase.py`: advanced-Block überspringen wenn WAAAGH! Stage 1 + ORKS CORE/CHARACTER (Details: §Offene Tasks)
2. **WAAAGH! +1 Attacks** — `_common.py`: WAAAGH! +1 auf `unit.attacks` in Deklarations-Attackenberechnung addieren
3. **Nahkampf-Deklaration regelkonform** — Jede Attacke deklariert (Waffe × Ziel); Plan zeigen + Freigabe einholen vor Implementierung (Details: `docs/goals/ziel6.md §Nahkampf-Deklaration`)
4. **6l Relic-Effekt-Interpreter** — Schema noch nicht spezifiziert; zuerst alle Necron + Ork Relics durchgehen, dann Schema vorschlagen, Freigabe einholen
5. **GOs in gameActionArea** — kontextuelle GO-Buttons für aktiven + inaktiven Spieler

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
- [ ] **Advance & Charge:** `chargephase.py` — wenn WAAAGH! Stage 1 aktiv + Einheit hat ORKS CORE oder ORKS CHARACTER → advanced-Block überspringen; Einheit darf trotzdem chargen
- [ ] **+1 Attacks:** In `render_attack_declaration` → `_total_attacks_int()`: WAAAGH-Modifier (+1) auf `unit.attacks` addieren bevor Gesamtattacken berechnet werden; gilt für Stage 1 und Stage 2

### 🔴 HOCH — Nahkampf-Deklaration regelkonform

**Problem:** Aktuelle Deklaration wählt Waffe pro Ziel (Multiselect). Bei 2 Waffen auf dasselbe Ziel zeigt die App für jede Waffe die volle Attackenzahl → Doppelzählung. Regel verlangt, dass jede Attacke (Waffe × Ziel) einzeln deklariert wird und die Summe gleich den Gesamtattacken ist.

**Regel (core_rules.txt Z. 1995–2040):**
- Vor Auflösung: Ziel(e) + Waffe(n) für ALLE Attacken deklarieren
- Jede Attacke wählt genau eine Waffe und genau ein Ziel
- Attacken können frei zwischen Zielen UND Waffen aufgeteilt werden
- Auflösungsreihenfolge: erst alle Attacken gegen Ziel A, dann Ziel B; innerhalb eines Ziels erst alle Attacken mit Profil X, dann Profil Y

**Lösung:** Deklarationsstruktur auf `(weapon, profile, target, attacks)` umstellen:
- Gesamtattacken = `models_alive × unit.attacks` (+ WAAAGH! falls aktiv)
- UI: Für jede Waffe + jeden Ziel-Kombination: Eingabe wie viele Attacken
- Validierung: Summe aller Einträge ≤ Gesamtattacken; Warnung bei Unter-/Überzählung
- Gilt einheitlich für Single- und Multi-Modell-Einheiten (model-counter entfällt für melee)

**Betroffene Dateien:** `uiLayout/_common.py` (render_attack_declaration + Eintrags-Struktur), `gameMechanic/fightPhase.py`

- [ ] Plan zeigen + Freigabe einholen bevor Implementierung beginnt

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
