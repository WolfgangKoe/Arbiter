STATUS: ANSWERED — S156-Abschluss-Review, behalten bis S157-Start

# S156 — DoD-Abschluss-Review (Reviewer Opus, ADR-0007)

**Prüfumfang:** uncommitteter Arbeitsstand S156 (`git status`: 19 M, 1 D, 3 ??).
Inhalt: B-056 Quantum Shielding (neuer generischer Effekttyp `wound_auto_fail`),
B-098 Teil 2 Kombi-Waffen (Berechnung + Loader-Guard + Daten, Verdrahtung offen).
Zentral gemessen (übernommen, nicht neu gefahren): `pytest --tb=short` → **1903 passed /
99,11 %** (Floor 99 % ✓); Doku/Acceptance/Architektur → **31 passed**.

**Gesamturteil: GO für den Commit** — der Code ist regelkonform, generisch, testgedeckt und
architektur-grün. GO steht unter der Auflage, dass der Abschluss-Schritt die unter DoD-7
gelisteten Artefakt-Lücken schließt (Backlog/Briefing/Beobachtungen); das ist Abschluss-Arbeit,
kein Code-Blocker.

---

## DoD-Katalog

### 1. Regelkonform — ✅
- **Quantum Shielding (Unit-Ability):** `rule_text` + `modifier: 3` decken
  `wahapedia_necrons/units_all.txt:112` **wörtlich**: „an unmodified wound roll of 1-3 always
  fails, irrespective of any abilities that the weapon or the attacker may have." Die Umsetzung
  als Verwundungswurf-**Floor** (`max(2, N+1)`) gegen den UNMODIFIZIERTEN Wurf ist korrekt: kein
  Wund-Buff kann darunter senken — genau die „irrespective of any abilities"-Klausel.
