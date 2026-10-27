# Moderation

Stand: Technikphase 8 (Zyklus 8). Die Items 1 bis 3 in [Plan 8](plan.md) laufen: Tests zu
Item phasenUndSchlachtrunden sind der nächste offene Schritt. Kein offenes Anliegen hält sie
auf; die vier Annahmen aus 5180 gelten, bis du antwortest.

## Dran
- Testautor: die Tests zu Item phasenUndSchlachtrunden und normalMove (Plan 8, Fortschritt);
  er arbeitet mit den Annahmen aus [5180](anliegen/5180-annahmenZurBewegungsphase.md) weiter.
- Implementierer: [4781](anliegen/4781-docstringNenntAltenVertrag.md) (Docstring von
  `web/anwendung.py`); klein, hält nichts auf.
- Regelumsetzer: [4780](anliegen/4780-linksNachDemUmordnenDerArchitektur.md) (Links auf die
  alte Architektur). [3780](anliegen/3780-restePruefcodeNach3301.md) und
  [3900](anliegen/3900-standNenntFalscheRolleFuerProzessItems.md) warten auf die Prozessphase 8.
- Stakeholder: [5180](anliegen/5180-annahmenZurBewegungsphase.md) F1 bis F4; hält nichts auf.
- Auf die Prozessphase (8): [3960](anliegen/3960-pythonOhneStrichUndLueckenInRegeln.md),
  [4120](anliegen/4120-hindernisformatInAblaufUndRegeln.md),
  [4140](anliegen/4140-architekturAlsReiterBisZuDenDateien.md),
  [4301](anliegen/4301-fortschrittFuerItemOhneKriterium.md),
  [4620](anliegen/4620-kuerzelJePhaseInDerDomaene.md),
  [4040](anliegen/4040-ablaufUndRegelnVerschlanken.md).
- Auf die Domänenphase 9: [4261](anliegen/4261-lueckenImNormalMoveFuerSpaeter.md),
  [4881](anliegen/4881-datenblaetterImGlossarUndInDenDaten.md),
  [4882](anliegen/4882-itemKatalogwerteGliedern.md),
  [5181](anliegen/5181-klickAufEineAufgestellteEinheit.md) (Anforderungsautor, falls A).
- Auf die Technikphase 9: [4901](anliegen/4901-ebeneImTestnamenUndKlickAufDenAnderenSpieler.md),
  [4921](anliegen/4921-klickUndHandgriffeDerSchlachtFuerSpaeter.md),
  [5000](anliegen/5000-vertragAufstellenGekuerztUndVoll.md).

## Vorschläge
- 4901 Punkt 1 ist als F3 in 5180 aufgegangen; der Architekt darf ihn in 4901 als erledigt
  vermerken und 4901 auf den Rest kürzen.
- 5180 F3 und 4921 (Klick der Schlacht) haben dasselbe Thema; der Architekt darf 4921 nach
  deiner Antwort auf F3 gegen 5180 abgleichen. 5181 bleibt eigenes Anliegen (Aufstellung).
- 4120 Schritt 1 und 2 sind Fälle von „doppelt“ aus 4040; der Organisationsentwickler darf
  sie dort einordnen und 4120 danach schließen.
- 4301 und 3900 ändern beide `standregeln/fortschritt.py` und `phasenfolge.py` samt Tests;
  der Regelumsetzer macht sie in einem Lauf. 4301 hängt zudem an der Tabelle in
  [Fortschritt](../prozess/ablauf/fortschritt.md) (Organisationsentwickler).
- 3960 und 3780 sind Hook-Code und laufen nacheinander, nicht neben 3900 und 4301.
- 4140 trägt Anliegen 4100 mit; der Architekt schließt 4100, wenn 4140 gebaut ist. 4140
  ändert kein Hook-Modul und darf neben den Hook-Strängen laufen.
- 4620 und 4040 ändern beide Dateien des Organisationsentwicklers; ein Strang, 4620 zuerst.
- Stränge Prozessphase 8: Regelumsetzer A: 3900 + 4301 (+ 4120 Schritt 1), dann 3780, dann
  3960; B daneben: 4140. Organisationsentwickler: 4620, dann 4040 mit 4120 Schritt 2 und der
  Tabelle aus 4301. Nichts davon läuft neben den Items der Technikphase.

## Fragen an dich
Mit `Annahme:` (die Arbeit läuft mit der Empfehlung weiter):
- [5180](anliegen/5180-annahmenZurBewegungsphase.md) F1: Steht „Bewegung der Einheit beenden“
  nur bei einer Einheit in Bewegung? Annahme: ja.
- 5180 F2: Zeigt die Karte beim Ziehen die letzte Stelle ohne Sperre? Annahme: ja (A).
- 5180 F3: Wählt in der Schlacht ein Klick auf ein Modell die ganze Einheit, nie ein Modell
  allein als Ebene? Annahme: A.
- 5180 F4: Wirkt ein doppelt ankommender Klick nur einmal? Annahme: A.
- [5181](anliegen/5181-klickAufEineAufgestellteEinheit.md) F1: Wählt in der Aufstellung der
  Klick auf eine aufgestellte Einheit nichts aus? Annahme: A, der Klick ändert nichts.

Ohne `Annahme:`: keine.
