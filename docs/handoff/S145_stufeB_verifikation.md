STATUS: NEEDS-VERIFICATION
Datum: 2026-07-14

## Zweck

Letzter offener Punkt von Ziel7 Stufe B (Necron-Gefechtsoptionen) ist eine manuelle
UI-Verifikation mit echtem Necron-Roster (`docs/goals/ziel7.md` Z. 76: „Manuelle
UI-Verifikation mit echtem Necron-Roster nach dem Delta-Fix."). Diese Datei bündelt die
Klickpfad-Anleitung dafür **und** die dazu passenden, noch offenen Necron-Punkte aus
`docs/goals/backlog.md` §3 („Offene manuelle UI-Verifikation") — damit eine Sitzung am
Bildschirm reicht, statt für jeden Punkt neu ein Necron-Spiel aufzusetzen.

**Lifecycle:** Nach bestandener Verifikation: Checkbox in `docs/goals/ziel7.md` (Z. 76)
abhaken, die entsprechenden Zeilen in `docs/goals/backlog.md` §3 abhaken/entfernen, diese
Datei löschen — macht der Koordinator/Executor der Folgesession auf Zuruf.

**Bewusst NICHT Teil dieser Prüfung** (damit nichts Unfertiges „geprüft" wird):
- Dynastie-Code-Anzeige (Uncanny Artificers Badge) — laut `ziel7.md` Z. 93–97 ist die
  Umsetzung von Dynastie-/Klan-Fähigkeiten erst „eigener Plan ab S145", also noch nicht
  gebaut.
- „Veil aus Nahkampf" (`backlog.md` Z. 473) — Veil of Darkness ist ein Relikt
  (`data/wh40k_9e/necrons/relics.yaml`), im empfohlenen Roster keiner Einheit zugewiesen;
  braucht eigenes Setup/Roster, hier nicht erzwungen.
- „WAAAGH Boss-Nob", „Cover Option B", „Big Mek Wargear" (`backlog.md` Z. 471/472/475) —
  Ork- bzw. fraktionsneutrale Punkte, kein Necron-Stufe-B-Scope.

---

## Vorbereitung

1. App starten: `streamlit run src/app.py` (Port 8501; ggf. `source .venv/bin/activate`
   vorher).
2. Setup-Screen (`src/uiLayout/setupScreen.py`):
   - **Game Mode:** „Matched Play" (Stratagems/CP brauchen Matched Play).
   - **Game Size:** „Strike Force" (2000 Pkt. Limit / 12 CP — deckt das 1500-Pkt.-Roster
     ab und gibt genug CP zum Stratagem-Testen).
   - **Player 1 Roster:** `necrons_1500pts_silent_king.yaml` — „Necrons 1500pts - Silent
     King" (per `ls data/rosters/` verifiziert vorhanden). Dynastie ist fix `szarekhan`
     (Roster-Header), enthält u. a. The Silent King (3-Modell-Einheit: Szarekh + 2
     Triarchal Menhirs), 2× Overlord, 3× Warriors, 2× Lychguard, Lokhust Heavy
     Destroyers, 2× Canoptek Scarabs.
   - **Player 2 Roster:** beliebiges anderes Roster (z. B. `orks.yaml`) — muss nur von P1
     verschieden sein (Setup-Screen blockt „same roster").
   - **Mission:** beliebig (nicht Teil dieser Prüfung).
   - „Start Game" klicken.

---

## Prüfschritte

### 1. Necron-Stratagems nach dem Delta-Fix
Quelle: `docs/goals/ziel7.md` Z. 63–75 (S123-Vollabgleich, 27 Befunde gefixt; OR-Bedingungen
wie `extermination_protocols`/`resurrection_protocols` bleiben bewusst offen → Plan 032,
NICHT Teil dieser Prüfung).

- [ ] Im Spiel den Tab **„⚔ Stratagems"** öffnen (Gefechtsoptionen-Bereich,
  `gameProtocoll.py`). Necron-Stratagems erscheinen in der Spalte des Necron-Spielers
  (fix `first_player`/`second_player`, nie an „active" gebunden).
- [ ] Stratagems sind nach Phase/Sektion sortiert sichtbar (z. B. Command/Movement/
  Shooting/Fight/Morale-Header) — kein Stratagem taucht in der falschen Phase oder gar
  nicht auf.
- [ ] Stichprobe 2–3 Necron-Stratagems öffnen (z. B. „Hand of the Phaeron", ein
  `before_battle`-Stratagem aus der ArmySetup-Liste) und CP-Kosten/Beschreibung gegen
  `data/wh40k_9e/necrons/stratagems.yaml` stichprobenhaft plausibilisieren.

### 2. Silent King Waffen (H2)
Quelle: `docs/goals/archive/ziel6.md` Z. 1096/1109 (S48/S50-Fix: Menhirs = Annihilator
Beam, Szarekh = Sceptre of Eternal Glory + Staff of Stars + Scythe of Dust;
`max_attacks` 4/3 statt fälschlich 10/9).

- [ ] The Silent King auswählen, Waffenliste/Angriffsdeklaration öffnen.
- [ ] Menhir-Gruppe zeigt **nur** „Annihilator Beam".
- [ ] Szarekh-Gruppe zeigt **Sceptre of Eternal Glory**, **Staff of Stars**,
  **Scythe of Dust** — keine anderen Waffen.
- [ ] Staff of Stars / Scythe of Dust (Nahkampf) erlauben höchstens 4 bzw. 3 zusätzliche
  Attacken (nicht 10/9).

### 3. Living Metal (H3) — gruppenbewusste Heilung
Quelle: `docs/goals/archive/ziel6.md` Z. 1096 („H3 Living-Metal-Bug — gruppen-bewusste
`unit_max_hp`"); Regel-Quelle `data/wh40k_9e/necrons/faction_abilities.yaml` (`living_metal`:
zu Beginn der eigenen Command-Phase heilt jedes beschädigte Modell 1 Wunde).

- [ ] Eine Necron-Einheit im Kampf beschädigen (z. B. Warriors oder eine Menhir-Gruppe des
  Silent King), dann in die nächste eigene Command-Phase gehen.
- [ ] Die betroffene Einheit/Gruppe heilt automatisch 1 Wunde je beschädigtem Modell
  (Living-Metal-Trigger sichtbar im Battle Log).
- [ ] Bei The Silent King (gemischte Gruppen Menhir/Szarekh): Gesundheitsbalken bleibt im
  gültigen Bereich [0,1], kein Crash, keine negative Anzeige (Regression zu S47c).

### 4. MWBD zweimal nutzbar (H5, PHAERON-Keyword)
Quelle: `docs/goals/archive/ziel6.md` Z. 1096 („H5 MWBD 2× bei PHAERON-Keyword");
Daten: `data/wh40k_9e/necrons/unit_abilities.yaml` Z. 248–257 (Silent King hat PHAERON als
Basis-Keyword, `extra_uses: has_keyword PHAERON, bonus 1`).

- [ ] In der eigenen Command-Phase bei The Silent King die Ability **„My Will Be Done"**
  aktivieren. Button zeigt zunächst „Activate My Will Be Done (1/2)".
- [ ] Nach der ersten Aktivierung (Ziel-Einheit wählen) zeigt der Button
  „Activate My Will Be Done (2/2)" — die Ability ist ein zweites Mal nutzbar.
- [ ] Nach der zweiten Aktivierung verschwindet der Button (max_uses erreicht) bis zur
  nächsten eigenen Command-Phase.

### 5. Reanimation Protocols (RP)
Quelle: `data/wh40k_9e/necrons/faction_abilities.yaml` (`reanimation_protocols`: reaktiv
nach gegnerischem Shooting/Fight, wenn Modelle der Einheit zerstört wurden, die Einheit
selbst aber nicht).

- [ ] Eine Necron-Infanterie-Einheit (z. B. Warriors) so beschießen/bekämpfen lassen, dass
  mindestens ein Modell stirbt, die Einheit aber nicht komplett vernichtet wird.
- [ ] Nach Abschluss der gegnerischen Attacken erscheint der RP-Wurf/-Hinweis für die
  betroffene Einheit (reaktiv, einmal pro Verteidiger nach voller Abhandlung der
  angreifenden Einheit — `docs/goals/archive/ziel6.md` S47 „G5").

### 6. Badge-Farben (H7 / RP / MWBD)
Quelle: `docs/goals/archive/ziel6.md` Z. 1096 („H7 Badge-Farben"); Soll-Farbschema:
`docs/spec/design_colors.md` §1/§3 (Buff-Badges grün `#4a9a5a`, kein separates
MWBD-Blau mehr).

- [ ] Aktive „My Will Be Done"-Buff-Badge auf der Ziel-unitCard ist **grün**, nicht blau.
- [ ] Dynasty-Subfaction-Badge auf der armyCard zeigt „Szarekhan" (Roster-Feld `dynasty`,
  `design_colors.md` §2a).

### 7. Optional/Zusatzcheck — Skorpekh-Roster (braucht anderes Roster)
Quelle: `docs/goals/backlog.md` Z. 474 („Skorpekh-Roster: 2× Threshers + 1× Reap-Blade
getrennt"). Das empfohlene Silent-King-Roster hat keine Skorpekh-Einheit — dieser Punkt
braucht ein zweites Spiel mit `data/rosters/zarekhan_sol_kampf_2.yaml` (ebenfalls Dynastie
Szarekhan, enthält `skorpekh_destroyers` mit `group_loadouts.skorpekh.swaps.reap_blade_swap`,
count 1 von 3 Modellen).

- [ ] Neues Spiel mit `zarekhan_sol_kampf_2.yaml` starten, Skorpekh Destroyers auswählen:
  UI zeigt 2 Modelle mit Standard-Thresher-Profil getrennt von 1 Modell mit
  Hyperphase-Reap-Blade-Profil (kein einheitliches Gruppenprofil).

---

## Ergebnis

| Schritt | Bestanden | Abweichung / Notiz |
|---|---|---|
| 1. Necron-Stratagems | ☐ ja / ☐ nein | |
| 2. Silent King Waffen | ☐ ja / ☐ nein | |
| 3. Living Metal | ☐ ja / ☐ nein | |
| 4. MWBD 2× | ☐ ja / ☐ nein | |
| 5. Reanimation Protocols | ☐ ja / ☐ nein | |
| 6. Badge-Farben | ☐ ja / ☐ nein | |
| 7. Skorpekh-Roster (optional) | ☐ ja / ☐ nein / ☐ ausgelassen | |

Abweichungen bitte zusätzlich in `docs/handoff/Stakeholder_Beobachtungen.md` eintragen
(stehender Eingangskanal) — dort mit Screenshot/Kurzbeschreibung, damit sie in die nächste
Session übernommen werden.
