STATUS: NEEDS-DECISION

# S159 — Planning-Entwurf

Grundlage: `.claude/tasks/briefing.md` (Stand nach S158), `docs/reference/agent_scopes.md`,
`docs/goals/backlog.md` + `backlog_details.md` (B-104/B-105/B-109/B-028b/B-112/B-113),
`docs/handoff/S158_design_crew.md`, `docs/handoff/S158_B104_ui_verifikation.md`,
`docs/handoff/S158_B111_ui_verifikation.md` (inkl. `Bildschirmfoto vom 2026-07-17 15-50-22.png`),
`docs/spec/design_system.md`, `docs/spec/design_colors.md`, Ist-Code
`src/uiLayout/diceCompose.py` + `src/uiLayout/diceHtml.py`.

---

## 0. Checkbox-Sync (Pflicht)

Aktive Zieldatei laut Backlog: `docs/goals/ziel7.md`. B-104/B-105/B-109/B-028b/B-112/B-113
sind dort **nicht** als Checkboxen dupliziert — sie leben ausschließlich in `backlog.md`, daher
kein Ziel7-Checkbox-Abgleich nötig für diese Items. Stattdessen Code-Beleg je Item direkt gegen
den beschriebenen Ist-Zustand geprüft (statt gegen Checkboxen):

| Item | Backlog-Status | Beleg | Ergebnis |
|---|---|---|---|
| B-111 | `UI-Verifikation` | `_badge_chip` (diceCompose.py:159–171) trägt `title="{label}"`; Stakeholder-Handoff bestätigt Testfall 1 „Verifiziert" | **kein Stale-Check** — Status korrekt, DONE-fähig (Rant im selben Handoff betrifft B-104-Optik, nicht die Tooltip-Mechanik) |
| B-104 | `UI-Verifikation` | `_marker_row_html` nutzt `_triggered_die_chip_html` (Text-Glyph im Span, kein SVG) — Stakeholder-Screenshot zeigt, dass das gemeinte Symbol das echte `dice_face_svg(1, miss=True)`/`miss_die_html`-Element ist | **kein Stale-Check** — Status korrekt `UI-Verifikation`/„nicht bestanden", neuer Zuschnitt nötig |
| B-105 | `ToDo` | `grep -rn "go_source_chip" src/` → kein Treffer, `_strength_source_badge_html` (diceHtml.py:83–95) noch nicht generalisiert | **kein Stale-Check** — echt offen |
| B-109 | `ToDo` | `always_fail_marker_row_html` (diceCompose.py:425) hat weiterhin `label or "Auto-fail"` | **kein Stale-Check** — echt offen |
| B-112 | `ToDo` | `python tools/mypy_gate.py` lokal ausgeführt: 25 Fehler vs. Baseline 24 (identisch zu S158-Review-Befund) | **kein Stale-Check** — echt offen |
| B-028b | `ToDo` | `grep -rn "noctilith_beacons" src/` → nur YAML-Treffer, kein `can_deny`-Erweiterung, keine GO-Card-Anbindung | **kein Stale-Check** — echt offen |

Kein Doku-Drift gefunden — alle sechs Backlog-Zeilen sind akkurat.

---

## 1. Prioritätenvorschlag S159

Vorschlag der Session-Vorlage aus `briefing.md`/Auftrag geprüft und **mit einer Korrektur**
bestätigt:

1. **Würfelsymbol-Katalog + Design-System-Aufräumen** (neuer Auftrag aus B-104-Verifikation) —
   MUSS zuerst, weil B-104 und B-105 beide gegen ihn implementiert werden sollen (Katalog
   definiert die kanonische Geometrie/Farblogik, die beide Folge-Tasks konsumieren).
2. **B-104-Re-Fix** (echtes Würfel-SVG statt Text-Chip) — direkt danach, auf Basis des Katalogs.
3. **B-105 Variante A** (`go_source_chip`) — danach, ebenfalls auf Basis des Katalogs; **Korrektur
   gegenüber der Auftrags-Reihenfolge:** B-109 wird **vor** B-105 eingeschoben (Begründung unten),
   nicht danach.
