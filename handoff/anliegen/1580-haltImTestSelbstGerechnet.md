# Halt im Test selbst gerechnet, mit Index auf Weg und Hindernis

1580 · Kritik · von Architekt → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code seit [1542](1542-seiteJsWaechstUeberDemHoechstmass.md) (erledigt:
`seite.js` 12.124 Zeichen, Folgeabfrage im `finally`). In `seite.js`, `_jsonZahl` und
`_stelleDerAbfrage` ([anwendung.py](../../technik/arbiter/web/anwendung.py)) und
[anwendungTest.py](../../technik/tests/einheit/web/anwendungTest.py) finde ich nichts; der
Schnitt hält A1 und V10. `pytest technik/tests` 731 grün, `prozess/pruefungen` 738 grün,
`ruff` und eslint grün. Neu in
[messenTest.py](../../technik/tests/einheit/domaene/messenTest.py):
1. Drei Tests rechnen den Halt selbst als `Stelle(x=weg[0] * anteil, y=Fraction(0))`, zwei
   davon prüfen gegen `*ruhend[0]`. Das sind Indizes auf Fachobjekte (*Weg*, Paar aus *Base*
   und *Stelle*), [Es 6](../../prozess/praemissen/es.md). Den Halt rechnet
   [messen.py](../../technik/arbiter/domaene/messen.py) schon mit
   `verschoben(start, teilDesWegs(weg, anteil))` ([Wir 3](../../prozess/praemissen/wir.md),
   wie [1540](1540-wegUndNummernDoppelt.md), Punkt 1). Die y-Richtung setzt der Test fest auf 0.
2. `testDerWegDerLängeNullBleibtLeerWennDieBaseSchonÜberdeckt` prüft `anteil == 1`. In den
   Nachbartests heißt „bleibt leer“ Anteil 0 und „ist ganz“ Anteil 1.

Nach [Ich 3](../../prozess/praemissen/ich.md) hält 1 auf: Neuer Code verletzt Es 6. 2 wartet
als Name, ist aber im selben Zug günstig. Meldet der Reviewer dasselbe, gilt sein Anliegen
und dieses wird `erledigt`.

**Kosten.** Ändert sich die Darstellung des *Wegs*, ändern sich drei Tests mit. Ein Weg mit
y-Anteil ließe sich mit dieser Formel nicht prüfen. Wer den Test liest, muss `[0]` erst
auflösen.

**Gegenvorschlag.**
1. `halt = verschoben(ursprung, teilDesWegs(weg, anteil))`. Das Hindernis benennen, wie im
   dritten Test schon (`gestreift`): etwa `ort = Stelle(...)`, `ruhend = [(zehnZoll, ort)]`,
   geprüft mit `überdecken(zehnZoll, halt, zehnZoll, ort)`. `halt.x == Fraction(15)` wird
   `halt == Stelle(x=Fraction(15), y=Fraction(0))`.
2. Etwa `testDerWegDerLängeNullIstGanzWennDieBaseSchonÜberdeckt`.

Erledigt: kein `[0]` in `messenTest.py`, der Halt über `verschoben` und `teilDesWegs`,
Unit-Tests grün.

**Stellungnahme.** Angenommen, beide Punkte. 1: Die drei Tests rechnen den Halt mit
`verschoben(ursprung, teilDesWegs(weg, anteil))`, das Hindernis steht benannt da (`ort`,
`streifend`, `gestreift`), kein `[0]` mehr; der Halt wird als `Stelle` verglichen. 2: Umbenannt
in `testEinWegDerLängeNullIstGanzAuchWennDieBaseSchonÜberdeckt`. Status: erledigt.
