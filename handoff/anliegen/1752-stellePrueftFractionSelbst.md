# Die Stelle prüft selbst, dass sie exakt ist

1752 · Kritik · von Architekt → Implementierer · Runde 1/3 · offen · wartet auf die Technikphase

## Runde 1
**Befund.** Kritik am Code zu Anliegen 1760. Die Abhilfe
dort hält [S2](../../technik/architektur.md#stelle-und-rechnen) wieder ein, und die
Architektur ist eingehalten. Der Fall zeigt aber eine Lücke: Eine *Stelle* mit float entstand
mitten in der Domäne, und keine Prüfung schlug an. S2 nennt als Prüfung nur „die Grenzfälle
der Akzeptanztests“, und `Fraction(20) == 20.0` ist wahr. Ein ganzzahliger Klick fällt also
nicht auf. Erst der Reviewer hat es beim Lesen gefunden.

Wegwerf-Versuch in einer Kopie unter `/tmp`: `Stelle` bekommt in `__post_init__` die Zeile
„x und y müssen `Fraction` sein, sonst Fehler“.
- Mit dem Code nach 1760 sind alle 744 Tests in `technik/tests/einheit` und
  `technik/tests/akzeptanz` grün. Keine Stelle im Bestand baut eine *Stelle* aus int oder float.
- Mit dem alten Fehler (`-sum(abstände) / 2`) und ohne den neuen Unit-Test aus 1760 schlagen
  8 bestehende Tests an, darunter `testAuf18_2EineEinheitAusEinemModellStehtAmKlick`.
- Die Abfrage zum Anhalten wird dadurch nicht messbar langsamer (60 gegen 150 Modelle: 0,11 s
  mit und ohne die Prüfung).

Vorbild im Bestand ist die Vorbedingung in `Aufstellung.auswählen`: Ein Aufruf außerhalb des
Vertrags scheitert laut, statt weiterzurechnen.

Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet. Der Fehler ist behoben,
keine Prüfung ist rot, und der Happy Path ist vollständig. Es fehlt nur die Prüfung, die den
nächsten solchen Fehler früh meldet.

**Kosten.** Ohne diese Prüfung bleibt jeder spätere Rechenweg mit int-Anfang (`sum`, `0 / 2`,
`max(0, …)`) unbemerkt, bis ein Rand mit Bruchzahlen eine *Sperre* zu Unrecht auslöst. Das
trifft künftig das Bewegen und den Charge, die mehr rechnen als das Aufstellen. Mit der
Prüfung kostet es eine Methode von drei Zeilen in
[spielobjekte.py](../../technik/arbiter/domaene/spielobjekte.py) und einen Unit-Test.

**Gegenvorschlag.** In der nächsten Technikphase prüft `Stelle.__post_init__`, dass `x` und
`y` jeweils eine `Fraction` sind (`isinstance`), sonst `TypeError`. Dazu kommt ein Unit-Test
„eine Stelle aus float ist ein Fehler“. S2 nennt danach als Prüfung diese Vorbedingung; den
Text ändere ich als Architekt. Bestehende Regel ([Ich 4](../../prozess/praemissen/ich.md)):
S2, nur mit Mechanismus statt Text. Eine neue Regel ist das nicht.

**Stellungnahme.**
