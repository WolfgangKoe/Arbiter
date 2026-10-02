# Vorgehen: Neuaufbau Arbiter

Stand 2026-10-02 · Stakeholder: Wolfgang · Übergabedokument zwischen den Sitzungen, bis die
Zielstruktur steht. Danach wandert der Inhalt an seine endgültigen Orte, und die Datei wird gelöscht.

## Einstieg für die nächste Sitzung

- **Stand:** Schritte 1–6 erledigt; Schritt 7 begonnen: Phasenmodell und Kontext-/Harness-Regeln
  entschieden (E38–E49), Harness-Proben gemacht (Ergebnis unten), Minimalgerüst steht:
  Root-CLAUDE.md, `domaene/ziel.md`, `.claude/settings.json` (E44, E45), Koordinator,
  Organisationsentwickler, Regelumsetzer, Hooks in `prozess/pruefungen/` (Stand,
  Schreibgrenze, Bash-Positivliste, je mit Scheiter-Tests). **Nächste Aufgabe:** Eine neue
  Sitzung startet als Koordinator; er führt den Rest von Schritt 7 mit den Rollen aus.
  Offen beim Stakeholder: fachlicher Override im Ziel (Empfehlung: erlaubt, protokolliert).
- **Arbeitsweise mit dem Stakeholder:** Schritt für Schritt; erst im Gespräch entwerfen, dann nach
  Freigabe schreiben; Rückfragen mit Empfehlung; starke Kritik ausdrücklich erwünscht.
- **Repo:** github.com/WolfgangKoe/Arbiter (öffentlich, main; der alte Prototyp heißt jetzt
  Arbiter-old). CLI 2.1.287 wie VS Code. Qualität des Koordinators ohne Claude-Code-Systemprompt
  im Betrieb beobachten (E45). Auto-Memory ist aus (E48).
- **Altbestand nur lesen:** `Arbiter/`, `ArbiterMap/` (Migrationsquelle, E8).

## Ziele

1. **Domänenziel:** Arbiter fertig entwickeln, einen Spielbegleiter für Warhammer 40.000, 9. Edition.
   Vision und Scope stehen.
2. **Organisationsziel:** ein Agentensystem mit Aufbau- und Ablauforganisation, das Ziel 1 erreicht,
   hohe technische Qualität sichert (lesbarer Code, SOLID, Tests auf allen Ebenen) und Schulden
   konsequent eindämmt.

## Ausgangslage

`Arbiter/` (Streamlit) und `ArbiterMap/` (Flask) sind Prototypen, nur noch Quelle für die Migration.

- **Technik:** toter, aber getesteter Code mit fachlichem Fehler (Feel No Pain in
  `combat.resolve_attack`); Fachregeln im UI-Code, aus der Coverage ausgenommen; Attackenabfolge in
  `uiLayout/_common.py` (4.402 Zeilen); mehrfache Parser; Dicts statt Domänentypen. Positivbeispiel:
  `ArbiterMap/backend/app/domain/rule_checks.py`.
- **Domäne:** kein Glossar und kein explizites Domänenmodell; „Spieler“ und „Fraktion“ verwechselt;
  Fachbegriffe in Kommentaren statt im Code; Lücken werden plausibel gefüllt.
- **Prozess:** Prozesshistorie im Code (ArbiterMap rund 40 % Prosa je Datei); Regeln ohne
  Mechanismus wirken nicht; die Organisation ist größer als das Produkt (14k Zeilen Produkt, 12k
  Harness, 11k Prozess-Markdown); Items bis 358 Zeilen; keine fachlichen Akzeptanztests.

## Leitbild

- Die Kontextstruktur bildet die drei Perspektiven mit je drei Flughöhen ab:

  | | oben | Mitte | konkret |
  |---|---|---|---|
  | **Domäne** | Ziel | Etappenziele, Anforderungen | Items, Mockups, Glossar |
  | **Prozess** | Entscheidungsprämissen | Rollen, Abläufe, DoR/DoD | Regeln, Prüfmechanismen |
  | **Technik** | Technologie | Architektur | Code, Tests |

- Trennung statt Vermischung, jede Aussage genau einmal, schlanke verlinkte Beziehungen.
- Fachsprache = Codesprache = Deutsch. Ein Begriff aus der Anforderung steht wörtlich im Code.
- Der Kontext wächst mit dem Produkt, nicht mit Historie. Git ist das Archiv.
- Eindämmung ist Aufgabe des Prozesses und läuft automatisch ohne Tokenkosten, nicht als Text.

## Entscheidungen

**Repo und Struktur**
- **E1** Ein neues Repo, später „Arbiter“. Python/Flask, Frontend und Backend getrennt.
- **E8** Das Repo ist `Arbiter_Structure/`; Altordner bis zum Ende der Migration in `.gitignore`.
- **E2** Je Perspektive ein Ordner. Subagenten schreiben nur dort und lesen alles. Durchgesetzt durch
  eine CLAUDE.md je Ordner und harte Hooks.
- **E10** CLAUDE.md, `.claude/` und die Prüfkonfiguration gehören zum Prozess, `pyproject.toml` zur
  Technik.
