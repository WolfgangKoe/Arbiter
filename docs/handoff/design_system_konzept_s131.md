STATUS: ANSWERED

# Design-System-Konzept v2 — GameActionArea & Gefechtsoptionen (S131)

**Entschieden (2026-07-09):** alle 4 Fragen aus §6 mit der Empfehlung beantwortet —
(1) GO-Karte mit 4 Zuständen + 3 Orten = verbindlicher Standard; (2) Hervorhebung
„bereit" = bestehendes Gold-Primary, kein neues Farb-Token; (3) doppelte Sichtbarkeit
(zentrale Liste ruhend + Inline-Anker bereit) für `bei_ereignis`-GOs bestätigt; (4)
Roadmap §5 (6 Pakete S132–S134+) freigegeben, jedes Paket geht einzeln durchs
Freigabe-Gate. Festlegungen übernommen nach
[`docs/spec/design_system.md`](../spec/design_system.md) §6, Roadmap nach
[`docs/goals/backlog.md`](../goals/backlog.md) §2.

Temporär — nach Entscheid wandern die Festlegungen nach `docs/spec/design_colors.md`
(bzw. neues `docs/spec/design_system.md`) und die Roadmap nach `docs/goals/`.
Grundlagen: `ui_inventar_s131.md` (17 Ist-Muster), `go_klassifikation_s131.md`
(95 GOs, 3 Achsen), Stakeholder-Sketch + Screenshots (Heroische Intervention als
Vorbild), fixierte Entscheidungen aus `planning_s131.md`.

## 1. Kernidee: EINE GO-Karte, drei Orte, vier Zustände

Statt drei verschiedener Bauformen (reaktive Box / Inline-Button / Expander-Liste)
gibt es genau **eine Komponente „GO-Karte"** nach deinem Sketch — überall gleich
aufgebaut, nur in Voll- oder Kompaktform gerendert:

```
▸ Fire Overwatch · 1 CP                    [Use]
[CORE] [CHARGE] [reaktiv]
   (▸ klappt den Regeltext aus — nur dafür)
```

- Header-Zeile: Name · CP-Kosten · genau EIN Aktions-Slot rechts ([Use] oder [↺]).
- Keyword-Chips wie in der UnitCard (bestehender `chip()`-Baustein).
- Regeltext nur ausklappbar (Akkordeon-Fix: klappt nie von selbst zu).
- Kein Pass-Button (passen = nicht drücken), keine CP-Gesamtanzeige auf der Karte
  (die steht nur im GameHeader — die kleine Doppel-Caption im Tab entfällt).

