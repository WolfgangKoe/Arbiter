# Retro · Zyklus 2

Etappe 1 · Aufstellen, Plan 2 mit drei Items. Grundlage: [Review 2](review.md), git seit
`Freigabe Retro 1`, Anliegen, Belegung je Lauf.

## Befunde
1. Inkrement: DoD erfüllt, alle Items abgenommen, ohne Nacharbeit wie in Zyklus 1.
2. Prozesslast: 77 Anliegen, 31 an den Regelumsetzer, 9 an mich: 52 % (neue
   [Kennzahl](../prozess/kennzahlen.md), Schwelle ein Drittel). Ketten: 142 → 148 um einen
   Test mit bekannter Lücke; der Sprung zweimal gebaut, ganz gelöscht. Prüfskripte 183.000
   Zeichen, Produkt 12.700.
3. Belegung: Der Regelumsetzer lag zweimal über 120.000 Token (einmal 197.000), je mit
   mehreren Anliegen im Auftrag.
4. Höchstmaße sind nur Text und verletzt: Retro 1 4.167/4.000, `rueckverfolgung.py`
   14.621/12.000, zwei Testdateien über 8.000.
5. Der Bash-Schutz für Anliegen wurde zum zweiten Mal umgangen
   ([138](anliegen/138-anliegenPerSkriptAmBashSchutzVorbei.md)); Bordmittel: Sandbox
   ([139](anliegen/139-bashSandboxStattHeuristik.md)).
6. Kritik am Code lief für jeden Code-Commit; die Lesbarkeit der Prüfskripte meldete sie erst
   nach [107](anliegen/107-kritikAnDenPruefungen.md), den Rest führt
   [114](anliegen/114-pruefskripteOrdnenUndLesbarMachen.md). Ein Mechanismus bräuchte Urteil.
7. Dein Anliegen [150](anliegen/150-sonarlintAbdeckungUndToterCode.md): SonarLint ist nicht
   scharf, Abdeckung ungemessen (Zweige: Produkt 100 %, Prüfskripte 93 %).
8. Plan 3 bringt die erste Oberfläche ([145](anliegen/145-ersteOberflaecheImBrowser.md)):
   Auslöser der Rolle UX ([151](anliegen/151-rolleUxFuerDieErsteOberflaeche.md)); du willst
   ihre Leitplanken sehen, ArbiterMaps Mockups als Gegenbeispiel.
9. Deine Antworten brachten 145 über das Höchstmaß; nach
   Anliegen 161 A zählen sie nicht mit.

## Geändert
- [Ablauf](../prozess/ablauf.md): DoD 1 Abdeckung 95 %, DoD 2 toter Code (157), SonarLint
  nur Text; DoR 5 erstes Mockup (155); Prozessphase: ein Item je Lauf, vor der Freigabe nur,
  was auf den nächsten Zyklus wirkt (156); Antworten zählen nicht (161); Kritik am Code
  auch für das Dashboard.
- [Regelumsetzer](../.claude/agents/regelumsetzer.md): ein Item je Lauf, Abdeckung der
  Prüfskripte 95 %; Schreibpfade `dashboard.html`, `prozess/dashboard/` (90).
- [Kennzahlen](../prozess/kennzahlen.md): Prozesslast. [Backlog](../prozess/backlog.md):
  zurückgestellte Items.

## Prozess-Items (Regelumsetzer, vor Plan 3, je Lauf eins)
Nur, was auf Plan 3 wirkt oder du vorher willst
([Ablauf, Prozessphase](../prozess/ablauf.md#prozessphase) 1).
- P1 Abdeckung (150, Anliegen 157): Zweige
  ≥ 95 % für `technik/arbiter`, eigene Meldung für `prozess/pruefungen`; vulture nach DoD 2,
  zuerst Wegwerf-Versuch ohne Ausnahmeliste.
- P2 SonarLint (150): Wegwerf-Versuch mit dem Analysator ohne VS Code, sonst „Sonar way“
  auf ruff. Wirkt auf die DoD von Plan 3.
- P3 `pfadeTest.py` löschen: bekannte Lücke, drei Anliegen; die Löschung der Kennzahl.
- P4 Dashboard ([158](anliegen/158-dashboardVorOderNachPlan3.md), dein Wunsch): Lauf-Log
  mit Rolle und Belegung, `dashboard.html` im Wurzelordner, Daten und Skripte in
  `prozess/dashboard/` (90); verschlankt aus `ArbiterMap/steering/metrics/process_dashboard.html`:
  Tokenstände, daneben ihre Verteilung, Legende mit höchstens fünf Wörtern je Eintrag.
- P5 Antworten zählen nicht ([162](anliegen/162-antwortenNichtZaehlen.md)).

## Empfehlung
Zur Freigabe: P1 bis P5. 135 und 161 sind mit A entschieden, 145 und 158 beantwortet. Zu
139, 151 und 159 liefere ich Optionen mit Folgen nach; 151 und 159 entscheidest du vor
Plan 3, 139 wirkt nicht darauf und wartet mit 138.

## Freigabe
Freigabe: ja
Kommentar: .