- **E6** Mockups gehören zur Domäne, Bildschirmtests zur Technik.
- **E12** Bezeichner deutsch mit Umlauten, Dateinamen in ASCII.
- **E13** Regeltexte und Katalogdaten sind Nachschlagewerk der Domäne. Haiku behält seine Rolle
  (Nachschlagen, Belegprüfung).

**Rollen und Entscheidung**
- **E3** Je Perspektive ausführende und prüfende Rollen. Prüfende Rollen kritisieren die anderen
  Perspektiven stark; Kritik blockiert nicht automatisch.
- **E4/E15** Der Koordinator gehört zum Prozess, hält das System am Laufen, ist dein Hauptkontakt,
  schreibt keine Dateien und committet.
- **E5** Der Stakeholder ist für alle Ebenen zuständig und entscheidet, wenn keine Regel
  entscheidet. Eine wiederholte Entscheidung wird zur Prämisse.
- **E9** `handoff/` ist an den Stakeholder gerichtet; dort laufen Dreiklang und Diskussionen
  (E33), der Stakeholder kommentiert. Die spätere Prozessrolle **Moderation** liest alle
  Diskussionen, macht Vorschläge und schreibt nur in `handoff/`.
- **E16** Den Planungsmodus des Harness verwenden wir nicht. Planende und prüfende Rollen sind durch
  ihre Werkzeugliste und Schreib-Hooks begrenzt und schreiben nur ihr eigenes Dokument.
- **E19** Der Skill `improve` (nur lesend, schreibt Umsetzungspläne) wird gezielt eingesetzt.

**Arbeitsweise**
- **E7** Eine knappe CLAUDE.md im Wurzelordner legt die Arbeitsweise fest.
- **E21** Dreiklang mit abgeleitetem Stand statt Briefing (siehe Ablauf).
- **E22** ATDD ist Standard für Fachlogik (siehe Ablauf).
- **E11/E17** Der Harness wird aktiv genutzt. Wer Regeln umsetzt, prüft zuerst die Bordmittel. Eine
  wiederkehrende Aufgabe prüft Harness-Neuerungen und baut ersetzbare eigene Mechanismen zurück.
- **E18** Das Dashboard aus ArbiterMap (`steering/metrics/process_dashboard.html`) wird übernommen
  und neu verdrahtet; Budget- und Aufsichtswirkung (`harness/hooks/subagent_budget.py`,
  `subagent_oversight.py`) bleibt erhalten, wenn möglich mit Bordmitteln.

**Qualität und Prüfung**
- **E14** Jede Prozessregel verweist auf ihren Mechanismus (Berechtigung, Hook, Test, Linter) wie ein
  Kriterium auf seinen Test. Eine Regel ohne Mechanismus ist als „nur Text“ gekennzeichnet.
- **E20** Jede Kennzahl hat Bedeutung, Schwelle und Reaktion (wer handelt). SonarLint (Sicht des
  Stakeholders) und die Werkzeuge der Agenten verfolgen dieselben Ziele mit abgestimmten Schwellen.
- **E23** Prozess-Prämissen werden nach Wilber (AQAL) gegliedert und mit Luhmanns Begriffen ergänzt
  (siehe Landkarte).

**Rollen (Schritt 4)**
- **E24** Wir starten mit dem Nötigsten: Jeder Dreiklang-Zyklus liefert ein Inkrement; Rollen,
  Regeln und Skills kommen erst hinzu, wenn ein Bedarf beobachtet wird.
- **E25** Startbesetzung: Domäne: Planer, Anforderungsautor, Fachkritiker (Opus),
  Regel-Nachschlager (Haiku) · Technik: Architekt, Reviewer (Opus), Testautor, Implementierer
  (Sonnet) · Prozess: Organisationsentwickler (Opus), Regelumsetzer (Sonnet), Koordinator. Später, mit Auslöser: UX (erstes UI-Item), Moderation (mehr
  als 5 offene Anliegen), Belegprüfer (erste falsche Behauptung), Prozesskritiker (fehlende
  Prozesskritik). Planer und Anforderungsautor bleiben getrennt.
- **E26** Ein Auslösezähler (Hooks) gilt gleichermaßen für Regeln, Rollen und Skills; was über
  mehrere Zyklen nie auslöst, kommt in die Retro.
- **E27** Testautor auf Sonnet; Wechsel auf Opus, wenn Fachkritik oder Mutationstests wiederholt
  fehlende Fälle zeigen.
- **E28** Eine eigene UX-Rolle schreibt einbaufähige Mockups: statisches HTML mit dem echten CSS
  des Projekts, keine JS-Logik, nur Inhalte, die sich auf Kriterien oder Katalogdaten zurückführen
  lassen, ein Mockup je Anforderung, gelöscht nach dem Einbau.
- **E29** Der Koordinator schreibt nur im Chat und committet: Write/Edit gesperrt, Bash nur über
  eine Positivliste. Zuarbeitende Rollen (Haiku) startet die Rolle, die das Ergebnis braucht; ein
  Hook auf das Agent-Werkzeug erlaubt nur festgelegte Typen.
