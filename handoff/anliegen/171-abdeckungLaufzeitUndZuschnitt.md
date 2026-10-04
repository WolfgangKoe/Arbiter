# Abdeckung: Laufzeit und Zuschnitt

171 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Kritik am Code zu Commit `6dfe473`; die falschen Grünmeldungen stehen in
[170](170-abdeckungMeldetFalschGruen.md).

**Befund.**
1. **Effizienz.** `testDiePrüfskripteErreichenDieSchwelleMitIhrenTests` startet die ganze
   Suite `prozess/pruefungen` noch einmal unter coverage. Gemessen: 25 s von 43 s;
   `abdeckungTest.py` allein 34 s, der Rest der Suite etwa 9 s. Die Suite läuft im
   pre-commit-Hook (`.pre-commit-config.yaml`, `pruefungen`) bei jedem Commit, auch bei
   reinen Handoff-Commits. Dafür braucht es `innenMarke`, die Umgebungsvariable und
   `imÄußerenLauf`, und `conftest.py` löscht im inneren Lauf erledigte Anliegen ein zweites Mal.
2. **Ausnahmen zu breit.** `ignore_names = ["test*", "zweite"]` gilt für jeden Namen in
   `technik/arbiter`, nicht nur für das Mitglied `Aufstellungszone.zweite` und die
   Testfunktionen. Eine unbenutzte Variable `zweite` oder eine Funktion `testlauf…` im
   Produkt meldet vulture nie.
3. **Lesbarkeit** ([wir.md](../../prozess/praemissen/wir.md), der Name trägt die Bedeutung):
   `testEinKriteriumDasDenCodeBraucht` hat keine Aussage;
   `testDieKriterienAndersAlsEinheitstestsZählenAlsBenutzung` ist die Prüfung „technik/arbiter
   hat keinen toten Code“, der Name beschreibt aber die Zählweise.
4. **Vereinfachung.** `suchpfad="technik"` beim Produkt wiederholt `pythonpath = ["technik"]`
   aus `pyproject.toml`, das pytest mit `cwd=wurzel` ohnehin liest.

**Kosten.** 1: etwa 30 s mehr je Commit und je Lauf des Regelumsetzers, wachsend mit jeder
neuen Prüfung, dazu drei Bausteine nur für die Verschachtelung. 2: Die Ausnahmeliste
verdeckt mehr, als der Wegwerf-Versuch gefunden hat. 3, 4: kleiner Lese- und Pflegeaufwand.

**Gegenvorschlag.**
1. Die Prüfskripte nicht in sich selbst messen: Ein eigener Hook in
   `.pre-commit-config.yaml` startet `python3 -m coverage run --branch
   --source=prozess/pruefungen -m pytest prozess/pruefungen`, danach `coverage report
   --fail-under=95`; das ist zugleich die eigene Meldung aus 157 und ersetzt den normalen
   Lauf. `innenMarke` und `imÄußerenLauf` entfallen. Der Scheiter-Test an der Probe bleibt.
2. `zweite` über eine Whitelist-Datei von vulture zulassen (`Aufstellungszone.zweite`),
   die nur dieses Mitglied nennt; `test*` auf die Testfunktionen beschränken, etwa als
   `test[A-Z]*`, oder ebenfalls über die Whitelist.
3. Etwa `testCodeDenEinKriteriumAufruftIstBenutzt` und `testDasProduktHatKeinenTotenCode`.
4. `suchpfad` beim Produkt weglassen.
