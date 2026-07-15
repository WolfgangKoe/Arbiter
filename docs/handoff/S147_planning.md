STATUS: ANSWERED

# S147 — Planungsentwurf

**Rolle:** Planner-Subagent (general-purpose, Tier Sonnet). Gelesen: `CLAUDE.md`,
`.claude/tasks/next_session.md`, `docs/goals/backlog.md` (vollständig), `docs/goals/ziel7.md`,
`docs/reference/agent_scopes.md`, `docs/handoff/Stakeholder_Beobachtungen.md`,
`docs/handoff/S146_planning.md`, `docs/handoff/README.md`, plus gezielte `grep`/`git log`
gegen `data/wh40k_9e/`, `src/gameMechanic/`, `src/gameObjects/`.

## Kontextstand

S146 hat Welle 1 (on_target-Anker + Vigilus-Traits-Entfernung) committet (`2a169b6`) und
Ziel-7-Stufe-B abgeschlossen; Welle 2 (Klan/Dynastie K1 ∥ FixD Brief 1) war freigegeben,
lief aber am Headroom-Gate nicht mehr an. Review kam mit **Auflage B1** (Deklarations-Anker
zeigt Wound-only-GOs auch am Hit-/Save-Anker) zur GO. Für S147 kommt vom Stakeholder ein
neuer, größerer Auftrag: ein systematisches GO-Effekt-Audit (Ergänzung A/B) plus eine
Handoff-Bereinigung (C) — beide werden unten in die bestehende Prioritätenliste eingeordnet.

---

## Befunde

### Checkbox-Sync (PFLICHT, gegen `git log --oneline -20`)

Einzige zuvor offene Checkbox in `ziel7.md` (Zeile 76, Stufe-B manuelle UI-Verifikation) ist
korrekt in Commit `2a169b6` gesetzt (`git show 2a169b6` zeigt den Diff `- [ ]` → `+ [x] …S146,
Stakeholder-Verifikation 2026-07-14…`). **Kein stale Check.** Alle übrigen Ziel7-Haken liegen
außerhalb des 20-Commit-Fensters und wurden bereits in S146 verifiziert (keine gegenteilige
Spur im aktuellen Log). Ergebnis deckt sich mit dem eigenen Checkbox-Sync in `S146_planning.md`.

### grantsKeyword — Ist-Bestand (PFLICHT-Grep, Bestandsaufnahme vor Audit-Vergabe)

Die Stakeholder-Prämisse „GAUSS-Waffen tragen eine Ability `grantsKeyword`, die der Einheit
das Keyword GAUSS gibt (analog TESLA)" ist **so nicht belegbar**:

- Das Feld heißt in Code/Daten durchgängig `grant_keyword` (Singular, snake_case) —
  `grantsKeyword`/`grants_keyword` kommt in `data/` und `src/` **nirgends** vor.
- `grep -rn "grant_keyword" data/ src/` findet genau **2 Verwendungen**:
  1. `data/wh40k_9e/necrons/wargear.yaml:16` (Canoptek Cloak → `keyword: FLY`)
  2. `data/wh40k_9e/necrons/stratagems.yaml:47` (Hand of the Phaeron) — **aber mit falschem
     Sub-Feld:** `effect: {type: grant_keyword, stat: phaeron}` statt `keyword: phaeron`.
     `_apply_persistent_effect` (`src/gameObjects/loader.py:822-825`) liest nur
     `effect.get("keyword", "")`; mit `stat:` statt `keyword:` ist `kw == ""`, der Guard
     `if kw and …` verhindert jede Wirkung — **dieses Stratagem vergibt das PHAERON-Keyword
     aktuell nie**, obwohl Loader + Test (`test_apply_persistent_effect_grant_keyword_adds_to_keywords`)
     den Mechanismus grundsätzlich unterstützen.
- Für **GAUSS** existiert **keine** `grant_keyword`-Ability in irgendeiner Necron-YAML.
  Necron Warriors (`units.yaml:148`) haben keinen Eintrag, der ihnen GAUSS als Keyword
  zuweist. GAUSS/TESLA werden stattdessen ausschließlich **auf Waffenebene** als
  Text-Erkennung behandelt (`_detect_weapon_special`, `src/uiLayout/_common.py:1605/1920`) —
  ein separater Mechanismus, der nichts mit `unit.keywords`/der unitCard-Badge-Zeile zu tun hat.

