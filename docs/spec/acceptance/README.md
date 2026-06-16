# Akzeptanzkriterien — die fachliche Schranke

> Zweck: Jede **fachliche** Anforderung bekommt ein stabiles, testbares Kriterium.
> Ändert sich die Fachlichkeit und ein Kriterium bricht, wird der Build **rot** —
> das erzwingt ein Gespräch mit dem Nutzer statt eines stillen Drifts (genau der
> Fehler hinter Finding 9.2: Pfeile wurden lautlos umgebaut).

## Format

Jedes Kriterium ist **Given / When / Then** mit einer stabilen ID:

```
AC-<BEREICH>-<NN>     z. B. AC-SUBFACTION-03
```

Die ID ist eine Markdown-Überschrift in [index.md](index.md). Darunter:

- **Given** — Ausgangszustand (Daten/Session)
- **When** — Aktion / Render
- **Then** — erwartetes, **messbares** Ergebnis
- *(optional)* **Diagramm** — Verweis auf eine Skizze in `img/`; der Doku-Test
  prüft, dass die Skizze existiert und nicht älter als dieses Dokument ist.

## Verbindlichkeit (Gate)

`tests/acceptance/` ist eine **vierte messbare Schranke** neben Coverage,
Architektur-Gate und Doku-Gate:

1. Jede AC-ID in `index.md` muss von **mindestens einem** Test angepinnt sein —
   `@acceptance("AC-…")` auf der Testfunktion.
2. Jede in einem Test referenzierte AC-ID muss in `index.md` **dokumentiert** sein.
3. Bricht (1) oder (2), bricht der Build (`tests/acceptance/test_registry_consistency.py`).

Damit können Spec und Test nicht auseinanderlaufen: ein gelöschtes Kriterium
ohne Test (oder umgekehrt) ist sofort sichtbar.

## So fügst du ein Kriterium hinzu

1. AC in `index.md` als `### AC-<BEREICH>-<NN>` mit Given/When/Then schreiben.
2. Test in `tests/acceptance/test_<bereich>.py` mit `@acceptance("AC-<BEREICH>-<NN>")`.
3. `pytest tests/acceptance/ -q` — grün heißt: Spec ↔ Test ↔ Code im Gleichtakt.

Die Registry startet **klein** und wächst Finding für Finding. Das Gate erzwingt
Konsistenz, nicht Vollständigkeit ab Tag 1.
