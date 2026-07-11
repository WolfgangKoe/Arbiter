STATUS: ANSWERED
<!-- Lifecycle: NEEDS-DECISION → ANSWERED (Stakeholder-Entscheid eingetragen) → DONE (Umsetzung committet, Datei löschen) -->
<!-- S139-Entscheid: Stakeholder gibt Umsetzung für S140 frei. Befund bestätigt =
     alter S96/S97-Backlog-Punkt (subfaction_affinity existiert, nur Round-Zweig
     wertet nicht aus). -->

# Konzept: Dynastie↔Protokoll-Kopplung „beide Direktiven" (S139, E6)

## Grundannahmen (bestätigungspflichtig)

- Die App würfelt NICHT — alle Würfe passieren am Tisch.
- Die Dynastie-Bonus-Regel ist ein reiner **Freischalt-Mechanismus** (welche Direktiven
  aktiv sind), keine neue Wurf- oder Schadensmechanik — sie verändert nur, *welche*
  bereits bestehenden Effekt-Einträge in `_active_directive_effects` einfließen.
- Die 1:1-Zuordnung Dynastie↔Protokoll ist laut Regeltext fix (6 Dynastien, 6 Protokolle,
  siehe Tabelle unten) — keine Dynastie hat mehr als einen Affinitäts-Fall.
- Betroffen sind nur die 6 **offiziellen** Dynastien (Mephrit, Nephrekh, Nihilakh, Novokh,
  Sautekh, Szarekhan). „Ancient Dynasties" (selbst zusammengestellte Codes) haben laut
  Regeltext **keine** Protokoll-Affinität — kein Sonderfall dafür nötig.

## Befund F-B: EIN Thema, nicht zwei

Der Stakeholder-Hinweis war richtig: **dasselbe Thema**, nicht zwei getrennte Lücken. Beleg:

- Das Datenfeld existiert bereits — `subfaction_affinity` steht seit S52 an jeder
  `round_choice`-Ability in `data/wh40k_9e/necrons/faction_abilities.yaml` (z. B.
  `protocol_eternal_guardian: subfaction_affinity: nihilakh`) und ist in
  `docs/spec/faction_abilities.md:36` dokumentiert. Der im Auftrag genannte Arbeitstitel
  `linked_protocol` beschreibt exakt dieses bereits vorhandene Feld — nur aus der
  umgekehrten Blickrichtung (Dynastie→Protokoll statt Protokoll→Dynastie). Es fehlt
  **kein neues YAML-Feld**.
- Der Regeltext ist für alle 6 Dynastien identisch formuliert („When the Protocol of
  the … becomes active for your army, if every unit … has this code, you can select
  both of that command protocol's directives instead of just one.",
  `faction_overview.txt` Z. 862–871/889–907/917–936/953–971/992–1010/1023–1041) —
  unabhängig davon, ob das Protokoll **rundenzugewiesen** oder das **6./permanent
  aktive** ist. Die Regel kennt diesen Unterschied gar nicht.
