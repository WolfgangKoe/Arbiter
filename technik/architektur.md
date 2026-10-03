# Architektur

Jede Regel nennt, was sie prüft. „Nur Text“ heißt: noch ohne Mechanismus; der Auslöser steht
dabei, danach baut der Regelumsetzer ihn auf Anliegen des Architekten.

## Schichten
```
technik/
  arbiter/
    domaene/    Fachlogik, nur Standardbibliothek
    katalog/    liest das YAML aus domaene/daten/ in Objekte der Domäne
    speicher/   Datenbank; setzt die Schnittstellen der Domäne um
    web/        Flask; übersetzt Anfragen in Handlungen der Domäne
  frontend/     HTML, CSS, JS; spricht nur über HTTP mit web/
  tests/        akzeptanz/, einheit/
```
Ein Ordner entsteht mit dem ersten Item, das ihn braucht.

## Abhängigkeiten zeigen nach innen
- **A1** `arbiter.domaene` importiert nur die Standardbibliothek und sich selbst. Prüft:
  `importvertrag.py`, relative Importe erst nach Anliegen 125.
- **A2** `web`, `speicher` und `katalog` kennen die Domäne, nie umgekehrt. Braucht die
  Domäne Speicherung, beschreibt sie eine Schnittstelle (`typing.Protocol`) in
  `arbiter/domaene/`; `speicher/` setzt sie um, `web/` verdrahtet beides. Prüft: wie A1.
- **A3** Katalogdaten stehen nur als YAML in `domaene/daten/`, `katalog/` liest sie
  (`yaml.safe_load`). Der Spielstand liegt nur in der Datenbank. Prüft: nur Text; Auslöser:
  erster Spielstand, der eine Sitzung überlebt; dann importiert `katalog/` in die Datenbank.

Altbestand: `ArbiterMap/backend/app/domain/rule_checks.py` importiert nur die eigene Geometrie.

## Grundschnitt der Domäne
`arbiter/domaene/` gliedert sich wie `domaene/anforderungen/`:
- `spielobjekte.py`: `Spieler`, `Armee`, `Einheit`, `Modell`, `Base`, `Spielfeld`, `Stelle`
  und was mehr als eine Phase braucht.
- `phasen/<phase>.py` heißt wie die Anforderungsdatei. Was eine Phase einführt, liegt dort,
  bis eine zweite Phase es braucht; dann zieht es nach `spielobjekte.py`. Darum liegen
  `Ausgangslage`, `Aufstellungszone`, *aufgestellt* und *gesetzt* in `phasen/aufstellen.py`.
- `querschnitt.py`: was nach `querschnitt.md` in jeder Phase gilt, zuerst QUE-1.2.
- `sperre.py`: `Sperre` und `Grund`; Übergehen und Protokoll gelten für alle Phasen.
- `messen.py`: die Messungen (M1).
- `spielablauf/` nur unter `tests/akzeptanz/`: Szenarien über mehrere Phasen.

Ein Modul wird zum Paket, ohne dass sich ein Import ändert. Prüft: die Importe der
Akzeptanztests; Spiegel im Code: nur Text (DoD 2).

## Stelle und Rechnen
- **S1** Eine *Stelle* ist der Mittelpunkt der *Base*, `Stelle(x, y)` in Zoll, Ursprung in
  einer Ecke des Spielfelds; x läuft entlang der ersten Seitenlänge aus `onlyWar.yaml` (44″),
  y entlang der zweiten (60″). Die erste *Aufstellungszone* liegt an der Kante x = 0, die
  zweite an x = 44. Prüft: die Fixture `zone`.
- **S2** Gerechnet wird exakt mit `fractions.Fraction`, ohne Toleranz und ohne Wurzel:
  Durchmesser in ganzen mm, 1″ = 254/10 mm, Abstände als Quadrate verglichen; `web/`
  übersetzt in `Fraction`. Mit `float` überdecken sich zwei berührende Boyz, das Raster in
  `ArbiterMap/backend/app/domain/geometry.py` rundet 16 mm auf 0,63″. Wegwerf-Versuch: alle
  Grenzfälle exakt, 9 µs je Vergleich. Prüft: die Grenzfälle der Akzeptanztests.

