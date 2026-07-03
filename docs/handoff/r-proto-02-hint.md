ANSWERED

# R-PROTO-02 — UI-Hinweis für Conquering-Tyrant-Direktive 1 (Aura-Range +3", max 12")

## IST (belegt)

**1. Wo werden Protokoll-Direktiven gewählt/angezeigt?**

`src/uiLayout/armyCard.py`, drei Render-Pfade (alle für `round_choice`-Fähigkeiten,
Necrons Sautekh-Dynastie „Protocol of the Conquering Tyrant" ist eine davon):

- `_render_round_choice_ui()` (Z. 272–…) — Haupt-Direktive des Runden-Slots. Sobald
  `active_directive` gesetzt ist (Z. 325–331), rendert sie:
  ```python
  badge_text = f"{short_round_choice_label(p.name_en).upper()} — {active_directive.upper()}"
  st.markdown(_active_ability_badge(badge_text), unsafe_allow_html=True)
  chosen_text = p.primary if active_directive == "primary" else p.secondary
  st.caption(f"↳ {chosen_text}")
  ```
  → Zeile 331 ist die Stelle, an der der Rule-Text der gewählten Direktive erscheint.
  **Hier fehlt der Tisch-Hinweis.**

- `_render_extra_round_choice()` (Z. 206–269) — die „6th / always-active" Direktive
  (Dynastie-Sonderfall). Analoge Stelle: Z. 232–238 (`extra_directive` gesetzt) und
  Z. 225–229 (`affinity_bonus`-Zweig, beide Direktiven simultan aktiv — Dynastie-Bonus).

- `gameProtocoll.py` (Battle-Log/Stratagems-Tab) behandelt **nicht** die Direktiven-Wahl,
  nur Stratagems + Log — kein Ziel für diesen Hinweis.

**2. Existiert bereits ein Muster für `enforcement: table`-Hinweise?**

Ja, zweifach belegt:

- **Design-Konvention** `docs/spec/design_system.md` §3 (S115, verbindlich) definiert
  den Hinweistyp `info` exakt für diesen Fall: *„Neutraler Hinweis, keine Wertung
  (Regel-Erinnerung, Tisch-Hinweis Klasse B/C)"* — **Beispiel in der Tabelle ist wörtlich
  „Aura-Range-Hinweis"**, also unser R-PROTO-02-Fall. Farbe: `--arb-blue`. Rendering:
  über `st.info()` (analog zu `warning` → `st.warning()`, s. §3 Zeile 89).
- **Code-Präzedenz** (`ignore_cover_half_range`, Vengeful Stars D2 — gleiche Klasse
  B/hybrid, Kommentar in `ability_engine.py` Z. 243–246: „App only surfaces the hint
  inline"): dort wird kein `st.info()` benutzt, sondern das Label über
  `get_short_label_for_effect_type()` in ein Checkbox-Label eingebettet
  (`_common.py` Z. 1104–1125), weil der Spieler dort noch etwas ankreuzt. Für
  Aura-Range gibt es aber **keine** Checkbox/Interaktion — reiner Text-Hinweis, daher
  passt `st.info()` direkt besser als das Checkbox-Label-Muster.
- Bestehender Test dokumentiert die Schuld direkt und nennt den Zielort selbst:
  `tests/uiLayout/test_common.py::test_conquering_tyrant_protocol_directive_primary_loaded`,
  Docstring: *„UI display … NOT yet implemented (`_render_rp_block or similar`)"*.
  (Zielort dort nur vage benannt — die Recherche oben lokalisiert ihn präzise in
  `armyCard.py`, nicht `_common.py`.)

**3. Zugriffspfad auf die Direktiven-Daten zur Laufzeit (datengetrieben)**

`src/gameMechanic/ability_engine.py` bietet bereits generische, faction-agnostische
Helfer, die exakt für diesen Zweck gebaut sind:

- `_active_directive_has_type(player: str, effect_type: str) -> bool` (Z. 235–237) —
  prüft ob irgendeine aktive Direktive (Runden-Slot ODER 6th/Dynastie) den gegebenen
  `effect.type` hat. Aufruf: `_active_directive_has_type(faction, "aura_range_bonus")`.
- `get_active_protocol_effects(player, types) -> list[dict]` (Z. 310–321) — liefert die
  vollen Effekt-Dicts (inkl. `value`, `max`, `_source_id`) für Label-/Text-Aufbau, falls
  der Hinweistext Zahlen aus der YAML ziehen soll statt sie hart zu codieren.
- `get_short_label_for_effect_type(player, effect_type) -> str | None` (Z. 286–307) —
  löst den Anzeigenamen der tatsächlichen Quell-Direktive auf (wichtig, falls sowohl
  Runden- als auch 6th-Direktive `aura_range_bonus` tragen könnten — Label bleibt korrekt).

Alle drei sind bereits in `armyCard.py` importierbar (Modul importiert schon aus
`gameMechanic.ability_engine`, Z. 16–21) — kein neuer Fraktions-String nötig. Der Hinweis
kann komplett generisch bleiben: *„zeige `st.info()` mit `value`+`max` aus dem Effekt-Dict,
wenn `_active_directive_has_type(faction, "aura_range_bonus")` true ist"* — funktioniert für
jede Fraktion/jedes Protokoll, das künftig `aura_range_bonus` nutzt, nicht nur Necrons.

## Vorschlag Anzeige-Ort

`src/uiLayout/armyCard.py::_render_round_choice_ui()`, direkt nach Zeile 331
(`st.caption(f"↳ {chosen_text}")`), zusätzlich analog in `_render_extra_round_choice()`
nach Zeile 229 (Affinity-Zweig) und nach Zeile 238 (Extra-Direktive-Zweig) — dieselbe
Bedingung, dreimal dieselbe Helper-Funktion aufgerufen (kein neuer Code-Pfad, nur der
gemeinsame Hinweis-Helfer an drei bestehenden Stellen).

Sichtbarkeit: **nur wenn die jeweils aktive Direktive** (Runden-Slot, 6th/Dynastie oder
Affinity-Doppel) den Effekt-Typ `aura_range_bonus` trägt — datengetrieben über
`_active_directive_has_type()`, nicht über einen Namensvergleich („Conquering Tyrant").
Dadurch feuert der Hinweis automatisch für jede künftige Fraktion mit demselben
Effekt-Typ, ohne Codeänderung.

## Mini-Mockup (ASCII)

```
[SAUTEKH — PRIMARY]                              ← bestehender Badge (_active_ability_badge)
↳ Add 3" to the range of this unit's aura         ← bestehender chosen_text (Z. 331)
  abilities (to a maximum of 12"), including
  Lord's Will, My Will Be Done, and Rites of
  Reanimation

ℹ️ Aura range +3" (max 12"): Lord's Will,         ← NEU: st.info(), Klasse info/blau
   My Will Be Done, Rites of Reanimation.
   Table-only — no distance tracking in the app.
```

## Vorschlag Wortlaut (Englisch)

```
Aura range +3" (max 12"): Lord's Will, My Will Be Done, Rites of Reanimation. Table-only — no distance tracking in the app.
```

Kurzform ohne den letzten Satz ist auch denkbar, falls der Stakeholder die
„table-only"-Erklärung als redundant zum Badge/Caption empfindet (siehe Entscheidungsfrage 2).

## Datengetriebenheit

- Sichtbarkeits-Bedingung: `_active_directive_has_type(faction, "aura_range_bonus")`
  (bestehender Helfer, kein neuer Code in `ability_engine.py` nötig).
- Zahlenwerte (`+3"`, `max 12"`) und die Fähigkeitsnamen-Liste (`Lord's Will; My Will Be
  Done; Rites of Reanimation`) stehen aktuell **nur als Freitext** im YAML-Feld
  `primary` (Z. 95–96 `faction_abilities.yaml`), nicht strukturiert im `effect`-Dict
  (das trägt nur `value: 3`, `max: 12`, keine Namensliste). Zwei Optionen:
  a) Hinweistext direkt aus `round_choice.primary` (dem YAML-Freitext) ableiten/anzeigen
     — 100 % datengetrieben, aber der Wortlaut ist dann exakt der Wahapedia-Rule-Text
     (schon oben als `chosen_text` sichtbar) statt einer kompakten Badge-Form.
  b) Kompakten Hinweistext aus `value`/`max` im Effekt-Dict zusammenbauen
     (`f'Aura range +{value}" (max {max}")'`) + eine **neue** strukturierte YAML-Liste
     der betroffenen Aura-Fähigkeiten (z. B. `affects: [...]`) ergänzen, um die
     Namen nicht hart zu codieren. Sauberer, aber ein (kleiner) YAML-Schema-Zusatz.
  → Siehe Entscheidungsfrage 1.
- Keine Fraktions-Strings in `src/`: weder "Necrons" noch "Conquering Tyrant" noch die
  drei Fähigkeitsnamen dürfen als Literal in `armyCard.py`/`ability_engine.py` stehen —
  der Hinweis muss ausschließlich über `effect.type == "aura_range_bonus"` + YAML-Text
  gespeist werden (Generic-src-Regel, CLAUDE.md).

## Test-Plan

Echter Anzeige-Test (nicht nur YAML-Ladetest), analog zu bestehenden UI-Tests in
`tests/uiLayout/test_common.py` / `tests/uiLayout/test_army_card.py` (Streamlit
`AppTest`-Harness, falls dort etabliert — sonst direkter Funktionsaufruf mit
`st.session_state`-Fixture + Prüfung auf den `st.info`-Aufruf/-Text via Mock oder
Streamlit-Testing-API):

1. `test_conquering_tyrant_directive_primary_shows_aura_range_hint` — Session-State mit
   aktivem `protocol_conquering_tyrant`, `directive="primary"` → `_render_round_choice_ui`
   (oder extrahierte Helper-Funktion) rendert den `info`-Hinweis mit Text, der `3` und
   `12` enthält.
2. `test_conquering_tyrant_directive_secondary_no_aura_range_hint` — `directive="secondary"`
   gewählt → Hinweis erscheint NICHT (Regressionsschutz gegen „Hinweis immer sichtbar").
3. `test_other_faction_round_choice_no_aura_range_hint` — eine andere Fraktion/Protokoll
   ohne `aura_range_bonus`-Effekt aktiv → kein Hinweis (belegt Generic-src: Bedingung ist
   `effect.type`, nicht Fraktionsname).
4. Ergänzend: bestehenden Test `test_conquering_tyrant_protocol_directive_primary_loaded`
   (Docstring nennt die „display debt") um einen Kommentar/Verweis auf den neuen Test
   aktualisieren, damit die Schuld im Ledger als geschlossen markierbar ist.

Empfehlung: der Render-Ausschnitt (Badge + Caption + Hinweis) wird am besten in eine
kleine, direkt testbare Helper-Funktion ausgelagert (z. B.
`_render_active_directive_hint(faction, round_choice, active_directive)` in `armyCard.py`),
statt den `st.info()`-Call nur inline in `_render_round_choice_ui` zu verstecken — sonst
ist er nur über die volle Streamlit-Render-Pipeline testbar (hoher Aufwand, s. CLAUDE.md
„Render-Code wird manuell verifiziert"). Die Sichtbarkeits-**Logik** (welcher Effekt aktiv
ist) bleibt in `ability_engine.py` testbar ohne Streamlit — das ist bereits Konvention im
Projekt (`get_active_round_choice_*`-Funktionen sind Streamlit-frei, INV-Trennung).

## Entscheidungsfragen

1. **Freitext vs. strukturierte YAML-Erweiterung für die Fähigkeitsnamen?**
   Default-Empfehlung: **Freitext** — den Hinweis aus `value`/`max` (strukturiert, schon
   vorhanden) + einer kompakten, in `armyCard.py` fest formulierten Phrase bauen, OHNE
   die drei Aura-Fähigkeitsnamen aus YAML zu ziehen (sie sind nicht generisch — jede
   Fraktion hätte andere Namen). Der Zusatztext „Lord's Will, My Will Be Done, Rites of
   Reanimation" bleibt Teil von `round_choice.primary` (schon als `chosen_text` sichtbar
   direkt darüber) — der neue `st.info()`-Zusatz wiederholt nur `+3" (max 12")` kompakt
   und verweist auf „this unit's aura abilities" generisch, ohne Namen zu duplizieren.
   Vermeidet YAML-Schema-Änderung, bleibt 100 % generisch.

2. **Hinweistext mit oder ohne „Table-only" Erklärsatz?**
   Default-Empfehlung: **mit**, da es laut `design_system.md` §3 die definierende
   Eigenschaft von `info`-Hinweisen ist (Regel-Erinnerung ohne App-Berechnung) und
   Nutzer sonst erwarten könnten, die App würde die Reichweite selbst tracken.

3. **Reicht ein einziger gemeinsamer Helper für alle drei Anzeige-Stellen
   (Runden-Slot, Extra/6th, Affinity-Doppel), oder soll er in `ability_engine.py`
   als reine Text-Bau-Funktion liegen (Streamlit-frei) und nur das `st.info()` in
   `armyCard.py` verbleiben?**
   Default-Empfehlung: **Split** — Text-Bau (`build_aura_range_hint_text(player) -> str
   | None`) in `ability_engine.py` (testbar ohne Streamlit), `st.info(text)`-Aufruf an
   den drei Stellen in `armyCard.py` (folgt der etablierten Schichttrennung im Projekt).

   Antwort: Alle diese Fragen sollten an sich schon entschieden sein. Warum wird dies zum Stakeholder eskaliert?

**Koordinator-Nachtrag (S119, 2026-07-03):** Rückfrage berechtigt — alle drei Fragen sind aus
verbindlichen Specs ableitbar, die Eskalation war unnötig. Es gelten die Default-Empfehlungen:
Frage 1 = Freitext (Generic-src-Regel, keine YAML-Namensliste); Frage 2 = mit „Table-only"-Satz
(design_system.md §3); Frage 3 = Split (Text-Bau in ability_engine.py, st.info() in armyCard.py —
etablierte Schichttrennung). Umsetzung in einer kommenden Session (Kandidat: UX-Pass vor Ziel8).
