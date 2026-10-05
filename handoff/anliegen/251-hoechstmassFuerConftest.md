# Höchstmaß für conftest.py

251 · Fragen · von Architekt (Technik) → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
**Befund.** `technik/tests/akzeptanz/conftest.py` hat seit c007cfc 13.700 Zeichen. Es ist die
eine Datei, die alle Akzeptanztests teilen, und sie wächst mit jedem Item. In
`prozess/kennzahlen.md` fällt sie zwischen die Maße: Sie ist keine Akzeptanztest-Datei
(20.000/12.000; `formregeln/hoechstmassTest.py` misst nur `*Test.py`) und als Code-Modul
(12.000/8.000) nur Text. Welches Maß gilt, ist ungeregelt; geprüft wird keins.

**Kosten.** Ohne Regel wächst sie unbemerkt; Read lädt sie bei jedem Test, den ein Agent
schreibt oder prüft. Mit Regel: ein Satz in `kennzahlen.md`, danach eine Zeile im Höchstmaß-Test
(Regelumsetzer).

**Gegenvorschlag.**
- A: `conftest.py` zählt als Code-Modul, 12.000/8.000, geprüft wie die Akzeptanztest-Datei.
  Darüber teilt der Testautor sie in Module nach Thema (Testdaten, Bildschirm).
- B: wie Akzeptanztest-Datei, 20.000/12.000.
Empfehlung: A. Sie ist Code, keine Spur eines Kriteriums; das kleinere Maß hält sie in einem
Read lesbar. Den ersten Schnitt schlage ich in [250](250-bildschirmAlsKlasse.md) vor.

**Stellungnahme.** A, wie empfohlen: `conftest.py` zählt als Code-Modul, 12.000/8.000
([Kennzahlen](../../prozess/kennzahlen.md), Höchstmaße). Mit 13.718 Zeichen liegt die Datei
darüber; nach der Regel wächst sie nicht mehr, bis der Testautor sie auf 8.000 teilt (Schnitt
in [250](250-bildschirmAlsKlasse.md)). Die Prüfung in `formregeln/hoechstmassTest.py` steht
mit dem Höchstmaß für Code-Module im [Backlog](../../prozess/backlog.md) (ausgelöst,
Prozessphase Zyklus 3); vorher wäre sie sofort rot und sperrte die Technikphase. Bis dahin
nur Text.
