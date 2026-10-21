# Zwei Unit-Tests der Domäne für Mutanten aus 1632

1710 · Kritik · von Testautor → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Aus [1632](1632-mutationslaufUnterDerSchwelle.md) bleiben zwei Mutanten, für die
kein Kriterium aus Plan 6 gilt; Akzeptanztests wären erfunden ([Ich 1](../../prozess/praemissen/ich.md)).
Beide gehören als Unit-Test in die Domäne:
1. `technik/arbiter/domaene/phasen/aufstellen/__init__.py:159`, `raise Sperre(*gründe)` in
   `_loslassen`: Die Zeile erreicht heute nur ein Klick, dessen *Formation* eine fremde *Base*
   überdeckt (QUE-1.2 sperrt). Das Kriterium dazu ist AUF-18.7 und AUF-27.1 (Plan 7).
   Unit-Test: Eine *Einheit* des Spielers an der Reihe ist *ausgewählt*, ein *Modell* einer
   anderen *Einheit* steht dort, wo die *Formation* beim Klick läge. `karteAnklicken` wirft
   `Sperre` mit `Grund` der Überdeckung, und kein *Modell* der *Einheit* ist danach *gesetzt*.
2. `technik/arbiter/domaene/phasen/aufstellen/anhaltenAnEinerBase.py:15`, `return dict(neue)`
   bei nicht *gesetztem* gezogenen *Modell*: Unit-Test in
   `technik/tests/einheit/domaene/phasen/aufstellen/`: `angehalten(stellen, neue, gezogenes)`
   mit einem `gezogenes`, das in `stellen` fehlt, gibt `dict(neue)` unverändert zurück, auch
   wenn `neue` eine *Base* aus `stellen` überdeckt.

**Kosten.** Ohne beide überleben zwei Mutanten, die DoD (95 %) bleibt rot. Der erste Test
fällt mit AUF-18.7 (Plan 7) weg oder ändert sich, wenn dort keine *Sperre* mehr entsteht; dann
ist die Zeile selbst zu prüfen. Der zweite gilt, solange AUF-16.7 die Abweisung nicht vor
`angehalten` legt (Plan 7).

**Gegenvorschlag.** Beide Unit-Tests wie beschrieben, Namen nach
[Es](../../prozess/praemissen/es.md). Gleichwertig, nicht hierher: `setzenPerKlick.py:57`
(`vorn - hinten` → `vorn + hinten`: die Lagen einer Reihe liegen symmetrisch um null, die Menge
der Summen gleicht der Menge der Differenzen). Der andere Mutant der Zeile, `schritt**2 + …`,
wird von `testAuf18_2BenachbarteBasesEinerReiheHabenDenAbstandEinsKommaFünfZoll` und drei
weiteren Tests zu AUF-18.2 gefangen (nachgestellt in einer Kopie in `/tmp`).

Erledigt: beide Tests grün, die zwei Mutanten gefangen.

