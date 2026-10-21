# Architektur

Jede Regel nennt, was sie prüft. „Nur Text“: ohne Mechanismus; ein Auslöser dabei: Danach
baut ihn der Regelumsetzer auf Anliegen des Architekten.

## Schichten
Hexagonal: Die Domäne kennt keine Technik, Adapter stecken an den Ports von
[`anwendung/`](architektur/anwendung.md).
```
technik/
  frontend/     HTML, CSS, JS; nur über HTTP an web/
  arbiter/
    web/        Flask: Anfrage → Befehl, Spielstand → JSON, Sperre → 409
    anwendung/  je Handlung ein Dienst; Ports, Befehle, Spielstand
    katalog/    Port Katalog: YAML aus domaene/daten/
    speicher/   Port Partien: die Folge der Befehle (P2)
    domaene/    Fachlogik
    __main__.py steckt Adapter und Dienste zusammen (W5)
  tests/        akzeptanz/, einheit/
```
Ordner entstehen mit dem ersten Item, das sie braucht. Themen: [Web](architektur/web.md),
[Vertrag](architektur/vertrag.md), [Oberfläche](architektur/oberflaeche.md),
[Speicher](architektur/speicher.md).

## Abhängigkeiten zeigen nach innen
- **A1** `arbiter.domaene` importiert nur die Standardbibliothek und sich selbst. Prüft:
  `formregeln/importvertrag.py`, auch relative Importe.
- **A2** Außen kennt innen, nie umgekehrt: `anwendung/` und `katalog/` kennen die Domäne,
  `speicher/` nur `anwendung/` (P1); `katalog/` und `speicher/` kennt nur `__main__.py`.
  Prüft: wie A1, `speicher/` nach P1; der Rest nur Text.
- **A3** Katalogdaten stehen nur als YAML in `domaene/daten/`, `katalog/` liest sie
  (`yaml.safe_load`). Prüft: nur Text; Auslöser: erstes Modul in `speicher/`.
- **A4** `web/` kennt von `arbiter` nur `anwendung/`; `anwendung/` nur die Domäne und die
  Standardbibliothek. Prüft: nur Text; Auslöser: Freigabe des Plans mit dem ersten Item zum
  Speicher, dann `formregeln/importvertrag.py` vor dem Umbau.

## Grundschnitt der Domäne
`arbiter/domaene/` spiegelt `domaene/anforderungen/`:
- Ein Ordner der Anforderungen ist ein Modul (`spielobjekte.py`), ein Paket
  (`phasen/aufstellen/__init__.py`), sobald eine seiner Anforderungen ein Modul hat. Darin
  liegt, was mehrere seiner Anforderungen brauchen (`Aufstellung`, Spielobjekte).
- Eine Anforderung mit eigenen Regeln der Domäne wird ein gleichnamiges Modul:
  `phasen/aufstellen/auswahl.md` → `phasen/aufstellen/auswahl.py` (`Auswahl`). Anzeige und
  Bedienung (`karte.md`) liegen in `web/` und `frontend/`.
- Ohne Anforderung nur die Werkzeuge `sperre.py` (`Sperre`, `Grund`) und `messen.py` (M1).

Wird ein Modul zum Paket, bleiben die Importe dessen, was im Ordnermodul bleibt. Prüft:
kein Modul ohne Spiegel `formregeln/spiegel.py`; was wohin gehört der Reviewer.

## Stelle und Rechnen
- **S1** Eine *Stelle* ist der Mittelpunkt der *Base*, `Stelle(x, y)` in Zoll, Ursprung in
  einer Ecke des Spielfelds; x läuft entlang der ersten Seitenlänge aus `onlyWar.yaml` (44″),
  y entlang der zweiten (60″). Die erste *Aufstellungszone* liegt an der Kante x = 0, die
  zweite an x = 44. Prüft: die Fixture `zone`.
- **S2** Gerechnet wird exakt mit `fractions.Fraction`, ohne Toleranz und ohne Wurzel:
  Durchmesser in ganzen mm, 1″ = 254/10 mm, Abstände als Quadrate verglichen; `web/`
  übersetzt in `Fraction`. Mit `float` überdecken sich zwei berührende Boyz.
  Prüft: die Grenzfälle der Akzeptanztests.
