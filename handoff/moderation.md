# Moderation

Stand vor „Freigabe Review 6“. Nichts in [Plan](plan.md) ist blockiert: alle Items sind
gebaut; [Review 6](review.md) nennt SonarLint ohne Funde. Danach beginnt die Prozessphase.

## Dran
- Stakeholder: [1640](anliegen/1640-basesBlitzenNachDemLoslassen.md) prüfen (der
  Implementierer meldet es bereit, du hältst es auf „offen“); Fragen unten.
- Organisationsentwickler: [1671](anliegen/1671-prozessphaseVorziehen.md) (F1 mit A
  beantwortet, F2 offen); nach „Freigabe Retro 6“ die Prozess-Items P1 bis P5 der
  [Retro](retro.md).
- Implementierer: [1640](anliegen/1640-basesBlitzenNachDemLoslassen.md) (Rückmeldung
  steht), [1752](anliegen/1752-stellePrueftFractionSelbst.md),
  [1761](anliegen/1761-loslassenOhneAntwortBleibtInDerVorschau.md),
  [1750](anliegen/1750-testLegtFestWasAuf27AndersRegelt.md) (alle drei Technikphase 7).
- Regelumsetzer: [490](anliegen/490-fortschrittInPlanReviewRetro.md) zuerst, es hält 421,
  991 und den Fortschritt der Retro auf.
- Testautor: [1320](anliegen/1320-kreuztDieStreckeEineBaseUndLiegtDasZielFrei.md): dein
  Kommentar fragt „Was wäre die richtige Antwort?“; die Antwort steht noch aus.
- Wartend (Prozessphase): 730, 740, 991, 1070, 1570, 1581, 1591, 1660, 1670, 1740, 1751.
  Wartend (Domänenphase 7): 978, 1213, 1362, 1400, 1480, 1541, 1610, 1653, 1655; 1191
  auf 1213, 1651 auf 1655, 1654 auf 1653, 421 auf 490.

## Vorschläge
- Zusammen (Organisationsentwickler, ein Lauf): [1740](anliegen/1740-mutationsschwelleAlsUntereGrenze.md),
  [1751](anliegen/1751-gleichwertigeMutantenNichtUmDasWerkzeugBauen.md) und
  [1570](anliegen/1570-mutationstestsEffizienter.md): dieselbe DoD-Stelle (Mutation).
  1751 ergänzt nur einen Satz zur Empfehlung in 1740.
- Zusammen (Organisationsentwickler): [1581](anliegen/1581-erledigtVomEmpfaengerUndRuffFormatOhneRegel.md)
  und [1591](anliegen/1591-erledigtSetztDerEmpfaenger.md) (Empfänger setzt nie `erledigt`),
  dazu [740](anliegen/740-commitFuerMehrereItemsImAblauf.md) und
  [730](anliegen/730-werKritisiertUndZurueckgenommeneRegeln.md): alle in P1.
  [1660](anliegen/1660-regelkommentareEntbehrlich.md) ist P5, [1670](anliegen/1670-anliegenboardNachPhasen.md) P4.
- Zusammen (Regelumsetzer): 490 und 991, danach 421.
- Zusammen (Anforderungsautor, Domänenphase 7): 1400 und 1320 (dieselbe Frage zum
  Anhalten, Kommentar „wie ArbiterMap, Anforderungen erst im nächsten Zyklus“), dazu 978
  und 1610.
- Zusammen (Architekt/Planer): 1362 und 1541 (Höchstmaß), 1653, 1654 und 1655 als Items.
- Nur Entscheidungen ablegt: 1070 (Wartende sind nicht fällig) deckt sich mit
  [Ablauf, Prozessphase](../prozess/ablauf.md#prozessphase); der Organisationsentwickler
  prüft, ob er bereits erfüllt ist und der Regelumsetzer schließen kann.
- Schließen: nichts jetzt. 1640 schließt du nach der Prüfung (Status bei dir).
- Stränge ([Ablauf](../prozess/ablauf.md#gleichzeitige-läufe)): Prozessphase
  Organisationsentwickler (P1) und Regelumsetzer (490, 991, P2 bis P5) getrennt;
  Implementierer-Strang (1752, 1761, 1750) hat getrennte Dateien.

## Fragen an dich
Mit Annahme zuerst:
1. [1320](anliegen/1320-kreuztDieStreckeEineBaseUndLiegtDasZielFrei.md) F1: Hält ein
   Modell an einer Base an, die seine Strecke kreuzt? Annahme: Nein (Tests bleiben).
2. [1671](anliegen/1671-prozessphaseVorziehen.md) F2: Wohin gehen Lücken aus dem
   Mutationslauf? Empfehlung A (Technikphase 7 für Tests und Code). Dein Kommentar dort
   fordert Kritik an einem fehlerhaften Inkrement; das ist keine Antwort auf F2.

Ohne Annahme:
3. [1400](anliegen/1400-nahkampfreichweiteBeimLoslassen.md) F1: Neues Kriterium in AUF-12
   (Modelle zurück, Grund nennen)? Empfehlung: ja; dein Kommentar in 1320 verschiebt
   Anforderungen auf den nächsten Zyklus.
