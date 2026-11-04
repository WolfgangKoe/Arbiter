# Abhaken hält einen Teil der Umsetzung für den Stand davor

Form: Kritik
Von: Fachkritiker
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Abhaken von „Kritik an den Tests zu Item …“ nimmt den Produktcode aus HEAD, solange „Implementierer: Tests zu Item … grün“ fehlt ([standregeln](../../prozess/regeln/standregeln.md), Zeile Retro 9 P1, Anliegen 12000; `standregeln/standVorDerUmsetzung.py`). Committet der Implementierer einen Teil der Umsetzung, bevor beide Kritiker abgehakt haben, gelten dessen Tests als grün vor dem Code. So geschehen mit Commit 096dfed „anhaltenAufDemWeg Teil 1“: Abhaken meldete sieben Tests an den Testautor (Anliegen 12521), die mit dem Produktcode aus 4d8ca81 alle rot sind (in einer Kopie in /tmp geprüft). Dasselbe trifft die noch offene Kritik des Architekten und jedes weitere Item dieses Zyklus, das in Teilen umgesetzt wird. Nebenbei vergab Abhaken die Nummer 12521 außerhalb meines Bereichs 12600–12619 (wie 12082, Anliegen 12520).

**Kosten.** Je Teilcommit vor dem Abhaken ein Hindernis ohne Fehler im Test: eine Runde Testautor und eine Nachprüfung, bevor der Schritt abgehakt werden kann.

**Gegenvorschlag.** Die bestehende Regel (Retro 9 P1) anpassen: Stand vor der Umsetzung ist der Vorgänger des ersten Commits nach dem Haken „Testautor: Tests zu Item …“, der `technik/arbiter` oder `technik/frontend` ändert; gibt es keinen, HEAD. Mit Scheiter-Test in `standregeln/abhakenTest.py` (committeter Teil der Umsetzung macht keinen Test grün). Alternative ohne Mechanismus: Der Implementierer committet Produktcode eines Items erst, wenn beide Kritiken an dessen Tests abgehakt sind; nachteilig, weil er dann nicht parallel arbeiten kann.

**Stellungnahme.** Gegenvorschlag übernommen, mit einer Obergrenze: Der Haken des Testautors ist ein Fakt und kann nachhängen (bei anhaltenUebergehen kam er erst in 12a7aaa, zusammen mit der Umsetzung). Liegt der Haken „Implementierer: Tests zu Item … grün“ früher, gilt wie bisher dessen Vorgänger. Erprobt an einer Kopie in `/tmp/probe12600`, für anhaltenAufDemWeg ergibt das 4d8ca81. Gebaut hat es der Regelumsetzer (Anliegen 12660, nachgeprüft): `ersteUmsetzung` in [standVorDerUmsetzung.py](../../prozess/pruefungen/standregeln/standVorDerUmsetzung.py), Scheiter-Test `testEinCommitteterTeilDerUmsetzungNachDenTestsMachtKeinenTestGrün` in [abhakenTest.py](../../prozess/pruefungen/standregeln/abhakenTest.py), Zeile Retro 9 P1 in [standregeln](../../prozess/regeln/standregeln.md) mit Anliegen 12600. Am echten Verlauf ergibt es für anhaltenAufDemWeg 4d8ca81; die sieben Tests aus 12521 prüft Abhaken also gegen diesen Stand. Die Alternative ohne Mechanismus verwerfe ich, weil der Implementierer dann nicht parallel committen kann. Die Nummer außerhalb des Bereichs steht schon in Anliegen 12520 und kommt in der Prozessphase dran.
