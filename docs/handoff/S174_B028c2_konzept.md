STATUS: AWAITING-VERIFICATION
<!-- Class B (App zeigt Hinweis, rechnet nicht) + Grundannahmen A1–A4 vom Stakeholder
     bestätigt S174. Dies ist die Umsetzungs-Spec für S175 — nach Umsetzung + UI-Verifikation
     löschen. -->

# S174 — Mini-Konzept B-028c2 `reroll_rp` (Their Number is Legion)

## 1. Grundannahmen (S131 — Weltbild, VOR den Details bestätigen)

Diese Annahmen prägen die ganze Class-Entscheidung. Stakeholder bitte zuerst bestätigen
oder korrigieren:

- **A1 — Gewürfelt wird am Tisch, die App aggregiert nur.** Arbiter würfelt Reanimation
  Protocols nicht selbst und kennt keine einzelnen Würfelflächen. Der RP-Block fragt heute
  bewusst nur „wie viele Modelle sind zurück?" ab (`number_input`), nicht die Wurf-Ergebnisse.
- **A2 — Das RP-Datenmodell ist ein Skalar.** `revive_dice_count()` liefert eine
  aggregierte Würfelanzahl (`models_lost × wounds_per_model`), keine Liste von Einzelwürfen.
  Es gibt keinen Ort im State, an dem eine „1" stünde, die man rerollen könnte.
- **A3 — „Reroll von Einsen" ist eine physische Tisch-Handlung** vor der Erfolgs-Auswertung;
  ihr Ergebnis fließt beim Spieler bereits in „Modelle zurück" ein, wenn er den Block ausfüllt.