4. **B-109** (Auto-Fail-Badge-Label verpflichtend aus YAML) — vorgezogen vor B-105, weil beide
   dieselbe Funktion (`always_fail_marker_row_html`) anfassen; B-105 baut zusätzlich einen neuen
   Konsumenten (Invuln-Row) für denselben Chip-Baustein. Erst den Label-Fallback bereinigen, dann
   den Baustein auf einen weiteren Aufrufer ausweiten, vermeidet einen doppelten Bearbeitungs-
   Durchgang derselben Zeilen.
5. **B-112** (mypy-Baseline) — unabhängige Datei (`tools/mypy_gate.py`), läuft **parallel** zum
   Dice-Cluster (kein Datei-Overlap).
6. **B-028b** (Deny-Psychic-Konsolidierung) — unabhängige Dateien (`data/wh40k_9e/necrons/*.yaml`,
   `abilityEngine.py:can_deny`), läuft ebenfalls **parallel** zum Dice-Cluster.

**Abweichung von der Vorlage begründet:** Die Vorlage nannte B-105 vor B-109 nicht explizit,
der Auftrag selbst sagt nur „danach ggf. B-109/B-112/B-028b nach Token-Lage" — die Prüfung gegen
den Code ergibt, dass B-109 und B-105 denselben Call-Site-Bereich (`always_fail_marker_row_html`
+ `_badge_chip`) berühren; B-109 zuerst vermeidet Merge-Reibung und eine zweite Anfassung
derselben Zeilen. B-113 (Skorpekh/Destroyer-Lord-Reroll) bleibt außerhalb dieser Session-Planung
— bereits als eigenständiges Item im Backlog, nicht Teil des B-104-Testfalls, kein Bezug zum
Dice-Symbol-Katalog.

**Token-Lage:** Punkte 1–4 (Dice-Cluster, sequenziell wegen Datei-Overlap) plus Punkte 5–6
(parallel) passen in den Korridor <150k, wenn jeder Task sein Budget einhält (s. §5). Sollte der
Dice-Cluster nach Punkt 2 (B-104) bereits ~90k erreichen, wird B-105/B-109 in die S160 verschoben
— B-112/B-028b sind in jedem Fall abschließbar, da sie datei-disjunkt und klein/mittel sind.

---

## 2. Bestandsaufnahme — Würfel-/Symbol-Render-Stellen (Rohstoff für den Katalog)

Vollständige Liste aller Dice-/Symbol-Render-Funktionen in `src/uiLayout/diceCompose.py` +
`src/uiLayout/diceHtml.py` (per `grep -n "^def "` + Lesen verifiziert):