- **E30** Agentendefinitionen sagen, wer eine Rolle ist und was sie darf (höchstens 40 Zeilen).
  Wie wiederkehrende Arbeit gemacht wird, steht in Skills mit genau einem echten Beispiel und einem
  kurzen Gegenbeispiel. Was sich berechnen lässt, wird ein Skript. Kandidaten:
  `anliegen-schreiben`, `akzeptanztest-schreiben`, `anforderung-schreiben`, `regel-nachschlagen`
  (Haiku, `context: fork`), `improve`. Bordmittel-Fragen beantwortet der eingebaute Agent
  `claude-code-guide`.
- **E31** Das Design-System gehört der Technik, die Domäne kritisiert es, der Prozess verhindert
  tote Gestaltung. Eine lebende Komponentenseite (HTML mit dem echten CSS) ist Doku, Vorlage für die
  UX-Rolle und Ziel eines Bildschirmtests. Mockups verwenden nur vorhandene Komponenten (per Skript
  geprüft); Neues geht als Anliegen an die Technik. Tot ist eine Komponente, die in keinem Template
  vorkommt. Messbare Gestaltungsregeln (Kontrast, Mindestgrößen) werden Prüfmechanismen.
- **E32** `doku/` im Wurzelordner ist eine Dokumentation für Menschen, nicht für Agenten (keine
  CLAUDE.md verweist darauf): grafisch, kurz, präzise. Sie zeigt nur, was sich selten ändert
  (Drei-Perspektiven-Modell, Landkarte, Rollen, Dreiklang, ATDD) und verlinkt statt zu wiederholen.
  Rollentabelle und Ordnerbaum erzeugt ein Skript aus `.claude/agents/` und dem Dateisystem.
  Pflege: Organisationsentwickler, geprüft in der Retro.
- **E33** Eine Datei je Diskussion in `handoff/anliegen/`. Sie entsteht nur bei einem Befund (ohne
  Befund keine Datei). Anlegen dürfen alle Rollen außer dem Koordinator und den Haiku-Zuarbeitern.
  Wer das kritisierte Artefakt gebaut hat, nimmt in derselben Datei Stellung; nimmt er an, reicht
  ein Kommentar, dann setzt er um. Der Kritiker prüft nach: in Ordnung → er löscht die Datei (git
  bewahrt sie); sonst nächste Runde. Nach höchstens 3 Runden: Eskalation an den Stakeholder oder
  Hebung auf eine höhere Flughöhe (Test → Kriterium → Anforderung, Code → Architektur). Der
  Koordinator liest keine Inhalte; ein Hook meldet ihm aus dem Dateizustand, wer als Nächstes dran
  ist. Kennzahlen (Anzahl, Runden, Eskalationen, Perspektivenpaare) kommen aus der git-Historie.
- **E34** Bemängelt die Fachkritik einen roten Akzeptanztest („trifft das Kriterium nicht“), geht
  nur dieser Test nicht in die Umsetzung, bis die Diskussion geklärt ist; widerspricht der
  Testautor, wird sie zum Kriterium gehoben. Alles andere läuft weiter.
- **E35** Fachbegriffe in Kriterien stehen *kursiv*; ein Skript prüft sie per Wortanfang gegen das
  Glossar.

**Prüfwerkzeuge (Schritt 6)**
- **E36** Kommentare: keine Quote, sondern eine Positivliste, jeweils einzeilig: `# Regel: <Fundstelle>`
  (nicht offensichtlicher Regel-Sonderfall) und `# Warum: …` (nicht offensichtliche technische
  Entscheidung). Docstrings höchstens einzeilig. TODO, FIXME und Prozessverweise sind verboten; offene
  Punkte werden Diskussion oder Item. Geprüft per Skript bzw. semgrep.
- **E37** Werkzeugsatz der Agenten: ruff (Stil, ARG, PLR2004, PLR0913, FBT, ERA) · mypy oder
  pyright strikt · import-linter (Architekturverträge) · complexipy (kognitive Komplexität 15) ·
  vulture (nur Produktcode) · Duplikaterkennung (jscpd oder pylint) · semgrep (eigene Konventionen)
  · cSpell mit deutschem Wörterbuch aus dem Glossar · eslint/stylelint fürs Frontend. SonarLint ist
  die Sicht des Stakeholders; die Sperre der Agenten ist mindestens so streng. Mutationstests ab
  Schritt 8. Nicht verwendet: radon-Wartbarkeitsindex, ruff-McCabe. Später denkbar: wily (Trends),
  deptry.

**Phasen (Schritt 7)**
- **E38** Ein Zyklus hat drei Phasen in fester Reihenfolge: Domäne → Technik → Prozess → Domäne.
  In jeder Phase ist genau eine Perspektive operativ; die anderen kritisieren über
  `handoff/anliegen/` und schreiben nicht in ihren Ordner. Eine Phase ohne Auftrag wird
  übersprungen (der Hook leitet das aus dem Dateizustand ab). Reihenfolge in Texten: D, T, P.
- **E39** Kritik an Zwischenstationen, nicht nur am Phasenende: in der Technikphase nach den roten
  Akzeptanztests (E34) und nach dem Code (fachliche Abnahme). Prozesskritik ist überwiegend Skript
  (DoR, Format, Maße, Verlinkung); ein Prozess-Agent wird nur für Urteile gestartet.
