STATUS: ANSWERED

# S135 — B6 Kurz-Mockup: Faction-Ability-Wahl nebeneinander (korrigiert)

> **Stakeholder-Antwort (S135, via Koordinator):** Mockup **freigegeben**. Zu den zwei
> offenen Fragen: Die Quelle für die beiden Direktiven ist **dieselbe wie später im
> Spiel** — das, was in der armyCard für jedes Protokoll angezeigt wird (Wiederverwendung
> des bestehenden Anzeige-Pfads, kein neuer Text-Pfad). Lese-Dropdown je Spieler-Block
> wie in der Skizze bestätigt.

Bezug: `docs/handoff/S134_offene_punkte.md` (B6 — Option B, „aktuelle Funktionalität
muss erhalten bleiben"), `docs/goals/backlog.md` §2 (B6, Screenshot `…21-27-05.png`).
Betroffener Code: `src/uiLayout/gameActionsArea.py::_render_round_choice_assignment`
— **bleibt dort** (Stakeholder-Korrektur unten; kein Umzug nach `armyCard.py`).

## Grundannahmen (bitte bestätigen)

1. Die App würfelt nicht — gewürfelt wird am Tisch (Standard-Weltbild, unverändert).
2. **Render-Ort bleibt die Center-Spalte** (`_render_setup`, unterhalb von
   „Start Game") — keine Migration in die armyCard/Spieler-Spalten, kein Expander,
   keine Status-Zeile. Einzige Layout-Änderung: die beiden Spieler-Blöcke stehen
   **nebeneinander** (`st.columns(2)`: Player A links, Player B rechts — Reihenfolge
   fest an den Slots, nicht an `active`).
3. **Datenmodell/State bleibt exakt gleich:** sechs Slots (Runde 1–5 + „Always
   active"/6.) als Bijektion, Swap-Logik `_round_choice_slots_after_swap`,
   Session-Keys `proto_slots_<faction>` / `round_choice_assignments` — unverändert.
   Auch die Auswahl-Dropdowns (Selectboxes) bleiben wie sie sind.
4. **Sichtbarkeit bleibt Setup-exklusiv:** Block erscheint nur in der Setup-Phase;
   ab „Start Game" übernimmt unverändert die In-Game-Anzeige
   (`armyCard._render_round_choice_ui`).
5. **Kein neuer Farb-/Geometrie-Baustein:** nur natives `st.columns(2)` + bestehende
   Selectboxes + `st.caption()` für Regeltext — keine eigenen Farbentscheidungen.

## Ist-Stand Regeltext (verifiziert per Read/grep)

`_render_round_choice_assignment` (`gameActionsArea.py:143–210`) rendert heute
**ausschließlich die sechs Selectboxes** — es gibt dort **keinerlei Regeltext-Anzeige**,
weder statisch noch der Auswahl folgend (einziger `rule_text`-Treffer in der Datei ist
Zeile 107, Unit-Datasheet, anderer Kontext). Die Regeltexte existieren im Datenmodell:
`RoundChoiceAbility` (`src/gameObjects/round_choice_ability.py`) trägt je Protocol
**zwei** Direktiven-Texte (`primary`, `secondary`), kein einzelnes `rule_text`-Feld.

**Folge:** Der vom Stakeholder geforderte mitwechselnde Regeltext ist Teil des
B6-Fixes (Neubau), nicht nur eine Kopplungs-Korrektur.

## Mockup (verbindlich = Stakeholder-Skizze)

**Vorher:** beide Spieler-Blöcke untereinander in der Center-Spalte (volle Breite).

**Nachher:**

```
Roll-Off for First Player
[ Player A ]                                                    [ Player B ]
────────────────────────────────────────────────────────────────────────────
                              [ ⚔ Start Game ]
────────────────────────────────────────────────────────────────────────────
Player A — Command Protocols                 Player B — Command Protocols
  [Always active protocol (6th)▾]            [Always active protocol (6th)▾]
  [Round 1 protocol▾]                        [Round 1 protocol▾]
  [...▾]                                     [...▾]
────────────────────────────────────────────────────────────────────────────
```

Ergänzt um den Regeltext-Bereich je Spieler-Block (Neubau, s. Ist-Stand): ein
Lese-Dropdown unter den Slot-Selectboxes; wechselt die Auswahl darin (oder in einem
Slot), wechselt der angezeigte Regeltext mit:

```
  Read protocol: [Protocol of the Eternal Guardian ▾]
  ↳ Primary: <Direktiven-Text primary>
  ↳ Secondary: <Direktiven-Text secondary>
```

Bausteine (design_system.md): Zwei-Spalten-Layout = natives `st.columns(2)` (wie
Roll-Off-Buttons direkt darüber); Selectboxes unverändert; Regeltext als
`st.caption()` (etabliertes Ability-Text-Muster, vgl. `gameActionsArea.py:107`);
Label weiterhin aus `load_round_choice_label(faction_dir)` (faktionsgenerisch).

## Stakeholder-Korrektur (S135) — dokumentiert, bindend

> KOMMENTAR: Ich denke, hier liegt ein großes Missverständnis vor! Ich stelle mir das
> Mockup eher so vor: *(ASCII-Skizze — oben als „Nachher" übernommen)*
> - Es gibt einen Dropdown, um den Regeltext lesen zu können.
> - Der Dropdown zur Auswahl des Protocols bleibt so wie es ist. (Der Regeltext muss
>   ebenfalls wechsel!)
> - Es ist also fast dieselbe Funktionalität in derselben Area, nur nebeneinander für
>   beide Spieler statt untereinander.

Die drei ursprünglichen Entscheidungsfragen (Status-Zeile, Expander-Default,
Wortlaut-Sprache) sind damit **gegenstandslos** — Status-Zeile und Expander entfallen,
der Wortlaut bleibt der bestehende.

## Entscheidungsfragen (neu, aus dem Ist-Stand-Befund)

1. **Regeltext-Inhalt** — `RoundChoiceAbility` hat keine Einzelbeschreibung, sondern
   zwei Direktiven-Texte (`primary`/`secondary`). **Empfehlung:** beide anzeigen
   (wie im Mockup) — die Direktiven-Wahl fällt erst im Spiel am Rundenanfang, beim
   Setup-Lesen braucht der Spieler beide, um sinnvoll zuzuordnen.
2. **Regeltext-Quelle** — eigenes Lese-Dropdown (Skizze, Empfehlung) vs. Kopplung an
   den zuletzt geänderten Slot. **Empfehlung:** eigenes Lese-Dropdown je Spieler-Block,
   exakt wie in der Stakeholder-Skizze beschrieben („Dropdown, um den Regeltext lesen
   zu können") — die Slot-Selectboxes bleiben dadurch unangetastet.

## Nächster Schritt

Nach Antwort auf Frage 1+2 (+ Bestätigung Grundannahmen): S-Fix als eigener
Executor-Auftrag (Sonnet) — `_render_round_choice_assignment`-Aufrufe in
`_render_setup` in `st.columns(2)` legen, Lese-Dropdown + mitwechselnden
Regeltext-Bereich ergänzen, Render-Test; manuell prüfen: Setup-Phase → Blöcke
nebeneinander, Regeltext wechselt mit der Auswahl, Slot-Swap funktioniert weiter,
nach „Start Game" verschwindet der Block.