**Einordnung:** Das ist kein Anzeige-Bug einer bestehenden Funktion, sondern zwei getrennte
Befunde: (a) ein wahrscheinlich echter, aber winziger Bug (Hand of the Phaeron `stat`→`keyword`),
(b) eine **fehlende Konvention** „Waffen-Sondertyp verleiht der tragenden Einheit ein
sichtbares Keyword" — die gibt es heute schlicht nicht, weder für GAUSS noch für TESLA. Muss
dem Stakeholder als Klärungsfrage zurückgespiegelt werden (s. Entscheidungsfrage 1 unten),
nicht stillschweigend als „Bug" in den Audit-Fixing-Plan geschrieben.

### Fire-Overwatch-Bedingungsprüfung — Ist-Bestand bestätigt lax

`grep -n "ranged\|has_ranged" src/gameMechanic/stratagemEngine.py` → **0 Treffer**. Fire
Overwatch (`data/wh40k_9e/_shared/stratagems.yaml:73-85`) hat `conditions: []`
(keyword-basiert, s. Kommentarblock `stratagemEngine.py:113-141`) — es gibt **keinen** Check,
ob die reagierende Einheit überhaupt eine Fernkampfwaffe besitzt. Die Skorpekh-Destroyers-
Beobachtung ist damit strukturell erklärt: die generische `stratagem_conditions_met`-Prüfung
kennt nur Keyword-Bedingungen, keine Waffentyp-/Reichweiten-/Phasen-Bedingungen. Bestätigt
Stakeholder-Punkt B.2 als reale, systematische Lücke (nicht nur ein Einzelfall).

### Handoff-Drift (Koordinator-Befund verifiziert)

`next_session.md` Zeile 65-67 behauptet, `S145_planning.md` sei „gelöscht S146" — **falsch**:
`git show 2a169b6 --stat` zeigt nur zwei gelöschte Handoff-Dateien
(`S143_on_target_anker_konzept.md`, `S145_stufeB_verifikation.md`); `S145_planning.md`
existiert weiterhin (STATUS: ANSWERED) und wird **aktuell noch aktiv referenziert**:
`docs/goals/backlog.md` Zeilen 16, 32, 34 verweisen auf seine §6.2/6.3-Herleitung und
§Option C (abilityEngine-Vorplanung) als Detailquelle — die Inhalte sind dort **nicht**
dupliziert, nur die Ergebnisse (Prioritätenliste-Tabelle). Löschen wäre daher aktuell ein
Verstoß gegen den DONE-Lifecycle (Erkenntnisse überführen **vor** dem Löschen) — s.
Handoff-Bereinigungsliste unten.

### GO-Effekt-Badge-Lücke (4 GOs) geht im neuen Audit auf

Der bestehende Backlog-Punkt „aktive GO-Effekte ohne Badge am Wirkort" (Techno-Oracular
Targeting, Disintegration Capacitors, Relentless Onslaught, Solar Pulse) ist ein **Spezialfall**
der vom Stakeholder neu beauftragten systematischen Frage „Effekt in YAML deklariert, aber von
Engine/UI nicht ausgewertet". Empfehlung: **nicht mehr als eigenen 4-GO-Punktfix einplanen** —
der Audit-Brief „Stratagems" (Aufgabe 3 unten) deckt Necron-Stratagems ohnehin vollständig ab
und wird diese 4 Fälle als Teilmenge seines Befundkatalogs wiederfinden. Der Fixing-Plan aus
dem Audit behandelt sie dann gemeinsam mit allen anderen gefundenen Lücken statt isoliert.

---

## Aufgabenliste (vorgeschlagene Reihenfolge)

