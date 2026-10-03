# AUF-1.6: die begonnene Einheit erneut wählen

41 · Kritik · von Fachkritiker (Domäne) → Anforderungsautor · Runde 1/3 · offen

## Runde 1
**Befund.** [AUF-1.6](../../domaene/anforderungen/phasen/aufstellen.md) lautet „Eine wählbare
*Einheit* löst die *Einheit in Aufstellung* ab, wenn von ihr kein *Modell* *gesetzt* ist; sonst
*Sperre* ‚Einheit begonnen‘.“ Offen ist der Fall, dass die *Spieler* die *Einheit in Aufstellung*
selbst noch einmal wählen, nachdem ein *Modell* von ihr *gesetzt* ist. Sie ist nach AUF-1.5
wählbar; wörtlich folgt die *Sperre*, obwohl nichts abgelöst wird. Das [Ziel](../../domaene/ziel.md)
sperrt nur, „was nicht erlaubt ist“, und die Regel (`core_rules.txt:2322`) verbietet nichts, wenn
dieselbe *Einheit* weiter aufgestellt wird. Der Test, der hier „keine *Sperre*“ verlangte, ist
deshalb aus [aufstellenTest.py](../../technik/tests/akzeptanz/phasen/aufstellenTest.py)
gestrichen; jetzt regelt den Fall weder Kriterium noch Test.

**Kosten.** Der Implementierer entscheidet den Fall ohne Kriterium, die Abnahme kann ihn an
nichts halten. Mit Touch ist erneutes Antippen der *Einheit in Aufstellung* alltäglich; eine
*Sperre* ‚Einheit begonnen‘ dort meldet einen Fehler, den es nach der Regel nicht gibt.

**Gegenvorschlag.** AUF-1.6 ergänzen, etwa: „Eine andere wählbare *Einheit* löst die *Einheit in
Aufstellung* ab, …; dieselbe erneut zu wählen ändert nichts.“ Oder ausdrücklich die *Sperre*
festhalten, falls das gewollt ist. Danach ergänzt der Testautor den Test.

**Stellungnahme.** Offen.
