STATUS: ANSWERED

# Konzept: "on_target"-Anker vor dem Hit-/Wound-/Save-Auflösungs-Stack

Auftrag: Recherche-Subagent W1-G (Effort S), Folge-Task zum Stakeholder-Befund
Whirling Onslaught (UI-verifiziert S142). Read-only — keine Code-Änderung.
FixD-Plan (`docs/audit/plans/S142_fixD_resolution_tabs.md`) ist bereits freigegeben
und bleibt unberührt; dieses Konzept ist additiv/Folge-Task.

## Grundannahmen (bestätigungspflichtig)

- Die App würfelt **nicht** — jeder Wurf ist ein Tischwurf, den der Spieler einträgt
  (§6.3 design_system.md). Ein `on_target`-Anker ändert daran nichts: er entscheidet
  nur, WANN eine reaktive GO-Karte klickbar ist, nicht wer würfelt.
- Seitenleisten/Spalten-Layout ist unveränderlich auf `first_player` links /
  `second_player` rechts — nie an `active`/Angreifer gebunden (Domänen-Constraint).
  Ein neuer Anker muss in der Verteidiger-Spalte rendern, analog FixD Brief 2.
- Whirling Onslaught ist laut design_system.md §6.2 (Zeile 279-284) bereits
  **mechanisch erreichbar** (Wound-Anker, Paket 4a) — der Stakeholder-Befund ist
  kein "unreachable GO"-Bug, sondern ein **Timing-/UX-Wunsch**: die Karte soll schon
  bei Ziel-Wahl erscheinen, nicht erst am Wound-Anker im Auflösungs-Screen.

## Regel-Beleg (wörtlich, `data/wh40k_9e/necrons/stratagems.yaml:400`)

> "Use this Stratagem in any phase, when a SKORPEKH DESTROYERS or SKORPEKH LORD unit
> from your army is selected as the target of an attack. Until the end of the phase,
> each time an attack is made against that unit, subtract 1 from that attack's wound
> roll."

Trigger-Wortlaut ist wörtlich "selected as the target of an attack" — der Effekt ist
aber ein **lingernder Modifier bis Phasenende**, kein Einmal-Effekt. Das heißt: der
mechanische Effekt (−1 Wound-Roll) muss weiterhin am Wound-Anker ausgewertet werden
(bestehende Plumbing unverändert) — nur die **Klick-Gelegenheit** (Use-Button) soll
zusätzlich/stattdessen früher erscheinen.

`phase: any`, `stage: active`, `player: inactive` (YAML Z. 382-384) — Fenster ist
phasenübergreifend (Shooting UND Fight), passend zu beiden Ist-Ablauf-Stellen unten.

## Ist-Ablauf: wo ein Ziel deklariert wird

Die Ziel-Wahl passiert NICHT über einen dedizierten "Deklarations-Screen", sondern
über Klicks in der gegnerischen Armeeliste, die eine Zuordnungs-Liste befüllen:

- **`toggle_group_target(def_faction, def_uid)`** — `src/uiLayout/_common.py:2257-2283`.
  Fügt/entfernt `(def_faction, def_uid)` in `st.session_state.group_targets[gid]`.
  Das ist der Moment, in dem eine Einheit "als Ziel einer Attacke gewählt" wird
  (Docstring Z. 2258: "Assign/unassign a target to the selected model group").
  **Wichtig:** es ist ein **Toggle** — ein Ziel kann mehrfach an/ab geklickt werden,
  bevor der Angreifer die Gruppe final bestätigt. Der Trigger-Moment ist also nicht
  eindeutig "einmalig", sondern eher "solange in `group_targets` vorhanden".
- Aufrufer/Klick-Orte:
  - `src/uiLayout/unitCard.py:351` — Klick auf eine gegnerische Einheit in der
    Armeeliste (Attacker-Sicht, aber der Klick betrifft die Zielauswahl).
  - `src/uiLayout/_common.py:2448` — innerhalb `render_group_assignment` selbst
    (Expand-Button "Designate a target", Z. 2456).
- **`render_group_assignment(atk_faction, atk_uid, atk_unit, atk_state, use_melee,
  in_melee)`** — `src/uiLayout/_common.py:2485-…`. Docstring (Z. 2493-2496):
  "Defender-side panel: assign attacks/models of the selected group to its targets.
  Rendered in the opposite player area." — **das ist bereits die Verteidiger-Spalte**,
  nicht vollbreit wie das spätere `render_attack_resolution`-Panel (FixD-Scope).
  Diese Funktion läuft in Shooting- UND Fight-Phase (gemeinsamer Baustein).