- **E40** Das Schreibrecht hängt an der Perspektive, die Phase regelt nur, wer neue Arbeit beginnt.
  Auf ein Anliegen antwortet der Besitzer jederzeit in seinem Ordner.
- **E41** Jede Perspektive hat Backlog und Items mit harten Kriterien. Refactoring- und
  Prozess-Items entstehen nur aus einem Befund (Kennzahl über Schwelle, Anliegen, Auslösezähler)
  und nennen eine prüfbare Erledigt-Bedingung; Refactoring zusätzlich „Verhalten unverändert“
  (Akzeptanztests grün), Prozess-Items Mechanismus und Scheiter-Test. Löschen zählt wie
  Hinzufügen. Nur Anforderungen wachsen mit dem Code (Spiegel) und liefern die Grundlage für Befunde.
- **E42** Der Stakeholder gibt am Ende der Domänenphase (Plan) und der Prozessphase
  (Regeländerungen) frei. Die Technikphase endet mechanisch (DoD 1–5) und mit der fachlichen Abnahme.

**Kontext und Harness (Schritt 7)**
- **E43** Ladeschichten: (0) immer: Root-CLAUDE.md mit `@domaene/ziel.md` — Ziel, Technik-Rahmen in
  wenigen Sätzen, Arbeitsweise, Ordnerkarte; kein SOLID · (1) je Rolle: Agentendefinition und
  `skills:` · (2) je Ort: Ordner-CLAUDE.md, lädt beim Lesen im Ordner; sie dient Lesern („was liegt
  hier“), Schreibkonventionen (etwa SOLID-Verträge) stehen in den Skills der schreibenden Rollen ·
  (3) je Auftrag: `SubagentStart`-Hook gibt Zyklus, Item und Pfade mit, aus dem Dateizustand · (4)
  bei Bedarf: grep, Read, Skill, Haiku. CLAUDE.md ist Kontext, keine Durchsetzung (dafür Hooks).
- **E44** Der Harness wird bewusst begrenzt: an ist nur, was entschieden ist; was fehlt, wird bemerkt
  und bewusst eingeschaltet. **An:** Read, Edit, Write, Bash, ToolSearch, AskUserQuestion
  (Koordinator), Agent (nur Koordinator, Positivliste), SendMessage, Monitor, TaskStop, WebSearch,
  WebFetch, `claude-code-guide`; je Rolle `tools:` als Positivliste und `disallowedTools: mcp__*`.
  **Bei Bedarf:** Browser (Claude in Chrome per `@browser`, nicht dauerhaft). **Nur für den
  Stakeholder** (`skillOverrides: user-invocable-only`; `/code-review` zusätzlich Werkzeug des
  Reviewers, E49): `/code-review`, `/simplify`, `/verify`,
  `/run`, `/loop`, `/debug`, `/doctor`, `/update-config`, `/fewer-permission-prompts`. **Aus:**
  claude.ai-Connectoren (`disableClaudeAiConnectors`), Auto-Memory, synchronisierte
  claude.ai-Skills und -Plugins (`settings.local.json`), übrige mitgelieferte Skills (dataviz,
  artifact-\*, design, slides, claude-api, batch, workflow-authoring, plugin-authoring), Agenten
  general-purpose, Explore, Plan, statusline-setup, fork, Planmodus, Artifact, Cron,
  Git-Anleitung samt Git-Status. Beleg ArbiterMap (668 Protokolle): general-purpose verdeckte eine
  Rollenlücke (95 Starts für Briefe, Retro, Briefing); Skill, MCP und Browser wurden nie benutzt.
- **E45** Der Koordinator läuft als `"agent": "koordinator"` (eigener Systemprompt statt dem von
  Claude Code, Werkzeug- und Agentenliste nativ). Eingeschaltet erst am Ende von Schritt 7; danach
  läuft auch Strukturarbeit über den Koordinator, Ausnahmen per `claude --agent <rolle>`.
- **E46** Maße in Zeichen, nicht Zeilen. Statische Texte haben ein Höchstmaß, lebende Artefakte
  Höchst- und Kürzungsmaß mit Hysterese: pre-commit sperrt über H, die Sperre erzeugt einen Befund
  und daraus ein Item bis ≤ K; bis dahin darf die Datei nicht wachsen. Wachsen darf nur der
  Spiegel; auch dort heißt Kürzen aufteilen, weil Read die ganze Datei lädt. Wichtigstes Maß ist
  die Grundlast je Rolle, danach die Summe der Agenten- und Skillbeschreibungen.
- **E47** Messung mit Bedeutung: Grundlast je Rolle per Probe (`OTEL_LOG_RAW_API_BODIES=file:<dir>`);
  Arbeitslast per `PostToolUse`-Hook als Rolle · Artefakttyp · Aktion · Zeichen („Implementierer ·
  Plan gelesen · 3.100“), Bash-Lesebefehle eingeschlossen; dazu `InstructionsLoaded` und
  `SubagentStart`. Die Zuordnung Pfad → Artefakttyp ist die Kontextlandkarte als eine Datei; ein
  unbekannter Pfad ist ein Befund. OpenTelemetry allein reicht nicht (eigene Agenten heißen dort
  „custom“).