## Regeln im Domänencode
- **D1** Spielobjekte haben Identität: Vergleich mit `is`, `@dataclass(eq=False)`. Werte
  (`Stelle`, `Base`) nach Inhalt. Prüft: Akzeptanztests (gleiche Armeen, `stelle(…) == stelle`).
- **D2** Eine Handlung prüft erst alle Sperren, dann ändert sie den Zustand; so kann ein
  Übergehen die Prüfung überspringen und protokollieren. Prüft: je Handlung und Grund ein
  Akzeptanztest auf den unveränderten Zustand.
- **D3** Zustand ändern nur Handlungen. Spielobjekte sind `frozen`, Sammlungen Tupel oder
  `MappingProxyType`. Den Zustand einer Phase hält die Phase in `_`-Feldern, lesbar über
  Properties ohne Setter (`aufstellung.anDerReihe`) oder Abfragen
  (`aufstellung.gesetzt(modell)`); sonst umginge `modell.gesetzt = True` jede Sperre. Prüft:
  Python wirft bei der Zuweisung; der Rest nur Text; Auslöser: `web/`, dann eine Prüfung
  „nur `_`-Felder zuweisen, Dataclasses `frozen`“.
- **M1** Phasen messen nur über drei Messungen in `messen.py`: zwei *Bases* *überdecken*
  sich, der *Abstand* zweier Modelle ist höchstens eine Zahl, eine *Base* liegt *ganz in*
  einer Fläche. Die Baseform kennt nur `messen.py`. Prüft: nur Text; Auslöser: zweite
  Baseform (Etappe 6), dann ein Vertragstest je Baseform und ein Importvertrag „`phasen`
  importiert keine Baseform“.

## Tests
- **T1** Je Anforderung eine Testdatei im Ordner der Anforderungsdatei: AUF-1 in
  `domaene/anforderungen/phasen/aufstellen.md` → `tests/akzeptanz/phasen/aufstellen/auf1Test.py`.
  Für die erste Anforderung einer Datei genügt die Sammeldatei (`querschnittTest.py`), bis
  ein offenes Item eine zweite nennt. Höchstmaß: `prozess/kennzahlen.md`; darüber wird
  die Anforderung geteilt, nicht der Test. Prüft: `rueckverfolgung.py`, `benennung.py`,
  `hoechstmassTest.py`.
- **T2** Der Weg vom Kriterium zum Test und zurück wird berechnet, nicht gespeichert: keine
  Links in Anforderung oder Test, die Zuordnung steht nur im Namen (`AUF-1.4`,
  `testAuf1_4…`). Spur: `python3 prozess/pruefungen/rueckverfolgung.py AUF-1.4`; Strg+Klick
  in VS Code: [Anliegen 124](../handoff/anliegen/124-sprungPerKlickErproben.md).
- `tests/einheit/` spiegelt `arbiter/`, etwa `tests/einheit/domaene/phasen/aufstellenTest.py`.
  Jeder Ordner dort hat eine `__init__.py`; sonst kollidiert der Dateiname mit dem
  Akzeptanztest. Prüft: `pytest technik/tests` bricht ab.
- `arbiter` liegt über `pythonpath` in `pyproject.toml` im Pfad, ohne `sys.path`-Eingriff.
  Prüft: `konfigurationTest.py`.

## Oberfläche
Auslöser: erstes Item mit Oberfläche. Das Design-System gehört der Technik: eine lebende
Komponentenseite (HTML, echtes CSS) als Doku, Vorlage der Mockups und Ziel eines
Bildschirmtests. Mockups nutzen nur vorhandene Komponenten, Neues ist ein Anliegen an die
Technik. Tot ist eine Komponente ohne Template. Messbare Gestaltungsregeln werden Prüfungen.
