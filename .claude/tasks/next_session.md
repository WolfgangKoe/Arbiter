# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## ⚠️ Session-Regeln (immer beachten)

**Zu Beginn jeder Session lesen:**
- `CLAUDE.md` — Workflow, Freigabe-Pflicht, Code-Qualität, Branch-Strategie
- `docs/goals/ziel6.md` — aktueller Ziel-6-Stand: Spec, Checkliste, offene Punkte

**Am Ende jeder Session:**
- `docs/goals/ziel6.md` aktualisieren: Checkboxen abhaken, neue Erkenntnisse ergänzen, nächste Schritte fortschreiben

---

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Aktueller Status

| Ziel | Status |
|------|--------|
| Ziel 1–4 — Grundgerüst, Phasen, UI | ✅ fertig |
| **Ziel 5 — Setup & Datenlage** | ✅ 2026-06-03 |
| **Ziel 6 — [nächster Schritt]** | ⬜ wird in nächster Session definiert |
| Ziel 7 — Crusade-Erweiterung | ⬜ |
| Ziel 8 — Wahapedia Faction Fetcher | ⬜ |

Details: `docs/goals/index.md`

---

## Nächste Schritte

### Ziel 6 definieren

`docs/goals/ziel6.md` ist noch ein Platzhalter. Zu Beginn der nächsten Session:

1. Ziel 6 gemeinsam spezifizieren — wahrscheinlich Kampfmechanik vertiefen:
   - Volle Attack-Sequenz (To Hit, To Wound, Save, Damage)
   - Mortal Wounds
   - Command Re-Roll als Stratagem korrekt verdrahtet
   - Oder etwas anderes — erst besprechen, dann festlegen
2. Spec in `docs/goals/ziel6.md` schreiben
3. Implementieren

---

## Bekannte offene Lücken

| Lücke | Beschreibung | Priorität |
|-------|-------------|-----------|
| Adeptus Custodes | Nur Placeholder-Dateien — kein spielbarer Katalog | Nach Ziel 8 |

---

## Wichtige Constraints

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts
- Setup-Buttons: `player_slots` verwenden, NICHT `first_player`/`second_player`
- dev-Branch — kein direktes Committen auf main
- **Keywords immer `UPPERCASE` in YAML** — Checks via `unit.has_keyword()`
- Weapon-Zugriff mit Dual-Profile: `w.for_phase(use_melee)` — nicht `w.is_melee`
- Session-State Unit-Keys: `p1_units` / `p2_units` mit `#N`-Suffix für Duplikate
- Weapon strength: `_parse_strength()` in `_common.py` — nie direkt `int(profile.strength)`

### State-Key System

Mehrfach-Units gleichen Typs werden mit `#N`-Suffix disambiguiert:
- Erstes Vorkommen: `wh40k_9e.necrons.unit.warriors`
- Zweites Vorkommen: `wh40k_9e.necrons.unit.warriors#1`

`unit_id_from_state_key(key)` → echte `unit.id`.
`lookup(faction, uid)` in `_common.py` versteht State-Keys.

### Streamlit 1.57 — CSS-Selektoren

Vor dem Schreiben von CSS-Overrides immer JS-Source prüfen — Emotion-Klassen ändern sich zwischen Versionen.

| Komponente | Korrekte Selektoren |
|---|---|
| NumberInput Container | `[data-testid="stNumberInputContainer"]` |
| NumberInput Step-Buttons | `[data-testid="stNumberInputStepUp"]`, `[data-testid="stNumberInputStepDown"]` |
| Buttons allgemein | `button[data-testid="stBaseButton-{kind}"]` |
| Container border=True | `.e1rw0b1u3` (Emotion-Klasse — prüfen bei Streamlit-Update!) |
| Selectbox | `.stSelectbox [data-baseweb="select"] > div` |