| # | Aufgabe | Effort | Token-Schätzung | Modus | Subagent + Tier | Scope |
|---|---|---|---|---|---|---|
| 1 | Handoff-Bereinigung | S | ~10k | Gate (Edit) | Executor, Sonnet* | s. Bereinigungsliste unten |
| 2 | B1-Design-Entscheid (Konsens-Frage) | XS | ~2k | Konsens | — (Koordinator fragt direkt) | `docs/handoff/S146_review.md`, `backlog.md` §2 B1 |
| 3 | GO-Audit A — Stratagems (alle Fraktionen) | M | ~35k | Konsent (Recherche, kein Code) | Audit-Subagent, Sonnet** | `_shared/stratagems.yaml`, `necrons/stratagems.yaml`, `orks/stratagems.yaml`, `stratagemEngine.py`, `core_rules.txt` |
| 4 | GO-Audit B1 — Necron-Abilities | M | ~35k | Konsent | Audit-Subagent, Sonnet** | `necrons/{faction_abilities,unit_abilities,subfaction_abilities,wargear,relics,arkana}.yaml`, `abilityEngine.py`, `loader.py` |
| 5 | GO-Audit B2 — Ork-Abilities | M | ~30k | Konsent | Audit-Subagent, Sonnet** | `orks/{faction_abilities,unit_abilities,subfaction_abilities,wargear,relics}.yaml`, `abilityEngine.py`, `loader.py` |
| 6 | B1-Umsetzung (nach Entscheid aus #2) | S–M | ~15–30k | Gate | Executor, Sonnet | `src/uiLayout/_common.py`, `tests/uiLayout/` |
| 7 | Welle 2a — Klan/Dynastie Brief K1 | S | ~15k | Gate | Executor, Sonnet | `necrons/subfaction_abilities.yaml`, `orks/subfaction_abilities.yaml`, `tests/gameObjects/` |
| 8 | MWBD-Instanz-Fix | S | ~12k | Gate | Executor, Sonnet | `src/gameMechanic/commandPhase.py`, `tests/gameMechanic/` |
| 9 | Welle 2b — FixD Brief 1 (NACH #6, gleiche Datei) | M | ~38k | Gate | Executor, Sonnet | `src/uiLayout/_common.py`, `tests/uiLayout/test_common.py` |

\* Sonnet statt Haiku-Default: Aufgabe 1 erfordert das Umschreiben eines
Querverweis-Satzes in `backlog.md` (kein reiner Lookup, s. u.).
\*\* Sonnet statt Haiku-Default: Audit erfordert Cross-Referenzierung mehrerer YAML-Dateien
gegen Engine-Code **und** Regelwortlaut (`core_rules.txt`), keine geschlossene Ja/Nein-Prüfung
gegen einen einzelnen Text — Interpretationsspielraum rechtfertigt die Abweichung.

**Reihenfolge-Begründung:**
- **#1 sofort:** keine Abhängigkeiten, klein, schafft Ordnung vor dem großen Audit.
- **#2 an den Session-Anfang:** Konsens-Frage braucht vollen Stakeholder-Headroom (agent_scopes.md
  „Entscheidungs-Timing"); Umsetzung (#6) hängt von der Antwort ab.
- **#3–#5 parallel zu #2/#6:** reine Recherche, kein Code, keine Dateikonflikte mit irgendetwas
  anderem in dieser Liste — laufen im Hintergrund, während auf die B1-Antwort gewartet wird.
  Aufteilung in 3 Briefs (Stratagems / Necron-Abilities / Ork-Abilities) hält jeden unter
  Effort M (ein einzelner Brief über alle ~15 YAML-Dateien + 2 Engines + Regeltext wäre L).
- **#6 nach #2:** kann erst starten, wenn die Design-Entscheidung feststeht.
- **#7/#8 dateidisjunkt zu #6** — können parallel dazu laufen, sobald Freigabe vorliegt.
- **#9 zwingend NACH #6:** beide schreiben `_common.py` (dieselbe Kollisionsregel wie in
  S145/S146 zwischen on_target-Anker und FixD Brief 1).
- Die **Fixing-Pläne aus #3–#5** landen als eigene Aufgaben in der nächsten Session (S148) —
  zu groß, um in S147 noch umgesetzt zu werden; das Audit selbst ist das Ziel dieser Session.

**Testschichten je Aufgabe:**
- #1: kein Test nötig (reine Doku/Handoff-Pflege), Doku-Gate (`pytest tests/docs/ --no-cov -q`) am Ende.
- #2: keine.
- #3–#5: keine Code-Tests (reine Recherche); Audit-Output selbst muss jede Lücken-Behauptung
  mit Datei:Zeile belegen (Bestandsaufnahme-Pflicht S144-M1).
- #6: Render-Test (HTML-Output des betroffenen Ankers) + Negativ-Test (B2 aus Review) +
  Vollsuite + Architektur-Gate.
- #7: Loader-/Daten-Regressionstest je korrigiertem Wortlaut + Vollsuite.
- #8: Regressionstest `_render_buff_roll_ability` mit 2 gleichen Einheiten (`_wargear_state_key`-
  Muster) + Vollsuite.
