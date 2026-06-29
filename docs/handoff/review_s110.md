# Review-Befund S110 — Commit b25e1f7

**Reviewer-Subagent (Opus), 2026-06-29.** Ganzheitlicher Abschluss-Review gegen die 7 DoD-Punkte.
Gates selbst ausgeführt (pytest, architecture, ruff, black), Code gelesen. Nur diese Datei geändert.

## DoD-Ampel

1. **Regelkonform — 🟢 grün.** Wound-Fix deckt sich exakt mit 9E (`core_rules.txt:1681`):
   „A wound roll can never be modified by more than -1 or +1." Code kappt korrekt an zwei Stellen:
   `net = min(1, max(-1, sum(...)))` (dice_html.py:87) für den Eff.-Wert und
   `next_thresh = max(2, max(base-1, min(base+1, base-value)))` (Z. 128) base-verankert pro Anzeige.
   Identisches Muster wie der freigegebene S109-Hit-Fix.

2. **Generisch — 🟢 grün (mit Vorbehalt zu conftest, s. Befund 1).** Kein neuer Fraktions-String in `src/`;
   `dice_html.py`-Diff entfernt nur die Verkettung (`current = next_thresh`). INV-4b-Ledger unverändert
   (11 Tokens, 28 Fundstellen — Bestandsschuld, nicht von S110 erhöht). Die conftest-Mocks liegen in `tests/`,
   nicht `src/`, verletzen die Invariante also nicht — bewertet aber kritisch unten als **Test-Design-Schuld**.

3. **Tests grün — 🟢 grün.** `pytest --tb=short`: **1260 passed**, Coverage **97,29 %** (Floor 92 %).
   Regressionstest `test_stacked_wound_debuffs_both_reference_base_threshold` vorhanden, kein Tautologie-Test
   (prüft, dass red-die-4 ≥2× erscheint — bei alter Verkettung wäre der zweite ein red-die-5).

4. **Architektur-Gate — 🟢 grün.** `pytest tests/architecture/ --no-cov -q`: **8 passed**. Alle 4 Invarianten halten.

5. **Clean Code — 🟢 grün.** `ruff check src/ tests/` → „All checks passed!". `black --check` → 107 Dateien unverändert.

