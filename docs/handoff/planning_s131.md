STATUS: ANSWERED

# Planning S131 — ENTWURF v2 (Re-Plan nach Stakeholder-Anmerkungen)
Datum: 2026-07-09

## Kontext — was sich gegenüber v1 ändert
Stakeholder hat `docs/handoff/go_ui_concept_s131.md` (5 Anmerkungen) + 3 Screenshots
kommentiert. Kernverschiebung: **kein App-Würfeln** (Anmerkung 1 — App ist Erinnerer/
Entscheidungshelfer, Schiedsrichter erst bei Phasen-/Zug-/Rundenende), die
Reroll/Reaktiv/Proaktiv-Dreiteilung aus v1 ist ungesichert (Anmerkung 2 — neue
UI-unabhängige Recherche nötig), und der Stakeholder will das **ganze
GO-UI-Chaos über alle Phasen** in dieser Session (ggf. über mehrere) recherchieren,
konzipieren und planen (Anmerkung 5) — nicht nur Command-Re-Roll-Undo isoliert lösen.
Schwerpunkt S131: **Recherche + Konzept**, nicht Implementierung.

## Fixierte Entscheidungen (nicht neu fragen)
- Würfe passieren am Tisch, nicht in der App; App = Erinnerer/Entscheidungshelfer.
  Vollrückgängig ist Standard für alle GOs bis zum Schiedsrichter-Moment — kein
  „abgeschwächter Undo", das v1-Sonderfall-Konzept für Command-Re-Roll entfällt.
- Kein Pass-Button (passen = Use nicht drücken); keine doppelte CP-Anzeige.
- Komponenten-Sketch (Header: Name · CP · [Use]/[↺]; Keyword-Chips wie UnitCard;
  Regeltext ausklappbar) ist Design-Richtung — analog für Inline und Tab-Schalter.
- GOs sind IMMER sichtbar in der Runde, werden bei Trigger hervorgehoben/aktiviert
  statt plötzlich aufzutauchen — gilt für Inline UND Tab-Schalter; beide müssen
  konsistent sein (Begriffe, Farben, Verhalten).
- Vorbild-Darstellung: heroische Intervention (schlank, s. Screenshot 18-26-00);
  Zielauswahl-UI (Screenshot 18-27-11) ist zu überladen; Profilwert-Vergleich per
  Dropdown zurückgestellt.

