# Moderation

Stand: Retro 2 vor der Freigabe. Plan 2 ist abgenommen; kein offenes Anliegen blockiert ein
Item aus [plan.md](plan.md). Auf Plan 3 wirken 145, 151, 159 und die Prozess-Items P1 bis P5
der [Retro](retro.md). Köpfe stehen auf `offen`, bis die Absender nach der Freigabe
`beantwortet` setzen.

## Dran
- Regelumsetzer, ein Item je Lauf: P1 bis P5 der Retro (P4 Dashboard 158, P5
  [162](anliegen/162-antwortenNichtZaehlen.md); 161 ist angenommen, 162 gilt). Danach die
  Kritik am Code zu 6a64835: [163](anliegen/163-altbestandEinmalNennen.md),
  [165](anliegen/165-umbenennungPerTestBemerken.md),
  [166](anliegen/166-anliegenUeberschreibenBeiParallelenLaeufen.md), ferner
  [114](anliegen/114-pruefskripteOrdnenUndLesbarMachen.md). Nicht in der Retro; Vorschlag:
  nach P1 bis P5 oder im Backlog.
- Organisationsentwickler: [164](anliegen/164-specsPfadInDomaene.md) (eine Zeile in
  `domaene/CLAUDE.md`); Optionen mit Folgen zu [139](anliegen/139-bashSandboxStattHeuristik.md),
  [159](anliegen/159-zweiteTechnikdatei.md) und Leitplanken zu
  [151](anliegen/151-rolleUxFuerDieErsteOberflaeche.md); außerdem
  [134](anliegen/134-praemisseUndDodHinkenDenPruefungenNach.md),
  [150](anliegen/150-sonarlintAbdeckungUndToterCode.md),
  [155](anliegen/155-technikBrauchtPlatzUndErstesMockup.md); 138 wartet auf 139.
- Architekt: [152](anliegen/152-solidUndVieleIf.md), Rückfrage zu einem Tag in
  [83](anliegen/83-sprungErproben.md), Nachprüfung 124 und 157.
- Planer: [145](anliegen/145-ersteOberflaecheImBrowser.md) einarbeiten, 156 nachprüfen.
- Stakeholder: Nachprüfung 107 und 153.

## Vorschläge
- Zusammen (Regelumsetzer): 163 mit 165 (dieselbe Liste der Altbestand-Ordner, Test aus
  `agenten.nurLesbar`); 114 mit 162 und 163 (`hoechstmassTest.py`, Prüfskripte).
- Zusammen (Organisationsentwickler): 139 mit 138; 145, 151, 159; 134 mit 155.
- 164 hat Erledigt-Bedingung `git grep`; kann sofort laufen, ohne Regelumsetzer.
- Nur ablegen, dann `erledigt` durch die Absender: 135, 161, 83 F2.
- Schließen: 124 mit dem Sprungverzicht aus 83 (Architekt); 150 und 157 teilen Abdeckung,
  150 erledigt der Stakeholder nach P1 und P2.

## Fragen an dich
Keine neue. Offen, bis der Organisationsentwickler nachgeliefert hat:
[139](anliegen/139-bashSandboxStattHeuristik.md) F1,
[159](anliegen/159-zweiteTechnikdatei.md) F1 und
[151](anliegen/151-rolleUxFuerDieErsteOberflaeche.md) F1. Die Retro-Empfehlung ist
nachgezogen und stimmt mit deinen Antworten überein.
