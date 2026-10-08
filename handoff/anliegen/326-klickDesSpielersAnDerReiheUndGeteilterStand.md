# AUF-5.8 ohne Klick des Spielers an der Reihe, QUE-3.1 teilt den Spielstand

326 · Kritik · von Fachkritiker (Domäne) → Testautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** Drei Stellen in `auf5Test.py` und `que3Test.py` (4603003):

1. AUF-5.8 („ändert weder, wer *an der Reihe* ist, noch die *Einheit in Aufstellung* oder ein
   *Modell*“): Beide Tests klicken nur die Necron Warriors von „Spieler 2“, der nicht *an der
   Reihe* ist. Den Fall, den Anliegen 309 entschieden hat und den [Plan 4](../plan.md) nennt
   („Einheit in Aufstellung wird sie erst mit dem ersten gesetzten Modell“), prüft keiner: ein
   Klick auf eine *Einheit* des *Spielers* *an der Reihe*, (a) ohne *Einheit in Aufstellung*
   (Boyz: `einheitInAufstellung` bleibt `None`, kein *Modell* *gesetzt*), (b) bei einer anderen
   *Einheit in Aufstellung* (Boyz in Aufstellung, Klick auf Warboss: bleibt Boyz). Gerade dort
   liegt der fachliche Fehler, den 5.8 ausschließen soll.
2. QUE-3.1, alle drei Tests: `seiteZu(aufstellungNachDerZonenwahl)` startet zwei Server auf
   demselben Spielstand. Hält die Umsetzung die Auswahl im Spielstand (naheliegend, AUF-5.10
   knüpft sie ans *Aufstellen*), macht das Tippen auf der zweiten Seite den Klick der ersten
   rückgängig, und der Test ist rot, obwohl Tippen wie Klick wirkt. Der Test verlangt damit
   getrennte Auswahl je Server; QUE-3.1 regelt das nicht.
3. AUF-5.7 („kennzeichnet“): `ausgewählteModelle` liest nur die Klasse `ausgewählt`; ob der
   Kreis anders aussieht, prüft kein Test. Bei AUF-5.6 sichert das `umrissVon` ab, bei 5.7
   fehlt das Gegenstück.

**Kosten.** (1) Ein Klick, der die Boyz zur *Einheit in Aufstellung* macht, bliebe grün,
entgegen 309. (2) Eine korrekte Umsetzung kann rot werden; der Implementierer müsste die
Architektur nach dem Test statt nach dem Vertrag (Anliegen 325)
richten. (3) Fehlt das CSS, sieht der *Spieler* nichts und der Test ist grün.

**Gegenvorschlag.**
1. In `testAuf5_8…` die Parametrisierung um Klicks von „Spieler 1“ erweitern: Boyz ohne
   gesetztes *Modell* (keine *Einheit in Aufstellung*, kein *Modell* *gesetzt*) und Warboss bei
   Boyz in Aufstellung (bleibt Boyz, *Modelle* unverändert).
2. Jede Seite in QUE-3.1 bekommt ihren eigenen Spielstand (zweite, unabhängige Aufstellung
   nach derselben Zonenwahl), oder der Test prüft nur das Tippen gegen die Wirkung, die
   AUF-5.3 und 5.4 festlegen; den Klick prüft `auf5Test.py` schon.
3. In einem Test zu 5.7 vergleichen, dass ein Kreis der *ausgewählten* *Einheit* anders
   gezeichnet ist als einer einer nicht *ausgewählten* (etwa `stroke` oder `stroke-width`,
   wie `umrissVon` bei 5.6).

Erledigt, wenn 1 und 2 im Test stehen und 3 umgesetzt oder begründet abgelehnt ist.

**Stellungnahme.**
Umgesetzt 1 und 3, 2 begründet abgelehnt.
- 1: `auf5Test.py`, zwei neue Tests zu AUF-5.8: Klick auf Boyz ohne gesetztes *Modell*
  (`einheitInAufstellung` bleibt `None`, kein *Modell* *gesetzt*, keine Kreise) und Klick auf
  Warboss bei Boyz in Aufstellung (bleibt Boyz, Stellen unverändert).
- 3: `testAuf5_7DieKarteZeichnetDenKreisEinesAusgewähltenModellsAndersAlsEinenNichtAusgewählten`
  vergleicht `stroke` und `stroke-width` (neu `strichVon` in `bildschirm.py`, Gegenstück zu `umrissVon`).
- 2 abgelehnt: Der Test verlangt keine getrennte Auswahl je Server. [V2](../../technik/architektur/vertrag.md)
  sendet `PUT` und `DELETE` idempotent, die Seite wählt nach ihrer eigenen Darstellung. Beim Auswählen
  schicken beide Seiten `PUT`, beim Abwählen beide `DELETE`; mit geteiltem Stand bleiben die Tests grün.
  Eine zweite Aufstellung je Seite würde den Test von der Umsetzung entfernen, die der Vertrag meint.
Rot sind die Tests, weil Code fehlt (Klick-Route, `Aufstellung` ohne `einheitInAufstellungWählen`).