- **E48** Auto-Memory wird abgeschaltet, sobald die Root-CLAUDE.md auf VORGEHEN.md verweist; die
  Memory-Dateien werden dann gelöscht.
- **E49** Probe an ArbiterMap-Commit 533e748 (BW-4.7, Kopie im Scratchpad): `/code-review` prüft nur
  Korrektheit, läuft im eigenen Kontext, fand keinen Fehler, aber einen ungeregelten Fall (Anliegen
  an die Domäne) → **Werkzeug des Reviewers**. `/simplify` (vier Agenten, rund 200k Token) fand
  die Belegungsregel nur beim Zurücksetzen statt beim Ziehen und Aufstellen (fehlende Anforderung),
  N×M-Datenbankabfragen, Nachbauten vorhandener Bausteine und Prozesshistorie in Kommentaren;
  8 von 12 Befunden umgesetzt, Tests grün. Es startet seine Agenten ohne Typ (general-purpose,
  E44) → **bleibt Befehl des Stakeholders**; seine vier Blickwinkel (Wiederverwendung,
  Vereinfachung, Effizienz, Flughöhe) werden Prüfliste im Reviewer-Skill.

## Kontextlandkarte

```
Arbiter_Structure/
├── CLAUDE.md · .claude/ · ruff.toml …   Prozess
├── pyproject.toml                       Technik
├── domaene/   ziel.md · etappen.md · anforderungen/<bereich>.md · backlog.md · items/ · glossar.md
│              mockups/ · daten/ (Katalog-YAML) · referenz/ (Regeltexte, nur lesen)
├── technik/   architektur.md · backlog.md · items/ (Refactoring) · arbiter/
│              tests/{akzeptanz,einheit,bildschirm,architektur}/
├── prozess/   praemissen/{ich,wir,es,system} · ablauf.md · regeln.md · kennzahlen.md · backlog.md
│              items/ · pruefungen/ · messwerte/ · dashboard/   (Rollen: system/ + .claude/agents/)
├── doku/      für Menschen: grafischer Überblick (E32)
└── handoff/   plan.md · review.md · retro.md · anliegen/<nr>-<kurz>.md
```

- **Anforderung** (dauerhaft): `### BW-4 · Zug zurücksetzen`, Zweck in ein bis zwei Sätzen,
  Kriterien `BW-4.1 …` je ein Satz, höchstens 15 Zeilen, keine Technik, keine Historie.
- **Item** (bis erledigt): Umfang (Kriterien-IDs), warum jetzt, Abhängigkeit, Link auf Anliegen;
  etwa 5 Zeilen.
- **Akzeptanztest**: eine Datei je Anforderung, mindestens ein Test je Kriterium, Name
  `test_bw_4_3_<satz>` auf Deutsch. Mehrere Fälle als benannte Parameter nach Äquivalenzklassen und
  Grenzwerten; zu wenig oder zu viel zeigen Mutationstests.
- **Anliegen** = eine Datei je Diskussion (E33): Kopf `Nr · Typ · von (Rolle, Perspektive) → an ·
  Runde n/3 · Status`, je Runde Befund, Kosten, Gegenvorschlag, Stellungnahme. Höchstens 30 Zeilen.
- **Glossar**: eine Zeile je Begriff (Begriff | englischer Regelbegriff | Code-Bezeichner |
  Definition), Zugriff per `grep`.
- **Spiegel**: `tests/einheit/` ↔ `arbiter/`, `tests/akzeptanz/` ↔ `anforderungen/`.
- **Grundschnitt** für Anforderungen, Code und Tests: `spielobjekte/` (Einheit, Modell, Armee,
  Spielstand, phasenübergreifender Zustand) · `phasen/<phase>/` · `querschnitt/` (Fähigkeiten,
  Modifikatoren) · `spielablauf/` (nur Akzeptanztests: Szenarien über mehrere Phasen).
- **Daten**: Katalog-YAML in `domaene/daten/` → Importer (Technik) → Datenbank; Spielstand nur in
  der Datenbank; die Domäne kennt Speicherung nur als Schnittstelle (Abhängigkeitsumkehr).
- **Prämissen nach Wilber, mit Luhmann**: Ich (Haltung einer Rolle) · Wir (Sprache, Kultur) · Es
  (beobachtbares Agentenverhalten) · System (Programme, Kommunikationswege, Personal = Rollen).
  Außen (Es, System) wird automatisch durchgesetzt und gemessen; innen (Ich, Wir) ist bewusst Text
  und wird beobachtet. Eine wiederholt verletzte Innen-Prämisse bekommt ein Außen-Gegenstück.
