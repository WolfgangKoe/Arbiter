STATUS: ANSWERED — Plan freigegeben und umgesetzt/verschoben wie entschieden (B-056 fertig, B-098 Teil 2a fertig, B-028 auf Scope-Dokument S157 reduziert); behalten als aktuelle Session S156

# S156 — Planning-Entwurf

Datum: 2026-07-17

---

## Checkbox-Sync (Pflicht vor Einplanung)

`git log --oneline -15` gegen die S155-Behauptungen in `.claude/tasks/briefing.md` geprüft.
Commits S155: `ab36b80` (Fix Counter-Offensive timing, add availability hint) → `316240f`
(Pass unit key through stratagem spend callbacks) → `aeae746` (Remove gretchin_mob relic,
archive resolved backlog items) → `6ca8ef8` (Codify planner priority, UI-verification handoff
and retro rules) → `ee6eb15` (Close S155: archive done items, add B-102, ship UI-verification
handoff) → `8a69281` (Record S155 state in briefing, rotate session history) — **6 Commits**,
nicht 5 wie im Briefing-Kopf gezählt; der 6. (`8a69281`) ist der reine Abschluss-Commit
(Briefing-Stand + History-Rotation), keine inhaltliche Lücke.

**Ergebnis: keine Stale Checks gefunden.** Im Detail verifiziert:

- B-036/B-053/B-079/B-087 sind in `docs/goals/backlog.md` nicht mehr als Zeile vorhanden und
  tragen je einen `✅ …ERLEDIGT (S155)`-Abschnitt in `docs/goals/backlog_archive.md`
  (Zeilen 417/419/464/469/476) mit Commit-Beleg.
- `gretchin_mob` hat null Treffer mehr in `data/` oder `src/` (`grep -rn gretchin_mob data/ src/`).
- B-027 (`unit_key` durch Stratagem-Spend-Callbacks) ist in `316240f` verdrahtet
  (`chargePhase.py`, `movementPhase.py` + 2 Testdateien, 56 Zeilen Diff).
- B-102 ist neu in `docs/goals/backlog.md` als letzte Tabellenzeile vorhanden (E1-Zusatzbefund).
- Planner-Prio-Sortierung bereits umgesetzt: `docs/goals/backlog.md` führt B-056/B-098/B-028
  schon jetzt als die drei obersten `ToDo`-Zeilen — keine Umsortierung durch diesen Plan nötig.
- `docs/handoff/S155_ui_verifikationen.md` bleibt `NEEDS-DECISION` (Stakeholder-Vorgabe:
  Ergebnisse können in S156 nicht eingesammelt werden — siehe „Offene Fragen" unten, nur als
  Kenntnisstand geführt, kein Blocker für diesen Plan).

---

## Punkt 0 — S155-Review/Retro nachholen (R3-Regel, operating_model.md Event 1)

Laut `operating_model.md` Zeile 143–147 ist ein ausstehendes Review/Retro automatisch Punkt 0
der nächsten Planning-Session — hier der Fall, da S155 laut Briefing „Review/Retro steht aus".

