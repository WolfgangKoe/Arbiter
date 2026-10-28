# Moderation

Stand: Review 8 wartet auf deine Freigabe ([Plan 8](plan.md), [Review 8](review.md)). Kein
offenes Anliegen hält sie auf; die 30 offenen warten alle auf spätere Phasen.

## Dran
Blockiert das Inkrement: nichts.
- Stakeholder: Freigabe Review 8; Fragen unten.
- Anforderungsautor, Domänenphase 9: [4261](anliegen/4261-lueckenImNormalMoveFuerSpaeter.md),
  [5520](anliegen/5520-bewegungsphaseFuerSpaeter.md),
  [6240](anliegen/6240-abwaehlenInDerSchlacht.md),
  [6300](anliegen/6300-anklickenUndFremdesModellLoslassen.md),
  [4881](anliegen/4881-datenblaetterImGlossarUndInDenDaten.md).
- Planer, Domänenphase 9: [5521](anliegen/5521-etappe2SperrtNichtMehrUeberB.md),
  [4882](anliegen/4882-itemKatalogwerteGliedern.md).
- Ux, Domänenphase 9: [5542](anliegen/5542-mockupBewegungGanzeEinheitAusgewaehlt.md).
- Testautor, Technikphase 9: [4901](anliegen/4901-ebeneImTestnamenUndKlickAufDenAnderenSpieler.md),
  [4921](anliegen/4921-klickUndHandgriffeDerSchlachtFuerSpaeter.md),
  [5241](anliegen/5241-sperrmeldungBeimNaechstenZiehenUndKlickInDerAufstellung.md),
  [5781](anliegen/5781-bewegungstestsAblageFuerSpaeter.md),
  [6241](anliegen/6241-bewegungOhneTestZuQue1_3UndAuf8_7.md),
  [6340](anliegen/6340-namenDerTestsZu6291.md).
- Implementierer, Technikphase 9: [5380](anliegen/5380-testmodellUndKopierteWerteImKatalogtest.md),
  [5701](anliegen/5701-gegnerUndTestnameDerSchlacht.md),
  [6102](anliegen/6102-ablageDerBewegungFuerSpaeter.md),
  [6122](anliegen/6122-normalMoveDoppeltesUndUnklares.md),
  [6290](anliegen/6290-reviewNachbauUndDistanz.md).
- Architekt, Technikphase 9: [5000](anliegen/5000-vertragAufstellenGekuerztUndVoll.md).
- Reviewer, Technikphase 9: [6361](anliegen/6361-review8LinksBelegeKlickpfad.md).
- Regelumsetzer, Prozessphase 8: [3780](anliegen/3780-restePruefcodeNach3301.md),
  [3900](anliegen/3900-standNenntFalscheRolleFuerProzessItems.md),
  [3960](anliegen/3960-pythonOhneStrichUndLueckenInRegeln.md),
  [4120](anliegen/4120-hindernisformatInAblaufUndRegeln.md),
  [4140](anliegen/4140-architekturAlsReiterBisZuDenDateien.md),
  [4301](anliegen/4301-fortschrittFuerItemOhneKriterium.md).
- Organisationsentwickler, Prozessphase 8: [4620](anliegen/4620-kuerzelJePhaseInDerDomaene.md),
  [4040](anliegen/4040-ablaufUndRegelnVerschlanken.md).

## Vorschläge
- 6240, 5520 (F3 Ebene in der Schlacht) und 6300 haben dasselbe Thema: Auswahl, Abwählen und
  Klick in der Schlacht. Der Anforderungsautor darf sie in einem Lauf bearbeiten und die
  Fragen an dich in einem Anliegen bündeln. 4921 (Architekt/Testautor) gehört dazu.
- 4261, 5520 Punkt 1 und 5521 betreffen Advance, Zurücksetzen und die Wahl der Bewegung;
  der Anforderungsautor darf sie zusammenlegen, der Planer zieht 5521 danach nach.
- 4261 trägt dein `Kommentar:`: Die Umbenennung von „Normal Move“ (Item heißt
  normalMove, Anforderungen „Normale Bewegung“) ist zu beachten; der Anforderungsautor darf
  das beim Bearbeiten einbeziehen, es geht meinen Vorschlägen vor.
- 4901 Punkt 1, 5241 und 6340 sind Testnamen und Testlücken desselben Testautors; ein Lauf.
- 6102, 6122, 6290 und 5701 ändern dieselben Domänenmodule (Bewegung, messen); der
  Implementierer macht sie in einer Kette, 6290 zuerst.
- 4120 Schritt 1 und 2 sind Fälle von „doppelt“ aus 4040; der Organisationsentwickler darf sie
  dort einordnen, der Regelumsetzer führt Schritt 1 aus; dann kann 4120 schließen.
- 4301 und 3900 ändern beide `standregeln/fortschritt.py`; ein Lauf des Regelumsetzers.
- Stränge Prozessphase 8: Regelumsetzer A: 3900 + 4301, dann 3780, dann 3960; B daneben:
  4140 (kein Hook-Modul). Organisationsentwickler: 4620, dann 4040. Domänenphase 9:
  Anforderungsautor, Planer und Ux laufen getrennt nebeneinander (getrennte Dateien).

## Fragen an dich
Mit `Annahme:` (die Arbeit läuft mit der Empfehlung weiter):
- [5181](anliegen/5181-klickAufEineAufgestellteEinheit.md) F1: Wählt in der Aufstellung der
  Klick auf eine aufgestellte Einheit nichts aus? Annahme: A, der Klick ändert nichts.

Ohne `Annahme:`:
- [4882](anliegen/4882-itemKatalogwerteGliedern.md) F1: Kommt das Item Katalogwerte gliedern
  als erstes Item von Plan 9 (A) oder erst in Etappe 8 (B)? Empfehlung: A. Eine Antwortzeile
  fehlt dort; trage sie im Anliegen ein.