- **Jede Regel**: eine Zeile, ein Link auf den Mechanismus, ein Scheiter-Test, ein Auslösezähler.
- **Maße in Zeichen** (E46, Startwerte, nach dem Durchstich geeicht). Nur Höchstmaß (statisch oder
  je Zyklus überschrieben): Root-CLAUDE.md samt Ziel 4.000 · Ordner-CLAUDE.md 1.500 ·
  Agentendefinition 2.500 · Beschreibung eines Agenten oder Skills 150 · Anforderung 1.200 · Item
  400 · Anliegen 2.400 · Plan/Review/Retro je 4.000. Höchst-/Kürzungsmaß (lebend): Code-Modul,
  Einheits- und Akzeptanztest-Datei 12.000/8.000 (aufteilen) · `anforderungen/<bereich>.md`
  12.000/8.000 (aufteilen) · Backlog je Perspektive 3.000/2.000 (löschen) · `etappen.md`
  2.000/1.200 (Erreichtes löschen) · `architektur.md` 6.000/4.000 (verdichten) · Regeln, Prämissen,
  Kennzahlen je Datei (löschen nach Auslösezähler) · Grundlast je Rolle und Summe der
  Beschreibungen (Werte nach der Messung). Glossar ohne Gesamtmaß (grep), je Zeile 300. Anzahl
  offener Items je Perspektive und offener Anliegen begrenzt (> 5 Anliegen → Moderation).

**Automatische Prüfungen ohne Tokenkosten** (Details in Schritt 6): Format der Anforderungen ·
Kriterium ↔ Akzeptanztest · Glossar ↔ Code · Spiegel · Regel ↔ Mechanismus (keine verwaisten Hooks)
· Scheiter-Test je Mechanismus · Höchstmaße · Schreibgrenzen. SonarLint prüft den Code, auch den
der Mechanismen.

## Ablauf

**Dreiklang (E21, E38):** Domänenphase (Plan, Anforderungen, Items) → Technikphase
(Akzeptanztests, Code, Refactoring-Items, Review) → Prozessphase (Retro, Prozess-Items) →
Domänenphase. Je Phase ist eine Perspektive operativ, die anderen kritisieren (E39, E40).
- Die drei Artefakte liegen in `handoff/`, tragen die Zyklusnummer und werden je Zyklus
  überschrieben. Jede Rolle schreibt nur ihr eigenes.
- Ein `SessionStart`-Hook leitet den Stand aus den Artefakten ab („Review 12 da, Retro 12 fehlt →
  Organisationsentwicklung“) und gibt dem Koordinator diese eine Zeile mit. Kein Briefing.
- Der Plan bekommt vor deiner Freigabe Kritik aus Technik und Prozess. Die fachliche Abnahme kommt
  aus Akzeptanztests und fachlicher Kritik, gemessen an Zielen, Etappen und Kriterien.

**ATDD (E22):**
1. Domäne: Anforderung mit prüfbaren Kriterien, Begriffe im Glossar (DoR).
2. Testautor (Technik): Akzeptanztests je Kriterium, Fälle vollständig, Tests rot.
3. Kritik vor der Umsetzung: Domäne prüft, ob der Test das Kriterium trifft; Architektur prüft die
   Schnittstelle.
4. Implementierer (Technik): Auftrag „mache Test X grün“; Unit-Tests während der Umsetzung, wo die
   Logik nicht trivial ist; der Akzeptanztest bleibt für ihn gesperrt.
5. Review und Retro.

Ausnahmen: UI (Mockup zuerst, Bildschirmtest danach), technisches Neuland (Wegwerf-Versuch, dann
Test). Akzeptanztests laufen überwiegend gegen Domäne und Services.

## Beziehungen (Schritt 5)

**Grundregel:** Kritik ändert nie direkt ein fremdes Artefakt, sie wird eine Diskussion (E33). Der
Besitzer des Artefakts entscheidet zuerst; verletzt die Übernahme keine Prämisse, ändert er selbst.
Der Stakeholder entscheidet nach drei Runden oder wenn eine Prämisse berührt ist. Mechanismen
blockieren hart; Kritik blockiert nicht (Ausnahme E34).

| Richtung | Typische Kritik | Wer (Perspektive · Art) | automatisch |
|---|---|---|---|
| Domäne → Technik | Test trifft Kriterium? Fälle? Namen = Glossar? Ziel/Etappe erfüllt? Design-System? | Fachkritiker (Domäne · prüfend) | Kriterium ↔ Test, Glossar ↔ Code |
| Technik → Domäne | Kriterium nicht prüfbar/widersprüchlich, Fall ungeregelt, Kosten und Alternative | Testautor, Architekt (Technik · ausführend), Reviewer (Technik · prüfend) | Format der Anforderung |
| Domäne → Prozess | Regel oder Höchstmaß behindert die Fachlichkeit | Fachkritiker (Domäne · prüfend) | – |
| Prozess → Domäne | unklare Kriterien, zu große Items, Muster | Organisationsentwickler (Prozess · ausführend) | DoR-Prüfungen |
| Technik → Prozess | Regel schränkt unnötig ein, Fehlalarm, Bordmittel besser | jede Technikrolle (Technik) | Auslösezähler |
| Prozess → Technik | Korrekturschleifen, Schulden, Verstöße | Organisationsentwickler, Regelumsetzer (Prozess · ausführend) | alle Prüfmechanismen |

Der Prozess hat zum Start keine prüfende Rolle; das tragen die automatischen Prüfungen und die
Retro. Auslöser für den Prozesskritiker: Prozesskritik fehlt, oder der Organisationsentwickler
verteidigt wiederholt eigene Regeln.

