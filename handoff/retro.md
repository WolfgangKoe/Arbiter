# Retro · Zyklus 2

Etappe 1 · Aufstellen, Plan 2 mit drei Items. Grundlage: [Review 2](review.md), git seit
`Freigabe Retro 1`, Anliegen, Belegung je Lauf.

## Befunde
1. Inkrement: DoD erfüllt, alle Items abgenommen, ohne Nacharbeit wie in Zyklus 1.
2. Prozesslast: 77 Anliegen, 31 an den Regelumsetzer (15 Kritik am Code), 9 an mich, also
   52 % (neue [Kennzahl](../prozess/kennzahlen.md), Schwelle ein Drittel). Ketten:
   142 → 144 → 147 → 148 um einen Test auf Pfad-Literale mit bekannter Lücke; der Sprung
   (83, 118, 124, 127, 133, 143) zweimal gebaut, ganz gelöscht. `prozess/pruefungen` +2.646/−562
   Zeilen, `technik/arbiter` +220/−12; Prüfskripte 183.000 Zeichen, Produkt 12.700.
3. Belegung: Der Regelumsetzer lag zweimal über 120.000 Token (einmal 197.000), je mit
   mehreren Anliegen im Auftrag. Das löst „Last je Rolle messen“ im Backlog aus.
4. Höchstmaße sind nur Text und verletzt: Retro 1 4.167/4.000, `rueckverfolgung.py`
   14.621/12.000, `rueckverfolgungTest.py` 12.979 und `standTest.py` 14.179 gegen 8.000.
5. Der Bash-Schutz für Anliegen wurde zum zweiten Mal umgangen (Retro 1, Befund 4; jetzt
   [138](anliegen/138-anliegenPerSkriptAmBashSchutzVorbei.md)). Bordmittel statt Heuristik:
   Sandbox ([139](anliegen/139-bashSandboxStattHeuristik.md)). Sonst ersetzt keine Neuerung
   von Claude Code einen eigenen Mechanismus.
6. Kritik am Code (Zusage aus [107](anliegen/107-kritikAnDenPruefungen.md)): Sie lief für
   jeden Code-Commit (29 Kritik-Commits). Die Lesbarkeit der Prüfskripte meldete sie erst nach
   107, danach folgte jedem Fix ein Rest (Kette in 2). wir.md 6 (Indizes) ist nur in
   Prüfskripten verletzt; den Rest führt [114](anliegen/114-pruefskripteOrdnenUndLesbarMachen.md)
   (B 1, B 7). Ein Mechanismus bräuchte Urteil, darum keiner.
7. Dein Anliegen [150](anliegen/150-sonarlintAbdeckungUndToterCode.md): SonarLint ist nicht
   scharf gestellt, Abdeckung wird nicht gemessen (Zweige: Produkt 100 %, nur Akzeptanztests
   94 %, Prüfskripte 93 %).
8. Plan 3 bringt die erste Oberfläche ([145](anliegen/145-ersteOberflaecheImBrowser.md)):
   Auslöser der Rolle UX ([151](anliegen/151-rolleUxFuerDieErsteOberflaeche.md)).

## Geändert
- [Ablauf](../prozess/ablauf.md): DoD 1 mit Abdeckung 95 %, DoD 2 mit totem Code, SonarLint
  als nur Text; Prozessphase: ein Item je Lauf des Regelumsetzers (Befund 3).
- [Regelumsetzer](../.claude/agents/regelumsetzer.md): ein Item je Lauf; Schreibpfade
  `dashboard.html` und `prozess/dashboard/` (deine Antwort in Anliegen 90).
- [Kennzahlen](../prozess/kennzahlen.md): Prozesslast. [Backlog](../prozess/backlog.md):
  Dashboard und Last je Rolle sind P5, Abdeckung und vulture P1.

## Prozess-Items (Regelumsetzer, je Lauf eins, in dieser Reihenfolge)
- P1 Abdeckung (150): Zweige ≥ 95 % für `technik/arbiter` und `prozess/pruefungen` im Lauf
  der Prüfungen; vulture über `technik/arbiter`; Liste der Zeilen, die nur Einheitstests
  erreichen, für den Reviewer.
- P2 SonarLint (150): Wegwerf-Versuch mit dem Analysator der installierten Erweiterung ohne
  VS Code; gelingt er nicht, „Sonar way“ (Python) auf ruff abgebildet. Architekt kritisiert.
- P3 Höchstmaße in `hoechstmassTest.py`: Code-Modul 12.000, Einheitstest-Datei 8.000, Plan,
  Review, Retro 4.000; vorher die drei Dateien aus Befund 4 teilen (`rueckverfolgung.py`:
  114 B 7).
- P4 `pfadeTest.py` löschen, `pfade.py` bleibt: Der Test prüft nur Prüfskripte, hat eine
  bekannte Lücke und kostete drei Anliegen. Das ist die Löschung, die die Kennzahl verlangt.
- P5 Dashboard nach Anliegen 90 (git): Lauf-Log mit Rolle und Belegung, Seite `dashboard.html`.
- P6 `kennzahlen.py` rechnet die Prozesslast.
Danach 114 und, nach deiner Antwort, 139.

## Empfehlung
Zur Freigabe: [135](anliegen/135-koordinatenXundYAlsAusnahme.md) und 139 je A, 145, 151 A.
134 und 138 warten auf 135 und 139.
