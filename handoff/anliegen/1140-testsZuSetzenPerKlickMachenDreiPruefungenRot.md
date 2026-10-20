# Tests zu Setzen per Klick machen drei Prüfungen rot

1140 · Kritik · von Architekt → Testautor · Runde 2/3 · erledigt

## Runde 1
**Befund.** Kritik an den Tests zu Item setzenPerKlick (`git diff`, Lesbarkeit nach
[Es](../../prozess/praemissen/es.md)). Nach Ich 3 hält alles auf: Eine Prüfung ist rot
(`pytest prozess/pruefungen -m "stand and not abdeckung"`). Der Vertrag V5 bis V8 ist
getroffen, die Schichten auch (B1, kein `flask`).
1. Reihenfolge nach [Architektur, T1](../../technik/architektur.md) (3), `formregeln/spiegel.py`:
   [setzenPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/setzenPerKlickTest.py)
   ordnet nach Schicht (Domäne, Dienst, Seite), so steht AUF-18.1 nach 18.5 (Zeilen 141, 201);
   [auswahlTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/auswahlTest.py) nennt
   AUF-5.4 nach 5.11 (Zeile 136) und 5.7 nach 5.12 (Zeile 225).
2. Ruff `ARG001`, 5 Stellen in
   [sperreOhneStelleTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/sperreOhneStelleTest.py):
   Jeder Aufbau des Fixtures `sperrendesLoslassen` nimmt `boyz` und `necronWarriors`, nutzt
   aber nur eines.
3. Toter Code (`formregeln/abdeckung.py`): `umrissVon` in `bildschirm.py` (Nutzer AUF-5.6
   entfallen), `reihenDerFormation` in `handgriffe.py` (Nutzer AUF-8.5 entfallen),
   `längeInDerMitte` in `setzenPerKlickTest.py`.

**Kosten.** Rot verhindert den Commit (Hook `stand`), und der Implementierer baut auf einer
roten Grundlage. Zu 3: Mit den Tests zu AUF-8.5 ging auch der einzige Test weg, der die
Reihen der *Formation* nach dem Glossar prüft. AUF-18.2 prüft nur die Mitte.

**Gegenvorschlag.**
1. Je Kriterium alle Tests beisammen, die Schichten darin hintereinander (wie in
   `sperreOhneStelleTest.py`). Die Tests zu 5.4 und 5.7 stellst du vor 5.11 und 5.12.
2. Ein Aufbau nimmt nur `aufstellung`, das Fixture holt die *Einheit* mit
   `request.getfixturevalue` (wie `sperrfall` in `gesperrterKlickTest.py`), oder jeder Aufbau
   nimmt nur, was er nutzt.
3. `umrissVon` und `längeInDerMitte` löschen. `reihenDerFormation` nutzt der Test zu
   AUF-18.2: Er prüft die Reihen wie früher der Test zu 8.5. Ob 18.2 und 18.3 genug prüfen
   (Reihen, „auf kürzestem Weg“), entscheidet der Fachkritiker; sonst löschen.

Erledigt, wenn `pytest prozess/pruefungen -m "stand and not abdeckung"` nur noch die
fehlenden Testdateien der Items 2 und 3 und AUF-9.2 meldet (Item anhaltenAnBases) und
`ruff check technik/tests` grün ist.

**Stellungnahme.** Alle drei Punkte umgesetzt.
1. [auswahlTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/auswahlTest.py) steht
   jetzt in der Folge der Kriterien (5.4, 5.7 bis 5.10, 5.11, 5.12);
   [setzenPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/setzenPerKlickTest.py)
   hat je Kriterium alle Tests beisammen, die Schichten darin hintereinander.
2. In [sperreOhneStelleTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/sperreOhneStelleTest.py)
   nimmt jeder Aufbau `aufstellung` und die *Einheit*; das Fixture holt sie mit
   `request.getfixturevalue`. `ruff check` und `ruff format --check` sind grün.
3. `umrissVon` ist gelöscht. `reihenDerFormation` nutzt der Test zu AUF-18.2 (Reihen, Abstände,
   Reihenabstand, Warboss am Klick, dazu 1120). `längeInDerMitte` ist gelöscht. Der Stand-Lauf
   meldet nur noch die fehlenden Testdateien der Items 2 und 3 und AUF-9.2 sowie den
   Glossarbefund zu `Grund.modelleFehlen` in `sperre.py` (nicht aus den Tests).

## Runde 2
**Befund.** Nachprüfung: Punkte 1 bis 3 sind umgesetzt. Spiegel und Ruff sind grün,
`umrissVon` und `längeInDerMitte` sind weg, der Test zu AUF-18.2 nutzt `reihenDerFormation`.
Der Stand-Lauf meldet nur noch fehlende Testdateien der Items einheitVerschieben und
anhaltenAnBases und `Grund.modelleFehlen` (1170, 1121). Weiter hält auf, nach Ich 3 (neuer
Code verletzt Lesbarkeit): Zwei Stellen in
[setzenPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/setzenPerKlickTest.py)
greifen per Index auf Fachobjekte zu ([Es 6](../../prozess/praemissen/es.md)).
1. Zeile 289, Test zu AUF-18.2 (schräg benachbarte Bases): `hintere[0].x - vordere[0].x`,
   die erste *Stelle* einer Reihe.
2. Zeile 379, Test zu AUF-18.3: `{*grenzen[0], *grenzen[1]}`, die Grenzen der
   *Aufstellungszone* in x und in y.

**Kosten.** Wer `grenzen[0]` liest, muss in `Ausgangslage.grenzenDerZone` nachsehen, welche
Achse gemeint ist; ein Name sagt es. Gering: zwei Zeilen.

**Gegenvorschlag.**
1. Entpacken: `ersteVordere, *_ = vordere` und `ersteHintere, *_ = hintere`, oder eine kleine
   Hilfe `reihenabstand(vordere, hintere)` mit benannten ersten *Stellen*.
2. `grenzenInX, grenzenInY = grenzen` neben `zone` und `{*grenzenInX, *grenzenInY}`.

Erledigt, wenn die Akzeptanztests des Items keinen Index auf ein Fachobjekt mehr nehmen und
`ruff check technik/tests` grün bleibt.

**Stellungnahme.** Beide Stellen umgesetzt in setzenPerKlickTest.py: Der Reihenabstand steht in
der Hilfe `abstandDerReihen(vordere, hintere)` mit benannten ersten *Stellen*, die Grenzen sind
als `grenzenInX, grenzenInY` entpackt. `ruff check` und `ruff format --check` sind grün.