**DoR** (Item bereit für die Technik), außer dem letzten Punkt per Skript: Format und Höchstmaß,
Kriterien-IDs existieren · keine vagen Wörter (Wortliste) · kursive Fachbegriffe stehen im Glossar
(E35) · regelbasierte Kriterien nennen ihre Fundstelle · Abhängigkeiten erledigt, keine offene
Diskussion zum Item · bei UI: Mockup aus vorhandenen Komponenten · fachliche Vollständigkeit ist
Urteil und zeigt sich spätestens an den roten Tests.

**DoD** (Item fertig), Punkte 1–5 per pre-commit, sodass der Koordinator nichts Unfertiges committen
kann: (1) Akzeptanz-, Gesamt- und Architekturtests grün · (2) Prüfmechanismen grün (ruff, toter Code,
Komplexität, Kommentaranteil, Spiegel, Glossar ↔ Code, Höchstmaße, Rückverfolgung) · (3)
Mutationsschwelle der geänderten Domänenmodule, sobald eingeführt · (4) bei UI: Bildschirmtest grün,
Mockup gelöscht · (5) Item gelöscht, die Anforderung beschreibt das gebaute Verhalten · (6) Review
geschrieben, Fachkritik hat gegen Ziel, Etappe und Kriterien abgenommen (Urteil).

DoR und DoD stehen später in `prozess/ablauf.md`, jeder Punkt mit Link auf seinen Mechanismus.

## Ergebnis der Werkzeugprobe (Schritt 6, an `abilityEngine.py`)

- SonarLint (installiert: SonarQube for IDE 6.0.1) meldet 2 Befunde: kognitive Komplexität 17 in
  `check_conditions`, unbenutzter Parameter `phase`. 54 weitere Meldungen kommen von cSpell
  (englisches Wörterbuch), 1 von Pylance.
- Die Werkzeuge zählen unterschiedlich (complexipy 20 statt Sonar 17; eine Funktion sieht nur
  complexipy). Regel: Die Sperre der Agenten ist mindestens so streng wie die Sicht des
  Stakeholders.
- Linter-Befunde zeigen Lücken im Domänenmodell an: magische `5` (Schlachtrunden), Ja/Nein-Schalter
  `use_melee` (fehlender Begriff *Angriffsart*).
- Toter Code bleibt nur durch Tests am Leben: vulture über `src/` findet `resolve_attack`, über
  `src/` und `tests/` nichts. Regel: Die Suche nach totem Code läuft nur über den Produktcode.
- Der Wartbarkeitsindex (radon „A“) ist ohne Aussage und wird nicht verwendet.
- Vorgeschlagener Werkzeugsatz: ruff (Stil, ARG, PLR2004, PLR0913, FBT, ERA) · complexipy
  (Schwelle 15) · vulture (nur Produktcode, Ausnahmeliste) · eigenes Skript für den Kommentaranteil
  · cSpell mit einem Wörterbuch aus dem Glossar (deutsch) · SonarLint als Sicht des Stakeholders.
  Offen: Mutationstests, Kontrast/Design, Schwelle für den Kommentaranteil.

## Harness-Fakten (geprüft 2026-10-01, code.claude.com/docs: hooks, sub-agents)

- Hooks können in der Agentendefinition stehen und gelten nur für diesen Subagenten; die
  Hook-Eingabe enthält `agent_type` (Name) und `agent_id` (fehlt beim Koordinator).
- Schreibpfade pro Subagent gibt es nicht als Bordmittel: Write/Edit per `PreToolUse`-Hook über
  `tool_input.file_path` sperren; Bash per Nachkontrolle (`git status` bei `SubagentStop`).
- `permissionMode: plan` greift nicht, wenn die Hauptsitzung in `acceptEdits`, `auto` oder
  `bypassPermissions` läuft. Darum begrenzen wir über Werkzeuglisten.
- Nachgeprüft 2026-10-02 (memory, sub-agents, settings, env-vars, permissions, skills,
  monitoring-usage, chrome): Subagenten laden die ganze CLAUDE.md-Hierarchie samt `@`-Importen,
  Regeln und Git-Status, aber weder Auto-Memory noch Gesprächsverlauf noch die Ausgabe des
  SessionStart-Hooks; Ordner-CLAUDE.mds und Regeln mit `paths:` laden erst beim Lesen passender
  Dateien; `@`-Importe sparen keinen Kontext; HTML-Kommentare in CLAUDE.md kosten nichts. Ein
  Werkzeugname ohne Muster in `permissions.deny` entfernt das Werkzeug aus dem Kontext.
  `"agent": "<name>"` ersetzt den Systemprompt der Hauptsitzung. `SubagentStart` kann
  `additionalContext` mitgeben; `InstructionsLoaded` meldet jede geladene CLAUDE.md mit Grund.
  Skill-Beschreibungen kosten bis 1 % des Kontextfensters; `skillOverrides` blendet einzeln aus.