- Im Code ist der Fall bereits für EINEN der beiden Zweige gelöst:
  `_extra_directive_effects` (`src/gameMechanic/ability_engine.py:95-125`) prüft
  `subfaction == extra.subfaction_affinity` und gibt bei Treffer **beide** Effekte
  zurück (Zeile 116-120) — analog `armyCard._render_extra_round_choice`
  (`src/uiLayout/armyCard.py:208-229`, Badge „… BONUS (BOTH)").
  Der **Round-Zweig** von `_active_directive_effects` (Zeile 154-158) macht diesen
  Check **nicht** — er hängt immer nur die eine gewählte Direktive an. Ebenso zeigt
  `_render_directive_buttons` (`armyCard.py:169-192`) immer Primary/Secondary-Buttons,
  ohne die Affinität zu prüfen.
- Fazit: Dies ist exakt der S96/S97-Backlog-Punkt (`docs/goals/backlog.md` §2,
  „Dynastie-Affinität ‚beide Direktiven' greift nicht beim rundenzugewiesenen
  Protokoll"). Dieser Auftrag liefert kein neues Konzept, sondern bestätigt: die Lücke
  ist rein **Engine/UI im Round-Zweig**, das Datenmodell ist bereits vollständig.

## Regeltext-Zusammenfassung: Dynastie → Protokoll

| Dynastie | gekoppeltes Command Protocol | YAML-`subfaction_affinity` (schon vorhanden) |
|---|---|---|
| Mephrit | Protocol of the Vengeful Stars | `mephrit` (`protocol_vengeful_stars`) |
| Nephrekh | Protocol of the Sudden Storm | `nephrekh` (`protocol_sudden_storm`) |
| Nihilakh | Protocol of the Eternal Guardian | `nihilakh` (`protocol_eternal_guardian`) |
| Novokh | Protocol of the Hungry Void | `novokh` (`protocol_hungry_void`) |
| Sautekh | Protocol of the Conquering Tyrant | `sautekh` (`protocol_conquering_tyrant`) |
| Szarekhan | Protocol of the Undying Legions | `szarekhan` (`protocol_undying_legions`) |

Bedingung laut Regeltext (identisch für alle 6): **jede** Einheit der Armee (außer
DYNASTIC AGENT / C'TAN SHARD) muss den Dynastie-Code tragen — nicht nur die Dynastie-Wahl
im Roster. Diese Prüfung leistet die App bereits nicht granular (auch im 6er-Zweig nicht) —
`subfaction_value_for(player)` prüft nur die Roster-Dynastie, keine Pro-Unit-Codes. Das ist
bestehendes, bekanntes Verhalten (kein neuer Scope-Punkt dieses Konzepts).

## Datenmodell-Vorschlag: KEINE YAML-Änderung nötig

Kein neues Feld. Der generische Fix liegt ausschließlich im Round-Zweig von
`_active_directive_effects`:

```
if has_round:
    active = next((p for p in round_choices if p.id == active_id), None)
    if active:
        subfaction = subfaction_value_for(player)
        if subfaction and subfaction == active.subfaction_affinity:
            effects.append(_tagged_effect(active.primary_effect, active.id))
            effects.append(_tagged_effect(active.secondary_effect, active.id))
        else:
            raw = active.primary_effect if directive == "primary" else active.secondary_effect
            effects.append(_tagged_effect(raw, active.id))
```

Analog dazu: `_render_directive_buttons` (armyCard.py) braucht denselben Zweig wie
`_render_extra_round_choice` — bei Affinitäts-Treffer keine Primary/Secondary-Buttons,
sondern die „… BONUS (BOTH)"-Badge, keine manuelle Wahl nötig (Wahlzwang entfällt laut
Regeltext bei Affinität). Reine `src/`-Logik, kein Fraktions-String — `subfaction_affinity`
ist bereits generisch aus der YAML gelesen.

## Betroffene Dateien + Effort

- `src/gameMechanic/ability_engine.py` — `_active_directive_effects` (Round-Zweig)
- `src/uiLayout/armyCard.py` — `_render_directive_buttons` (Affinitäts-Zweig analog `_render_extra_round_choice`)
- `tests/gameMechanic/test_ability_engine.py` — Regressionstest je Dynastie-Fall (Round-Zweig, beide Direktiven aktiv)
- `docs/goals/backlog.md` §2 — S96/S97-Punkt bei Umsetzung schließen (nicht zwei Punkte)
- `docs/spec/faction_abilities.md:36` — „UI-Implementierung noch ausstehend" → nach Fix streichen

**Effort-Schätzung: S–M** (kein neues Datenmodell, ein Bedingungszweig + ein UI-Zweig +
Tests je 6 Dynastien). Passt in einen Executor-Brief ohne Split.

## Offene Entscheidungsfragen an den Stakeholder

1. Soll der Fix in einem Schritt (Engine + UI + Tests) oder aufgeteilt (erst Engine/Tests,
   UI-Anzeige als Folge-Schritt) laufen?
2. Reicht die bestehende Roster-Ebene-Prüfung (`subfaction_value_for`) weiterhin als
   Näherung für „jede Einheit trägt den Code", oder soll das als eigener, separater
   Befund (Pro-Unit-Dynastie-Codes) neu in den Backlog aufgenommen werden?
