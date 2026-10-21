# Moderation

Stand vor „Freigabe Retro 6“. Nichts in [Plan](plan.md) ist blockiert; die [Retro](retro.md)
wartet nur auf deine Freigabe. Danach folgen P1 bis P5.

## Dran
- Stakeholder: Anliegen 1860 F1 bis F3 (unten),
  dann „Freigabe Retro 6“. Deine Prüfung von 1640 ist abgeschlossen (erledigt).
- Organisationsentwickler: [1670](anliegen/1670-anliegenboardNachPhasen.md),
  [1660](anliegen/1660-regelkommentareEntbehrlich.md),
  Anliegen 1581,
  Anliegen 1591,
  [740](anliegen/740-commitFuerMehrereItemsImAblauf.md),
  [1570](anliegen/1570-mutationstestsEffizienter.md),
  [1740](anliegen/1740-mutationsschwelleAlsUntereGrenze.md),
  Anliegen 1751: alle Prozessphase,
  also nach der Freigabe. Nachprüfung fällig: Anliegen 1671
  (F1, F2 beantwortet, dein Kommentar dort verlangt eine Klärung zur Kritik am Inkrement),
  Anliegen 730.
- Regelumsetzer: Anliegen 490 zuerst (hält 421 und
  991), Anliegen 1790,
  Anliegen 991,
  [1070](anliegen/1070-wartendeNachpruefungIstNichtFaellig.md).
- Testautor: Nachprüfung [1320](anliegen/1320-kreuztDieStreckeEineBaseUndLiegtDasZielFrei.md)
  (Antwort Ja steht); AUF-22, 23, 27, 13, 11, 16.7, 18.7, 3.9, QUE-5 bis 7 warten auf ihn.
- Anforderungsautor: Nachprüfung [1400](anliegen/1400-nahkampfreichweiteBeimLoslassen.md)
  (Antwort Ja steht).
- Wartend (Domänenphase 7): 978, 1213, 1362, 1400, 1480, 1541, 1610, 1653, 1655, 1820;
  (Technikphase 7): 1750, 1752, 1761; dazu 1191 auf 1213, 1651 auf 1655, 1654 auf 1653,
  421 auf 490.

## Vorschläge
- Organisationsentwickler, ein Lauf Mutation: 1740, 1751 und 1570 (dieselbe DoD-Stelle,
  P2); 1751 ergänzt nur einen Satz in 1740.
- Organisationsentwickler, P1: 1581, 1591, 740, 730; 1660 ist P5 (Regelumsetzer), 1670 P4.
- Regelumsetzer: 490, 991, danach 421; 1790 getrennt davon.
- Anforderungsautor (Domänenphase 7): 1400 mit 1820 (Anhalten an der ersten Base, nach
  deinem Kommentar in 1320 erst im nächsten Zyklus), dazu 978, 1610, 1653.
- Architekt/Planer: 1362 und 1541 (Höchstmaß); 1653, 1654, 1655 als Items.
- Nur Entscheidungen ablegt: 1070 deckt sich mit
  [Ablauf, Prozessphase](../prozess/ablauf.md#prozessphase); der Regelumsetzer prüft, ob er
  erfüllt ist und schließt.
- Erledigt, nichts mehr zu tun: 1640, 1840, 1841, 1850.
- Stränge ([Ablauf](../prozess/ablauf.md#gleichzeitige-läufe)): Prozessphase
  Organisationsentwickler (P1, Regeltexte) und Regelumsetzer (Prüfcode: 490, 991, P2 bis P5)
  laufen getrennt, doch höchstens einer ändert Hook-Code. Implementierer-Strang
  (1752, 1761, 1750) hat getrennte Dateien. Die Kritiker laufen gleichzeitig.

## Fragen an dich
Mit Annahme zuerst:
1. Anliegen 1860 F1: Wie viele TODOs im Code?
   Annahme: drei (Empfehlung A).
2. 1860 F2: Welche Werkzeugkommentare bleiben? Annahme: feste Liste mit Regelcode (A).
3. 1860 F3: Wer entfernt die 58 `Regel:` und 100 `Warum:`? Annahme: nach A, in der
   Technikphase 7, ohne dass Items blockieren.

Offen ohne Annahme: keine. Deine Antworten in 1320, 1400, 1671 und 730 stehen.