6. **UI manuell verifiziert — 🟡 gelb (Pflicht offen).** Render-Code, Coverage-ausgeschlossen → Stakeholder muss
   im laufenden Streamlit prüfen. Konkret (s. Abschnitt „Manuelle UI-Prüfung").

7. **Artefakte aktuell — 🟡 gelb (planmäßig).** `next_session.md` noch auf S109-Stand; S110-Endstand kommt im
   Abschluss. `backlog.md`/`agent_scopes.md` bereits im Commit gepflegt. Was rein muss: s. Abschnitt „next_session.md".

## Manuelle UI-Prüfung (Pflicht, DoD-6)

Szenario: Angreifer mit **zwei gestapelten −1-Wound-Debuffs**, z. B. S4 vs T4 (base = 4+).
Im WOUND-Block der Resolution-UI muss sichtbar sein:
- **Beide** Modifier-Zeilen zeigen ihren roten „Von"-Würfel auf **4** (dem Profil-/Base-Threshold) —
  nicht die zweite Zeile auf 5 (das wäre der alte Verkettungsfehler).
- Die **Eff.-Zeile** zeigt **5+** (base 4 − net −1, am ±1-Cap gekappt) — NICHT 6+ (kumulativ wäre 4→5→6).
- Gegenprobe mit **drei** Debuffs: Eff. bleibt bei 5+ (Cap greift), jeder Einzel-Modifier weiterhin base-verankert auf 4.

## next_session.md — was beim Abschluss rein muss

- Stand „nach S110": Wound-Verkettungs-Bug ✅ gefixt (analog S109-Hit), Eintrag Z. 52–54 als erledigt markieren.
- Coverage-Punkt Z. 55–57: **97,29 %** erreicht (war 93,02 %); Rest-Lücken als Schuld notieren (s. Befund 3).
- Carry-over: conftest-Mock-Schuld (Befund 1) neu aufnehmen.
- Planning-Template-Erweiterung Z. 59–61 ist umgesetzt (agent_scopes.md +2 Spalten) → als erledigt führen.
- Vollsuite-Zahl 1182→**1260**, Coverage 93,02→**97,29 %** aktualisieren.

## Befunde / Empfehlungen (Input Retro)

1. **`tests/gameMechanic/conftest.py` — fragiler Mock-Re-Pointer, technische Schuld (Code gelesen).**
   Der autouse-`_reset()` iteriert über **alle** `sys.modules`, re-pointet jedes `gameMechanic.*`/`gameObjects.*`-Modul-
   `st`-Attribut auf das aktuelle `sys.modules["streamlit"]` und synct zusätzlich jedes `_st_mock`-Attribut über alle Module.
   Das ist ein **globaler, kollektionsreihenfolge-abhängiger Workaround** für die Wurzel: Testdateien legen je eigene
   `MagicMock()`-Streamlit-Instanzen an und schreiben in `_st_mock.session_state`, während src-Helfer aus `_gs.st.session_state`
   lesen — zwei verschiedene Objekte. Der Fix kuriert das Symptom (Reads/Writes auf dasselbe Objekt zwingen), nicht die Ursache
   (uneinheitliches Streamlit-Mocking pro Testdatei). **Risiko:** bricht still, sobald eine neue Testdatei ein anders benanntes
   Mock-Attribut nutzt oder src ein Modul außerhalb der zwei Präfixe importiert. **Empfehlung (mittelfristig):** eine **einzige
   gemeinsame Streamlit-Mock-Fixture** (session-scoped, in der obersten conftest), die `sys.modules["streamlit"]` einmal setzt und
   ein `fake_session_state`-Fixture pro Test liefert; Testdateien hören auf, eigene `_st_mock` anzulegen. Damit entfällt das
   sys.modules-Sweeping ganz. Als entscheidbare Retro-Maßnahme vormerken (nicht in S110 nachziehen — Gates sind grün).

2. **Aufgaben-Brief vs. Commit-Realität — `rotate_history.py` nicht in b25e1f7.** Der Review-Auftrag nennt die
   `rotate_history.py`-Marker-Korrektur als S110-Inhalt; sie liegt aber in einem **separaten früheren Commit** (`2c90b5e`),
   nicht in `b25e1f7`. Reine Zuordnungs-Notiz, kein Qualitätsmangel — beim Session-Archiv/Metrik-Eintrag sauber trennen.

3. **Rest-Coverage-Lücken als Schuld ok — aber explizit benennen.** Nicht alles ist auf 100 %:
   `game_state.py` 92 % (u. a. 256–264, 567–568), `ability_engine.py` 94 % (211–216, 388–431),
   `rosz_importer.py` 95 %. Das ist **vertretbar** (Gesamt 97,29 %, Floor 92 %), sollte aber im
   `next_session.md`/Backlog als bewusste Rest-Schuld stehen, damit der Stakeholder-Wunsch „~100 %" nicht stillschweigend
   als „erledigt" verbucht wird. Empfehlung: `game_state.py` + `ability_engine.py` als nächste Coverage-Ziele führen.

4. **Wound-Fix-Symmetrie mit Hit-Block — gut, aber DRY-Kandidat.** `_render_dice_roll_block` (Hit) und
   `_render_dice_wound_block` (Wound) enthalten jetzt **identische** Stack-Schleifen-Logik
   (base-verankert + ±1-Cap, `next_thresh = max(2, max(base-1, min(base+1, base-value)))`). Ab dieser dritten Wiederholung
   (Save-Block hat eine Variante) lohnt eine kleine geteilte Helfer-Funktion. **Kein Blocker** (DRY erst ab 3. Wiederholung,
   Render-Code), aber als Aufräum-Kandidat vormerken.

5. **Kein blinder Fleck im Verhalten gefunden.** Der `on_six_ap`-Pfad (Hungry Void D1) ist unabhängig vom Stack-Block
   und vom Fix unberührt; die `net`-Kappung beeinflusst nur den Eff.-Wert, nicht die value-triggered AP-Zeile — korrekt.

---

**Gesamtbild:** Gates alle grün (Tests, Architektur, Lint, Format, Regelkonformität). Offen sind nur die
planmäßigen 🟡-Punkte: manuelle UI-Prüfung (DoD-6) und der Artefakt-Abschluss (DoD-7). Keine Stakeholder-
**Blocker** — die conftest-Schuld (Befund 1) ist eine Retro-Maßnahme, kein S110-Korrekturbedarf.

DONE
