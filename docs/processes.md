# Arbiter — Process Diagrams

> Numbering: P-NN (global unique). Find by phase or topic in the index below.
> Format: Mermaid flowcharts. Render in any Markdown viewer with Mermaid support.

---

## Index

| Nr.  | Prozess                                          | Phase(n)           |
|------|--------------------------------------------------|--------------------|
| P-01 | Unit wählen / abwählen                           | alle               |
| P-02 | Gegner-Einheit als Ziel designieren              | shooting/charge/fight |
| P-03 | Phasenstadien — Weiter-Logik                     | alle               |
| P-04 | Effektbestätigung — Schaden in PlayerArea        | alle (Effekt-Trigger) |
| P-05 | CommandPhase — Living Metal Heilung              | command            |
| P-06 | GO-Sichtbarkeit — Prüfkette                      | alle (Stratagems)  |
| P-07 | Schussphase — vollständiger Ablauf               | shooting           |

---

## P-01 — Unit wählen / abwählen (alle Phasen)

```mermaid
flowchart TD
    A[Spieler klickt Einheitsnamen\nin seiner armyList] --> B{setup_complete?}
    B -- nein --> Z[kein Effekt]
    B -- ja --> C{Einheit bereits\nselektiert?}
    C -- ja --> D[selected_unit = None\nselected_target = None]
    C -- nein --> E[selected_unit = faction, uid]
    D --> F[st.rerun]
    E --> F
    F --> G[gameActionsArea rendert\naktive PlayerArea mit Einheit]
```

**Zustand nach Selektion:**
- `st.session_state.selected_unit = (faction, uid)` oder `None`
- `st.session_state.selected_target = None` (wird bei Neu-Selektion immer zurückgesetzt)

---

## P-02 — Gegner-Einheit als Ziel designieren (shooting / charge / fight)

```mermaid
flowchart TD
    A[Spieler klickt Einheitsnamen\nder gegnerischen armyList] --> B{Phase erlaubt\nTargeting?}
    B -- nein\ncommand/movement/etc. --> C[nur Namens-Label anzeigen\nkein Button-Effekt]
    B -- ja\nshooting/charge/fight --> D{Einheit bereits\nals Target gesetzt?}
    D -- ja --> E[selected_target = None]
    D -- nein --> F[selected_target = faction, uid]
    E --> G[st.rerun]
    F --> G
    G --> H[inactive PlayerArea zeigt\nZiel-Info + T/Sv/++ Werte]
    H --> I[DisplayArea zeigt\nkombinierten Angriffs-Summary]
```

---

## P-03 — Phasenstadien — Weiter-Logik (alle Phasen)

Jede Phase durchläuft drei Stadien: **start → active → end**.
Der „→"-Pfeil springt erst durch Stadien, dann zur nächsten Phase.

```mermaid
flowchart TD
    A[Spieler klickt →] --> B{phase_stage?}
    B -- start --> C{gibt es Effekte\nfür 'active'?}
    C -- ja --> D[phase_stage = active\nst.rerun]
    C -- nein --> E{gibt es Effekte\nfür 'end'?}
    E -- ja --> F[phase_stage = end\nst.rerun]
    E -- nein --> G[next_phase\nphase_stage = start für neue Phase]
    B -- active --> E
    B -- end --> H[next_phase\nphase_stage = start]
    D --> Z[PlayerArea zeigt\nrelevante Aktionen für Stadium]
    F --> Z
    G --> Z
    H --> Z
```

**Hinweis:** Kein hartes Sperren — nur ein Hinweis wenn End-Effekte existieren.
Ein Phasensprung ist immer möglich (bewusste Entscheidung des Spielers).

---

## P-04 — Effektbestätigung — Schaden/Heilung in PlayerArea

Wenn ein Effekt Schaden oder Heilung an einer Einheit verursacht, erscheinen
die Wundbuttons in der **PlayerArea des betroffenen Spielers** (nicht auf der unitCard).

