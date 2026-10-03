# AUF-1-Tests: erneute Wahl der begonnenen Einheit, Gewinner nach der Zone

26 · Kritik · von Fachkritiker (Domäne) → Testautor · Runde 1/3 · offen

## Runde 1
**Befund.** In [aufstellenTest.py](../../technik/tests/akzeptanz/phasen/aufstellenTest.py) gegen
[AUF-1](../../domaene/anforderungen/phasen/aufstellen.md):
1. *Test verlangt, was das Kriterium nicht sagt:*
   `testAuf1_6DieBegonneneEinheitErneutZuWählenIstNichtGesperrt`. AUF-1.6 lautet
   „Eine wählbare *Einheit* löst die *Einheit in Aufstellung* ab, wenn von ihr kein *Modell*
   *gesetzt* ist; sonst *Sperre* ‚Einheit begonnen‘.“ Die begonnene *Einheit* ist nach 1.5
   wählbar, von der *Einheit in Aufstellung* ist ein *Modell* *gesetzt*: Wörtlich folgt die
   *Sperre*, der Test verlangt das Gegenteil. Eine Ausnahme für dieselbe *Einheit* steht
   nirgends.
2. *Fehlender Fall:* AUF-1.2 „je einmal“. Den *Gewinner* nach gewählter *Aufstellungszone*
   noch einmal zu wählen, prüft kein Test; geprüft ist das zweite Wählen nur, solange die
   Zone offen ist.

**Kosten.** Zu 1: Der Implementierer baut eine Ausnahme ohne Kriterium; die Abnahme kann sie
nicht gegen AUF-1.6 halten, und die Anforderung beschreibt das gebaute Verhalten nicht.
Fachlich ist die Ausnahme vermutlich richtig (gesperrt wird nur Regelwidriges,
[17](17-auf1-reihe-nach-dem-beenden.md) Stellungnahme 3), aber das entscheidet der
Anforderungsautor. Zu 2: Ein Gewinnerwechsel mitten in der *Aufstellung* drehte, wer *an der
Reihe* ist, und bliebe grün.

**Gegenvorschlag.**
1. Den Test aus der Umsetzung nehmen, bis AUF-1.6 den Fall regelt; widersprichst du, hebe
   ihn an den Anforderungsautor, etwa „Eine andere wählbare *Einheit* löst … ab“ oder
   „dieselbe erneut zu wählen ist keine *Sperre*“.
2. Ein Test: *Gewinner* und *Aufstellungszone* gewählt, dann `gewinnerWählen` →
   ‚nicht wählbar‘, *Gewinner* und *an der Reihe* unverändert.

Die übrigen Tests treffen ihr Kriterium; ihre Namen stehen im
[Glossar](../../domaene/glossar.md). Den Zwischenzustand von AUF-1.3 behandelt
[25](25-auf1-an-der-reihe-zwischen-gewinner-und-zone.md).

**Stellungnahme.** Offen.
