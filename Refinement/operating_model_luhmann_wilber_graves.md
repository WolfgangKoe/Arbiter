# Aufbau- und Ablauforganisation mit KI-Systemen — nach Luhmann, Wilber und Graves

> **Zweck dieser Datei:** Grundlage für einen LinkedIn-Artikel (inkl. Titelbild). Sie
> beschreibt am realen Beispiel **Arbiter** (ein KI-gebautes Software-Projekt), wie sich
> eine funktionierende Aufbau- und Ablauforganisation *mit* KI-Systemen bauen lässt,
> wenn man sie durch drei Theorie-Linsen denkt: **Luhmann** (Organisation als
> Entscheidung/Kommunikation), **Wilber** (AQAL — vier Quadranten), **Graves/Spiral
> Dynamics** (Wertememe als Komplexitätsstaffel). Eine KI wie Opus oder GPT-5.5 soll aus
> dieser Datei einen flüssigen Artikel + ein passendes Bild erzeugen können.
>
> **Schreib-Stil-Hinweis für den Artikel:** keine Theorie-Vorlesung. Die Theorie ist das
> Skelett, das Projekt das Fleisch. Konkrete Mechanik (Hooks, Gates, Token-Korridor)
> zeigen, dass es *funktioniert*, nicht nur klingt.

---

## 0. Der Aufhänger (Hook für den Artikel)

KI-Agenten werden meist als *Werkzeug* gedacht: Prompt rein, Code raus. Das skaliert nicht
— und es zerfällt, sobald die Arbeit über eine Sitzung hinausgeht. Der eigentliche Hebel
ist ein anderer: **Man baut keine bessere KI, man baut eine bessere *Organisation* um die
KI herum.** Eine Organisation hat Rollen, Entscheidungswege, Gates, ein Gedächtnis und
eine Kultur — und genau das lässt sich für ein Team aus Mensch + KI-Agenten explizit
konstruieren.

Der provokante Kern: **Der Agent existiert zwischen zwei Sitzungen nicht.** Er hat kein
Bewusstsein, keine Erinnerung, keine Kontinuität. Die Organisation darf sich deshalb
*nicht* auf das Gedächtnis des Agenten verlassen. Sie erinnert in **Artefakten und
vollzogenen Regeln (Hooks/Gates)** — nicht im Kopf. Das ist exakt Luhmanns Pointe:
Organisationen bestehen aus *Kommunikation/Entscheidungen*, nicht aus Personen. Bei
KI-Agenten ist das keine Abstraktion mehr, sondern wörtlich wahr.

Praxisbeleg ist **Arbiter** — ein digitaler Spielbegleiter für Warhammer 40.000, gebaut
in einem Mensch-+-Opus/Sonnet/Haiku-Team, mit messbaren Gates über mehrere Dimensionen.

---

## 1. Luhmann — Organisation als entscheidbare Prämissen

Luhmann: Eine Organisation reproduziert sich über **Entscheidungen**, und Entscheidungen
stützen sich auf **Entscheidungsprämissen**. Vier davon sind gestaltbar. Wir haben sie 1:1
zum Fundament unseres Operating-Models gemacht:

| Luhmanns Prämisse | Bei uns | Wo sie lebt |
|---|---|---|
| **1 · Programme** (Zweck- + Konditionalprogramme) | Ziele/Backlog/„nächster Schritt" (Zweck) **+** Tests, Coverage-Gate, Architektur-Gate, Rule-Conformance-Catalog, Debt-Scoreboard, CLAUDE.md-Regeln (Konditional) | `docs/goals/`, `docs/spec/architecture_invariants.md` |
| **2 · Kommunikationswege / Zuständigkeiten** | Wer redet mit wem, wer entscheidet in welchem Modus, wie Eskalation fließt | `docs/governance/operating_model.md` |
| **3 · Personal / „Stellen"** | Welche **Rolle** bekommt welches **Modell-Tier** (Opus/Sonnet/Haiku) | operating_model.md, Abschnitt Rollen |
| **4 · Kultur** | Prinzipien, die *nicht pro Task* verhandelt werden: Freigabe-Pflicht, „Generic src", „No Laziness", Simplicity First | `CLAUDE.md` |

