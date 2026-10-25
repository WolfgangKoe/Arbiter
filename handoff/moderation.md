# Moderation

Stand vor „Freigabe Retro 7“. Nichts hält die Freigabe auf; die Prozess-Items P1 bis P8
stehen in der [Retro](retro.md). Offene Annahme nach [Ich 1](../prozess/praemissen/ich.md): keine.

## Dran
Alle Anliegen warten auf die Prozessphase, außer wo vermerkt.
- Organisationsentwickler:
  Anliegen 2360,
  Anliegen 3050,
  Anliegen 2201 (alle P1),
  Anliegen 2590 (P2),
  [2591](anliegen/2591-innenIchDesStakeholdersInDenPraemissen.md) (P3).
- Regelumsetzer:
  Anliegen 2040 und
  Anliegen 2592 (P4),
  Anliegen 2460 und
  Anliegen 2720 (P5),
  Anliegen 3301 (P6),
  Anliegen 3120 (P7).
- Stakeholder: Anliegen 3550.
- Spätere Phase, nichts zu tun: Planer
  [3051](anliegen/3051-architekturUmordnenInPlan8.md); Ux
  [2920](anliegen/2920-leistenNamenInDenMockups.md),
  [3040](anliegen/3040-que7MockupZeigtZurueckUndUebergehenBeiKohaerenz.md);
  Anforderungsautor [3500](anliegen/3500-verweiseAufEtappe1.md); Architekt
  [2215](anliegen/2215-leistenOhneEigenenNamen.md) (wartet auf 2920).

## Vorschläge
- 2740 hat die Antwort A und wartet auf 3120. Schließen darf der Architekt, sobald P7 gebaut
  ist und du die Karte gesehen hast.
- 2201 ist Beleg der Retro; der Organisationsentwickler arbeitet es in P1 ab und schließt es.
- 2040 und 2592 meinen dieselbe Lücke (Schreiben über Bash). Zusammenlegen darf der
  Organisationsentwickler als Absender; der Regelumsetzer baut sie in P4 in einem Lauf.
- Stränge Organisationsentwickler: P1, dann P2, dann P3, nacheinander (alle ändern
  Ablauf, Regeln oder Prämissen). P2 und P8 gehen in einem Commit, die Links des Architekten
  in `technik/` ziehen im selben Commit nach, ohne eigene Zeile im Fortschritt.
- Stränge Regelumsetzer: P6 läuft neben P1. P8 läuft mit P2. P4, P5, P7 nacheinander, weil
  alle Hook-Code unter `prozess/pruefungen/` ändern ([Gleichzeitige Läufe](../prozess/ablauf.md#gleichzeitige-läufe)).
  P3 darf neben P4 laufen.
- Architekt: nur die Links für P2; sonst keine Arbeit in dieser Phase.
- Reihenfolge wie die Empfehlung der Retro: P6 neben P1, P2 mit P8, P3 neben P4, dann P5, P7.

## Fragen an dich
- Anliegen 3550: Zählen Stand und Dashboard die
  belegten Kriterien je Etappe (A, Empfehlung) oder weiter über alle (B)? Hält die
  Freigabe nicht auf; Retro 7 legt dafür kein Item an.
- [3051 · F1](anliegen/3051-architekturUmordnenInPlan8.md): Nimmst du das Umordnen der
  Architektur als erstes Item in Plan 8? Empfehlung ja; hält die Freigabe nicht auf.
