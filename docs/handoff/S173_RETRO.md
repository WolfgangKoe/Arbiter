STATUS: NEEDS-DECISION

# S173 — Retro (Maßnahmen zur Entscheidung im S174-Planning)

Lebensdauer: bis Stakeholder-Entscheid im S174-Planning; gewählte Maßnahmen dort in die
kanonischen Artefakte überführen, danach Datei löschen. Nicht genannte gelten als verworfen
(operating_model.md §ev1).

## Was gut lief

- **Live-Verifikation im Fluss:** B-125 + B-126 noch in derselben Session stakeholder-positiv
  bestätigt (`S173_explode_panel_verifikation.md`).
- **Review GO im ersten Anlauf** (zweite Session in Folge).
- **Careen! korrekt generisch modelliert:** neuer `pre_explode_stratagem`-Effekttyp statt
  `auto_explode` — die S165-Fehlklassifikation (Explosion erzwingen) bewusst vermieden.
- **Delegation hielt den Koordinator-Kontext lange schlank:** Planner + beide Executor + Review
  als Subagenten; deren Verbrauch belastete das Hauptfenster nicht.

## Was schief lief

- **Brief-1-Executor ignorierte die „Vollsuite synchron / `run_in_background` VERBOTEN"-Auflage**
  und hängte an einem verlorenen Background-pytest — exakt das S172-Muster. Der Koordinator musste
  die Vollsuite selbst im **Vordergrund** fahren (~7 min, ~414 s) — teuerster Einzel-Kontext-Posten
  der Session. Bittere Pointe: **S172-Retro-M1 (Vollsuite synchron) wurde in S173 NICHT übernommen**
  — das Problem trat prompt wieder auf.
- **Koordinator-Kontext-Überlauf:** trotz Wind-down über 135k gelaufen (Vordergrund-Vollsuite +
  viele Verifikations-Bashes). Delegation der Gate-Messung griff zu spät.
- **Doku-Zitat-Drift (Review-F1):** `design_system.md` §7.1 zitiert Careen! noch mit dem alten
  Wortlaut, während YAML + P-16 in derselben Session korrigiert wurden.

## Maßnahmen (nummeriert, entscheidbar)

1. **Retro-M1 „Vollsuite synchron" doch übernehmen** (`agent_scopes.md`, Executor-Brief-Pflichten):
   Testläufe in Executor-Briefs SYNCHRON/Vordergrund, `run_in_background` für pytest verboten. In
   S172 verworfen, in S173 zweimal als Fehlerquelle bestätigt. **Empfehlung: übernehmen (XS).**
2. **Koordinator fährt keine Gate-Vollsuiten selbst im Vordergrund** (`operating_model.md`/
   `agent_scopes.md`): Bei Executor-Hänger die Suite entweder per SendMessage vom Executor synchron
   nachfahren lassen oder als Background + Monitor-until-Loop messen — nie ~7 min Vordergrund im
   Koordinator-Kontext. **Empfehlung: übernehmen (XS).**
3. **Wind-down härter ab ~110k:** ab dieser Marke keine teuren eigenen Bash-Läufe (Vollsuite,
   lange greps) mehr im Koordinator — delegieren oder verschieben. **Empfehlung: übernehmen (XS).**

## Offene Nachzüge (aus Review, KEINE Retro-Maßnahmen — direkt fürs S174-Planning)

- **F1:** `design_system.md` §7.1 Careen!-Zitat an YAML/P-16 angleichen; Fenster-Entscheid
  (GO-Karte sichtbar VOR vs. AB Wurf) in die offene Careen!-UI-Verifikation aufnehmen.
- **F2:** stale „(Umsetzung Folgesession)"-Marker in §1.7 (Zeilen 197/253/276) entfernen — durch
  B-125 umgesetzt.
- **F3 (nice-to-have):** überlange Docstrings im Baustein-②-Block gegen die Kommentar-Konvention
  verschlanken (Ratchet).

## Sessionstand-Kurzfassung (für S174-Planning)

- Review S173: **GO, keine Blocker**; Gates: 2144 passed, Coverage 99,20 %, Arch 8/8,
  black/isort/ruff sauber.
- Geliefert: Retro-M3 verankert (agent_scopes); B-125 + B-126 (Explodes-Panel: value-Seed +
  `dice_notation_max`-Cap) **stakeholder-verifiziert positiv**; B-122 „Careen!" als generischer
  `pre_explode_stratagem`-GO (CP via cp_overrides, Wurf unberührt), §7.1 + P-16 nachgezogen.
- **Offen S174:** (1) diese Retro entscheiden; (2) **Backlog-Archivierung** B-125/B-126/B-122
  (eigener ~100k-Brief laut Retro-M3); (3) **Careen!-UI-Verifikation** (`S173_careen_verifikation.md`);
  (4) Review-Nachzüge F1/F2/F3; danach B-028c2 (`reroll_rp`) / Spyder-Konzept laut `backlog.md`.
