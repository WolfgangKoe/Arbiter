# Sprung-Versuch: Klick trifft nur den Anfang des Testnamens

127 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
Gegenstand: 047a564 (Kritik am Code, Wegwerf-Versuch zu
[124](124-sprungPerKlickErproben.md)). Das `arbiter-sprung.vsix` enthält die drei Quellen
unverändert; `testsZu` findet im Repo die 4 Tests zu AUF-1.3, `kriteriumZu` die Zeile 17.

**Befund.**
1. `suche.js`, `testMuster` ist faul (`*?`) und endet bei `_\d+`. `extension.js` nimmt es
   als Bereich für `getWordRangeAtPosition`: Bei
   `testAuf1_4EinModellDerEinheitInAufstellungLässtSichSetzen` deckt der Bereich nur
   `testAuf1_4` (mit node nachgestellt). Ein Strg+Klick auf den Rest des Namens springt
   nicht zum Kriterium.
2. [wir.md](../../prozess/praemissen/wir.md) gilt für jeden Code in `prozess/pruefungen/`:
   `baue.py` hat einen fünfzeiligen Modul-Docstring (Regel 8: höchstens einzeilig);
   `extension.js` und `suche.js` haben beschreibende Kommentare, keine `Warum:`- oder
   `Regel:`-Zeilen (Regel 8); `alsOrte` nutzt `(s) =>` (Regel 5: mindestens 3 Zeichen);
   `arbiter-sprung.vsix` ist kein camelCase (Regel 2).
3. Das Namensschema steht ein zweites Mal: `suche.js` hat eigene Muster neben
   `rueckverfolgung.py` (`kriteriumZeile`, `testKriterium`), und sie weichen schon ab
   (`[A-Za-zÄÖÜäöüß]*?` gegen `[a-zäöüß]*`).
4. Das gebaute `arbiter-sprung.vsix` liegt neben den Quellen im Repo. Ändert jemand
   `suche.js` ohne `baue.py`, installiert der Stakeholder still den alten Stand.

**Kosten.** Zu 1: Der Versuch kann beim Stakeholder scheitern, obwohl die Suche stimmt; wer
in die Mitte des Namens klickt, landet bei Pylance auf der Definition selbst, und 83 hält
einen falschen Befund fest. Zu 2: Regelbruch, klein, solange der Versuch Wegwerf ist. Zu 3:
Ändert sich Regel 4 oder das Format der Kriteriumszeile, springt der Klick still ins Leere,
während `rueckverfolgung.py` grün bleibt. Zu 4: Quelle und Paket können auseinanderlaufen.

**Gegenvorschlag.**
1. Vor der Probe des Stakeholders: als Bereich der ganze Bezeichner, etwa
   `/test[A-ZÄÖÜ][a-zäöüß]*\d+_\d+[\wÄÖÜäöüß]*/`; die Zerlegung in `kriteriumZu` bleibt.
   Neu bauen und im Anliegen 124 sagen, dass er neu installieren muss.
2. Bleibt der Versuch: Docstring einzeilig, Kommentare streichen oder als `Warum:`,
   `stelle` statt `s`, Paketname ohne Bindestrich (`arbitersprung`).
3. Bleibt der Versuch: Der angekündigte Scheiter-Test prüft, dass `suche.js` zu jedem Test,
   den `rueckverfolgung.py` einem Kriterium zuordnet, dieselbe Kriteriumszeile findet.
4. Bleibt der Versuch: das vsix nicht einchecken; die Installationszeile baut es zuerst
   (`python3 prozess/pruefungen/sprung/baue.py && code --install-extension …`), oder eine
   Probe vergleicht Paket und Quellen.

**Stellungnahme.** Alle vier umgesetzt. 1: `testMuster` deckt den ganzen Bezeichner (`suche.js`); das Paket ist neu gebaut, Version 0.0.3, Name `arbitersprung`. Der Stakeholder muss neu installieren: `python3 prozess/pruefungen/sprung/baue.py && code --install-extension prozess/pruefungen/sprung/arbitersprung.vsix`, dann „Developer: Reload Window“. 2: Docstring einzeilig, Kommentar als `Warum:`, `stelle` statt `s`. 3: `sprung/sucheTest.py` (läuft mit node) prüft für jeden Test aus `rueckverfolgung.py`, dass der Bereich den ganzen Namen deckt und `kriteriumZu` dieselbe Zeile findet; mit dem alten Muster rot. `testKriteriumMuster` in `suche.js` gleicht jetzt dem Python-Muster; eine echte gemeinsame Quelle gibt es nicht. 4: das vsix ist nicht mehr eingecheckt (`.gitignore`). Anliegen 124 nennt noch den alten Pfad `arbiter-sprung.vsix`; dort bin ich nicht dran.

**Nachprüfung.** 1 bis 3 in Ordnung (`sucheTest.py` mit altem `suche.js` rot). 4 liegt nur im
Arbeitsbaum. Rest: [133](133-sprungpaketBeimStakeholderVeraltet.md).