**Die zentrale Luhmann-Einsicht für KI-Teams:**
- **Zweckprogramm vs. Konditionalprogramm** ist die wichtigste Unterscheidung. Ein
  *Konditionalprogramm* ("wenn Bedingung X, dann Y") braucht **kein Urteil** — es kann an
  ein niedriges Modell-Tier oder direkt an die Maschine (Hook/Gate) delegiert werden. Ein
  *Zweckprogramm* ("erreiche Ziel Z, Weg offen") braucht **Sinn und Urteil** — es bleibt
  beim höchsten Tier (Opus) und beim Menschen.
- **Diskontinuität als Designprinzip.** Weil der Agent zwischen Sessions „aufhört zu
  existieren", sind alle Prozess-Events explizit auf *Wiederanlauf aus Artefakten* gebaut:
  Session-Start liest den Stand, Session-Ende schreibt ihn zurück und committet.
- **Entscheidung wird von Prämisse getrennt.** Die „Verfassung" (operating_model.md) ist
  selbst versioniert und *iterierbar wie Code*: Änderungen an Prämissen laufen über
  **ADRs** (Architecture Decision Records) und Commits — die Organisation kann ihre
  eigenen Regeln beobachten und ändern (Luhmanns „Entscheidung über
  Entscheidungsprämissen").

---

## 2. Wilber — AQAL: das System aus vier Quadranten betrachtet

Wilbers Integrales Modell (AQAL) sagt: Jedes Phänomen hat vier irreduzible Perspektiven —
Innen/Außen × Einzeln/Kollektiv. Auf unser Mensch-+-KI-System gemappt ergibt das ein
vollständiges Bild, das erklärt, *warum* einzelne Gates nicht reichen und man **in jeder
Dimension** ein Sicherheitsnetz braucht:

```
                INNEN (Bewusstsein/Sinn)        AUSSEN (Verhalten/Form)
              ┌───────────────────────────┬───────────────────────────┐
   EINZELN    │  UL — Das Urteil          │  UR — Der Code / Artefakt │
   (Ich/Es)   │  Intention, Sinn,         │  Konkrete Datei, Funktion,│
              │  Scope-Verständnis des    │  Test, Render-Pixel.      │
              │  Orchestrators (Opus).    │  Messbar: pytest, Build.  │
              ├───────────────────────────┼───────────────────────────┤
   KOLLEKTIV  │  LL — Die Kultur          │  LR — Prozess & System    │
   (Wir/Sie)  │  CLAUDE.md: geteilte      │  Operating-Model, Hooks,  │
              │  Prinzipien, Haltung,     │  Gates, Artefakt-Landkarte,│
              │  „so arbeiten wir".       │  Kommunikationswege.      │
              └───────────────────────────┴───────────────────────────┘
```

| Quadrant | Was er im Projekt ist | Sicherungsmechanismus |
|---|---|---|
| **UR — Es/außen, einzeln** | Der einzelne Code, eine Funktion, ein Render-Output | Unit-Tests, Coverage-Gate ≥ 90 %, Linter |
| **LR — Sie/außen, kollektiv** | Prozess, Struktur, Artefakte, Kommunikationswege | Operating-Model, Hooks, Architektur-Invarianten, Doku-Gates |
| **LL — Wir/innen, kollektiv** | Geteilte Kultur & Prinzipien | `CLAUDE.md` (wird gepflegt, nicht pro Task entschieden) |
| **UL — Ich/innen, einzeln** | Sinn, Urteil, Scope-Klärung | Bleibt beim Orchestrator (Opus) + Mensch; nicht delegierbar |

**Die Wilber-Pointe für den Artikel:** Die meisten „KI-Coding"-Setups optimieren nur **UR**
(besserer Code) und vielleicht **LR** (Pipelines). Sie ignorieren **LL** (eine explizite,
gepflegte Kultur) und **UL** (wo Sinn/Urteil bewusst *nicht* automatisiert wird). Ein
robustes System braucht **alle vier** — und für jeden Außen-Quadranten ein *messbares*
Gate, für jeden Innen-Quadranten eine *bewusst menschen-/Opus-gehaltene* Entscheidung.
Genau dieses „nicht alles automatisieren" ist die reife Variante.

---

## 3. Graves / Spiral Dynamics — Tiering als Wertememe-Staffel

Graves (popularisiert als Spiral Dynamics) beschreibt Entwicklung als Staffel zunehmender
**Komplexitäts-Bewältigung**: jedes Wertememe ist für ein bestimmtes Maß an Offenheit/
Ambiguität das passende. Übertragen auf KI-Tiering ist das unsere **Faustregel der
Rollen-/Modell-Zuweisung**:

> **Je geschlossener das Konditionalprogramm → desto niedriger das Tier.**
> **Je offener das Zweckprogramm / je mehr Sinn, Urteil, Stakeholder-Abgleich → desto höher.**

| Komplexitätsgrad der Aufgabe | Wertememe-Analogie | Modell-Tier | Beispiele |
|---|---|---|---|
| Geschlossen, deterministisch, eine richtige Antwort | „Blau" — Regel, Ordnung | **Haiku** | Reiner Regel-Lookup, Klassifikation nach festem Schema, ja/nein gegen expliziten Text |
| Synthese aus mehreren Quellen, fixer Plan | „Orange" — Leistung, Methode | **Sonnet** | Implementierung nach freigegebenem Plan, Code-Review-Befund erstellen, Recherche bündeln |
| Offen, mehrdeutig, sinn-tragend, Abwägung | „Grün/Gelb" — Integration, System | **Opus** | Architekturentscheidung, Scope-Klärung, Urteil über Subagenten-Befunde, Prämissen-Änderung |
| Deontische Grenze, kein Abwägen | (Veto-Ebene) | **Maschine/Gate** | Rote Tests, Architektur-Bruch, Security — niemand „stimmt ab" |

**Die Graves-Pointe:** Tiering ist nicht „billig vs. teuer", sondern **Passung von
Komplexität zu Bewältigungs-Kapazität**. Ein Lookup an Opus zu geben ist genauso ein
Fehlgriff wie eine Architekturentscheidung an Haiku. Die Organisation *staffelt* bewusst —
und macht die Staffelung explizit (die „Stellenbesetzung" aus Luhmanns Prämisse 3). Das
spart nicht nur Token, es hält **Urteil dort, wo Urteil nötig ist** und automatisiert dort,
wo es schadet, ein Urteil zu erfinden.

---

## 4. Die Synthese — wie die drei Linsen zusammenwirken

Die drei Theorien sind keine Konkurrenz, sondern drei Schnitte durch dasselbe System:

- **Luhmann** liefert die **Bauteile**: Programme, Kommunikationswege, Stellen, Kultur —
  und die Einsicht, dass Gedächtnis in Artefakten/Regeln liegen muss, nicht im Agenten.
- **Wilber** liefert die **Vollständigkeitsprüfung**: Habe ich alle vier Quadranten
  abgesichert — Code (UR), Prozess (LR), Kultur (LL), Urteil (UL)? Lücken in einem
  Quadranten kippen das Ganze.
- **Graves** liefert die **Zuweisungsregel**: Welche Komplexität gehört auf welche Stelle/
  welches Tier — und was bleibt bewusst un-automatisiert.

Zusammen ergibt das eine **Aufbauorganisation** (wer/welche Rolle/welches Tier) und eine
**Ablauforganisation** (welche Events in welcher Reihenfolge, welche davon als Hook
vollzogen).

---

## 5. Gates über Dimensionen — das messbare Rückgrat

Das Herzstück für den Artikel: **In jeder relevanten Dimension gibt es ein eigenes,
messbares Gate.** Kein einzelnes Gate sichert alles ab (Wilber: vier Quadranten). Gates
*entscheiden nicht* — sie *beschränken*. Bricht ein Gate, ist das ein **Signal, kein
Fehler** (Luhmann: Konditionalprogramm feuert).

| Dimension (Quadrant) | Gate / Mechanismus | Frage, die es beantwortet | Vollzug |
|---|---|---|---|
| **Technische Korrektheit** (UR) | `pytest`, Unit-Tests, Coverage-Gate ≥ 90 % | Funktioniert der Code, ist er gedeckt? | Maschine (CI + lokal) |
| **Fachliche Korrektheit** (UR/LR) | Rule-Conformance-Catalog mit **Akzeptanzkriterien** (Klasse A/B/C) | Stimmt es mit den echten Spielregeln überein? | Tests gegen Akzeptanz-Ledger |
| **Architektur-Integrität** (LR) | `tests/architecture/` — 6 Invarianten (z. B. „keine Fraktions-Logik in src/", „YAML nur über Loader") | Bleibt die Struktur sauber? | Wächter-Tests, brechen den Build |
| **Doku-/Artefakt-Pflege** (LR) | Doku-Gates (Zeilen-Limit für Startprompt, Akzeptanz-/Doku-Tests), „ein kanonischer Ort je Frage" | Driftet die Doku von der Realität ab? | Tests + Artefakt-Landkarte |
| **Schulden-Transparenz** (LR) | Debt-Scoreboard (Ratchet — darf nur schrumpfen) | Wächst die technische/fachliche Schuld? | Hook nach jedem Testlauf |
| **Freigabe / Sinn** (UL) | Freigabe-Gate: Edit/Write blockiert bis Mensch physisch freigibt | Will der Mensch das wirklich so? | Hook (`freigabe_gate.py`) |
| **Kontext-Ökonomie** (LR) | Token-Korridor < 150 k, Wind-down bei ~135 k | Bleibt die Session arbeitsfähig/bezahlbar? | Hook (`session_context.py`) |
| **Verhaltensbruch** (Veto) | „Vorher grüne Tests werden rot → STOP + Mensch fragen" | Wurde unabsichtlich Verhalten gebrochen? | Kultur-Regel + Mensch |

**Das Ratchet-Prinzip** ist artikel-würdig: Schuld-Ledger dürfen nur *schrumpfen*. Eine
Invariante bewusst zu ändern heißt: **Wächter UND Doku gemeinsam** anpassen — nie still
aufweichen. Das ist Luhmanns „Entscheidung über Prämissen" als laufender Mechanismus.

---

## 6. Hooks — Konditionalprogramme, die die Harness *vollzieht*

Der entscheidende Trick gegen die Diskontinuität: **Alles, was sich als
Konditionalprogramm formulieren lässt, überlässt man nicht der Erinnerung des Agenten,
sondern lässt es die Harness (das Laufzeit-System) automatisch feuern.** Das ist die
Brücke von Luhmanns Theorie zur Mechanik.

| Hook | Event | Was er erzwingt |
|---|---|---|
| `freigabe_gate.py` | vor jedem Edit/Write | Blockiert Schreibzugriff, bis der Mensch physisch freigibt; jede Session neu scharf |
| `session_context.py` | bei jeder Nutzer-Eingabe | Zeigt Live-Kontextstand, eskaliert bei 120 k (Warnung) / 135 k (Stopp) |
| `test_report_reminder.py` | nach jedem `pytest` | Injiziert die Pflicht, Token-Report/Peak-Kontext zu teilen |
| Debt-Scoreboard | nach jedem `pytest` | Schreibt den Schuldenstand fort (Ratchet) |

**Pointe:** Ein Mensch (oder ein Agent) „vergisst" Prozessschritte. Ein Hook nicht. Indem
man Disziplin *aus dem Bewusstsein in die Mechanik verlagert*, wird die Organisation
robust gegen ihre eigene Diskontinuität. Was Urteil braucht, bleibt beim Menschen/Opus;
was Wiederholung ist, wird vollzogen.

---

## 7. Die Ablauforganisation — der Event-Zyklus

```
1 · Planning           → next_session.md + Ziel lesen (Wiederanlauf aus Artefakt)
2 · Plan-Freigabe 🔧    → Plan + Dateien + Token-Schätzung + Modus-Label; Mensch gibt frei
3 · Sprint             → Opus führt aus ODER routet an Sonnet/Haiku-Subagenten
4 · DoD-Review         → 7-Punkte-Check (Regelkonform · Generisch · Tests · Architektur ·
                          Clean Code · UI manuell · Artefakte aktuell)
5 · Review→Retro→Abschluss → Sessionstand, vorausschauender Fragenkatalog, Commit, Clear
  ↑ Kontext-Korridor 🔧 → bei ~135 k erzwungenes, geordnetes Wind-down
7 · Refinement         → rohe Ideen (Fotos) → Inbox → gemeinsames Verständnis → Backlog
```

🔧 = als Hook vollzogen. **Entscheidungsmodi** strukturieren, *wer* entscheidet:
- **Gate/Konditional** — das Programm entscheidet, niemand stimmt ab.
- **Konsent** — Orchestrator schlägt vor, Gates + Mensch haben Einspruch (bounded).
- **Konsens** — Mensch + Orchestrator gemeinsam (mehrdeutig, sinn-tragend).
- **Veto** — jeder einzelne Wächter kann alles stoppen (deontische Grenze).

---

## 8. Die Aufbauorganisation — Rollen & Tier

```
Stakeholder (Mensch) ◄──── Plan-Freigabe / Eskalation ────┐
        │                                                 │
        ▼                                                 │
Orchestrator (Opus) ─────────── eskaliert ────────────────┘
   = Scrum-Master + Tech-Lead + Kontext-Hüter; "hier lebt der Sinn"
        │              │                │
        ▼              ▼                ▼
   Executor        Regel-Recherche   Auditor
   (Sonnet,        (Haiku Lookup /   (Sonnet liefert
    fixer Plan)     Sonnet Synthese)  Befund → Opus urteilt)
        │
        ▼
   Increment = die App (Arbiter)
        ▲
        │ beschränkt (entscheidet nicht)
   Gate-Wächter (pytest · Architektur · Coverage · Debt) — Automatik
```

**Kanal-Regel:** Subagenten reden **nie direkt** mit dem Menschen. Der Orchestrator ist der
einzige Kommunikationskanal — er mediiert, bündelt und reviewt. „Subagent-grün" ≠
„verdrahtet": der Orchestrator prüft Wiring + Architektur-Heimat, nicht nur die Testfarbe.

---

## 9. Das Increment — die App als greifbarer Beweis

Die ganze Organisation produziert ein konkretes Artefakt: **Arbiter**, ein Streamlit-
Spielbegleiter für Warhammer 40.000 9. Edition (Python). Er rechnet Angriffssequenzen,
erzwingt Spielregeln aus YAML-Daten (keine Fraktions-Logik im Code — „Generic src" als
Architektur-Invariante), zeigt Würfel-Wahrscheinlichkeiten und Modifikatoren. Über 1000
Tests, ~93 % Coverage, mehrere messbare Gates. Das Increment ist der Realitäts-Check der
Organisation: Theorie, die nicht in lauffähigem, getestetem Code landet, zählt nicht.

---

## 10. Die Take-aways (für den Schluss des Artikels)

1. **Baue die Organisation, nicht (nur) den Prompt.** Rollen, Wege, Gates, Gedächtnis,
   Kultur — explizit und versioniert.
2. **Verlagere Gedächtnis in Artefakte und Hooks.** Der Agent ist diskontinuierlich;
   verlasse dich nie auf seine Erinnerung.
3. **Ein Gate je Dimension** (Wilbers Quadranten) — Code, Fachlichkeit, Architektur, Doku,
   Sinn/Freigabe. Kein Gate sichert alles.
4. **Staffle Komplexität auf Tiers** (Graves) — und automatisiere bewusst *nicht* das
   Urteil (Wilbers UL bleibt beim Menschen/Opus).
5. **Konditionalprogramme vollziehen, Zweckprogramme verhandeln** (Luhmann) — die
   Trennlinie zwischen Hook und Mensch.

---

## 11. Bild-Vorschlag für den LinkedIn-Artikel

**Motiv:** Ein integriertes Schaubild, das die drei Linsen über einem Maschinenraum
zusammenführt — z. B. eine stilisierte Wilber-Vier-Quadranten-Matrix als Grundfläche, auf
der eine Graves-Spirale (vier Stufen Haiku→Sonnet→Opus→Mensch) aufsteigt, verbunden durch
Luhmann'sche „Kommunikations-Pfeile" (Plan-Freigabe, Eskalation, Befund). Am unteren Rand
kleine „Gate-Symbole" (Schloss = Freigabe, Häkchen = Test, Waage = Architektur).
Farbwelt: technisch-ruhig (Dunkelblau/Anthrazit) mit drei Akzentfarben für die drei
Theorie-Linsen. Stil: editorial / Infografik, kein Stockfoto.

**Alternativ-Prompt (knapp):** „Editorial infographic, dark slate background, three subtle
accent colors. A four-quadrant grid (Wilber AQAL) as the base plane; an ascending spiral of
four nodes labeled Haiku → Sonnet → Opus → Human (Spiral Dynamics tiers); thin directed
arrows between nodes labeled 'approval', 'escalation', 'finding' (Luhmann communication);
small lock / checkmark / scales icons along the bottom edge representing gates. Clean,
modern, no people, no logos."

---

*Quellen im Repo: `docs/governance/operating_model.md` (Operating-Model), `CLAUDE.md`
(Kultur/Prinzipien), `docs/spec/architecture_invariants.md` (Gates/Invarianten),
`docs/governance/decisions/` (ADRs).*