**0.1 — Reviewer-Subagent (Opus, ADR-0007-Rolle „Reviewer")**

Auftrag: DoD-Review (CLAUDE.md 7-Punkte-Katalog) über die 6 S155-Commits `ab36b80`…`8a69281`.
Prüfumfang:

1. **Regelkonform** — E1-Fix (`ab36b80`, Counter-Offensive-Timing) gegen `core_rules.txt:3256`
   nachvollziehen (bereits von der Vorsession zitiert, hier gegenprüfen).
2. **Generisch** — kein neuer Fraktions-String in `src/` durch B-027-Wiring
   (`chargePhase.py`, `movementPhase.py`) eingeschleppt.
3. **Tests grün** — `pytest --tb=short` erneut fahren, gegen Briefing-Zahl (1880 passed /
   99,14 %) abgleichen.
4. **Architektur-Gate** — `pytest tests/architecture/ --no-cov -q` (31 passed laut Briefing
   erwartet inkl. Doku/Acceptance).
5. **Clean Code** — `pre-commit run` über die geänderten Dateien der 6 Commits.
6. **UI manuell verifiziert** — NICHT prüfbar in dieser Session (Stakeholder-Antwort zu
   `S155_ui_verifikationen.md` steht aus); Reviewer vermerkt das als „begründet n/a, wartet
   auf Stakeholder", kein Blocker fürs Review-Urteil selbst.
7. **Artefakte aktuell** — Backlog-/Ziel-Checkboxen, Handoff-Marker-Lifecycle (insbesondere ob
   `S155_planning.md` korrekt auf ANSWERED steht und die Löschregel für DONE-Marker eingehalten
   wurde) gegenprüfen.

Ergebnis als Datei (`docs/handoff/S156_review.md` o. ä.), Koordinator reicht wortgleich durch.

**0.2 — Retro (im selben Durchgang, getrennter Schritt)**

Vorausschauender Fragenkatalog (operating_model.md §ev5) durchgehen, endet mit einer
**nummerierten, entscheidbaren Maßnahmenliste**. Stakeholder-Vorgabe für S156 (vom Koordinator
mitgegeben): sobald Token-Schwellen erreicht sind, Review+Retro-Maßnahmen direkt nach der
DoD-Prüfung vorlegen und **möglichst schon committen** — Übernahme/Ergänzung der Maßnahmen
selbst erst zu Beginn der Folgesession. Das ändert nichts an der Reihenfolge Review→Retro→
Maßnahmen-Entscheid, verkürzt nur die Wartezeit bis zum Commit.

**Tier:** Opus (Reviewer-Subagent, ADR-0007). **Token-Schätzung:** ~20–25k (6 Commits, überschaubarer
Diff — siehe `git diff ab36b80~1..8a69281 --stat`: 21 Dateien, 618/476 Zeilen).
**Modus:** Gate (Review-Urteil selbst kein Stakeholder-Entscheid, aber Maßnahmen-Entscheid danach ist Konsent).

---

## Arbeitswelle (nach Punkt 0), Backlog-Reihenfolge B-056 → B-098 → B-028

### B-056 — Quantum Shielding fester Invuln-Wert

**Scope:** Zwei getrennte, gleichnamige Mechaniken (Stakeholder-Entscheid S152, Scope (b)):
(1) Stratagem „Quantum Shielding" (`data/wh40k_9e/necrons/stratagems.yaml:465-472`) — temporärer
**fester** 4+ Invuln, kein additiver Modifier; (2) Unit-Fähigkeit „Quantum Shielding"
(`data/wh40k_9e/necrons/unit_abilities.yaml:905-919`) — permanenter 5+ Invuln (bereits
funktionsfähig über `effect.type: invuln_save`/`ability_invuln_save()`,
`src/gameMechanic/abilityEngine.py:517-521`, `combine=min`) **plus** „unmod. Wound 1–3 = Attacke
schlägt automatisch fehl" — laut `rule_text` vorhanden, aber **kein Effekt-Feld in der YAML und
null Treffer für `quantumShielding`/`quantum_shielding` in `src/`** (`grep -rn quantumShielding
src/` → leer). **Planner-Korrektur gegenüber der bisherigen Backlog-Formulierung:** das ist
**kein reiner Anzeige-Bug**, sondern eine komplett fehlende Engine-Mechanik (analog, aber
invertiert zu `auto_wound`/Tesla — „auto-fail bei unmod. Wound 1–3" statt „auto-wound bei
unmod. 6"). Das S148-Anzeige-Symptom (keine 3× ✕ in der Wound-Zeile) ist eine *Folge* der
fehlenden Mechanik, nicht Ursache. Effort-Risiko: ~35k könnte knapp sein, wenn beide Teile
(neuer fester-Invuln-Typ + neuer Auto-Fail-Effekttyp) in einem Brief landen sollen — siehe
Auftragsgrößen-Gate-Hinweis unten.

**Betroffene Dateien (belegt):**
- `data/wh40k_9e/necrons/stratagems.yaml:465-472` (Stratagem-Effekt umstellen auf neuen Typ)
- `data/wh40k_9e/necrons/unit_abilities.yaml:905-919` (neues `effect`-Feld für Auto-Fail ergänzen)
- `src/gameMechanic/combat.py:223-257` (`resolve_save`, Invuln-Logik — neuer „fest statt additiv"-Pfad)
- `src/gameMechanic/abilityEngine.py:517-521` (`ability_invuln_save`, ggf. Auto-Fail-Sammelfunktion)
- `src/uiLayout/_common.py` (Save-Block-Anzeige + Wound-Zeilen-Debuff-Marker, S148-Befund)
- Tests: `tests/gameMechanic/test_combat.py`, `tests/gameMechanic/test_ability_engine.py`

**Test-Anforderung (4-Schichten-Mandat):** (1) reine Funktionstests für den neuen
„fest-statt-additiv"-Invuln-Pfad in `combat.py`, (2) Ability-Engine-Test für den neuen
Auto-Fail-Effekttyp, (3) HTML-Output-Test für die Wound-Zeilen-Debuff-Anzeige (Render-Code-Pfad,
S122-Lehre: Anzeige kann lokal neu rechnen), (4) Regressionstest gegen den S148-Befund
(Annihilation Barge, unmod. Wound 1-3).

**Tier:** Sonnet (Implementierung nach fixem Muster, kein offenes Zweckprogramm).
**Token-Schätzung:** ~35k (M-Obergrenze) — **Selbst-Stopp bei ~50k**, danach Zwischenstand
zurückgeben statt weiterzuarbeiten (Auftragsgrößen-Gate).
**Parallel zu:** B-098 (disjunkte Dateien: Necrons vs. Orks, `combat.py`/`abilityEngine.py`
vs. `weapon.py`/Ork-YAML — kein Überschneidungsrisiko).

### B-098 Teil 2 — Boss Nob Kombi-Waffenprofile

**Scope:** Zwei Teilaufgaben laut Backlog, beide verifiziert:

(a) **`weapon_swap` für Kombi-Waffen** — `data/wh40k_9e/orks/units.yaml`, Boss-Nob-Gruppe
(Zeile 542-565, NICHT die Warbike-Nob-Gruppe ab Zeile 1095). **Planner-Korrektur:** Das generische
`weapon_swaps`-Schema (`scope: group`, `replaces: [...]`, `options: [...]`, `pick: N`) existiert
bereits und wird an derselben Stelle schon für den `nob_weapons`-Swap genutzt
(`src/gameObjects/loader.py:177-267`) — das ist vermutlich **kein neuer Loader-Code**, sondern
ein zweiter `weapon_swaps`-Eintrag (`pick: 1`, `replaces: [slugga, choppa]`,
`options: [kombi_rokkit, kombi_skorcha]`). **Zu klären vor Umsetzung:** Verträgt der Loader zwei
`weapon_swaps`-Einträge mit überlappender `replaces`-Liste auf derselben Modellgruppe
(gegenseitig exklusive Wahl: entweder zwei Einzelwaffen aus `nob_weapons` ODER eine Kombi-Waffe)?
Das ist der einzige noch offene Verdrahtungspunkt in Teil (a) — kurzer Code-Check zu
Sitzungsbeginn des Executor-Briefs, kein Extra-Plan nötig.

(b) **Kombi-Mechanik „ein oder beide Profile, -1 to hit bei beiden"** — echte Engine-Lücke,
bestätigt: `kombi_rokkit`/`kombi_skorcha` (`data/wh40k_9e/orks/weapons.yaml:1099-1148`) haben
bereits beide Profile inkl. Freitext-`abilities`-Beschreibung, aber **kein strukturiertes
`effect`-Feld** für „Profil(e) wählen + kombinierter −1-Hit-Malus bei beiden". Das ist eine neue
generische Mehrprofil-Auswahl-Mechanik (nicht Necron-/Ork-spezifisch — gehört generisch in
`shootingPhase.py`/`weapon.py`).

**Betroffene Dateien (belegt):**
- `data/wh40k_9e/orks/units.yaml:542-565` (Boss-Nob-Gruppe, neuer `weapon_swaps`-Eintrag)
- `data/wh40k_9e/orks/weapons.yaml:1099-1148` (neues `effect`-Feld auf beiden Profilen je Kombi-Waffe)
- `src/gameObjects/weapon.py:6-21` (`WeaponProfile`, ggf. neues Feld für Profil-Gruppierung)
- `src/gameMechanic/shootingPhase.py` (Profil-Auswahl-UI + −1-Hit-Anwendung bei „beide gewählt")
- Tests: `tests/gameObjects/test_weapon.py`, `tests/gameMechanic/test_shooting.py`

**Test-Anforderung:** (1) Loader-Test für den neuen `weapon_swap` (Boss Nob bekommt Kombi-Waffe,
Warbike-Nob NICHT), (2) Engine-Test „nur ein Profil gewählt" (kein Malus), (3) Engine-Test
„beide Profile gewählt" (−1 to hit auf beide), (4) HTML/Render-Test der Profil-Auswahl-UI.

**Tier:** Sonnet. **Token-Schätzung:** ~35k, **Selbst-Stopp ~50k**.
**Parallel zu:** B-056 (disjunkt).

### B-028 — „used on ⟨Einheit⟩"-Suffix auf alle reaktiven GOs ausweiten

**Läuft NICHT parallel zu B-056** (beide berühren `src/uiLayout/_common.py`). Reihenfolge:
nach der B-056/B-098-Welle.

**Erster Teilschritt — Menge zählen (M1-Pflicht, S155-Lehre), hier vom Planner bereits erledigt:**

`render_reactive_stratagem_box` (`src/uiLayout/_common.py:746-`) ist laut Docstring und Code
(Zeile 810: `load_stratagems(...)`) **ausschließlich auf Stratagems zugeschnitten** — sie lädt
nur `stratagems.yaml`, keine Ability-Dateien. „used on"-Suffix (`stratagem_used_elsewhere_unit_name`,
`docs/handoff/S150_usedon_renderpaths.md`) hängt komplett an `stratagem_use_anchors`
(stratagem-spezifischer State).

**Reaktive Non-Stratagem-GOs (per `grep -c "timing: phase_reactive"` gezählt, IDs per `awk`
extrahiert — 11 insgesamt):**

| Datei | Anzahl | IDs |
|---|---|---|
| `data/wh40k_9e/necrons/unit_abilities.yaml` | 8 | `the_silent_king.noctilith_beacons`, `the_silent_king.vengeance_of_the_enchained`, `warriors.their_number_is_legion`, `canoptek_plasmacyte.infused_madness`, `hexmark_destroyer.inescapable_death`, `gauss_pylon.arc_fields`, `seraptek_heavy_construct.wrath_of_the_seraptek`, `triarch_stalker.targeting_relay` |
| `data/wh40k_9e/necrons/faction_abilities.yaml` | 1 | `reanimation_protocols` |
| `data/wh40k_9e/necrons/wargear.yaml` | 1 | `gloom_prism` |
| `data/wh40k_9e/orks/subfaction_abilities.yaml` | 1 | `klan.freebooterz.competitive_streak` |

**Wichtiger Vorab-Befund (Planner, per grep bestätigt):** Diese 11 Einträge werden **nirgends**
über einen Reactive-GO-Card-Pfad gerendert — `grep -rn "phase_reactive" src/` findet nur zwei
Konsumenten (`gameProtocoll.py:298`, `_common.py:430`-Kommentar), beide ausschließlich für
Stratagems. Es gibt aktuell **keinen** generischen „reaktive Ability als GO-Card"-Renderer.
**Konsequenz:** B-028 ist damit nicht nur „Suffix auf bestehende Boxen ausweiten", sondern setzt
voraus, dass diese 11 Fähigkeiten überhaupt erst als reaktive GO-Card gerendert werden — eine
größere Vorstufe als der Backlog-Eintrag suggeriert. **Empfehlung an den Executor-Brief:** vor
Implementierungsbeginn mit dem Stakeholder klären, ob B-028 in S156 auf **Konzept/Scope-Schärfung**
reduziert wird (Ist-Stand dokumentieren, Aufwand neu schätzen) statt direkt Code zu schreiben —
siehe „Offene Fragen" unten.

**Betroffene Dateien (falls Umsetzung freigegeben wird):**
- `src/uiLayout/_common.py` (`render_reactive_stratagem_box` generalisieren oder neuer
  paralleler Renderer für Ability-GOs)
- `src/gameMechanic/abilityEngine.py` (Zugriffsfunktion analog `stratagem_used_elsewhere_unit_name`
  für Abilities)
- `docs/handoff/S150_usedon_renderpaths.md` (Nachzug, sobald neue Pfade existieren)

**Tier:** Sonnet für die Zähl-/Bestandsaufnahme ist bereits durch diesen Plan erledigt; falls
Umsetzung startet: Sonnet (Implementierung), aber Scope-Entscheid (Konzept vs. direkte Umsetzung)
ist **Konsens**-Modus — siehe offene Frage 1.
**Token-Schätzung:** ~35k falls direkte Umsetzung freigegeben; ~10–15k falls nur
Scope-Dokument (Konzept + Aufwandsschätzung, kein Code).

---

## Token-Budget der Session

| Punkt | Schätzung | Kumulativ |
|---|---|---|
| Checkbox-Sync + Planning (dieser Schritt) | bereits verbraucht | — |
| Punkt 0 (Review + Retro + Maßnahmen-Entscheid) | ~20–25k | ~25k |
| B-056 (Sonnet, parallel) | ~35k | ~60k |
| B-098 Teil 2 (Sonnet, parallel zu B-056) | ~35k | ~60k (parallel, nicht additiv zum Hauptfenster außer Koordinations-/Review-Overhead ~10k) |
| Koordinator-Review beider Diffs + eine zentrale Vollsuite | ~10k | ~95k |
| B-028 (nur falls Headroom reicht, s. u.) | ~15k (Scope-Dokument) oder ~35k (volle Umsetzung) | ~110k / ~130k |

**Abbruchkriterium:** Wind-down ab ~120k Koordinator-Kontext (geordnet, laufende Aufgabe
abschließen, nichts Neues beginnen), spätestens ~135k Session beenden. Nach der B-056/B-098-
Welle liegt der Verbrauch voraussichtlich bereits bei ~95-100k inkl. Punkt 0 — **B-028 nur als
Scope-Dokument (~15k) einplanen**, volle Umsetzung (~35k) realistisch erst S157, es sei denn
Punkt 0 + Welle laufen deutlich günstiger als geschätzt. Review/Retro-Budget (~45k) ist in der
obigen Zeile „Punkt 0" bereits enthalten (Review 0.1 ist Teil davon, Retro/Maßnahmen-Entscheid
kommt am Session-Ende nochmal dazu — nicht doppelt einplanen, sondern das End-Retro nutzt den
gleichen Reviewer-Output).

---

## Offene Fragen an den Stakeholder

1. **B-028-Scope (wichtigste Frage, früh im Plan platziert laut agent_scopes.md-Pflichtschritt
   „Entscheidungs-Timing"):** Der Vorab-Befund zeigt, dass die 11 reaktiven Non-Stratagem-GOs
   aktuell **gar nicht** als GO-Card gerendert werden — B-028 ist damit größer als „Suffix
   ausweiten". Zwei Optionen: **(A)** S156 liefert nur ein Scope-/Konzeptdokument (Aufwand neu
   schätzen, IST-Zustand der 11 Fähigkeiten dokumentieren) — Umsetzung folgt als eigener Plan;
   **(B)** direkte Umsetzung wird trotzdem versucht (höheres Risiko, das M-Obergrenze-Budget
   ~35k zu sprengen, da zuerst ein neuer Renderer-Pfad gebaut werden muss). Empfehlung des
   Planners: Option A.
2. **B-056-Effort-Risiko:** Die Auto-Fail-Mechanik (unmod. Wound 1-3) existiert engine-seitig
   noch gar nicht (nicht nur ein Anzeige-Bug, s. o.) — passt ~35k noch, oder soll B-056 in zwei
   Teil-Briefs (Stratagem-Fix / Ability-Fix) gesplittet werden, falls der Executor die
   Selbst-Stopp-Schwelle (~50k) erreicht?
3. **B-098(a) Loader-Frage:** Unterstützt der bestehende `weapon_swaps`-Loader zwei sich
   gegenseitig ausschließende Swap-Gruppen auf derselben Modell-Gruppe (Kombi-Waffe ALS
   Alternative zu den zwei Einzelwaffen, nicht zusätzlich)? Falls nicht, ist das ein kleiner
   Loader-Erweiterungspunkt zusätzlich zum Datenwunsch — Executor klärt das als erste
   Diagnose-Aktion im eigenen Brief, keine gesonderte Stakeholder-Entscheidung nötig, wird
   hier nur zur Transparenz genannt.

---

## Stale-Check-Befunde

Keine. Siehe „Checkbox-Sync" oben — alle S155-Behauptungen (E1-Fix, B-027, gretchin_mob,
B-036/053/079/087-Archivierung, B-102-Neuaufnahme, Doku-Regeln in agent_scopes.md/
operating_model.md) sind durch Commits belegt.