- **S3** Anhalten (AUF-26.2, 26.3, [V10](architektur/handlungen.md)): Die Berührung ist eine
  Wurzel, darum hält Arbiter auf einem Raster des Wegs an: Anteil k/n mit
  n = ⌈100 · (|Δx| + |Δy|)⌉, das größte k vor der ersten Überdeckung, exakt nachgeprüft (S2);
  so liegt der Halt höchstens 1/100″ vor der Berührung, wie die *Formation* (`setzenPerKlick.py`).
  Vorbild: `ArbiterMap/backend/app/domain/geometry.py:942`. Prüft: V10, Unit-Tests zu `messen.py`.

## Regeln im Domänencode
- **D1** Spielobjekte haben Identität: Vergleich mit `is`, `@dataclass(eq=False)`. Werte
  (`Stelle`, `Base`) nach Inhalt. Prüft: Akzeptanztests (gleiche Armeen, gleiche Stellen).
- **D2** Eine Handlung prüft erst alle Sperren, dann ändert sie den Zustand; so überspringt
  ein Übergehen die Prüfung und protokolliert. Prüft: je Handlung und Grund ein
  Akzeptanztest auf den unveränderten Zustand.
- **D3** Zustand ändern nur Handlungen und das Auswählen ([Vertrag, V3](architektur/vertrag.md)).
  Spielobjekte sind `frozen`, Sammlungen Tupel oder `MappingProxyType`. Die Phase hält ihren
  Zustand in `_`-Feldern, lesbar über Properties ohne Setter oder Abfragen
  (`aufstellung.gesetzt(modell)`). Andere Schichten lesen keine `_`-Felder; `web/` ändert
  Attribute nur an `self`, nie per `object.__setattr__`, das `frozen` umgeht.
  Prüft: Python wirft bei der Zuweisung; der Rest nur Text.
- **D4** Gründe, die zusammen gelten, stehen in einer Tabelle Grund → Prüfung oder
  Grund → Befund im Modul ihrer Anforderung (`sperrenBeimSetzen.py`, `beenden.py`); die
  Handlung sammelt ein, ein neuer Grund ist eine Zeile; ein ausschließender Grund bleibt
  Wächter. Prüft: `formregeln/gruendeTabellen.py`
  ([Regeln](../prozess/regeln.md#formregeln)).
- **M1** Die Baseform kennt in der Domäne nur `messen.py`; Phasen messen nur mit dessen
  Messungen: *überdecken*, *Abstand* höchstens, *ganz in* einer Fläche, der kürzeste Weg,
  der *Bases* gemeinsam *ganz in* eine Fläche rückt, der Anteil eines Wegs bis zur ersten
  Berührung (S3). Prüft: nur Text; Auslöser: zweite
  Baseform (Etappe 6), dann je Baseform ein Vertragstest.

## Tests
- **T1** Spiegel: `domaene/anforderungen/<pfad>/<name>.md` → `tests/akzeptanz/<pfad>/<name>Test.py`,
  daneben nur Hilfsmodule (`handgriffe.py`). Die Testdatei übernimmt von ihrer Anforderung
  (1) die Überschrift als Docstring (`"""AUF-7 · Einheit in Aufstellung."""`), (2) nur deren
  Kriterien (`testAuf7_<m>…`), (3) deren Reihenfolge: die Tests eines Kriteriums beisammen,
  in der Folge der Kriterien, (4) Gegeben, wenn, dann als Aufbau, Handlung, Prüfung, durch
  Leerzeilen getrennt; ohne **wenn** keine Handlung. Prüft: der Ort
  `formregeln/benennung.py`, 1 bis 3 `formregeln/spiegel.py`; 4 Kritik am Code.
- **T2** Der Weg vom Kriterium zum Test und zurück wird berechnet, nicht gespeichert: keine
  Links in Anforderung oder Test, die Zuordnung steht nur im Namen (`AUF-7.3`,
  `testAuf7_3…`). Spur: [Regeln](../prozess/regeln.md).
- `tests/einheit/` spiegelt `arbiter/`. Jeder Ordner dort hat `__init__.py`, sonst
  kollidieren Dateinamen mit Akzeptanztests. Prüft: `pytest technik/tests` bricht ab.
- `arbiter` liegt über `pythonpath` (`pyproject.toml`) im Pfad, ohne `sys.path`. Prüft: nur Text.