- #9: 6-8 neue Tests für `compute_resolution_context` (laut Plan `S142_fixD_resolution_tabs.md`)
  + Vollsuite + Architektur-Gate + manueller Pixel-Vergleich.

---

## Detailskizze — GO-Audit-Briefs (Aufgaben 3–5)

Jeder der drei Audit-Briefs bekommt denselben Auftrag-Rahmen, nur anderen Datei-Scope:

**Ziel:** Für jede GO (Stratagem/Ability) im Scope feststellen: (a) hat sie ein `effect`/
`persistent_effects`-Feld, das ein bestimmtes engine-seitiges Verhalten verspricht — wird
dieser Effekttyp tatsächlich von `stratagemEngine.py`/`abilityEngine.py` konsumiert (grep +
Lese-Beleg, nicht Vermutung)? (b) Umgekehrt: gibt es Engine-Effekttypen, die **keine** YAML
im Scope nutzt (totes Feature)? (c) Ist die `conditions`-Prüfung vollständig (Waffentyp/
Keyword/Phase/Reichweite), oder nur teilweise (Keyword-only wie bei Fire Overwatch)? Jede
Zeile im Ergebnis-Katalog braucht Datei:Zeile-Beleg (Bestandsaufnahme-Pflicht) und eine
Klassifikation (Lücke bestätigt / Lücke widerlegt / neuer Bug gefunden).

**Output:** ein Handoff-Dokument `docs/handoff/S147_go_audit_<scope>.md` (`STATUS: DONE` nach
Fertigstellung, da reines Recherche-Ergebnis ohne offene Stakeholder-Frage — außer die
grantsKeyword-Frage, die als eigener `NEEDS-DECISION`-Abschnitt hineingehört) mit: (1)
Lücken-Tabelle, (2) Fixing-Plan-Vorschlag (grob, ≤ M-Häppchen für die nächste Session), (3)
explizitem Bestandsaufnahme-Nachweis je Behauptung.

**Grundannahme, die jeder Audit-Brief bestätigen lassen muss (Konzept-Konvention):**
„Effekte, die die App nicht selbst würfelt, sondern nur anzeigt/hinweist (Klasse B/Hybrid),
zählen NICHT als Lücke, solange ein Tisch-Hinweis existiert — nur fehlende Auswertung UND
fehlender Hinweis ist ein Befund." (Analog zur bestehenden A/B/C-Klassifikation aus
`docs/spec/acceptance/rules.md`.)

**Selbst-Stopp:** Budget wie in der Tabelle, harte Schwelle 1,5× — bei Überschreitung
Zwischenstand (bereits geprüfte Dateien + offene) zurückgeben statt weiterzuarbeiten.

---

## Handoff-Bereinigungsliste (Aufgabe 1)