- Die Hit-/Wound-/Save-Anker liegen erst deutlich später, in
  `_render_resolution_tab` (`_common.py:1789-~2200`, Wound-Anker Z. 2075-2085) —
  das ist der heutige, vom Stakeholder als "zu spät" bemängelte Ort.

## Qualifizierende reaktive GOs (Trigger "when chosen as target")

Nur gegen `docs/work/wahapedia_necrons/` bzw. bereits eingepflegte YAML geprüft
(Whirling Onslaught liegt nur in `data/wh40k_9e/necrons/stratagems.yaml`, nicht als
eigene `.txt` im wahapedia-Rohtext-Ordner — Necron-Stratagems sind dort teils nur als
verarbeitetes YAML vorhanden, kein Roh-Textfund für den Wortlaut nötig, da bereits in
der YAML mit `rule_text` hinterlegt):

- **Whirling Onslaught** (Necrons, DESTROYER CULT) — Wound-Roll-Debuff, siehe oben.
- Aus design_system.md Paket-4-Debt-Tabelle (Zeile 265-276) zwei WEITERE
  `(phase, on_target)`-GOs, die bewusst NICHT in den Modifier-Stack passen und
  separat bewertet sind (Paket 4c/6, kein Bau):
  - **Reanimation Prioritisation** (Necrons) — keine Modifikation, sondern eine
    Zusatz-Aktion (Reanimate direkt bei Ziel-Auswahl) — würde von einem
    `on_target`-Deklarations-Anker eher PROFITIEREN als Whirling Onslaught, weil der
    Effekt selbst zeitlich an den Deklarationsmoment gebunden ist, nicht an einen
    späteren Wurf.
  - **Tough as Squig-Hide** (Orks) — Auto-Fail-Schwelle am Wound-Wurf, kein additiver
    Modifier; bleibt unabhängig vom Anker-Zeitpunkt ein Save-Anker-Sonderfall.

  Diese zwei sind laut Paket-6-Notiz (design_system.md Z. 294-299) bewusst
  zurückgestellt, weil sie eigene Auswertungslogik brauchen (kein Modifier-Eintrag).
  Ein neuer Deklarations-Anker würde **Reanimation Prioritisation** direkt lösen
  (Zusatz-Aktion, kein Wurf-Bezug) — das wäre ein Zusatznutzen dieses Konzepts über
  den Whirling-Onslaught-Fall hinaus, aber NICHT Teil des heutigen Stakeholder-Scopes.

## Einordnung ins Anker-Schema (design_system.md)

Kein neuer Anker-**Typ** nötig — `on_target` als Event existiert bereits (§6.2,
`reactive_stratagems_for(phase, event)` kennt es). Neu ist die **Render-Stelle**:
ein zusätzlicher `render_reactive_stratagem_box(def_faction, phase, event="on_target",
…)`-Aufruf **in `render_group_assignment`** (Deklarationsphase, bereits Verteidiger-
Spalte) statt ausschließlich in `_render_resolution_tab` (Auflösungsphase, aktuell
Wound-Anker).

