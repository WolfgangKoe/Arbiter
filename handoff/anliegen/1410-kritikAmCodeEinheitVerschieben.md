# Kritik am Code zu Item einheitVerschieben: Hineinrücken kennt die Baseform

1410 · Kritik · von Architekt → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.**
1. Hält auf ([Ich 3](../../prozess/praemissen/ich.md): neuer Code verletzt die Architektur, M1 in [architektur.md](../../technik/architektur.md)). Das Hineinrücken in die *Aufstellungszone* (AUF-21.2, 26.1) rechnet [einheitVerschieben.py](../../technik/arbiter/domaene/phasen/aufstellen/einheitVerschieben.py) selbst: wie weit eine *Base* über die Kante ragt, als Mittelpunkt ± Radius (`hineingerückt`, `_rückung`). Fast dasselbe `_rückung` steht in [setzenPerKlick.py](../../technik/arbiter/domaene/phasen/aufstellen/setzenPerKlick.py) für die *Formation* (AUF-18.3). Zwei Module kennen so die Baseform, und „gemeinsam auf kürzestem Weg hinein“ steht zweimal ([Wir 3](../../prozess/praemissen/wir.md)).
   Beispiel: Zieht ein *Spieler* die Boyz über die Kante x = 0, rückt Arbiter den Block um so viel zurück, wie die vorderste *Base* übersteht. Wie weit sie übersteht, hängt an ihrer Form; mit der ovalen *Base* (Etappe 6) wären zwei Stellen zu ändern. Vorbild: `ArbiterMap/backend/app/domain/geometry.py:513` (`clamp_group_vector`) rückt jede Gruppe an einer Stelle, „Feldkante und Aufstellungszone sind beides nur Aufrufer“. M1 nennt diese Messung jetzt als fünfte.
2. Wartet (Ich 3, Form): In `modellLoslassen` heißt eine leere `gruppe` „allein gezogen“ (AUF-20.4); das sagen nur `gruppe = {}` nach der Zuweisung und `gruppe.get(gezogenes, ziel)` in `verschobeneStellen`.
3. Wartet (Ich 3): `Gesperrtes.vorher` ist ein `dict`, das alle *gesperrten* *Modelle* eines Loslassens teilen; D3 verlangt für Sammlungen Tupel oder `MappingProxyType`.

Zu [1370](1370-hindernisTestsZuItemEinheitverschieben.md), Gegenvorschlag 3: Der Dienst rechnet den Weg nicht aus dem Spielstand. Die Seite schickt die *Stelle* des Loslassens (V5), kein Weg; `web/` liest sie als Dezimalzahl wie gesendet (S2), die übrigen *Modelle* folgen ihr exakt. Ein Float-Schritt neben `float(exakte Stelle)` ist Karte, nicht Tisch ([Ziel](../../domaene/ziel.md)); die Toleranz im Dienst-Test ist richtig.

Geprüft, grün: `ruff`, Import-, Spiegel-, Benennungs-, Kommentar-, Gründe-, Glossar- und Frontendprüfung, Unit-Tests (84), Akzeptanztests zu AUF-20, 21, 24.2, 25. Rot nur AUF-24.1 (Item anhaltenAnBases).

**Kosten.** Zu 1: zwei Rechenwege für eine Regel; der Vertragstest je Baseform (M1, Auslöser Etappe 6) prüft nur `messen.py` und sähe den zweiten nicht. Zu 2 und 3: Der Leser muss den Sonderfall erschließen.

**Gegenvorschlag.**
1. Eine Messung in [messen.py](../../technik/arbiter/domaene/messen.py), etwa `rückungInDieFläche(bases: Iterable[tuple[Base, Stelle]], grenzenInX, grenzenInY) -> tuple[Fraction, Fraction]`, „der kürzeste gemeinsame Weg, nach dem jede *Base* *ganz in* der Fläche liegt“ (Name nach deinem Urteil). `hineingerückt` und `stellenDerFormation` rufen sie, beide `_rückung` entfallen, die Unit-Tests dazu stehen in `tests/einheit/domaene/messenTest.py`. Docstring von `messen.py` („drei Messungen“) nachziehen.
2. Wenn billig: eine Abfrage mit frühem `return` ([Es 9](../../prozess/praemissen/es.md)), die den Block oder `{modell: stelle}` liefert; dann verlangt `verschobeneStellen` das gezogene in der Gruppe.
3. Wenn billig: `vorher` als `MappingProxyType`.

**Stellungnahme.** Angenommen, alle drei umgesetzt, Verhalten unverändert.
1. [messen.py](../../technik/arbiter/domaene/messen.py) hat `rückungInDieFläche`; `hineingerückt` und `stellenDerFormation` rufen sie, beide `_rückung` entfallen. Unit-Tests in [messenTest.py](../../technik/tests/einheit/domaene/messenTest.py), Docstring nachgezogen.
2. `Aufstellung._verschobeneStellen` liefert mit frühem `return` `{modell: stelle}` oder den Block; `verschobeneStellen` verlangt das gezogene in der Gruppe (der Unit-Test zum Fall ohne Stelle entfällt).
3. `vorher` ist ein `MappingProxyType`.

Geprüft: `ruff`, Unit-Tests (85) und `prozess/pruefungen` (719) grün; Akzeptanztests rot nur anhaltenAnBases (AUF-24.1, 26.x).
