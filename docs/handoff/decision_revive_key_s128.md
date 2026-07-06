STATUS: ANSWERED — Option B (YAML-getrieben) freigegeben (2026-07-06).
<!-- Temporär. Löschen nach Stakeholder-Entscheid + Übernahme in Paket 1 (planning_s128_teil2.md). -->

# Entscheidungsvorlage — `reanimationProtocols` in src/ (Paket 1c, S128 Teil 2)

## 1. Was der Code heute tut
Zwei Stellen in `src/uiLayout/_common.py` (beide DEBT-Tokens `reanimation`+`protocols`):
- **Z. 584 (Gate):** `_render_rp_block` zeigt den Würfelblock nach Schaden nur, wenn die
  Einheit den Rules-Key `reanimationProtocols` trägt (aus `necrons/units.yaml`, 5 Einheiten).
- **Z. 597-598 (Anzeige):** Überschrift **„REANIMATION PROTOCOLS"** und Schwelle **„Erfolg: 5+"
  sind ebenfalls hart in src/ codiert** — der Befund ist also größer als nur der Key.
Die Blocklogik selbst (Verluste × Wounds = Würfelzahl, Modelle zurück) ist fraktionsblind.

## 2. Option A — neutraler Mechanik-Key (`revive_roll`, reine Umbenennung)
Prinzipiell Generic-src-konform: src implementiert „Einheit mit Revive-Wurf nach Schaden",
nur Necron-YAML deklariert den Key. **Aber ehrlich: die Umbenennung allein ist unvollständig** —
Label „REANIMATION PROTOCOLS" und die 5+-Schwelle blieben hardcodiert in src/ (dieselben
Ledger-Tokens!). Ein vollständiges Option A müsste Label+Schwelle ohnehin nach YAML ziehen —
und steht dann schon halb bei Option B. Der Stakeholder-Einwand „zu billig" trifft zu.

## 3. Option B — strukturell aus der Necron-YAML getrieben (Ability-Engine)
Die Mechanik ist **bereits als strukturierte Fähigkeit modelliert**:
`necrons/faction_abilities.yaml` Z. 41-49 — `event: after_enemy_attack`, Bedingung
`has_rules: [reanimationProtocols]` (YAML-intern!), `effect: {type: reanimate, amount: D6_per_wound}`.
Der generische Effekt-Typ `reanimate` wird in src/ schon konsumiert (`armyCard.py:107`) und ist
Guard-sauber (nicht im Ledger). Konkret:
- `_render_rp_block` fragt die Ability-Engine: „hat die Einheit eine aktive Fähigkeit mit
  `effect.type == reanimate`?" — statt Key-Abfrage im Render-Code.
- Label (= `name_en` der Fähigkeit), Schwelle (neues Feld `success_on: 5`) und Würfelformel
  (`amount`) kommen aus dem YAML-Eintrag. `reanimationProtocols` verschwindet **komplett**
  aus src/ und bleibt reine Necron-interne Verdrahtung (units.yaml ↔ conditions).
- Passt zur Fähigkeits-Architektur (`docs/spec/faction_abilities.md`): strukturiertes
  `trigger`/`conditions`/`effect`-Muster, wie Arkana/Kategorie-Schema — kein Sonderweg.

**Aufwand:** M statt S (~+10k auf Paket 1, neu ~35-45k gesamt): Engine-Helper + Gate-Umbau +
Schema-Feld + Testmigration. **Nutzen:** alle Ledger-Tokens weg (Key UND Label UND Schwelle),
zukünftige Revive-Fraktionen (z. B. Space-Marine-Apothecary „return 1 slain model") nur per
YAML. **Risiken:** RP-Block ist kampferprobter Render-Code → Regressionstests auf den
Engine-Helper + manuelle UI-Verifikation (RP-Block nach Schaden, Würfelzahl, Direktiv-Hints).

## 4. Regel-Recherche — ist ein generischer Mechanik-Begriff gerechtfertigt?
In den drei lokal dokumentierten Fraktionen hat **nur Necrons** eine Modell-Revive-Mechanik
(Orks/Custodes: keine Treffer für revive/resurrect/return-slain). ABER: die 9E-Grundregeln
behandeln „models that were destroyed and returned to a unit" als **allgemeines Konzept**
(`rules_appendix.txt:1248-1249` — Morale-/Wound-Sonderregeln dafür), weil weitere 9E-Fraktionen
solche Mechaniken haben (außerhalb des lokalen Doku-Scopes). Die App führt zudem bereits
generisches Revive-Vokabular: `revive_wargear_*` (Plan 020, Res-Orb) und Effekt-Typ `reanimate`.

## Empfehlung: **Option B**
Sie beantwortet den Einwand exakt: die Fähigkeit ist dann **nur in der Necron-YAML** deklariert
und konfiguriert; src/ kennt weder Key noch Label noch Schwelle — nur den generischen
Effekt-Typ, den es heute schon gibt. Option A wäre die halbe Lösung (Label/Schwelle blieben
hardcodiert). Mehrkosten ~10k sind der Preis für die Wurzel- statt Symptom-Korrektur.
Falls Option B: Paket 1c wird M — bei Bedarf als eigener (weiterhin dateidisjunkter)
Folge-Executor nach 1a+1b, damit der Parallellauf nicht auf 1c wartet.
