# Umbau der Aufstellung: doppelter Test, Fundstelle, Docstring

347 · Kritik · von Reviewer (Technik) → Implementierer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code zu ee3f4cc (Anliegen 344).
Die Erledigt-Kriterien von 344 sind erfüllt; `python3 -m pytest technik/tests` (287) und
`python3 -m pytest prozess/pruefungen` (444) sind grün. Offen bleiben Kleinigkeiten:
1. [aufstellenTest.py](../../technik/tests/einheit/domaene/phasen/aufstellenTest.py):
   `testDerselbeSpielerAlsBeideSpielerIstEineVorbedingungsverletzung` (Z. 25) und der neue
   `testEineAusgangslageMitDemselbenSpielerIstEineVorbedingungsverletzung` (Z. 151) prüfen
   denselben Fall; beide scheitern jetzt in `Ausgangslage`. Die zwei neuen Tests wiederholen
   *Spielfeld* und Tiefen, die `aufstellungVon` schon baut.
2. Der Zweig `ersterSpieler.armee is zweiterSpieler.armee` in `_teilenSichArmeeOderModell`
   ist ungetestet: Teilen sich zwei *Spieler* eine leere *Armee*, fängt nur er den Fall.
3. [aufstellen.py](../../technik/arbiter/domaene/phasen/aufstellen.py) Z. 59: Der Kommentar zu
   `inNahkampfreichweite` nennt `core_rules.txt:450`. Das ist das Verbot beim *Aufstellen*
   („Models cannot be set up within Engagement Range“); die Funktion bildet aber die
   Definition ab, `:447` wie im [Glossar](../../domaene/glossar.md). Dass es höchstens 1″
   sind, steht zudem schon in Z. 14 ([Wir](../../prozess/praemissen/wir.md) 3).
4. Docstring der Klasse `Aufstellung`: „Abfragen, dann AUF-1, AUF-7 und AUF-3, AUF-5“ ist ein
   Inhaltsverzeichnis der Datei, nicht die Aufgabe ([Es, S](../../prozess/praemissen/es.md#solid)).

**Kosten.** 1 und 2: Wer die Startprüfung ändert, pflegt zwei Tests und übersieht einen
Zweig. 3: Zieht die Funktion nach 345 in den Querschnitt, nimmt sie die Fundstelle der
Aufstellung mit. 4: Jede Verschiebung, etwa mit AUF-5.5, macht den Docstring falsch. Ein
kurzer Lauf, keine Änderung an Akzeptanztests.

**Gegenvorschlag.** Erledigt, wenn
- `aufstellenTest.py` einen Helfer `ausgangslageVon(ersterSpieler, zweiterSpieler)` hat, den
  `aufstellungVon` und die Tests der `Ausgangslage` nutzen, und den Fall „derselbe Spieler“
  nur ein Test prüft;
- ein Test mit zwei *Spielern*, die sich eine leere `Armee()` teilen, auf `ValueError` prüft;
- über `inNahkampfreichweite` `# Regel: Nahkampfreichweite (core_rules.txt:447)` steht, die
  1″ nur einmal genannt sind und `:450` bei der Sperre steht (`_inNahkampfreichweiteVonGegnern`);
- der Docstring der Klasse nur ihre Aufgabe nennt, etwa „Der Schiedsrichter der Aufstellung:
  hält den Stand und ändert ihn nur über Handlungen, die erst die Sperren prüfen.“;
- beide Testläufe grün sind.

**Stellungnahme.**
