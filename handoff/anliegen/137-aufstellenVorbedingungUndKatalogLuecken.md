# Aufstellen: Vorbedingung über Einheiten statt Modelle, Katalog lässt Lücken durch

137 · Kritik · von Reviewer (Technik) → Implementierer · Runde 1/3 · erledigt

## Runde 1
Gegenstand: 6566da4 (Kritik am Code). `python3 -m pytest technik/tests` grün (143),
`python3 -m pytest prozess/pruefungen` grün (417). Befunde nachgestellt mit
`ausgangslageAus` und `Aufstellung` direkt.

**Befund.**
1. `aufstellen.py`, `_teilenSichArmeeOderEinheit`: geprüft wird eine gemeinsame *Einheit*,
   nicht ein gemeinsames *Modell*. Zwei *Spieler* mit je einer eigenen `Einheit((m,))` um
   dasselbe `m` nimmt `Aufstellung` an. Nach dem Glossar ist die *Armee* „alle *Modelle*
   unter dem Befehl eines *Spielers*“, ein *Modell* gehört also nur einer.
2. `aufstellen.py:39`: Die Meldung „Die Spieler führen verschiedene Armeen ohne gemeinsame
   Einheit“ klingt wie der Befund, beschreibt aber die verletzte Vorbedingung. Daneben steht
   „Die Aufstellung braucht zwei verschiedene Spieler“, dort ist die Form klar.
3. `katalog/ausgangslage.py`:
   a) Fehlt `zweite` unter `Aufstellungszone`, lädt die Ausgangslage. Erst beim ersten
      `modellSetzen` des zweiten *Spielers* fliegt `KeyError: Aufstellungszone.zweite` aus
      `_grenzenInX`. Ein unbekannter Name gibt beim Laden `KeyError` statt `ValueError`.
   b) `_durchmesserLesen` nimmt `true` (YAML 1.1 auch `yes`/`on`), `0` und `-5`, weil
      `bool` von `int` erbt und das Vorzeichen offen ist. Geladen: `Base(durchmesser=True)`,
      `Base(durchmesser=0)`, `Base(durchmesser=-5)`.
4. `sperre.py`: In `sorted(grund.value for grund in gründe)` verdeckt die Laufvariable den
   Parameter `grund`. Kein Fehler, aber beim Lesen zwei Bedeutungen für einen Namen.

**Kosten.** Zu 1: Teilen sich die *Spieler* ein *Modell*, kehrt der Fehler aus 129 zurück:
der zweite *Spieler* setzt das *Modell* des ersten um, AUF-3.4 zählt es für beide als eigenes.
Erreichbar heute nur über Unit-Tests oder später `web/`. Zu 2: Wer den `ValueError` liest,
weiß nicht, ob die Meldung den Zustand oder die Forderung nennt. Zu 3: Derselbe Fall wie
132.3, „Datenfehler zeigt sich fern der Ursache“, nur an zwei anderen Stellen. Zu 4: klein.

**Gegenvorschlag.**
1. Die Prüfung über die *Modelle*, mit dem vorhandenen `_modelleVon` (als Funktion des
   Moduls, es braucht `self` nicht):
   `ersteArmee is zweiteArmee or not _modelleVon(erster).isdisjoint(_modelleVon(zweiter))`.
   Eine gemeinsame *Einheit* hat mindestens ein *Modell* (Glossar, *Einheit*), der heutige
   Test bleibt also grün; dazu ein Test für das gemeinsame *Modell*.
2. Als Forderung formulieren, wie die Zeile darüber: „Die Spieler brauchen verschiedene
   Armeen ohne gemeinsames Modell“.
3. a) Nach der Schleife `if set(tiefen) != set(Aufstellungszone): raise ValueError(...)`,
      unbekannte Namen ebenso als `ValueError`.
   b) `if type(zahl) is not int or zahl <= 0: raise ValueError(...)`.
   Je ein Fall in `ausgangslageTest.py`.
4. Laufvariable umbenennen, etwa `einzelner`.

Erledigt, wenn 1 bis 3 umgesetzt sind, die Akzeptanztests unverändert grün und
`python3 -m pytest prozess/pruefungen` grün ist.

**Stellung (Implementierer).** Angenommen, alle vier Punkte umgesetzt: Prüfung über die
Modelle, Meldung als Forderung, Katalog wirft `ValueError` bei fehlender oder unbekannter
Zone und bei Durchmesser, der kein `int` über 0 ist, Laufvariable umbenannt. Tests in
`aufstellenTest.py` und `ausgangslageTest.py`.

**Nachprüfung (Reviewer).** In e817638 umgesetzt, Punkte 1 bis 4. Tests grün (150),
Prüfungen grün (419), `ruff check` und `ruff format --check` sauber. Neuer Befund am Test:
[140](140-indexImTestDesGemeinsamenModells.md).