- **A4 — Die App-Rolle bei solchen Würfen ist Erinnern, nicht Rechnen** (design_system §3:
  `info` = „Tisch-Hinweis Klasse B/C").

Wenn A1/A2 bestätigt sind, folgt Abschnitt 4 (Class B) zwingend. Werden sie verworfen
(App soll RP künftig selbst würfeln), ist das ein viel größeres Feature als B-028c2 und
gehört neu geschnitten — dann ist dieses Konzept obsolet.

## 2. Regelwortlaut (wörtliches Zitat + Quelle)

**Their Number is Legion** (Wahapedia, Necron-Einheiten):
> „Their Number is Legion : Re-roll Reanimation Protocol rolls of 1 made for this unit."
> — `docs/work/wahapedia_necrons/units_all.txt:277`

**Reanimation-Protocols-Mechanik** (die den Wurf definiert):
> „Each time a unit's reanimation protocols are enacted, make Reanimation Protocol rolls for
> that unit by rolling a number of D6 equal to the combined Wounds characteristics of all the
> reassembling models. Each Reanimation Protocol roll of 5+ is put into a pool. A Reanimation
> Protocol roll can never be modified by more than -1 or +1."
> — `docs/work/wahapedia_necrons/faction_overview.txt:504` (identisch :9866)

**Reroll-Timing** (Grundregel):
> „You can never re-roll a dice more than once, and re-rolls happen before modifiers (if any)
> are applied. Rules that refer to the value of an 'unmodified' dice roll are referring to the
> dice result after any re-rolls, but before any modifiers are applied."
> — `docs/work/wahapedia_core_rules/core_rules.txt:495`

Der Reroll wirkt also auf **einzelne, physisch geworfene D6 mit Wert 1**, vor der 5+-Poolung.

## 3. Ist-Zustand RP-Modell (Code-Belege)

- **Aggregat, kein Einzelwurf:** `revive_dice_count(amount, models_lost, wounds_per_model)`
  gibt bei `"D6_per_wound"` schlicht `models_lost * wounds_per_model` zurück — einen Skalar.
  `src/gameMechanic/abilityEngine.py:442-451`.
- **UI würfelt nicht:** `_render_rp_block` berechnet `rp_dice` (Anzeige „N Würfel") und bietet
  dann ein `number_input("Modelle zurück", …)`. Kein Würfelwurf, keine Einzelwerte, keine
  Poolung. `src/uiLayout/_common.py:2587` (rp_dice) und `:2597-2612` (number_input +
  „RP anwenden"/„Überspringen").
- **Vorhandener RP-Hinweis-Pfad (Vorbild):** `_rp_directive_hints` emittiert bei aktivem
  Reroll-Direktiv eine Caption `„⟳ …: re-roll one RP die."`. Gated ausschließlich über
  `get_active_rp_modifiers(def_faction).get("rp_reroll")` — das ist der **Runden-/Command-
  Protokoll-Pfad** (Undying Legions P), NICHT die Unit-Ability.
  `src/uiLayout/_common.py:2547-2549`; Modifier-Quelle `abilityEngine.py:399-410`.
- **Their Number is Legion ist heute totes Datenfeld.** In der YAML vollständig deklariert
  (`unit_abilities.yaml:419-438`: `effect.type: reroll_rp`, `trigger.event: reanimation_roll`,
  `conditions: has_rules: [theirNumberIsLegion]`; Rule-Key an `units.yaml:173`).
  Aber: `grep` über `src/` findet **keinen Konsumenten** für `reroll_rp` oder
  `reanimation_roll` — beide Strings existieren nur in der YAML. Warrior-Einheiten mit
  `theirNumberIsLegion` bekommen im RP-Block heute **keinerlei** Anzeige. Das ist die Lücke.

## 4. Class A vs. Class B — begründete Empfehlung

**Empfehlung: Class B (App zeigt Hinweis/Marker), Class A wird verworfen.**

Begründung aus Datenmodell + Regel:
- Der Reroll wirkt regeltechnisch auf **einzelne D6 mit unmodifiziertem Wert 1** (Abschnitt 2).
- Das App-Modell hat diese Einzelwürfe nicht (A2/Ist-Zustand): es kennt nur die Würfelanzahl
  und den vom Spieler eingetragenen End-Erfolg („Modelle zurück"). Es gibt keine „1", die die
  App umdrehen könnte.
- Um Class A zu bauen, müsste Arbiter die RP-Würfe **selbst würfeln und poolen** — ein
  fundamentaler Umbau des RP-Blocks von „Spieler trägt Ergebnis ein" zu „App würfelt". Das
  widerspricht der App-Grundhaltung (A1) und dem gesamten übrigen Wurf-Modell und ist weit
  größer als der B-028c2-Zuschnitt (~15–20k S/M).
- Class B ist regelkonform und ausreichend: Die App erinnert den Spieler, **vor** dem Eintragen
  von „Modelle zurück" die Einsen neu zu würfeln. Das ist exakt die Rolle, die der bestehende
  `_rp_directive_hints`-Pfad für die Direktiv-Variante schon erfüllt.

Class B ist zudem konsistent mit der Warnung im Backlog (B-028c2 als „Class-B-Kandidat —
Datenmodell-Frage, nicht Implementierungslücke").

## 5. Bauform-Vorschlag

**Keine neue Komponente nötig — bestehendes RP-Hinweis-Muster wiederverwenden.**

- **Komponente:** neutrale Caption im bestehenden RP-Block, identisch zur vorhandenen
  Direktiv-Caption (`⟳ …: re-roll RP rolls of 1.`) — `_common.py:2593-2594` iteriert bereits
  über `_rp_directive_hints(...)`. Vorschlag: einen zweiten Hinweis-Produzenten für
  Unit-Ability-basiertes `reroll_rp` ergänzen (analog `get_after_attack_revive_ability`:
  über `load_faction_abilities` + `check_conditions` prüfen, ob die Einheit eine
  `effect.type: reroll_rp`-Ability mit erfüllten `has_rules`-Conditions trägt).
- **Design-System-Anker:** `design_system.md §3` (Hinweis-Konvention, `info` = „Tisch-Hinweis
  Klasse B/C") + `§3.1` (Wortlaut-Budget: ein kurzer Satz, keine Regelbegründung im UI-Text).
- **Bewusst NICHT** die Pflicht-Trigger-Kachel (§1.5) mit Binär-Wurf-Baustein (§1.6): RP ist
  ein Pool-Mechanismus über viele Würfel, kein einzelner Schwellen-Wurf mit Erfolg/Fehlschlag.
  Die Kachel-Bauform (aus B-028c1) passt hier nicht — der Reroll modifiziert nur die
  Vorbedingung des ohnehin vom Spieler eingetragenen Ergebnisses.

→ **Kein NEEDS-DECISION auf Bauform-Ebene** (bestehendes Muster passt sauber). Der
NEEDS-DECISION-Status dieses Konzepts betrifft **nur die Grundannahmen (Abschnitt 1) und die
Class-Frage (Abschnitt 4)** — beides muss der Stakeholder bestätigen, bevor B-028c2
freigabe-reif ist.

## 6. Benötigte Regeln-Scopes (DoR-Kriterium a — konkret befüllt)

Für die freigabe-reife Backlog-Zeile B-028c2 einzutragen:
- `docs/work/wahapedia_necrons/units_all.txt:277` — Their Number is Legion (Wortlaut).
- `docs/work/wahapedia_necrons/faction_overview.txt:504` — Reanimation-Protocols-Wurf-Mechanik
  (begründet, warum Einzelwürfe im Modell fehlen).
- `docs/work/wahapedia_core_rules/core_rules.txt:495` — Reroll-Timing / „unmodified".
- `docs/spec/design_system.md §3 + §3.1` — Hinweis-Konvention + Wortlaut-Budget (Bauform-Anker).

## 7. Aufwand-Schätzung (Class B)

- Neuer Ability-Sucher in `abilityEngine.py` (Unit trägt `reroll_rp`-Ability, Conditions erfüllt)
  — klein, spiegelt `get_after_attack_revive_ability`.
- Zweiter Hinweis in `_render_rp_block` / Erweiterung von `_rp_directive_hints` — eine Call-Site.
- Ein kurzer Caption-Wortlaut (§3.1-konform).
- Tests: Unit mit `theirNumberIsLegion` → Caption erscheint; ohne Rule → keine Caption;
  Direktiv-Pfad unberührt (Regressionsschutz Koexistenz).
- **Schätzung: XS–S (~10–15k), deutlich ≤ M.** Kein Funktionsbruch der RP-UI-Aggregation,
  da nur eine zusätzliche Caption entsteht (Backlog-Bedingung „ohne Funktionsbruch" erfüllt).

**UI-Verifikation (nicht test-gedeckt):** Warrior-Einheit mit Verlusten → RP-Block zeigt die
Reroll-Caption; Einheit ohne die Ability zeigt sie nicht.

Befund: Ich habe es Necron Warrior-Einheit getestet. Schaden nach Fernkampf. Die RP-Rolloff Anzeige erscheint. Aber es gibt keinen Hinweis-Marker, dass Würfe von 1 wiederholt werden können. Sollte meines Wissens nur bei Necron Warriors erscheinen.
