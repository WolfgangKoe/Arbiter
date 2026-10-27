# Moderation

Stand vor „Freigabe Plan 8“ (Zyklus 8, Domänenphase). Nichts blockiert die Items 1 bis 3 in
[Plan 8](plan.md), außer der Antwort auf 4280, mit der wir schon bauen.

## Dran
- Stakeholder: [4280](anliegen/4280-begriffeUndAnnahmenZuPlan8.md), F1 bis F5; „.“ genügt.
  Es berührt Item 2 und 3 (QUE-9, QUE-10, BEW-1, BEW-2).
- Regelumsetzer, ohne Wartevermerk (Stand führt falsch, Prüfcode):
  [3900](anliegen/3900-standNenntFalscheRolleFuerProzessItems.md),
  [3780](anliegen/3780-restePruefcodeNach3301.md). Hält keinen Plan-Punkt auf.
- Sonst nichts in dieser Phase. Es warten auf die Prozessphase (8):
  [3960](anliegen/3960-pythonOhneStrichUndLueckenInRegeln.md),
  [4120](anliegen/4120-hindernisformatInAblaufUndRegeln.md),
  [4140](anliegen/4140-architekturAlsReiterBisZuDenDateien.md),
  [4301](anliegen/4301-fortschrittFuerItemOhneKriterium.md),
  [4040](anliegen/4040-ablaufUndRegelnVerschlanken.md) (Organisationsentwickler);
  auf die Domänenphase 9: [4261](anliegen/4261-lueckenImNormalMoveFuerSpaeter.md)
  (Anforderungsautor).

## Vorschläge
- 4120 Schritt 1 und 2 sind Fälle von „doppelt“ aus 4040; sie gehen in dessen Durchsicht und
  die Retro 8 ein. Zusammenlegen darf der Organisationsentwickler, 4120 danach schließen.
- 4301 und 3900 ändern beide `standregeln/fortschritt.py` und `phasenfolge.py` samt Tests;
  der Regelumsetzer macht sie in einem Lauf. 4301 hängt zudem an der Tabelle in
  [Fortschritt](../prozess/ablauf/fortschritt.md) (Organisationsentwickler, nach Freigabe
  Retro 8, wie 4120).
- 3960 und 3780 (Hook-Code: `bashSchreiben.py`, `kommentare.py`) sind Hook-Code und laufen
  nacheinander, nicht neben 3900 und 4301.
- 4140 (Dashboard, Tokenbericht) trägt Anliegen 4100 mit; der Architekt schließt 4100, wenn
  4140 gebaut ist. 4140 ändert kein Hook-Modul, darf neben den Hook-Strängen laufen.
- 4261 Punkt 5 (Wort „Weg“ in AUF) ist mit „Distanz“ aus 4280 F1 vermutlich erledigt; der
  Anforderungsautor prüft das in Phase 9 und streicht den Punkt.
- Stränge Regelumsetzer (Prozessphase 8): A: 3900 + 4301 (+ 4120 Schritt 1), dann 3780, dann
  3960 (Hook-Code, nacheinander); B daneben: 4140. Organisationsentwickler: 4040 mit 4120
  Schritt 2 und der Tabelle aus 4301, ein Strang. Architekt, Fachkritiker: keine Arbeit.

## Fragen an dich
1. Annahme: [4280](anliegen/4280-begriffeUndAnnahmenZuPlan8.md) F1 bis F5 (Begriffe, Kürzel
   BEW, Distanz als gerade Strecke, Overlord M 6″, Knöpfe). Wir bauen mit den Empfehlungen
   A; eine Änderung kostet neue Kennungen und Tests.
2. Spätere Frage, noch nicht gestellt: Soll Arbiter die bisher gezogene Distanz der gewählten
   *Einheit* anzeigen (4261, Punkt 6)? Kommt in Phase 9 als eigene Frage.
