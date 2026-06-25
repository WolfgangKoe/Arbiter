# Context Engineering — Slide-Inhalte (Referenz)

> **Quelle:** Vortrag „Context Engineering, weniger Token, bessere Agents" — Peter Wegner,
> andrena objects ag, Juni 2026.
> Bezogen am 2026-06-25 von <https://peter-wegner-slides.pages.dev/context-engineering-andrena-v2/>
> (per Subagent extrahiert; Speaker-Notes der 31 Folien). Die visuellen Grafik-Inhalte der
> Folien-PNGs sind hier nicht enthalten.
>
> **Zweck dieser Datei:** kanonische Inhaltsablage zur **Überarbeitung unserer Arbeits-Prinzipien**
> (`CLAUDE.md`, `docs/governance/operating_model.md`, geplante `context_engineering.md`). Reine
> Referenz — keine Entscheidungen. Die Ableitung in unsere Prinzipien erfolgt separat (Prinzipien-Revision).

---

## Kern-Modell: vier Hebel (Lance Martin / LangChain)

Jede Context-Engineering-Technik fällt in genau eines von vier Verben:

| Hebel | Bedeutung | Konkret im agentischen Coding |
|---|---|---|
| **Write** | Kontext bewusst **nach außen** ablegen | Scratchpad-Dateien (Plan/NOTES/DECISIONS), Memory (CLAUDE.md/AGENTS.md) — überleben Compaction |
| **Select** | das Richtige **hereinholen** | Just-in-Time-Retrieval (grep/glob/Ausschnitte statt ganzer Dateien), RAG, **Tool-Selektion** (5 passende Tools > 50) |
| **Compress** | dieselbe Info mit **weniger Token** | Structured Outputs (JSON statt Prosa), bewusste Summarization an Phasengrenzen, Trimming alter Tool-Ergebnisse |
| **Isolate** | Kontext **aufspalten** | Phasentrennung (Research/Plan/Implement getrennt), Sub-Agents (eigenes Fenster), Sandboxing, Lean MCP / State-by-Reference (IDs statt Datenblöcke) |

**Leitfrage bei jedem Token: „Ändert dieser Token die Antwort?"**
**Merksatz: Kontext ist ein Budget. Behandle ihn wie eines.**

---

## Das Problem (Teil 1)

- **Kontextfenster = Arbeitsspeicher fester Größe, kein durchsuchbares Archiv.** Token kosten bei
  *jedem* Schritt erneut Geld und Aufmerksamkeit. Tool-Ergebnisse (Datei-Inhalte, Suchen, Logs) sind
  der größte und am wenigsten kontrollierte Posten (~43 % des finalen Fensters).
- **Agenten-Loop:** Wir delegieren mehrstufige Aufgaben; jeder Schritt hängt sein Ergebnis an. Ohne
  aktives Management wächst das Fenster monoton, bis Qualität und Kosten kippen.
- **Kostenschock:** dieselbe Aufgabe je Modell Faktor ~27; Copilot-Usage kann ×100 der Flatrate
  erreichen. Sonnet 4.6: 3 $/15 $ pro 1M Token (In/Out). **Kostenkontrolle = Kontextkontrolle.**
- **Context Rot** (drei unabhängige Befunde): Modelle nutzen lange Kontexte ungleich.
  - „Lost in the Middle" (Liu et al., Stanford 2023): U-Form, Mitte fällt ab.
  - NoLiMa (2024): Einbrüche jenseits ~32K Token.
  - Chroma (2025): prägt den Begriff „Context Rot" — länger = unzuverlässiger.
  → **Nicht maximal füllen, gezielt kuratieren.**