```mermaid
flowchart TD
    A[Effekt tritt ein\nbsp. Living Metal Heilung] --> B[active_effect = Effekt-Dict\nst.rerun]
    B --> C[PlayerArea des Spielers\nzeigt Bestätigungs-Buttons]
    C --> D[Spieler klickt +1 / -3 / etc.]
    D --> E[apply_damage oder heal_unit\nwird aufgerufen]
    E --> F[active_effect = None\nst.rerun]
    F --> G[PlayerArea kehrt\nzu Normal-Ansicht zurück]
```

**Aktueller Stand:** Wundbuttons erscheinen direkt bei selektierter Einheit.
`active_effect`-Mechanismus wird in Ziel 3 vollständig ausgebaut.

---

## P-05 — CommandPhase — Living Metal Heilung

```mermaid
flowchart TD
    A[Befehlsphase beginnt\nphase_stage = start] --> B[resolve_command_start\nCP +1 wenn Battle-Forged]
    B --> C[get_triggered_abilities\nphase=command, stage=start]
    C --> D{Einheiten mit\nlivingMetal Regel?}
    D -- ja --> E[apply_living_metal\nfür jede berechtigte Einheit]
    E --> F[Heilungs-Ergebnis\nin PlayerArea anzeigen]
    D -- nein --> G[Keine Heilung]
    F --> H[Spieler bestätigt\noder passt an]
    G --> H
    H --> I[Log-Eintrag schreiben]
```

**Einschränkung Living Metal:** `max_alive = models_remaining × unit.wounds`
Verhindert dass Modelle über ihre Startanzahl hinaus geheilt werden.

---

## P-06 — GO-Sichtbarkeit — Prüfkette (Stratagems)

```mermaid
flowchart TD
    A[Phase beginnt] --> B[Alle Stratagems\nder Armee laden]
    B --> C{Stratagem-Phase\n= aktuelle Phase?}
    C -- nein --> HIDE[nicht anzeigen]
    C -- ja --> D{Stratagem-Stage\n= aktueller phase_stage?}
    D -- nein --> HIDE
    D -- ja --> E{Bedingungen\nerfüllt?}
    E -- nein --> HIDE
    E -- ja --> F{Bereits diese\nPhase eingesetzt?}
    F -- ja --> GREY[anzeigen, ausgegraut]
    F -- nein --> G{CP ausreichend?}
    G -- nein --> GREY
    G -- ja --> CLICK[anzeigen, klickbar]
```

**Player-Sichtbarkeit:** `player = "active"` → nur aktiver Spieler sieht GO.
`player = "inactive"` → nur inaktiver Spieler (Reaktion auf Gegneraktion).
`player = "both"` → beide Spieler sehen die GO.

---

## P-07 — Schussphase — vollständiger Ablauf

```mermaid
flowchart TD
    A[Schussphase beginnt] --> B[Spieler wählt\nAngreifer-Einheit ▶]
    B --> C{Kann schiessen?}
    C -- nein\nadvanced/retreated/melee --> D[Warnung in PlayerArea]
    C -- ja --> E[Waffen-Profile\nin active PlayerArea]
    E --> F[Spieler wählt\nZiel-Einheit ▷]
    F --> G[T/Sv/++ in\ninactive PlayerArea]
    G --> H[DisplayArea zeigt\nkombinierten Angriffs-Summary]
    H --> I[Spieler würfelt\nphysisch auf dem Tisch]
    I --> J[Spieler klickt\nSchaden-Buttons in PlayerArea]
    J --> K[apply_damage aufrufen]
    K --> L{RP triggerbar?\nmodels_lost_since_last_rp > 0}
    L -- ja --> M[Reanimation Protocol\nin inactive PlayerArea]
    L -- nein --> N[Log-Eintrag schreiben]
    M --> N
    N --> O[Nächste Einheit oder\nPhase beenden]
```

**MWBD-Effekt:** Falls `my_will_be_done_active = True` beim Angreifer:
Hit-Roll-Schwelle wird um 1 gesenkt (z.B. BS4+ → BS3+).
Wird in `active_buffs` der Einheit gespeichert und im Summary angezeigt.
