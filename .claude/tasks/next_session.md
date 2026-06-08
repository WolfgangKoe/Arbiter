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

## Aktueller Stand (nach Session 25, 2026-06-07)

- Ziel 1–5 vollständig abgeschlossen
- Ziel 6a–6k vollständig committed (inkl. 6j YAML-Konsolidierung)
- 6d-v3 Würfel-UI vollständig (Treffer/Verwundung/Save-Blöcke mit SVG-Würfeln, Modifier-Paaren, 7+-Handling)
- Cover: 3 phasengebundene Checkboxen (Dense → HIT, Light/Heavy → SAVE)
- Fight Phase: beide Spieler alternieren korrekt; CHARGED-Priorität; inaktiver Spieler startet
- Heroic Intervention: Step-2-Timing, CHARACTER-Check, Badge, Feind-Zielauswahl
- 6k: `persistent_effects` Interpreter; `wargear_ids`/`wargear_keywords` auf Unit; Resurrection Orb via Wargear-ID
- 6j: `weapon_abilities.yaml` + `wargear_abilities.yaml` gelöscht; alle YAML-Header vereinheitlicht
- 470 Tests grün

---

## Nächste Schritte (priorisiert)

1. **Necron Command Phase Fixes** — Living Metal einmalig, Dynastiebonus-Anzeige (Details: `docs/goals/ziel6.md §Testsession-Fixes`)
2. **WAAAGH!-Badge** auf unitCards (alle ORKS-Einheiten, keine Ausnahmen)
3. **Fight Phase Declaration-Block** — 6d-v3-Layout + Attacken regelkonform auf Zieleinheiten verteilen
4. **6l Relic-Effekt-Interpreter** — `ability_en` in maschinenlesbare `trigger:` + `effect:` überführen (Spec: `docs/goals/ziel6.md §6l`)

---

## Offene Tasks

### 🔴 HOCH — Nahkampf: Attacken auf Zieleinheiten verteilen

**Bug:** Regelkonform müssen Attacken auf **Einheiten** verteilt werden, nicht auf Modelle. Ein Overlord mit 4 Attacken darf 2+2 auf zwei Einheiten aufteilen. Fix im Zuge der 6d-v3-Überarbeitung des Declaration-Blocks umsetzen.

### 🟡 MITTEL — GOs in gameActionArea

- [ ] GO-Buttons kontextuell direkt in gameActionArea (aktiver + inaktiver Spieler), nicht als Liste
- [ ] Overwatch als reaktive GO in Charge Phase
- [ ] Counterattack GO in Fight Phase (reaktive Unterbrechung) — Teil von 6e
- [ ] GOs die Non-CHARACTER HI erlauben (z.B. `enslaved_protectors`) → HI-Eligibility erweiterbar

### 🟡 MITTEL — Necron Command Phase

- [ ] Living Metal: einmalig pro Phase (aktuell mehrfach anwendbar)
- [ ] Protokoll-Effekte auf Living Metal / RP-Verbesserungen abbilden
- [ ] Dynastiebonus: wenn Direktive durch Dynastiezugehörigkeit gilt → Effekt anzeigen
- [ ] Anzeigereihenfolge: Regelkasten immer ganz oben in allen Phasen

### 🟡 MITTEL — WAAAGH!

- [ ] WAAAGH!-Badge auf unitCards der betroffenen Einheiten (alle ORKS — keine Ausnahmen laut Regeltext)

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

- **WAAAGH!**: Keine Einheiten-Ausnahmen — alle ORKS-Modelle profitieren. GRETCHIN-Ausnahme gilt nur für "Waaagh! Energy"-Zählung, nicht für WAAAGH! selbst.
- **Resurrection Orb**: Keine KERN-Einschränkung — gilt für alle `<DYNASTY>`-Einheiten.
- **FNP**: Gilt für alle Wunden — normale UND tödliche. Pro Wunde nur eine Ignore-Regel verwendbar.
- **Fight Phase**: Startet mit dem **inaktiven** Spieler. CHARGED-Einheiten aller Spieler kämpfen zuerst, dann abwechselnd.
- **Heroic Intervention**: Schritt 2 der Charge Phase (nach allen Charges). Nur CHARACTER. ≤3" Bewegung, muss näher zum nächsten Feind enden.
