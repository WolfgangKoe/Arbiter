# Vorrücken wird beim Klick zweimal geprüft

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Wartet: Vereinfachung und ungeprüfte Sperre abseits des Happy Path. Nach 13260
entscheidet `Bewegungsphase.vorrückenAngeboten` BEW-5.1 und BEW-22.1 allein, richtig so.
`Schlacht.vorrücken` in
[schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) prüft aber
erst `self.vorrückenAngeboten` und ruft dann `vorrückenBeginnen`, das in
[bewegung/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/bewegung/__init__.py) dieselbe
Prüfung noch einmal macht. Folge: Die Prüfung in `vorrückenBeginnen` entscheidet nie, und kein
Test belegt sie. Probe auf einer Kopie in `/tmp`: Mit `if True:` statt der Prüfung in
`vorrückenBeginnen` bleiben alle Einheitstests und alle Akzeptanztests der Bewegungsphase
grün (739, ohne Fliegen). Alle Einheitstests rufen `vorrückenBeginnen` mit `gegner = {}` auf;
ob die neuen Parameter ankommen, prüft keiner. Die Mutationsprüfung merkt es nicht, sie
erzeugt für einen reinen Aufruf als Bedingung keinen Mutanten. Am Bildschirm ändert sich
nichts.

**Kosten.** Implementierer, etwa 10 Minuten: `Schlacht.vorrücken` wird kürzer, ein
Einheitstest kommt dazu.

**Gegenvorschlag.** `Schlacht.vorrücken` reicht nur weiter, wie es 13260 für das Angebot
festlegt: `einheit = self._einheitMitGrenzen()`, ist sie nicht `None`,
`self._bewegungsphase.vorrückenBeginnen(einheit, self._stellen, self._stellenDesGegners())`.
In [bewegungTest.py](../../technik/tests/einheit/domaene/phasen/bewegungTest.py) ein Fall:
Mit einem *Modell* in *Nahkampfreichweite* wartet die *Einheit* nach `vorrückenBeginnen`
nicht auf ihren Vorrückwurf.

**Stellungnahme.**