**Kollisionsfreiheit mit FixD:** FixD (Brief 1/2) refactort ausschließlich
`render_attack_resolution`/`_render_resolution_tab` (Auflösungs-Panel, nach "All
done"). `render_group_assignment` ist eine andere, bereits bestehende Funktion in
einer früheren Ablaufphase (Deklaration) und bereits spaltenweise (nicht vollbreit)
— beide Pläne berühren unterschiedliche Funktionen, kein Merge-Konflikt zu erwarten.
Die Stakeholder-Forderung "schmaler" ist an dieser Stelle **strukturell bereits
erfüllt** (Deklarationspanel ist schon je-Spieler-Spalte), nur die Forderung "einen
Screen früher" braucht den neuen Aufruf.

**Offene Design-Frage (nicht Teil dieser Recherche, s. Entscheidungsfragen unten):**
Whirling Onslaught würde dann an ZWEI Stellen im selben Fenster sichtbar sein können
(Deklaration + Wound-Anker), falls beide Aufrufe aktiv bleiben. Bestehende
Used-Bookkeeping (`used_stratagem_ids`/`used_battle_ids`, `stratagem_visibility`)
sperrt eine bereits verbrauchte GO an jeder weiteren Anker-Stelle korrekt (kein
Doppel-Verbrauch) — die offene Frage ist rein UX: zwei Erscheinungsorte für dieselbe
Karte (redundant, aber nicht falsch) vs. den Wound-Anker-Aufruf für Whirling Onslaught
gezielt entfernen, sobald der Deklarations-Anker existiert.

## Konzept-Optionen

**Option A — Zusätzlicher `on_target`-Aufruf in `render_group_assignment`, Wound-
Anker bleibt unverändert (additiv, kein Entfernen).**
- Aufwand: **S–M**. Ein neuer `render_reactive_stratagem_box(...)`-Call an der
  Stelle, wo `def_uid` erstmals zu `group_targets[gid]` hinzugefügt wird bzw. direkt
  im Render von `render_group_assignment` pro bereits zugewiesenem Ziel (Schleife
  über `tgts`, Zeile ~2506). `decline_key`/`anchor_id` je `(gid, def_uid)`, damit
  Mehrfach-Ziele nicht kollidieren.
- Risiko: doppelte Sichtbarkeit derselben Karte an zwei Ankern (s. o., UX-Frage);
  Toggle-Verhalten von `toggle_group_target` (Ziel kann wieder entfernt werden) —
  Karte müsste bei Entfernen des Ziels wieder verschwinden, sonst Geister-Anker für
  ein nicht mehr gewähltes Ziel. Erfordert Prüfung, ob `def_uid` noch in
  `group_targets[gid]` steht, JEDES Rerun (nicht nur beim ersten Hinzufügen).
- Testeinfluss: neue Regressionstests für Anzeige-/Verschwinden-Logik bei Toggle;
  bestehende Wound-Anker-Tests bleiben unberührt (kein Verhalten entfernt).

**Option B — `on_target`-Anker ersetzt den Wound-Anker für betroffene GOs (Whirling
Onslaught raus aus dem `effect_stat="wound"`-Wound-Anker-Filter, rein in den neuen
Deklarations-Anker).**
- Aufwand: **M**. Zusätzlich zu Option A: den Wound-Anker-Aufruf in
  `_render_resolution_tab` um einen Ausschlussfilter erweitern (oder Whirling
  Onslaught bekommt ein neues Unterscheidungsmerkmal, z. B. eigenes `anchor: on_target`
  Feld in der GO-Klassifikation `docs/reference/go_klassifikation.md`), damit sie NUR
  am Deklarations-Anker erscheint.
- Risiko: größerer Eingriff in bestehende Filterlogik (`effect_type`/`effect_stat`),
  potenziell Rückwirkung auf andere Wound-Anker-GOs (Quantum Deflection liegt am
  Save-Anker, sollte nicht betroffen sein, aber Filteränderung verdient eigenen Test).
  Sauberer bzgl. UX (kein Doppel-Erscheinen), aber mehr Änderungsfläche.
- Testeinfluss: wie A plus Regressionstest, dass Wound-Anker Whirling Onslaught NICHT
  mehr anzeigt, aber weiterhin den −1-Modifier korrekt anwendet, wenn am
  Deklarations-Anker "used" markiert wurde (Kopplung Anzeige-Anker ↔ Effekt-Ort
  sauber trennen — Effekt bleibt im Wound-Resolve, nur Klick-Gelegenheit wandert).

## Empfehlung

Option A zuerst (additiv, kleinerer Diff, kein Risiko für bestehende Wound-Anker-
Tests) — mit der Toggle-Verschwinden-Regel als Pflichtbestandteil des Effort-S/M-
Briefs. Option B als möglicher Folge-Schritt, falls der Stakeholder das Doppel-
Erscheinen als störend empfindet (nach manueller UI-Prüfung von A).

## Entscheidungsfragen an den Stakeholder

1. Ist ein Doppel-Erscheinen derselben GO-Karte (Deklarations-Anker + Wound-Anker,
   Option A) akzeptabel, oder soll der Wound-Anker für diese GOs von Anfang an
   entfernt werden (Option B, mehr Aufwand)?
2. Soll die Karte verschwinden, sobald der Angreifer das Ziel wieder entfernt
   (Toggle-Klick rückgängig), auch wenn die GO in der Zwischenzeit schon genutzt
   wurde (CP bereits ausgegeben)? Das ist ein Regel-Grenzfall (Tischrealität: einmal
   ausgegebenes CP wird nicht zurückerstattet, nur weil der Spieler die
   Zielzuordnung am Bildschirm ändert) — braucht eine explizite Reihenfolge-Regel.
3. Soll dieses Konzept gleich auf Reanimation Prioritisation (Paket-6-Debt) erweitert
   werden, da sie strukturell besser zum Deklarations-Anker passt als zum
   Wound-/Save-Stack, oder bleibt der Scope strikt auf Whirling Onslaught begrenzt?

## Stakeholder-Entscheid (S143, 2026-07-12)

Option A (additiver on_target-Anker bei Ziel-Zuweisung, mit Verschwinde-Regel bei
Ziel-Toggle) freigegeben — Umsetzung S144, kollisionsfrei neben dem FixD-Plan.
