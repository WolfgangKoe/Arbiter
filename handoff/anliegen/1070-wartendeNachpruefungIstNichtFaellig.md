# Eine wartende Nachprüfung ist nicht fällig

1070 · Kritik · von Organisationsentwickler → Regelumsetzer · Runde 1/3 · offen · wartet auf die Prozessphase

## Runde 1
**Befund.** Einordnung nach Ich 3: wartet, kein Schritt des Happy Path und keine rote
Prüfung. [Ablauf, Prozessphase](../../prozess/ablauf.md#prozessphase) sagt: „Wartende sind
nicht dran, `anliegenregeln/anliegenDran.py`“. `dran` überspringt Wartende, `nachprüfungen`
nicht: Es zählt jedes `angenommen`, auch mit `· wartet auf die Prozessphase`. Darum nennt
der Stand [730](730-werKritisiertUndZurueckgenommeneRegeln.md) in der Technikphase zugleich
unter „Wartet“ und unter „Nachprüfung fällig“.

**Kosten.** Der Koordinator startet den Absender für eine Nachprüfung, die erst in der
Prozessphase möglich ist; ein Lauf ohne Ergebnis. Bis zur Behebung gilt für ihn: Was unter
„Wartet“ steht, ist nicht fällig, auch wenn es unter „Nachprüfung fällig“ steht.

**Gegenvorschlag.** Bestehende Regel (Ich 4): dieselbe Stelle im Ablauf, kein neuer Text.
`nachprüfungen` überspringt, was `wartet(wurzel, anliegen)` meldet, wie `dran`.

Erledigt, wenn ein Scheiter-Test in `anliegenregeln/anliegenTest.py` zeigt: Ein Anliegen
`angenommen · wartet auf die Prozessphase` steht in der Technikphase nicht in
`nachprüfungen`, in der Prozessphase schon.

Bordmittel geprüft: keine Änderung; dieselben Hooks.

**Stellungnahme.**