- **Vier Failure-Modi** (Drew Breunig, „How Contexts Fail", 2025):
  1. **Poisoning** — Halluzinat/Fehler landet in Zusammenfassung/Ziel und kontaminiert alles Weitere.
  2. **Distraction** — Überfokus auf den angesammelten Verlauf (Gemini-Pokémon: ab ~100K alte Aktionen wiederholt statt neu geplant).
  3. **Confusion** — irrelevanter Kontext (zu viele Tooldefinitionen) wird fälschlich genutzt.
  4. **Clash** — widersprüchliche Inhalte in derselben Session („sharded prompts" −39 % Leistung).
- **Auto-Compaction** (~80 % Füllung) ist verlustbehaftet und unkontrolliert — die **Notbremse**,
  nicht die Lösung. Ziel: sie nie zu brauchen.

---

## Die Disziplin (Teil 2) — konkrete Praktiken

**Du bist der Architekt des Kontexts.** Prompt Engineering optimiert eine *einzelne* Anweisung;
Context Engineering managt, was über die *gesamte* Trajektorie im Fenster ist und was nicht.

### Sub-Agents — Read/Write-Asymmetrie (Slide 17)
- **Stark als Leser/Späher/Prüfer/Router:** Recherche, Codebase-Mapping, Review, Security-Audit, Log-Analyse — eigenes Fenster, nur **verdichtetes Ergebnis** zurück.
- **Schwach als parallel schreibende Co-Autoren** am selben, eng gekoppelten Code — Merge-Kosten sind *semantisch*.
- **Enger Vertrag entscheidet:** Ziel, Scope/Grenzen, erlaubte Tools/Quellen, Effort-Budget, Output-Format → verhindert Duplikate und Lücken. Ergebnisse als referenzierbare Artefakte.
- **Multi-Agent kostet grob das 15-fache an Token** ggü. einem Chat → gezielt einsetzen.

### Messen zuerst: `/context`
Zeigt die Fenster-Aufschlüsselung: System-Prompt, Tool-Defs + MCP-Server, Memory-Dateien, Verlauf
inkl. Tool-Ergebnisse, freier Platz. **Aha-Moment:** ein großer Teil ist oft schon vor der ersten
Eingabe belegt. **Diagnose vor Therapie.**

### Versteckter Ballast
- **MCP-Server** spiegeln *jede* Tool-Beschreibung in den System-Präfix (schnell Tausende Token, bei
  *jeder* Anfrage) — und viele Tools → schlechtere Tool-Wahl (Confusion).
- **Agent Skills** laden ihre Anleitungen ebenfalls in den Kontext.
- → **Nur verbinden/aktivieren, was die Aufgabe braucht.** CLI-first (`gh`/`az`/`glab`) statt MCP:
  null Grundlast statt N k Token. Playwright-MCP-Doku sagt selbst: standardmäßig aus.

### Prompt Caching
- Anbieter cacht das verarbeitete **stabile Präfix** (System-Prompt + Tool-Defs). Cache-Hit:
  **bis −90 % Kosten, −80 % Latenz**. Agentische Schleifen schicken denselben Präfix immer wieder → großer Effekt.
- Beim Coding-Agent ist der Präfix **gesetzt** (Harness baut ihn aus Tool-Defs, MCP-Defs, Skills,
  Rules-Files). Du sortierst ihn nicht um — **dein Hebel ist, WAS darin liegt** (kein toter Ballast).
- **TTL = 5 oder 60 Min** (Claude Code default 60). Pause > TTL → Cache kalt → nächster Call zahlt den
  *ganzen* Verlauf zum vollen Input-Preis. Editieren von CLAUDE.md bricht den Cache **nicht** pauschal.
- **Warnbeispiel:** 851,6 k Token im Fenster, Cache kalt, ein versehentliches Enter ≈ **8,50 $** für
  eine Eingabe. Lehre: auf großem, abgestandenem Kontext nicht weiterklicken — `/clear` oder Neustart.

### Falsch abgebogen? Zurückspulen statt nachbohren
Nach ~3 Fehlversuchen ist der Kontext mit toten Pfaden/Halluzinationen vergiftet (Poisoning). Bewusst
zum letzten guten Stand **zurückspulen** (Claude Code: 2× Esc / opencode: Timeline) — entfernt den
vergifteten Verlauf restlos. `/clear` an jedem Phasenübergang (Research→Plan→Implement) ist generell sinnvoll.
**Merksatz: Läuft Debugging im Kreis, ist das Werkzeug die Rückspultaste, nicht die Eingabetaste.**

### Sprache verdichten
- **Caveman-Prompting** (Brussee / Pocock 2026): Artikel/Füllwörter/Höflichkeiten/Hedges streichen,
  technische Präzision behalten, Fragmente ok, Code unangetastet → ~65 % weniger *Output*-Token.
- **Semantische Anker:** etablierte Begriffe („SOLID", „DRY", „Clean Architecture") tragen ganze
  Konzepte in wenigen Token.
- Ehrlich: stark gegen sprachliches Rauschen, **schwach gegen** Negationen, Compliance, teamweit
  gepflegte Prompt-Artefakte — dort nicht übertreiben.

### Tool-Output komprimieren (größter realer Posten)
1. **Tool-Output** — RTK (Rust Token Killer): CLI-Proxy filtert/gruppiert/dedupliziert (60–90 %, <10 ms).
2. **Code/Repo** — Repomix `--compress` (nur Signaturen/Struktur via Tree-sitter, ~70 %); cargo-prompt.
3. **Prompt/RAG** — LLMLingua-Familie (algorithmisch bis ~20×).

---

## Fazit: Wo anfangen (Aufwand→Wirkung)

1. **Initialer Kontext** (CLAUDE.md/Skills/MCPs) — größter Hebel, zählt im Cache-Präfix bei jeder Anfrage.
2. **Nutzungsverhalten** — Phasen trennen, Caching/TTL beachten (kostet nur eine Gewohnheit).
3. **Noisy Tool Calls/Files** — verbose Logs, große Artefakte (openapi.json, generierter Code) kompakter darstellen.
4. **Token-Optimierer** (RTK, Repomix, repomap) für Rohdaten an der Quelle.

**Die Kompetenzverschiebung: nicht „besser prompten", sondern „härter kuratieren."**

---

## Bezug zu unseren Artefakten (Hinweis, keine Entscheidung)

- **Write/Memory** ↔ unsere Artefakt-Landkarte, `next_session.md`, Memory-Dateien.
- **Isolate/Sub-Agents** ↔ unser Subagent-Muster (Sonnet/Haiku-Fleißarbeit, Opus reviewt) + die
  Read/Write-Asymmetrie und der „enge Vertrag" decken unsere Selbstprüf-Checkliste ab.
- **Compress/Caching/TTL** ↔ Token-Korridor (<150 k), `tools/session_context.py`, `tools/token_report.py`.
- Offene Ableitungen → Prinzipien-Revision (`CLAUDE.md` / `operating_model.md` / `context_engineering.md`).
