# Der Stand nennt die Prozess-Items vor dem nächsten Plan

173 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Seit `Freigabe Retro 2` (`12819fb`) meldet der Stand „Domänenphase · Anforderungsautor:
Anforderungen zu Plan 3“. Freigegeben sind aber P1 bis P5 der [Retro](../retro.md), vor
Plan 3; so schreibt es auch der Commit der Freigabe. Der Ablauf widersprach sich: Der
Regelumsetzer stand als Schritt 2 vor der Freigabe, `phasenfolge.lage` springt nach ihr
gleich in die Domänenphase. Neu: [Ablauf, Prozessphase](../../prozess/ablauf.md#prozessphase)
Schritt 5, die Prozess-Items laufen nach der Freigabe, abgeschlossen ist eins mit einem
Commit `P<k>: …`. So hat der Koordinator P1 schon committet (`6dfe473`).

**Kosten.** Bis dahin beauftragt der Koordinator nach dem Stand den Anforderungsautor, und
Plan 3 entsteht vor den Mechanismen, die auf ihn wirken sollen (Abdeckung, SonarLint in der
DoD). Der Koordinator muss den Stand jedes Mal gegen die Retro korrigieren.

**Gegenvorschlag.** In `phasenfolge.lage`, nach `Freigabe Retro <n>`:
1. Prozess-Items sind die Zeilen `- P<k> ` im Abschnitt `## Prozess-Items` von
   `handoff/retro.md`.
2. Abgeschlossen ist P<k>, wenn seit `Freigabe Retro <n>` ein Commit mit Betreff, der mit
   `P<k>:` beginnt, vorliegt; `P<k> Zwischenstand: …` zählt nicht.
3. Fehlt eins, meldet der Stand Prozessphase, Zyklus n, nächster Schritt
   „Regelumsetzer: Prozess-Item P<k> aus Retro n (Commit `P<k>: …`)“, das erste offene
   zuerst. Der Betreff im Text sagt dem Koordinator die Konvention, ohne seine Definition zu
   ändern.
4. Sind alle abgeschlossen oder hat die Retro keine, gilt wie heute die Domänenphase mit
   Plan n+1.
Anliegen aus der Kritik an einem Item (heute 170 bis 172 zu P1) halten den Schritt nicht
auf; sie nennt der Stand ohnehin unter „Dran“.

Scheiter-Tests: Retro mit P1 und P2, Freigabe, Commit `P1: …`: Stand nennt P2. Dazu
`P2 Zwischenstand: …`: weiter P2. Dazu `P2: …`: Domänenphase Plan n+1. Retro ohne Abschnitt
`## Prozess-Items`: gleich Domänenphase. Ein Commit `P1: …` vor der Freigabe zählt nicht.

`prozess/regeln.md` nennt den Mechanismus; „nur Text“ im Ablauf ersetze ich. Wirkt sofort
auf Zyklus 3 (P2 bis P5 offen), daher vor den übrigen Teilen von
[167](167-freigabefeldKommentareImStand.md); mit dessen Teil 1 teilt es `phasenfolge.lage`.

Erledigt, wenn die Scheiter-Tests so ausgehen, der Stand heute „Regelumsetzer: Prozess-Item
P2 aus Retro 2“ nennt, `python3 -m pytest prozess/pruefungen` grün ist und der Reviewer den
Code geprüft hat ([Kritik am Code](../../prozess/ablauf.md#kritik-am-code)).

**Stellungnahme.**
