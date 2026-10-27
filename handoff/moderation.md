# Moderation

Stand vor „Freigabe Plan 8“ (Zyklus 8, Domänenphase), nach der Kritik am Plan. Nichts
blockiert die Items 1 bis 3 in [Plan 8](plan.md).

## Dran
- Anforderungsautor: [4280](anliegen/4280-begriffeUndAnnahmenZuPlan8.md). F6 und F7 stehen
  mit „Antwort: .“ beantwortet (A, A); er setzt sie um (BEW bleibt, Daten mit Etappe 8) und
  schließt das Anliegen, oder fasst nach, wenn eine Rückfrage bleibt.
- Regelumsetzer, ohne Wartevermerk (Stand führt falsch, Prüfcode):
  [3900](anliegen/3900-standNenntFalscheRolleFuerProzessItems.md),
  [3780](anliegen/3780-restePruefcodeNach3301.md). Hält keinen Plan-Punkt auf.
- Es warten auf die Prozessphase (8):
  [3960](anliegen/3960-pythonOhneStrichUndLueckenInRegeln.md),
  [4120](anliegen/4120-hindernisformatInAblaufUndRegeln.md),
  [4140](anliegen/4140-architekturAlsReiterBisZuDenDateien.md),
  [4301](anliegen/4301-fortschrittFuerItemOhneKriterium.md),
  [4040](anliegen/4040-ablaufUndRegelnVerschlanken.md) (Organisationsentwickler).
- Auf die Domänenphase 9: [4261](anliegen/4261-lueckenImNormalMoveFuerSpaeter.md)
  (Anforderungsautor), [4540](anliegen/4540-plan8NenntErledigteAlsFehlend.md) (Planer;
  rührt er Plan 8 noch an, streicht er „Noch nicht bereit“).

## Vorschläge
- 4540: Der Planer darf es vor der Freigabe erledigen, wenn er Plan 8 ohnehin ändert;
  sonst gilt es für Plan 9.
- 4120 Schritt 1 und 2 sind Fälle von „doppelt“ aus 4040; sie gehen in dessen Durchsicht
  und die Retro 8 ein. Zusammenlegen darf der Organisationsentwickler, 4120 danach schließen.
- 4301 und 3900 ändern beide `standregeln/fortschritt.py` und `phasenfolge.py` samt Tests;
  der Regelumsetzer macht sie in einem Lauf. 4301 hängt zudem an der Tabelle in
  [Fortschritt](../prozess/ablauf/fortschritt.md) (Organisationsentwickler, wie 4120).
- 3960 und 3780 sind Hook-Code (`bashSchreiben.py`, `kommentare.py`) und laufen
  nacheinander, nicht neben 3900 und 4301.
- 4140 trägt Anliegen 4100 mit; der Architekt schließt 4100, wenn 4140 gebaut ist. 4140
  ändert kein Hook-Modul und darf neben den Hook-Strängen laufen.
- 4261 Punkt 5 (Wort „Weg“) ist mit „Distanz“ aus 4280 F1 vermutlich erledigt; der
  Anforderungsautor prüft das in Phase 9 und streicht den Punkt.
- Stränge Regelumsetzer (Prozessphase 8): A: 3900 + 4301 (+ 4120 Schritt 1), dann 3780,
  dann 3960; B daneben: 4140. Organisationsentwickler: 4040 mit 4120 Schritt 2 und der
  Tabelle aus 4301, ein Strang. Anforderungsautor: 4280 daneben, getrennte Dateien.
  Architekt, Fachkritiker: keine Arbeit.

## Fragen an dich
Offen ist keine. Dein „.“ unter F6 und F7 in
[4280](anliegen/4280-begriffeUndAnnahmenZuPlan8.md) gilt als A; die Annahme dort ist damit
bestätigt.

Später, noch nicht gestellt: Soll Arbiter die bisher gezogene Distanz der gewählten
*Einheit* anzeigen ([4261](anliegen/4261-lueckenImNormalMoveFuerSpaeter.md), Punkt 6)?
Kommt in Phase 9 als eigene Frage.