**Vier Zustände** (ersetzen das „plötzliche Auftauchen"):

| Zustand | Wann | Darstellung |
|---|---|---|
| ruhend | Trigger (noch) nicht erfüllt | sichtbar, gedimmt, [Use] disabled |
| bereit | Trigger erfüllt, CP reichen | hervorgehoben, [Use] aktiv |
| verwendet | Use gedrückt, Fenster noch offen | [↺ Undo (+N CP)] statt [Use] |
| gesperrt | CP fehlen / Voraussetzung weg | gedimmt, Grund als Suffix im Header |

Undo ist überall **Vollrückgängig** (CP zurück, Effekt/Wert zurück), solange das
Fenster offen ist — Schiedsrichter-Moment erst am Phasen-/Zug-/Rundenende.

## 2. Drei Orte — Zuordnung direkt aus der Klassifikation

| Klassifikation (Achse b) | Ort | Form |
|---|---|---|
| spielweit (12 GOs, before_battle) | Liste im ArmySetup, vor „Start Game" | Vollform |
| phasenweit/proaktiv (~22) | zentrale Stratagems-Liste (Spielerseite) | Vollform |
| bei_ereignis (~45) | zentrale Liste (ruhend) **+** Inline-Anker am auslösenden Schritt | Voll + Kompakt |
| vor_wurf / nach_wurf (11) | Inline-Anker direkt an der Wurf-Eingabe | Kompakt |

Die zentrale Liste ist der **Planungs-Überblick** („was habe ich diese Phase?"),
der Inline-Anker die **Erinnerung am Ort des Geschehens** — beide rendern dieselbe
Karte aus derselben Buchhaltung (`spend_stratagem`-Pipeline), nichts doppelt gebucht.
Damit ist auch der `before_battle`-Sichtbarkeitsfix (13 GOs matchen heute nie)
konzeptionell gelöst: eigener Ort statt Sonderphase.

## 3. Tisch-Wurf-Eingabe als Baustein (statt 8 verstreuter number_inputs)

Die App würfelt nicht. Jede Stelle „Spieler trägt Tischwurf ein" wird EIN Baustein:
Label-Schema `⟨Wurf⟩ (D6/2D6)`, Zahlenfeld, darunter ein **Anker-Slot** für
wurf-bezogene GO-Karten (Kompaktform). Gilt für: Advance-Wurf, Charge-Wurf,
Morale-Test, Manifest/Deny, Damage-Block — die Attackenabfolge bekommt so je einen
Anker bei Treffer / Verwundung / Rüstung / Rettung / Schadenszuweisung.

**Dein angefragter Vorschlag — Command Re-Roll beim Advance** (aktiver Spieler,
Button-UI der Bewegungsphase):

```
[Move] [Advance ✓] [Stationary] [Retreat]
Advance roll (D6):  [ 3 ]
▸ Command Re-Roll · 1 CP                   [Use]     ← ruhend bis Wert da, dann bereit
```

Ablauf: Wert eintragen → Karte wird „bereit" → [Use] bucht 1 CP, Feld öffnet sich
für den neuen Tischwurf → Karte „verwendet" mit [↺ Undo (+1 CP)] = Vollrückgängig
(alter Wert + CP zurück). Gleiches Muster später für Charge und alle 11 Wurf-GOs.

## 4. Wortlaut- und Farb-Konventionen

- **Sprache:** durchgehend Englisch (Ist-Befund: `moralePhase.py` komplett Deutsch,
  Subgruppen-Selector gemischt → Bereinigung als Roadmap-Punkt).
- **Aktions-Vokabular (eine Familie statt vier):** `Use (N CP)` · `↺ Undo (+N CP)`
  · `Confirm ⟨Aktion⟩` / `Cancel` · Toggle-Auswahl mit `✓`-Präfix (wie Heroische
  Intervention). „Reset", „Undo deny", „Rückgängig" etc. entfallen.
- **Ein** Stepper-Baustein (`wound_adjustment_buttons` bleibt, der Zweitbau in
  fightPhase wird migriert), **eine** CP-Anzeige (GameHeader).
- **Farben:** keine neuen Töne von meiner Seite — Vorschlag innerhalb des
  bestehenden Schemas (`design_colors.md`): „bereit" = Gold-Primary-Rahmen (wie
  ausgewählter Zustands-Button), „ruhend/gesperrt" = Secondary gedimmt. Falls du
  für „bereit" einen eigenen Akzent willst, ergänzt du das Schema (Frage 2).

## 5. Roadmap (Mehr-Session-Plan, je Auftrag ≤ M)

| # | Session | Paket | Effort |
|---|---|---|---|
| 1 | S132 | GO-Karten-Baustein (4 Zustände, Voll/Kompakt, Akkordeon-Fix) + zentrale Liste umstellen | M |
| 2 | S132 | Tisch-Wurf-Baustein + Command Re-Roll Advance/Charge (Stakeholder-Auflage) | M |
| 3 | S133 | Reaktive Boxen → GO-Karte migrieren; before_battle-Liste im ArmySetup (13 GOs sichtbar) | M |
| 4 | S133 | Inline-Anker Attackenabfolge (5 Wurfbereiche) + restliche Wurf-GOs | M |
| 5 | S134 | Wortlaut-/Sprach-Bereinigung (Englisch, Use/Undo/Confirm), CP-Single-Source, Stepper | S–M |
| 6 | S134+ | Einheiten-Auswahl in die GameActionArea (HI-Muster verallgemeinern), Zielauswahl entschlacken | M, eigenes Konzept-Inkrement |
| 7 | danach | Manuelle UI-Verifikation (S130-Checkliste + neues Design) | Stakeholder |

Reihenfolge-Logik: erst der Baustein (1), dann deine Auflage (2), dann Migration
Bestand (3–5); Paket 6 ist bewusst hinten — es braucht ein eigenes kleines Konzept
(Zielauswahl-Entschlackung), sobald die GO-Karte steht.

## 6. Entscheidungsfragen

1. **GO-Karte + Zustände + Orte (§1–§3) so festlegen?** Danach wird sie Spec
   (`design_system.md`) und Maßstab für jeden weiteren UI-Auftrag.
2. **Hervorhebung „bereit":** Gold-Primary aus dem Bestand (Empfehlung, kein neues
   Farb-Token) — oder willst du einen eigenen Akzent im Schema definieren?
3. **Doppelte Sichtbarkeit** (zentrale Liste ruhend + Inline-Anker bereit) für
   bei_ereignis-GOs okay? Empfehlung: ja — Liste = Planung, Anker = Erinnerung.
4. **Roadmap-Reihenfolge §5** freigeben (nur Reihenfolge — jeder Auftrag geht
   einzeln durchs Freigabe-Gate)?