## Screenshot-Check (Auftrag Punkt 2)
`Bildschirmfoto 17-34-26` zeigt tatsächlich den **Setup-Screen vor** „Start Game"
(Text „When ready, click × Start Game below"), nicht den Screen direkt danach — die
Beobachtung „nach Spielstart ganz nach unten gescrollt" bezieht sich auf den ersten
Phasen-Screen. Plausibel als Referenz trotzdem: GameHeader (VP/CP/Phase-Pills) ist
dieselbe Komponente in jedem Screen — der Screenshot zeigt, wie „voller Header sichtbar
von oben" aussehen soll. Siehe offene Frage 1.

## Aufgaben

1. **UI-Ist-Inventar** (Research-Subagent) — alle Interaktionsmuster der
   GameActionArea über alle Phasen katalogisieren: Buttons (Bewegung/Advance,
   Charge, Heroic Intervention), Boxen (reaktive GOs), Inline-Offers (Re-Roll),
   Zielauswahl, Tab-Schalter (Stratagems). Quellen: `src/uiLayout/gameActionsArea.py`,
   `src/uiLayout/_common.py`, `src/gameMechanic/{movementPhase,chargephase,fightPhase,
   moralePhase,psychicPhase}.py`, `src/uiLayout/gameProtocoll.py`. Output: Ist-Katalog
   als Datei (Muster, Fundstelle, Trigger, Farbgebung, Konsistenz-Lücken). Effort **M**
   (~35k). Tier **Sonnet** (Kategorisierung/Synthese über 8 Dateien, kein reiner Lookup).

2. **GO-Klassifikations-Recherche** (Research-Subagent) — UI-unabhängige Einteilung
   aller Stratagems/GOs: Achse reaktiv/proaktiv, Re-Roll & Co. als **Effekt**, nicht
   als dritte Kategorie (Anmerkung 2: ein Re-Roll kann pro- oder reaktiv sein).
   Quellen: `docs/work/wahapedia_core_rules/`, `docs/work/wahapedia_necrons/`,
   `docs/work/wahapedia_orks/`, `docs/work/wahapedia_adeptus_custodes/`,
   `data/wh40k_9e/*/stratagems.yaml`. Output: Klassifikations-Tabelle (GO → Trigger-Typ
   × Effekt-Typ) als Grundlage fürs Design-System. Effort **M** (~30k). Tier **Sonnet**
   (Regelinterpretation/Einteilungsurteil, ausdrücklich vom Stakeholder als eigene
   Analyse angefragt — kein Lookup).

3. **Design-System-Konzept v2** (Synthese, **Opus/Hauptsession — kein Subagent**,
   da mehrdeutig/entscheidungsrelevant) — aus 1+2+Sketch+Screenshots: Komponenten
   festlegen (GO-Karte inkl. Akkordeon-Fix aus Anmerkung 4, Hervorhebungs-/
   Trigger-Zustand, Inline-Ort je Wurfbereich in der Attackenabfolge: Treffer/
   Verwundung/Rüstung/Rettung/Schadenzuweisung + Modell-Auswahl-Trigger), konkreter
   **Vorschlag für Command-Re-Roll beim Advance in der Button-UI des aktiven
   Spielers** (Anmerkung 5, explizit angefragt), Farb-/Begriffs-Konventionen an
   `design_colors.md`/`design_system.md` andocken (bestehende `badge()`/`chip()`-
   Bausteine aus `src/uiLayout/badges.py` wiederverwenden statt neue Geometrie).
   Effort **M** (~40k, Hauptsession-Budget). Kein Tier — Opus direkt.

4. **Mehr-Session-Roadmap** (Teil von Aufgabe 3) — was passiert in S131 (Recherche +
   Konzept, dieser Plan) vs. S132+ (Phasen-UI-Umbau je Phase, Einheiten-Auswahl in
   GameActionArea ziehen analog Heroic Intervention — Anmerkung 5 Ausblick, bewusst
   noch kein Executor-Auftrag). Ergebnis: nummerierte Umbau-Reihenfolge mit
   Effort/Tier-Schätzung je Phase, damit S132 direkt startklar ist.

5. **Scroll-Bug „Setup → Spielstart"** (Executor-Subagent, klein, unabhängig vom
   Design-System) — nach „Start Game" sollte der neue Phasen-Screen von oben (voller
   GameHeader sichtbar) starten, aktuell springt die Seite nach unten. Untersuchung:
   Streamlit-Rerun-Scroll-Verhalten, `st.session_state`-getriebene Anchor-/Expander-
   Reste aus der langen Setup-Seite. Betroffene Dateien vermutlich
   `src/uiLayout/setupScreen.py`, `src/app.py`. Effort **S** (~12k). Tier **Sonnet**
   (Scroll-Verhalten ist kein reiner Lookup, braucht Untersuchung).

## Nicht in dieser Session (bewusst zurückgestellt)
- **Command-Re-Roll-Undo-Fix (v1-Kern) + `before_battle`-Sichtbarkeitsfix
  (v1-Aufgabe 3):** beide unabhängig vom Design-Entscheid technisch möglich, aber
  zurückgestellt — Fokus S131 bleibt Recherche/Konzept, Umsetzung wartet auf
  Aufgabe 3/4-Ergebnis (Command-Re-Roll braucht das fertige Inline-Komponentendesign,
  sonst Doppelarbeit).
- **Command-Re-Roll auf Charge/Advance ausweiten (v1-Aufgabe 4):** explizit an
  Design-System-Entscheid gebunden (Anmerkung 5 verlangt genau dafür einen Vorschlag
  in Aufgabe 3) — Umsetzung erst S132+.
- **Manuelle UI-Verifikation S130 (volle Checkliste):** siehe offene Frage 2.
- Ziel9-Fetcher, Mission-Scoring, §6e-Modifier-Engine, rp/directive-Vokabular,
  Stufe-C-Orks — unverändert zurückgestellt wie v1.

## Offene Fragen an den Stakeholder
1. **Screenshot 17-34-26 (Setup- statt Post-Start-Screen):** als Referenz für „voller
   Header von oben" trotzdem nutzen (gleiche GameHeader-Komponente), oder brauchst du
   noch einen echten Post-Start-Screenshot? **Empfehlung:** nutzen, GameHeader ist
   phasen-unabhängig identisch.
2. **Manuelle UI-Verifikation S130:** volle 7-Punkte-Checkliste jetzt durchgehen
   (Layout wird in S132 eh umgebaut), oder nur ein schneller **Funktionscheck**
   (CP-Buchung/Trigger korrekt, Layout ignorieren)? **Empfehlung:** nur Funktionscheck
   jetzt — volle UI-Verifikation erst nach dem S132-Umbau, sonst doppelte Prüfarbeit.
3. **Aufgabe 5 (Scroll-Bug) in S131 einplanen oder in den Backlog?**
   **Empfehlung:** in S131 einplanen — klein, unabhängig, schneller Nutzerwert,
   passt ins Token-Budget neben 1–4.
