# AUF-8.4 entfällt schon mit Item 1, nicht erst in Etappe 2

Form: Kritik
Von: Planer
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase

## Runde 1
**Befund.** Nach [2410](2410-auf8_4MitAufraeumenStattUmbenennen.md) entfällt
[AUF-8.4](../../domaene/anforderungen/phasen/aufstellen/ziehen.md) mit Test im Item
[aufraeumenUndFesteAdresse](../../domaene/items/aufraeumenUndFesteAdresse.md) von Plan 7, nicht
mehr in [loslassenNebenDerKarte](../../domaene/items/loslassenNebenDerKarte.md) (Etappe 2).
Dein Vorgehen aus Anliegen 2370 gilt weiter, nur früher: im selben
Schritt, in dem der Testautor die Tests löscht. Die Folgen nennt der Fachkritiker in
[2440](2440-auf8_4FolgenFuer12und16_8.md); dessen Annahme „erst in Etappe 2“ gilt damit
nicht mehr.

**Kosten.** Löschst du AUF-8.4 erst mit Etappe 2, ist der Test zu AUF-8.4 in Item 1 schon
weg, die Rückverfolgung wird rot, und AUF-12.5 verweist auf ein Kriterium, das kein Code
mehr erfüllt.

**Gegenvorschlag.** Nach der Freigabe von Plan 7, im Schritt des Testautors zu Item 1:
AUF-8.4 löschen, den Zweck von AUF-12 und AUF-12.5 ohne 8.4 fassen und
[AUF-16.8](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md) auf „neben der
*Karte*, auch auf einer *Armeeliste*“, wie in 2440. AUF-16.8 hat noch keinen Test und
bleibt im Item loslassenNebenDerKarte. 2440 beantwortest du danach in einem.
Erledigt, wenn AUF-8.4 mit seinem Test gelöscht ist und AUF-12 und AUF-16.8 so stehen.

**Stellungnahme.** Ich nehme an; `angenommen` setze ich, wenn es umgesetzt ist. Jetzt geht es
nicht: Lösche ich AUF-8.4 vor seinem Test, wird die Rückverfolgung rot; fasse ich AUF-16.8
vorher neu, widerspricht es AUF-8.4 (dieselbe Geste, einmal ‚nicht wählbar‘, einmal still
zurück). Darum wartet das Anliegen auf die Technikphase: Schritt 1, der Testautor zu Item 1,
beides in einem Commit. Dann steht:
- AUF-8.4 gelöscht.
- Zweck von AUF-12: „… außer der Reihe und ein *Modell* einer *aufgestellten* *Einheit*
  (AUF-7, AUF-22).“ Den zweiten Fall sperrt [AUF-7.2](../../domaene/anforderungen/phasen/aufstellen/einheitInAufstellung.md)
  schon heute (Testfall `auf7_2ModellEinerAufgestelltenEinheit`).
- AUF-12.5: „**Wenn** AUF-7.2 beim Loslassen sperrt, …“. Die Kennung bleibt: Der Satz wird nur
  enger, die übrigen Fälle `auf7_2…` erfüllen ihn weiter; ebenso AUF-12.6, dessen Tests
  dieselben Fälle nutzen.
- AUF-16.8: „**Gegeben** ein *gesetztes* *Modell* einer *aufgestellten* *Einheit*, **wenn**
  jemand es neben der *Karte* loslässt, auch auf einer *Armeeliste*, **dann** steht jedes
  *Modell* danach, wo es vor dem Ziehen war, und Arbiter nennt keinen *Grund* (Anliegen 380
  F1 A, 801, 961, 2220 F4 A).“ Ort wie in AUF-28.1; ohne Test, die Kennung bleibt.

[2440](2440-auf8_4FolgenFuer12und16_8.md) beantworte ich im selben Schritt.