- **Kombi-Waffen:** −1-Malus nur bei beiden Profilen matcht Profiltext („If you select both …
  subtract 1 from that attack's hit roll", `orks/weapons.yaml` + `faction_overview.txt:4226`).
  Boss-Nob-Swap `nob_kombi` (replaces slugga+choppa → kombi-rokkit|kombi-skorcha) matcht
  `units_all.txt:406` wörtlich („The Boss Nob's slugga and choppa can be replaced with one of the
  following: 1 kombi-rokkit; 1 kombi-skorcha").

### 2. Generisch — ✅
- INV-4b-Ledger **unverändert 6 Tokens / 16 Fundstellen / 3 Dateien** (Soll) — kein Wachstum.
- `git diff src/` trägt keine Fraktions-Strings: `abilityEngine` dispatcht auf `effect.type ==
  "wound_auto_fail"` (Tag in YAML), `combat` nimmt einen `int | None`-Parameter, `weapon.py` ist
  ein generisches `combi: bool`-Feld, Loader-Guard prüft `scope`/`replaces` strukturell.
- **Beleg-Wert:** `rules_insights.md` dokumentiert die INV-4b-Falle sauber — der Ability-`id`
  `quantum_shielding_wound_deny` (statt `..._wound_auto_fail`) verhindert, dass „fail" zum
  Necron-Token wird und quer durch `src/` flaggt. Bewusste, belegte Namenswahl.

### 3. Tests grün — ✅
- Zentral 1903/99,11 % übernommen; 21 gezielte Neu-Tests (combi / auto_fail / annihilation /
  quantum / exclusive-swap) **passed** in Stichprobe.
- **Mock-Vervollständigung `tests/uiLayout/test_common.py` verifiziert:** der Diff ergänzt
  ausschließlich `rules=[]` an zwei Mock-`def_unit`s und vier Session-Basis-Keys
  (`first_player`/`second_player`/`p1_faction_dir`/`p2_faction_dir`) in
  `_resolution_context_session`. **Keine** Assertion, kein Erwartungswert geändert — reine
  Mock-Angleichung, wie freigegeben.

### 4. Architektur-Gate — ✅
- 8 passed; Schulden-Scoreboard: Ledger (impl. ohne Test) **0**, Namen-Allowlist 3 (LEGIT),
  Konsistenz „alle Testnamen existieren". Keine Aufweichung.

### 5. Clean Code — ✅
- `unit_wound_auto_fail_max`, `_combi_hit_penalty`, `_exclusive_swap_clusters`/
  `_check_exclusive_swaps`: sprechende Namen, vollständige Type Hints, Early-Returns.
- Kommentar-Konvention gewahrt: Docstrings tragen Warum + Spec-/Quellenverweis
  (`units_all.txt:112`, `faction_overview.txt`), die ausführliche Design-Begründung liegt in
  `rules_insights.md`, nicht im Code. Kein magischer String.

### 6. UI manuell verifiziert — ✅ (mit Folge-Befunden)
- **Quantum-Shielding-WOUND-Block wurde bereits verifiziert** (Stakeholder, `S155_ui_verifikationen.md`
  Punkt 5): 3× ✕ erscheint korrekt gegen QS-Fahrzeuge, keine Marker gegen normale Ziele → **funktioniert
  wie erwartet.** Damit ist der Pflicht-Check erbracht.
- **Kombi-UI existiert noch nicht** (R-COMBAT-35 bewusst `offen`) → korrekt kein UI-Check nötig.
- **Aber drei neue UI-Folge-Befunde** aus derselben Verifikation, die als Backlog-Items zu erfassen sind:
  (a) Debuff-Label zeigt „Auto-fail", soll das Keyword „Quantum-Shielding" zeigen;
  (b) Symbol ist ein blankes „x" statt Würfelsymbol-mit-x → Design-System-Abweichung
  (Design-System ergänzen ODER Backlog-Item referenziert die Design-Stelle exakt);
  (c) keine Referenz auf die GO „Quantum Deflection" im Verwundungswurf (nur grünes „4+") →
  Design-Crew-Item.

### 7. Artefakte aktuell — ⚠️ (Abschluss-Schritt muss schreiben)
Was **fehlt** und der Abschluss-Schritt setzen muss:
- **B-056:** Code fertig → nach `backlog_archive.md` archivieren; **aber** die drei UI-Folge-Befunde
  (6a–c) zuvor als neue Backlog-Items + Eintrag in `Stakeholder_Beobachtungen.md` sichern, sonst
  gehen sie beim Archivieren verloren.
- **B-098:** **Teilerledigung** — Rest-Scope umformulieren (Berechnung `_combi_hit_penalty` + Daten +
  Loader-Guard stehen; offen bleibt Profil-Auswahl-UI + Malus-Weitergabe an `combat.py`/`_common.py`,
  = R-COMBAT-35 `offen`). Nicht archivieren.
- **Briefing** (`.claude/tasks/briefing.md`): noch **nicht** angefasst (nicht im Diff) — Stand/nächster
  Schritt/Erkenntnisse nachziehen.
- **Ziel 7:** B-056/B-098 sind Backlog-Items, **keine** ziel7-Checkboxen — hier ist kein ziel7-Haken
  fällig (Erwartung „ziel7-Checkboxen" trifft nicht zu; sauber dokumentiert statt still gesetzt).
- Bereits erledigt im Diff (kein Nachzug nötig): Acceptance R-COMBAT-35/36/37, `rules_insights.md`,
  `S155_ui_verifikationen.md` (Punkte 2/3 positiv, Punkt 5 Befund).

---

## Sessionstand

- **Peak-Kontext 128k / 150k ≈ 85 %** (overview.md, Session 0dfe), 89 % der Token über Subagenten.
  Wind-down aktiv (>120k) — richtig, nichts Neues mehr beginnen. Für S156 verbleibt nur noch der
  Abschluss-Schritt (Artefakte + Commit), kein Umsetzungs-Headroom mehr.
- **Ziel-7-Fortschritt: teils.** Sichtbar an zwei abgeschlossenen Fachlichkeits-Items (B-056 fertig,
  B-098 Kernmechanik+Daten) und drei neuen Acceptance-Regeln (R-COMBAT-35/36/37). Ziel 7 bleibt aktiv;
  Stufe B/C und UX-Pass offen.

---

## Retro-Input S156 (Beobachtungen, keine Maßnahmen)

1. **UI-Verifikations-Vorbereitung fehlt (Stakeholder-Rüge, stark).** In
   `S155_ui_verifikationen.md` fordert der Stakeholder explizit Vorbedingungen + präzise Schritte
   („Fight Phase erreichen" ist nicht durchführbar; Roster + wie erreiche ich die Bedingung).
   Idee im Text: Template. Klarer Kandidat für eine S157-Retro-Maßnahme.
2. **Mock-Fragilität (B-078) erneut bestätigt.** `test_common.py` brauchte wieder Mock-Angleichung
   (`rules=[]` + Faction-Dirs), weil `SimpleNamespace`-Mocks brechen, sobald der Code ein neues
   Attribut liest — dasselbe Muster wie B-078.
3. **INV-4b-Blast-Radius auf `id`-Suffixe.** Der Beinah-Fehler (`..._wound_auto_fail` hätte „fail"
   necron-exklusiv gemacht und quer durch `src/` geflaggt) wurde erkannt und dokumentiert — zeigt
   aber, wie empfindlich der Vokabular-Scanner auf frei gewählte YAML-`id`-Suffixe reagiert.
4. **Handoff-Marker-Konvention.** `S156_planning.md` trägt weiter `STATUS: NEEDS-DECISION`, obwohl
   die Session ausgeführt wurde — Marker nicht auf ANSWERED nachgezogen. Kleiner Konvergenzbruch der
   eigenen Marker-Regel.
5. **Bewusste Teil-Verdrahtung als Muster.** B-098 lässt die `combat.py`/`_common.py`-Anbindung
   bewusst offen (R-COMBAT-35 `offen`), um Kollision mit dem B-056-Pfad zu vermeiden — sauber
   dokumentiert, hinterlässt aber eine „offen"-Acceptance-Regel, die nicht verwaisen darf.