- **Proben 2026-10-02** (Sandbox im Scratchpad, Claude Code 2.1.287, Haiku, Mitschrift per
  `OTEL_LOG_RAW_API_BODIES`):
  - Schreibgrenze per `PreToolUse` mit `agent_type` wirkt (Write nach `domaene/` abgelehnt).
  - `PreToolUse` sieht `Agent` (`subagent_type`) und `Skill` (Skillname), auch im Subagenten.
  - Ein Subagent mit `Agent` in `tools` startet Subagenten (E29 machbar, Typen per Hook begrenzen).
  - Ordner-CLAUDE.md lädt nur beim Lesen, nicht beim Schreiben → der `SubagentStart`-Hook gibt
    schreibenden Rollen die Ordner-CLAUDE.md ihrer Perspektive mit (E43, Schicht 3).
  - `SubagentStart`-`additionalContext` und Root-CLAUDE.md kommen im Subagenten an.
  - `InstructionsLoaded` trägt kein `agent_type` → Zuordnung über `trigger_file_path` (E47).
  - Subagenten laufen standardmäßig im Hintergrund; `PostToolUse` auf `Agent` liefert keine
    Tokenzahlen, `SubagentStop` liefert `agent_transcript_path` (Tokens dort auslesen).
  - Neben general-purpose gibt es den Sammeltyp `claude` → ebenfalls sperren.
  - Grundlast Hauptsitzung mit Standardeinstellungen rund 105.000 Zeichen: Systemprompt 16.000,
    Werkzeuge 73.000 (davon Artifact 35.000, Bash 12.000, Agent 9.000), Skill-Liste 8.000,
    Agentenliste 2.600. Koordinator als `agent` mit E44 rund 19.500 Zeichen (Systemprompt 377,
    Agent/Read/Bash 16.000, Agentenliste nur die erlaubten Typen).
  - Subagent: `Agent` kostet 9.000 Zeichen, das Werkzeug `Skill` bringt die ganze Skill-Liste mit;
    ein Agent nur mit Read hat rund 7.000 Zeichen Grundlast.
  - Der Koordinator schrieb trotz fehlendem Write per `echo > x.txt` über Bash → die
    Bash-Positivliste (E29) muss ein Hook sein, Berechtigungsregeln reichen nicht.
  - `skillOverrides: user-invocable-only` verhindert auch das Vorladen per `skills:` → für den
    Reviewer `code-review` auf `on` (kostet nur bei Agenten mit Werkzeug `Skill`). Vorgeladen
    wendet der Reviewer es an; es braucht `ReportFindings` → nicht global sperren, nur über
    `tools:` je Rolle.
  - `permissions.allow` in einem nicht vertrauten Arbeitsordner wird ignoriert.
  - Die VS-Code-Erweiterung hängt nach jedem Edit Editor-Diagnosen an (hier rund 10.000 Zeichen
    cSpell-Meldungen zu deutschem Text) → cSpell mit deutschem Wörterbuch (E37) oder für Markdown
    abschalten.
- Subagenten können Subagenten starten (geprüft) → `Agent` entziehen, wo nicht gewollt. Eine
  Typliste `Agent(x, y)` wirkt nur in der Hauptsitzung (`--agent`), im Subagenten wird sie
  ignoriert → Hook auf das Agent-Werkzeug prüft `subagent_type`.
- Ein Subagent gibt nur seine Schlussantwort an den Aufrufer zurück.
- Skills: Zunächst ist nur die Beschreibung im Kontext, der volle Inhalt lädt beim Aufruf; `skills:`
  in der Agentendefinition lädt vorab. Skills können Skripte und Beispieldateien mitbringen und mit
  `context: fork` in einem eigenen Subagenten laufen. Ob Hooks Skill-Aufrufe sehen, ist nicht
  dokumentiert und wird in Schritt 7 ausprobiert.
- Nutzbare Felder: `tools`, `disallowedTools`, `model`, `maxTurns`, `effort`, `skills`, `hooks`,
  `isolation: worktree`, `omitClaudeMd`.
- `maxTurns` begrenzt Runden, nicht Token. Für die Budgetwirkung aus ArbiterMap gibt es nach
  heutigem Stand kein gleichwertiges Bordmittel.
- SonarLint läuft nur im Editor. Agenten brauchen Kommandozeilenwerkzeuge (Kandidaten: ruff, vulture,
  radon, Mutationstests).

## Schritte

| # | Schritt | Ergebnis | Status |
|---|---|---|---|
| 1 | Altbestand analysieren | Ausgangslage | erledigt |
| 2 | Grundsätze festhalten | diese Datei | erledigt |
| 3 | Kontextlandkarte | Abschnitt oben | erledigt |
| 4 | Rollenmodell | E24–E30; Feinschnitt je Rolle in Schritt 7 | weitgehend erledigt |
| 5 | Beziehungen | Abschnitt Beziehungen, E33–E35 | erledigt |
| 6 | Prüfmechanismen | E36, E37, Werkzeugprobe; Konfiguration folgt in Schritt 7 | erledigt |
| 7 | Repo-Gerüst | E38–E49; git init, Ordner, CLAUDE.mds, Agentendefinitionen, Skills, Hooks, Prüfkonfiguration | begonnen |
| 8 | Durchstich Nahkampfphase | Anforderung → Akzeptanztest → Code, gemessen | offen |
| 9 | Migration | Regeltexte, Daten, Mockups, Dashboard, Improve-Skill | offen |
| 10 | Doku für Menschen | `doku/` nach E32 | offen |

Jeder Schritt wird vom Stakeholder freigegeben, bevor der nächste beginnt.

## Offene Fragen

- derzeit keine; nächste Aufgabe: Root-CLAUDE.md im Gespräch entwerfen.
