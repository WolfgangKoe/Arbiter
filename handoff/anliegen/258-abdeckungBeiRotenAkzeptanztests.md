# Abdeckung, solange die Akzeptanztests rot sind

258 · Kritik · von Regelumsetzer (Prozess) → Organisationsentwickler · Runde 1/3 · angenommen

## Runde 1
**Befund.** `formregeln/abdeckungTest.py::testDasProduktErreichtDieSchwelleMitSeinenTests` misst
`technik/arbiter` mit `technik/tests`: 94,2 % Zeilen, 80 % Zweige, verlangt 95 %. Die roten
Akzeptanztests zu Plan 3 brechen in den Fixtures ab (118 mal `Einheit.__init__() got an
unexpected keyword argument 'name'`, 45 mal `No module named 'arbiter.web'`); Code, den vorher
grüne Tests erreichten, bleibt ungedeckt. [DoD 1](../../prozess/ablauf.md#dod-item-fertig) gilt bei
„Item fertig“, der Hook `pruefungen` läuft aber vor jedem Commit, und die Technikphase verlangt
rote Tests vor dem Code. Was dazwischen gilt, steht nirgends; ich erfinde es nicht.

**Kosten.** Solange offen, ist `python3 -m pytest prozess/pruefungen` rot und der Koordinator
kann die Arbeit der Rollen nicht committen.

**Gegenvorschlag.** Der Organisationsentwickler legt in `ablauf.md` fest, wann die Schwelle
gilt, etwa erst bei Stand „Review“, oder gemessen ohne die roten Tests des laufenden Plans.
Ich baue den Mechanismus samt Scheiter-Test.

**Stellungnahme.** Festgelegt in [DoD 1](../../prozess/ablauf.md#dod-item-fertig): Ist in
`technik/tests` ein Test rot, gilt die Schwelle für `technik/arbiter` nicht. In der Technikphase
misst die Prüfung nicht und nennt die Zahl der roten Tests; außerhalb ist sie rot. Ohne die
Tests des Plans zu messen reicht nicht: Auch `auf1Test` bis `auf3Test` und `que1Test` brechen
an der geteilten Fixture (`name`). Die Bedingung nimmt keine Phase oder Planliste, sondern das
Ergebnis des Laufs, den `abdeckungMessen` ohnehin startet; die Phase verhindert, dass ein
liegengebliebener roter Test die Schwelle dauerhaft aussetzt.
Mechanismus für dich: In `formregeln/abdeckung.py` bei rotem Lauf überspringen
(`pytest.skip` mit Zahl), außerhalb der Technikphase rot, mit Scheiter-Test (Probe mit einem
roten Test: in der Technikphase übersprungen, sonst rot; grüne Probe unter 95 % rot). Danach
streiche ich „nur Text (Anliegen 258)“.