| Datei | Aktion | Begründung |
|---|---|---|
| `S146_planning.md` | **Löschen** | STATUS ANSWERED; Inhalt (Welle-1-Ergebnis, Checkbox-Sync, Vigilus-Bestand, K1-Tabelle, Freigabe-Antworten) bereits vollständig in `next_session.md` + `backlog.md`-Prioritätenliste überführt; einziger Referenzierer ist `next_session.md` selbst (wird ohnehin am Session-Ende neu geschrieben). |
| `S145_planning.md` | **Behalten (noch nicht löschen)** — stattdessen zuerst `backlog.md` Zeilen 16/32/34 entkoppeln | Wird aktuell noch **aktiv referenziert** als Detailquelle für §6.2/6.3-Herleitung und §Option C (abilityEngine-Vorplanung) — diese Inhalte sind NICHT anderswo dupliziert. Löschen jetzt würde den S144-Retro-M2-Grundsatz verletzen (Erkenntnisse überführen VOR dem Löschen). Vorschlag: kleiner Folge-Schritt (Teil von Aufgabe 1) — §Option C wörtlich nach `backlog.md` §4 (Architektur-Schulden, abilityEngine-Punkt) verschieben, §6.2/6.3-Herleitung als knappe Fußnote in die Prioritätenliste selbst aufnehmen, DANACH löschen. Falls das in Aufgabe 1 zu groß wird: nur den next_session.md-Drift korrigieren (Zeile 65-67: Datei NICHT „gelöscht S146", weiterhin offen), Löschung auf S148 verschieben. |
| `S144_klan_dynastie_konzept.md` | Behalten | Explizit für K2 (Rang 7, Engine-Filter/`subfaction_passive`) vorgesehen — laut `S146_planning.md`-DoD „NICHT löschen, erst wenn K2 abgeschlossen ist". K2 ist noch nicht eingeplant. |
| `S141_ui_befunde_group_a.md` | Behalten | Lifecycle-Vermerk „bleibt bis FixC+FixD" — FixD Brief 1 läuft frühestens als Aufgabe 9 dieser Session, Brief 2/3 stehen noch aus. |
| `Stakeholder_Beobachtungen.md` | Behalten (STANDING) | Nie löschen, laut eigener Datei-Konvention. |
| `README.md` | Behalten (STANDING) | Dauerhafte Ordner-Dokumentation. |
| 10 Screenshots (`Bildschirmfoto vom …png`) | Behalten, alle | Jeder zugehörige Befund ist noch offen: 2026-07-09 20-53-48/20-58-07 → B4-Rest (offen); 21-29-43 → B7 (offen); 21-36-36 → B8 (offen); 2026-07-11 09-52-56 → B13 (offen); 11-54-31 → Rand-Design-Konzept (offen, Ratchet-Rest); 12-03-17 → GO-UI-Design-System Paket 6 (offen). Die drei 2026-07-12-Screenshots (17-48-56, 21-11-35, 21-13-42) sind in keinem Dokument namentlich verlinkt — mutmaßlich Bildbeleg der S146-Live-Verifikation (Roster-Builder-`before_battle`, Silent-King-Default, MWBD-Bug, GO-Badge-Lücke, Review-B1 — alle noch offen). Da die zugehörigen Findings nicht DONE sind, greift die Lifecycle-Regel „erst löschen wenn Finding DONE" ungeachtet der fehlenden Namensverknüpfung — im selben Zug empfehlen wir, künftige Screenshot-Referenzen im Beobachtungs-Text immer mit Dateinamen zu verankern (kleiner Prozess-Nit, keine Aufgabe für S147).

---

## Offene Entscheidungsfragen an den Stakeholder

1. **grantsKeyword-Konvention — echtes Feature-Gap, nicht nur Anzeige-Bug:** Der Ist-Bestand
   zeigt, dass es aktuell **keine** Ability gibt, die GAUSS-Waffen der tragenden Einheit als
   sichtbares Keyword zuweist (weder bei Necron Warriors noch sonstwo) — GAUSS/TESLA laufen
   rein über Waffen-Text-Erkennung. Soll der Audit-Fixing-Plan **eine neue generische
   Konvention** vorschlagen (Waffen-Sondertyp → Einheiten-Keyword, datengetrieben), oder war
   die Beobachtung eher als „Wahapedia zeigt GAUSS als Einheiten-Keyword, App sollte das
   spiegeln" gemeint (rein kosmetisch, kein Wargear-Mechanismus)? Das entscheidet, ob GAUSS/
   TESLA-Anzeige über den bestehenden `grant_keyword`-Pfad läuft oder einen neuen Anzeige-Weg
   braucht (z. B. abgeleitet direkt aus den zugewiesenen Waffen, ohne YAML-Ability).
2. **Nebenbefund Hand of the Phaeron (`stat` statt `keyword`):** Als eigener XS-Bugfix sofort
   einplanen, oder im Audit-B1-Fixing-Plan mitlaufen lassen (Necron-Stratagem, würde ohnehin
   von Aufgabe 3 gefunden)? Empfehlung: im Audit mitlaufen lassen — vermeidet Punktfix vor
   dem geforderten „ganzheitlich, dann sauber" laut Stakeholder-Auftrag.
3. **S145_planning.md-Löschung:** Reicht die vorgeschlagene Migration (Option C nach
   `backlog.md` §4, Herleitung als Fußnote) als Aufgabe-1-Umfang, oder soll die Datei vorerst
   unangetastet bleiben (nur next_session.md-Drift korrigieren) und die vollständige Migration
   auf einen späteren, eigenen kleinen Task verschoben werden?
4. **Fixing-Pläne aus dem Audit:** Sollen sie noch in S147 (bei ausreichend Headroom nach den
   3 Audit-Briefs) in Executor-Briefs heruntergebrochen werden, oder ist das bewusst S148-Scope
   (diese Session liefert nur den Befund-Katalog)?
5. **Reihenfolge Welle 2 vs. Audit:** Passt die vorgeschlagene Parallelität (Audit läuft im
   Hintergrund, während B1 + Welle 2 + MWBD-Fix im Vordergrund laufen), oder soll das Audit
   allein im Vordergrund stehen und Welle 2/MWBD auf S148 verschoben werden, um den
   Kontext-Korridor für Review/Retro sicherer einzuhalten (angesichts der Größe von 3× M-Audits
   zusätzlich zu 3 Executor-Briefs)?

---

## Stakeholder-Entscheidungen (2026-07-14, Chat + AskUserQuestion)

1. **grantsKeyword:** Neue Konvention gewünscht — Waffen tragen ein `grantsKeyword`-Feld
   (camelCase), Einheit erhält das Keyword sichtbar (unitCard). Schreibweise camelCase gilt
   künftig statt snake_case; Umsetzung als **Inventar + Migrationsplan** (Audits
   inventarisieren alle snake_case-Felder, Voll-Migration als eigener Task im Fixing-Plan,
   S148). Keywords immer dann vergeben, wenn die Regeln es suggerieren — Bedingungen
   keyword-basiert prüfen.
2. **Hand of the Phaeron:** im Audit-Fixing-Plan mitlaufen lassen (kein Punktfix).
3. **S145_planning.md:** migrieren (Option C → backlog §4, Herleitung als Fußnote), dann löschen.
4. **Fixing-Pläne:** Koordinator-Entscheid — S148-Scope; S147 liefert Befund-Kataloge.
5. **Parallelität:** alles Mögliche parallel, Abhängiges sequentiell; Aufgaben klein
   schneiden, Rest → S148. Koordinator: K1 läuft NACH den Ability-Audits (gleiche YAML),
   FixD NACH B1-Umsetzung (gleiche Datei `_common.py`).
6. **B1-Design:** Ziel-Kachel als **einziger Ort** für on_target-GOs — Hit-/Save-Anker
   dafür abschaffen (+ Negativ-Tests B2).
7. **Retro-Maßnahmen S146:** freigegeben, inkl. M4 (Selbst-Stopp-Budget gilt auch nach
   SendMessage-Resume → `agent_scopes.md`).

## Selbstprüf-Checkliste

- [x] STATUS-Marker erste Zeile, korrektes Format (`STATUS: NEEDS-DECISION`, nackte erste Zeile)
- [x] Checkbox-Sync gegen `git log --oneline -20` durchgeführt (s. Befunde — `git show 2a169b6` als Beleg)
- [x] grantsKeyword-Ist-Bestand per grep belegt (Fundstellen zitiert: `wargear.yaml:16`,
  `stratagems.yaml:47`, `loader.py:822-825`, Test `test_loader.py:602-613`)
- [x] Alle Aufgaben ≤ Effort M (L-Kandidat „ein Audit über alles" wurde in 3× M gesplittet)
- [x] Kein Aufgabenvorschlag ohne Bestandsaufnahme-Hinweis (grantsKeyword, Fire Overwatch,
  Handoff-Referenzen, GO-Badge-Lücke-Überlappung — alle mit Grep-/Git-Beleg unterlegt)
- [x] Handoff-Liste vollständig (alle 6 Markdown-Dateien + alle 10 Screenshots im Ordner adressiert)