| Funktion | Datei:Zeile | Heutige Optik | Farbe/Logik |
|---|---|---|---|
| `dice_face_svg(value, color, miss, size)` | diceCompose.py:91–110 | 32×32 SVG, `rx=4` abgerundetes Rechteck, Pip-Muster (`_PIP_POSITIONS`) oder bei `miss=True` + `value==1` zwei diagonale Linien (X über die volle Fläche) | Erfolg: `border=color` (Parameter, i.d.R. `_THRESHOLD_COLOR`), `bg=#1e293b`. Miss: `border` **hart** `#374151`, Kreuz-Linien **hart** `#c0392b` (Farbparameter wird bei `miss=True` ignoriert) |
| `miss_die_html(size)` | diceCompose.py:113–120 | Ruft `dice_face_svg(1, miss=True, size)` — identisches Symbol wie „echter" Miss-Würfel im Grid | s.o., keine eigene Farboption |
| `dice_row_html(threshold)` | diceCompose.py:123–153 | Reiht 6 `dice_face_svg`-Würfel, Erfolgsbereich in farbigem Rahmen (`frame_color`), Wert 1 immer als Miss-Würfel; bei `threshold>6` zusätzlicher `miss_die_html()` rechts | `_THRESHOLD_COLOR`-Palette je Schwelle |
| `threshold_header_html(threshold)` | diceCompose.py:68–88 | Zahlen-Header „1+ … 6+", aktiver Wert farbig umrandet | `_THRESHOLD_COLOR` |
| `_aligned_modifier_row_html` (→ `dice_face_svg`) | diceCompose.py:233–297 | Modifier-Zeile: zwei Würfel (alt/neu Threshold) verbunden durch Pfeil-Glyphen; `left_miss=True` rendert den linken Würfel als `dice_face_svg(1, miss=True)` | Buff-Grün/Debuff-Rot über `glyph_color`/`color`-Parameter je Aufrufer |
| `modifier_die_pair_html` / `save_modifier_die_pair_html` / `save_ap_modifier_row_html` | diceCompose.py:300–363 | Wrapper um `_aligned_modifier_row_html` für HIT/WOUND bzw. SAVE-Modifier | s.o. |
| `_badge_chip(label, color)` | diceCompose.py:159–171 | Kein Würfel — Label-Chip in der linken Spalte, `max-width` + Ellipsis-Truncation + `title`-Tooltip (B-111) | Farbe = Aufrufer-Parameter |
| `_triggered_die_chip_html(content, color)` | diceCompose.py:429–436 | 30×30 `<span>`, `border-radius:4px`, `border` = Parameterfarbe, `bg=#1e293b`, Text-Inhalt zentriert (Font 9px) — **kein SVG, kein Pip-/Kreuz-Zeichnung**, nur ein Text-Glyph in einer Box | Farbe = Aufrufer-Parameter (frei wählbar, im Gegensatz zu `dice_face_svg(miss=True)`) |
| `value_triggered_die_row_html` (→ `_triggered_die_chip_html`) | diceCompose.py:439–457 | AP-Trigger-Zeile (z. B. „AP-1" bei Hungry Void D1), Chip in der Trigger-Spalte | Aufrufer-Farbe (aktuell immer Buff-Grün) |
| `_marker_row_html` (→ `_triggered_die_chip_html`) | diceCompose.py:380–396 | Gemeinsame Basis für Reroll- und Auto-fail-Zeile — **Kern des B-104-Bugs**: nutzt den Text-Chip statt eines echten Würfelsymbols | Farbe = Aufrufer |
| `reroll_marker_row_html` | diceCompose.py:399–406 | ↺-Symbol via `_marker_row_html`/`_triggered_die_chip_html`; noch **nicht produktiv verdrahtet** (Kommentar im Code, S158-Handoff bestätigt) | fix `#f59e0b` (Reroll-Orange) |
| `always_fail_marker_row_html` | diceCompose.py:409–426 | ✕-Symbol via `_marker_row_html`/`_triggered_die_chip_html` — produktiv verdrahtet (Quantum Shielding), **visuell der gemeldete Bug** | `_modifier_color({"color_hint": color_hint, "value": -1})` → Buff-Grün oder Debuff-Rot |
| `special_die_html(label, content)` | diceCompose.py:366–373 | Trotz Namen **kein Würfel** — reiner Label-Chip für Waffenregeln (Tesla, Alt. Fire); irreführender Funktionsname | fix `#f59e0b` |
| `_strength_source_badge_html(label)` | diceHtml.py:83–95 | Inline-Chip (kein Würfel) neben S-vs-T — nennt die GO-Quelle eines Strength-Buffs; B-105-Kandidat für Generalisierung zu `go_source_chip` | fix `_BUFF_COLOR_HEX` (Bug-Potential: keine Debuff-Variante trotz B-105-Anspruch) |
| `_render_dice_save_block` → Invuln-Zeile | diceHtml.py:250–260 | `Inv N+` als reiner `<span>`, **kein** Würfelsymbol, **kein** GO-Namens-Bezug (B-105-Lücke) | `_BUFF_COLOR_HEX` bei `ability_invuln`, sonst `_THRESHOLD_COLOR` |

**Kernbefund für den Katalog:** Es gibt aktuell **zwei nicht vereinheitlichte visuelle Sprachen**
für „etwas in einem Würfel-Slot": (a) `dice_face_svg`-Familie — echte SVG-Würfel mit Pip-Muster
oder gezeichnetem Kreuz, Miss-Variante farblich **nicht parametrisierbar**; (b)
`_triggered_die_chip_html` — Text-in-Box, frei einfärbbar, aber optisch keine „Würfelfläche"
(genau das vom Stakeholder bemängelte „Auge"-Aussehen). Der Katalog muss diese Lücke schließen:
entweder (b) auf die SVG-Optik von (a) heben, oder (a) um einen Farbparameter für die
Miss-Variante erweitern und (b) als Sonderfall von (a) neu bauen. Letzteres ist der technisch
sauberere Weg (eine Zeichenroutine, zwei Konsumenten) und deckt sich mit dem vom Stakeholder
selbst markierten Referenzsymbol im Screenshot (echter Miss-Würfel oben im Grid).

---

## 3. Task-Zuschnitt

### Task 1 — Würfelsymbol-Katalog + Design-System-Struktur (Design-Crew, Sonnet)

**Scope:** Reines Konzept-/Doku-Dokument, kein Code. Ziel: `design_system.md` §4 wird zu einem
eigenständigen, geordneten Würfel-Design-Abschnitt ausgebaut (Stakeholder-Auftrag „mach das
ORDENTLICH" — Kritik: GO-Bereich riesig, Würfel-Bereich kaum vorhanden). Nutzt die Bestandsaufnahme
aus §2 dieses Plans als Rohstoff (bereits vollständig — kein zweiter Scan nötig, Zeit sparen).

**Inhalt des Katalogs (Vorgabe an den Subagenten):**
- Eine Tabelle **„Würfelflächen"** (echte Würfel-Slots: Erfolg/Miss/Off-Scale/Modifier-Paar) mit
  Geometrie (32px SVG, `rx=4`, Pip-Positionen) + Farblogik je Zustand.
- Eine Tabelle **„Effekt-Symbole in Würfel-Slots"** (AP-Trigger, Reroll-↺, Auto-fail-✕) — jede
  Zeile bekommt jetzt explizit: soll sie wie eine echte Würfelfläche aussehen (SVG-basiert) oder
  bewusst wie ein Chip? **Empfehlung an den Stakeholder: alle drei werden auf dieselbe
  SVG-Zeichenroutine gehoben** (konsistent mit dem Screenshot-Befund) — technischer Weg:
  `dice_face_svg`/`miss_die_html` bekommen einen optionalen Farbparameter für Rahmen+Kreuz (statt
  hart `#374151`/`#c0392b`), `_triggered_die_chip_html` wird für Auto-fail/Reroll durch diese
  SVG-Variante ersetzt; für AP-Trigger (kurzer Text „AP-1") bleibt der bestehende Text-Chip
  bestehen, da dort kein Würfel-Pip/Kreuz-Bild sinnvoll ist — das wird im Katalog explizit als
  bewusste dritte Kategorie **„Text-Chip in Würfel-Slot"** benannt, damit „Würfel" nicht auf Dinge
  gepresst wird, die keine sind (z. B. „AP-1" hat keine Würfelfläche in der Spielwelt).
- Klarstellung: `special_die_html` und `_strength_source_badge_html` sind **keine** Würfelsymbole
  (Namensverwirrung im Code vermerken, kein Rename in diesem Task — nur Doku-Klarstellung).
- Farbdefinitionen ausschließlich per Referenz auf `design_colors.md` (kein neues Token,
  `_BUFF_COLOR_HEX`/`_DEBUFF_COLOR_HEX`/`_THRESHOLD_COLOR` bleiben Quelle).
- Struktur-Vorschlag: §4 wird zu „§4 Symbol- & Würfel-Design-System" mit Unterabschnitten §4.1
  (Glyph-Konstanten, bestehend), §4.2 (Würfelflächen-Katalog, neu), §4.3 (Effekt-Symbol-Katalog,
  neu, ersetzt den bisherigen §4.1-Block aus S158), damit die Struktur parallel zu §6 (GO) auf
  Augenhöhe steht statt als Anhängsel.

**Output:** NEEDS-DECISION-Handoff `docs/handoff/S159_dice_symbol_catalog.md` mit
Grundannahmen-Block (Pflicht laut `agent_scopes.md`), konkretem Katalog-Entwurf als **eine**
Empfehlung (keine A/B/C-Variantenschleife mehr — der Stakeholder hat die Zielrichtung im
Screenshot bereits unmissverständlich vorgegeben; eine erneute Mehrfachauswahl würde die
Fünft-Anlauf-Frustration wiederholen). Enthält den fertigen Textentwurf für `design_system.md`
§4 zur Übernahme nach Freigabe (kein separater Schreib-Schritt nötig).

**Betroffene Dateien:** nur die Handoff-Datei (kein Code, kein Spec-Write vor Freigabe).

**Testansatz:** entfällt (reines Konzept).

**Akzeptanzkriterien:** Katalog ist vollständig (jede Zeile aus §2 dieses Plans erscheint),
jede Zeile hat Geometrie + Farblogik + Konsument benannt, „Neuer Fall künftig: erst Zeile
ergänzen, dann Code" bleibt als Ratchet-Prinzip erhalten (analog bisherigem §4.1).

**Token-Budget:** ~15k, Selbst-Stopp bei ~22k.

---

### Task 2 — B-104-Re-Fix: echtes Würfel-SVG für Auto-fail-Marker (Executor, Sonnet)

**Scope:** Nach Freigabe von Task 1. `dice_face_svg`/`miss_die_html` um einen optionalen
Farbparameter für die Miss-Variante erweitern (Rahmen + Kreuz-Linien statt hart `#374151`/
`#c0392b`), ohne bestehende Aufrufer zu verändern (Default bleibt der heutige feste Farbwert —
`dice_row_html`, `_aligned_modifier_row_html` mit `left_miss=True` dürfen sich optisch NICHT
ändern). `_marker_row_html` (Auto-fail-Zweig) auf die neue SVG-Miss-Variante mit
Perspektiv-Farbe (`_modifier_color`) umstellen. Reroll-Zweig (`reroll_marker_row_html`) laut
Katalog-Entscheid (Task 1) ebenfalls umstellen, sofern der Katalog das für ↺ vorsieht — sonst
explizit als „bewusst weiterhin Text-Chip" belassen.

**Betroffene Dateien:** `src/uiLayout/diceCompose.py` (`dice_face_svg`, `miss_die_html`,
`_marker_row_html`, `always_fail_marker_row_html`, ggf. `reroll_marker_row_html`),
`tests/uiLayout/test_dice_html.py` (bestehende Tests für `dice_face_svg`/`miss_die_html`/
`always_fail_marker_row_html` erweitern, nicht ersetzen — Regressionsschutz für unveränderte
Aufrufer).

**Namenswahl vorab gegen INV-4b-Vokabular prüfen** (`tests/architecture/test_generic_src_vocab.py`),
keine Fraktions-Wörter einführen.

**Testansatz (4-Schichten-Mandat):**
1. Unit: neuer Farbparameter von `dice_face_svg`/`miss_die_html` — Default-Fall unverändert
   (Regressionstest: bestehende Aufrufer liefern bytegleiches HTML wie vorher).
2. HTML-Output-Test: `always_fail_marker_row_html` liefert jetzt SVG-Markup (`<svg`,
   Kreuz-Linien-Farbe = `color_hint`-Perspektive) statt `<span>✕</span>` — expliziter
   String-Assert auf die neue Struktur.
3. Coverage: `diceCompose.py` bleibt im Coverage-Floor (INV-6, Streamlit-frei, gemessen) — keine
   Ausnahme.
4. Manuelle UI-Verifikation (PFLICHT, eigene Handoff-Datei `docs/handoff/S159_B104_ui_verifikation.md`
   nach dem in `agent_scopes.md` vorgegebenen Drei-Felder-Schema): Necron-Roster mit Quantum
   Shielding, Kampfphase, Wound-Block — Auto-fail-Slot zeigt jetzt ein Würfel-SVG mit
   vollflächigem Kreuz (wie das vom Stakeholder markierte Referenzsymbol), nicht mehr ein
   zentriertes Text-✕.

**Akzeptanzkriterien:** Auto-fail-Slot optisch identisch zur echten Miss-Würfel-SVG (nur Rahmen-/
Kreuzfarbe je nach Perspektive abweichend), alle bisherigen `dice_face_svg`/`miss_die_html`-
Aufrufer unverändert (Screenshot-Vergleich/Regressionstest), Katalog aus Task 1 vollständig
umgesetzt.

**Token-Budget:** ~20–25k (M), Selbst-Stopp bei ~35k. Falls Core+SVG-Logik+Tests den Umfang
sprengen, VOR Vergabe in „SVG-Parametrisierung" (Core) + „Call-Site-Umstellung+Tests" (Rest)
splitten (Retro-M4-Regel).

---

### Task 3 — B-109: Auto-Fail-Badge-Label verpflichtend aus YAML (Executor, Sonnet)

**Scope:** Nach Task 2 (gleiche Funktion `always_fail_marker_row_html`, sequenziell wegen
Datei-Overlap). `label or "Auto-fail"`-Fallback in `always_fail_marker_row_html`
(diceCompose.py:425) entfernen — Aufrufer MUSS ein Label liefern. Loader-Guard: fehlendes
`badge_label`/`name_en` bei `wound_auto_fail`-Effekten wird beim Laden abgelehnt statt still zu
fallbacken.

**Betroffene Dateien:** `src/uiLayout/diceCompose.py` (`always_fail_marker_row_html`),
`src/gameMechanic/abilityEngine.py` (`unit_wound_auto_fail_label`), `src/gameObjects/loader.py`
(neuer Guard), `tests/gameObjects/test_loader.py`, `tests/uiLayout/test_dice_html.py`.

**Testansatz:** Unit-Test für den Loader-Guard (fehlendes `badge_label`+`name_en` → Ladefehler),
Regressionstest, dass bestehende `wound_auto_fail`-Effekte (Quantum Shielding) weiter laden.
Kein manueller UI-Verifikationspunkt nötig (reine Guard-/Fallback-Logik, keine neue Optik).

**Akzeptanzkriterien:** kein stiller Fallback mehr möglich, Ladefehler bei fehlendem Label ist
aussagekräftig (nennt Fraktion+Ability-ID).

**Token-Budget:** ~10–15k (S), Selbst-Stopp bei ~20k.

---

### Task 4 — B-105 Variante A: generischer GO-Quellen-Chip (Executor, Sonnet)

**Scope:** Nach Task 3 (gleiche Datei-Nachbarschaft `diceCompose.py`/`diceHtml.py`).
`_strength_source_badge_html` (diceHtml.py) zu `go_source_chip(label, color)` in
`diceCompose.py` generalisieren — Farbe über `_modifier_color`/`color_hint` statt hart
`_BUFF_COLOR_HEX`, damit auch Debuff-GOs (z. B. Quantum Shielding an anderer Stelle) denselben
Chip nutzen können. Aufrufstellen: (a) bestehender Strength-Buff-Call (Rewire, keine
Verhaltensänderung), (b) neu: Invuln-Row in `_render_dice_save_block` — GO-Name neben `Inv N+`,
sofern die Invuln-Ability ihren Namen über den bestehenden `abilityEngine`-Pfad
(`ability_badge_label`, analog B-103/B-109-Muster) liefert; falls dieser Pfad für Invuln-Quellen
noch nicht existiert, das als Scope-Erweiterung im Bericht explizit melden statt improvisiert zu
verdrahten (Grundannahmen-Klärung nötig, ggf. NEEDS-DECISION statt Silent-Erweiterung).

**Wrap-Schutz (aus Design-Crew-Interaktionshinweis S158):** `go_source_chip` nutzt denselben
Wrap-fähigen `_badge_chip`-Unterbau (B-111 Variante C ist Tooltip, nicht Wrap — hier separat
prüfen: der neue Chip braucht mindestens dieselbe `title`-Tooltip-Absicherung, damit lange
GO-Namen nicht denselben Truncation-Bug wie B-111 reproduzieren).

**Betroffene Dateien:** `src/uiLayout/diceCompose.py` (neue Funktion `go_source_chip`),
`src/uiLayout/diceHtml.py` (`_render_dice_wound_block` Rewire, `_render_dice_save_block`
Invuln-Zeile), `tests/uiLayout/test_dice_html.py`.

**Namenswahl vorab gegen INV-4b-Vokabular prüfen.**

**Testansatz:** HTML-Output-Test für `go_source_chip` (Buff-Grün- und Debuff-Rot-Fall), Test für
den neuen Invuln-Aufrufer, Regressionstest für den bestehenden Strength-Buff-Aufrufer
(bytegleiches Verhalten). Manuelle UI-Verifikation PFLICHT (eigene Handoff-Datei
`docs/handoff/S159_B105_ui_verifikation.md`): Necron-Roster mit Quantum Deflection (Invuln-GO),
Save-Block zeigt jetzt „Inv 4+ [Quantum Deflection]" statt nacktem „Inv 4+".

**Akzeptanzkriterien:** ein Baustein für beide bisherigen Ad-hoc-Lösungen, Invuln-Lücke aus
S155-Befund geschlossen, kein zweites visuelles Muster.

**Token-Budget:** ~15–20k (S/M), Selbst-Stopp bei ~28k.

---

### Task 5 — B-112: mypy-Ratchet-Baseline korrigieren (Executor, Haiku — reiner Lookup+Zahl-Fix)

**Scope:** Unabhängig vom Dice-Cluster, **parallel startbar**. `python tools/mypy_gate.py`
ausführen, die 25 realen Fehler gegen die 24er-Baseline abgleichen (bereits in §0 dieses Plans
mit den 8 betroffenen Dateien belegt: `unitCard.py`, `gameProtocoll.py`, `armyCard.py`,
`detachmentCard.py`, `armyList.py`), `BASELINE = 24` auf den korrekten Ist-Wert setzen (Zahl
gegen den tatsächlichen `mypy_gate.py`-Lauf verifizieren, nicht raten) — oder, falls der
Stakeholder lieber die 1 neue Fehlerquelle gefixt sehen will, den einen Zusatzfehler beheben statt
die Baseline zu erhöhen (Entscheidung: Baseline-Korrektur ist die im Backlog vorgesehene Route,
kein neuer Entscheid nötig).

**Betroffene Dateien:** `tools/mypy_gate.py` (bzw. der eine neue Fehler in einer der 8 Dateien,
je nach gewählter Route).

**Testansatz:** `python tools/mypy_gate.py` grün nach Fix (exit 0), `tests/tools/test_token_report.py`
unberührt (kein Bezug), Vollsuite am Ende (Teil des Standard-Gate-Netzes).

**Akzeptanzkriterien:** `mypy_gate.py` exit 0, Baseline entspricht Ist-Zustand auf dem neuen HEAD.

**Token-Budget:** ~5k (XS), Selbst-Stopp bei ~8k.

---

### Task 6 — B-028b: Noctilith Beacons als erste GO über B-028a-Infrastruktur (Executor, Sonnet)

**Scope:** Unabhängig vom Dice-Cluster und von Task 5, **parallel startbar** (disjunkte Dateien).
`noctilith_beacons` (`data/wh40k_9e/necrons/unit_abilities.yaml:349`) als erste produktive
Callsite über die in B-028a gelieferte Infrastruktur
(`reactive_abilities_for`/`ability_visibility`/`spend_ability`/`undo_ability`/
`render_reactive_ability_box`) verdrahten; `can_deny()` um die neue Ability-Quelle erweitern.
`gloom_prism`-Migration optional (laut Backlog-Beschreibung), nur wenn Zeit/Budget reicht — sonst
explizit als offen vermerken statt stillschweigend auszulassen.

**Betroffene Dateien:** `src/gameMechanic/abilityEngine.py` (`can_deny`),
`data/wh40k_9e/necrons/unit_abilities.yaml` (falls Datenlücken auffallen),
`src/gameMechanic/psychicPhase.py` (voraussichtlicher Call-Ort, gegen `abilityEngine.py`
verifizieren), `tests/gameMechanic/test_ability_engine.py`.

**Testansatz:** Unit-Test für `can_deny()`-Erweiterung (Ability-Quelle wird erkannt), Test für
`spend_ability`/`undo_ability`-Zyklus am neuen Call-Site (Vollrückgängig-Garantie aus §6.1
design_system.md), Regressionstest, dass bestehende Deny-Pfade unverändert bleiben. Manuelle
UI-Verifikation PFLICHT (eigene Handoff-Datei): Necron-Roster mit `noctilith_beacons`-Träger,
gegnerischer Psychic-Test, reaktive Ability-Box erscheint am korrekten Anker.

**Akzeptanzkriterien:** erste produktive Callsite der B-028a-Infrastruktur, `can_deny()` erkennt
die neue Quelle, kein Bruch bestehender Deny-Pfade.

**Token-Budget:** ~20k (M), Selbst-Stopp bei ~30k.

---

## 4. Ausführungsreihenfolge (Zusammenfassung)

```
Task 1 (Katalog, Design-Crew) ─── NEEDS-DECISION, früh im Plan (Konsens-Punkt)
   │  (Freigabe)
   ▼
Task 2 (B-104 SVG-Fix) → Task 3 (B-109 Label-Guard) → Task 4 (B-105 go_source_chip)
   sequenziell, gleiche Dateien (diceCompose.py/diceHtml.py)

Task 5 (B-112, Haiku)         ─┐  parallel zum Dice-Cluster, disjunkte Dateien
Task 6 (B-028b, Sonnet)       ─┘
```

---

## 5. Token-Budget-Gesamtschätzung

| Task | Budget | Selbst-Stopp |
|---|---|---|
| 1 — Katalog (Design-Crew) | ~15k | ~22k |
| 2 — B-104 SVG-Fix | ~20–25k | ~35k |
| 3 — B-109 Label-Guard | ~10–15k | ~20k |
| 4 — B-105 go_source_chip | ~15–20k | ~28k |
| 5 — B-112 Baseline | ~5k | ~8k |
| 6 — B-028b Noctilith | ~20k | ~30k |
| **Summe (worst case)** | **~85–100k** | — |

Dice-Cluster (1–4) allein: ~60–75k, sequenziell. Bei vollem Verbrauch aller Budgets ist der
<150k-Korridor bei paralleler Task 5/6-Ausführung realistisch einhaltbar; falls der Dice-Cluster
nach Task 2 bereits über ~90k Gesamt-Kontext liegt, Wind-down nach Task 2/3, Task 4 in S160.

---

## Offene Entscheidungen (NEEDS-DECISION)

1. **Reihenfolge-Korrektur bestätigen:** B-109 vor B-105 (statt wie in der Auftragsvorlage
   angedeutet danach) — Begründung: Datei-Overlap vermeiden (§1).
2. **Task 1 (Katalog) läuft ohne erneute A/B/C-Variantenabfrage** — direkte Empfehlung auf Basis
   des Screenshot-Befunds. Falls der Stakeholder dennoch Varianten sehen will, bitte vorab sagen
   (sonst wird Task 1 wie oben beschrieben als Ein-Empfehlung-Katalog beauftragt).
3. **B-105 Invuln-Quelle:** falls `ability_badge_label` (oder ein Äquivalent) für Invuln-Auslöser
   noch nicht existiert, wird das als Scope-Fund im Task-4-Bericht gemeldet statt improvisiert
   gelöst — ggf. eigener Mini-Task nötig (Budget-Reserve einplanen).