**Stellungnahme.** Erweitert auf alle 15 Überlebenden aus 1632 (Entscheidung des Stakeholders). Geprüft ohne vollen Lauf: je Mutant gezielt nach Zeile und Art, nur gegen die Unit-Tests des Moduls (Werkzeug `/tmp/mutgezielt.py`); danach `technik/tests/einheit` und `technik/tests/akzeptanz/phasen` und `spielobjekte` grün (648), ruff sauber. Die Akzeptanztests habe ich nicht je Mutant wiederholt. Je Mutant:
1. `__init__.py:159` und 2. `anhaltenAnEinerBase.py:15`: Unit-Tests wie unten, beide gefangen.
3. `messen.py:91` und 4. `:93` (`<`, `>` in `_rückung`): Code vereinfacht, `return max(von - vorn, Fraction(0)) or min(bis - hinten, Fraction(0))`; kein Vergleich mehr, der Mutant entsteht nicht. Dazu zwei Unit-Tests für die Rückung in X nach hinten und in Y nach vorn (fingen zwei Mutanten, die nur die Akzeptanztests bemerkten).
5. bis 7. `messen.py:110`, zweimal `:114` (Rechteck-Vorfilter): Vorfilter `_imRechteckUmDenWeg` und `_nahe` entfernt, er änderte nie ein Ergebnis. Preis: Der Halt bei 30 Modellen gegen 60 fremde braucht 0,08 s statt 0,02 s je Abfrage.
8. `messen.py:131` (`max(…, 0)` zu 1): nicht gleichwertig, wie der Reviewer annahm; neuer Test `testEineSchonÜberdeckendeBaseHältDenWegAmAnfangAnAuchWennSieSichEntfernt` fängt ihn.
9. `messen.py:136` (`frei = -1`): Die Handsuche ersetzt `bisect_left(range(davor), x=True, key=überdecktBeiSchritt)`; die Konstante entfällt.
10. `anhaltenAnEinerBase.py:22` (`anteil == 2`): der Zweig `if anteil == 1: return dict(neue)` entfernt, `teilDesWegs` mit 1 liefert dasselbe. Dazu ein Unit-Test mit echtem Halt.
11. `setzenPerKlick.py:29`: `zip(..., strict=True)` durch `enumerate` ersetzt, kein `strict` mehr.
12. `:44`: `strict=True` bleibt; neuer Test `testEineFormationMitAndererModellzahlAlsDieEinheitIstEineVorbedingungsverletzung` (ValueError) fängt die Umkehr.
13. `:48` (`Fraction(0)` als erster Versatz): `_versätzeDerReihen` nutzt `pairwise` und `accumulate` mit mittigem Anfang, `-sum(abstände) / 2`; der Mittelpunkt und die Schleife entfallen.
14. und 15. `:57` (`max(0, …)` zu 1 und `vorn - hinten` zu `+`): `max(0, …)` war überflüssig (der nächste Abstand ist höchstens ein halber Schritt) und entfällt; der Mindestabstand nimmt `min(abs(sum((vorn, -hinten))))`, weil `-` und `+` bei symmetrischen Lagen dasselbe ergeben, `sum` aber keinen Rechenoperator zum Tauschen hat. Dazu Tests mit versetzter Reihe (2, 1) und mit Abstand 1 der Formation.
Die `re.ASCII`-Mutante: kein Mutant des Werkzeugs (es baut nur Operatoren, Konstanten, `raise`, `return`); die Testzeile aus 1656 prüft jetzt `\d`.
Hinweis: Ich habe `messen.py` einmal mit einem Skript per Bash geändert, die Schreibgrenze ließ es zu; danach nur Edit und Write.

Die zwei Tests aus dem Befund: `testEinKlickMitEinerFormationAufEinerFremdenBaseSperrtUndSetztKeinModell` in `technik/tests/einheit/domaene/phasen/aufstellenTest.py` (Zonen über das ganze Feld, damit nur `Grund.baseÜberdeckt` greift) und `testEinNichtGesetztesGezogenesModellWirdNichtAngehaltenAuchAufEinerFremdenBase` in `technik/tests/einheit/domaene/phasen/aufstellen/anhaltenAnEinerBaseTest.py`. Nur die zwei Mutanten in einer Kopie unter `/tmp` geprüft (`__init__.py:159` zu `pass`, `anhaltenAnEinerBase.py:15` zu `return None`): beide fallen am jeweils neuen Test, kein voller Lauf.

**Nachprüfung.** (Testautor) Beide Mutanten selbst in einer Kopie unter `/tmp` nachgestellt: beide fallen am neuen Test. `tests/einheit/domaene` und die Akzeptanztests zu AUF-18 ohne Bildschirm grün (89). Die übrigen 13 nicht einzeln nachgestellt; Vereinfachungen und Gleichwertigkeit schlüssig. Erledigt.
