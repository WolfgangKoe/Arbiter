# Architektur

Jede Regel nennt, was sie prüft. „Nur Text“ heißt: noch ohne Mechanismus; der Auslöser steht
dabei, danach baut der Regelumsetzer ihn auf Anliegen des Architekten.

## Schichten
```
technik/
  arbiter/
    domaene/    Fachlogik, nur Standardbibliothek
    speicher/   Datenbank; setzt die Schnittstellen der Domäne um
    katalog/    Importer: Katalog-YAML aus domaene/daten/ in die Datenbank
    web/        Flask; übersetzt Anfragen in Handlungen der Domäne
  frontend/     HTML, CSS, JS; spricht nur über HTTP mit web/
  tests/        akzeptanz/, einheit/
```
Ein Ordner entsteht mit dem ersten Item, das ihn braucht. Für AUF-1 nur `arbiter/domaene/`.

## Abhängigkeiten zeigen nach innen
- **A1** `arbiter.domaene` importiert nur die Standardbibliothek und sich selbst. Prüft: nur
  Text; Auslöser: der zweite Ordner unter `arbiter/`, dann ein Importvertrag (import-linter).
- **A2** `web`, `speicher` und `katalog` kennen die Domäne, nie umgekehrt. Braucht die
  Domäne Speicherung, beschreibt sie eine Schnittstelle (`typing.Protocol`) in
  `arbiter/domaene/`; `speicher/` setzt sie um, `web/` verdrahtet beides. Prüft: wie A1.
- **A3** Der Spielstand liegt nur in der Datenbank, Katalogdaten nur als YAML in
  `domaene/daten/` und importiert in der Datenbank. Prüft: nur Text; Auslöser: erster
  Spielstand, der eine Sitzung überlebt.

Altbestand: `ArbiterMap/backend/app/domain/rule_checks.py` importiert nur die eigene
Geometrie; `app/services/` übersetzt Datensätze in `ModelState`, bevor die Prüfung sie sieht.

## Grundschnitt der Domäne
`arbiter/domaene/` gliedert sich wie `domaene/anforderungen/`:
- `spielobjekte.py`: `Spieler`, `Armee`, `Einheit`, `Modell` und was mehr als eine Phase
  braucht.
- `phasen/<phase>.py` heißt wie die Anforderungsdatei. Was eine Phase einführt, liegt dort,
  bis eine zweite Phase es braucht; dann zieht es nach `spielobjekte.py`. Darum liegen
  `Aufstellungszone`, *aufgestellt* und *gesetzt* in `phasen/aufstellen.py`.
- `querschnitt/`: Fähigkeiten und Modifikatoren, mit der ersten Anforderung dort.
- `sperre.py`: `Sperre` und `Grund`; Übergehen und Protokoll gelten für alle Phasen.
- `messen.py`: die zwei Messungen (M1), mit dem ersten Abstand.
- `spielablauf/` nur unter `tests/akzeptanz/`: Szenarien über mehrere Phasen.

Ein Modul wird zum Paket, ohne dass sich ein Import ändert. Prüft: die Importe der
Akzeptanztests; Spiegel im Code: nur Text (DoD 2).

## Regeln im Domänencode
- **D1** Spielobjekte haben Identität: Vergleich mit `is`, `@dataclass(eq=False)`. Prüft:
  die Akzeptanztests, deren Spieler gleiche Armeen haben.
- **D2** Eine Handlung prüft erst alle Sperren, dann ändert sie den Zustand. So kann ein
  Übergehen dieselbe Prüfung überspringen und protokollieren. Prüft: jeder Akzeptanztest
  einer Sperre prüft den unveränderten Zustand.
- **D3** Zustand ändern nur Handlungen. Spielobjekte sind unveränderlich
  (`@dataclass(frozen=True, eq=False)`, Sammlungen als Tupel). Zustand einer Phase hält die
  Phase in `_`-Feldern; lesbar über Properties ohne Setter (`aufstellung.anDerReihe`) oder
  Abfragen nach dem Muster `aufstellung.aufstellungszone(spieler)`:
  `aufstellung.aufgestellt(einheit)`, `aufstellung.gesetzt(modell)`. Sonst umgeht
  `modell.gesetzt = True` jede Sperre und jedes Protokoll. Altbestand: `ModelState` in
  `rule_checks.py` ist `frozen`. Prüft: Python wirft bei der Zuweisung; dass alles so gebaut
  ist: nur Text; Auslöser: `web/`, dann eine Prüfung „in `arbiter/` nur `_`-Felder zuweisen,
  Dataclasses der Domäne `frozen`“.
- **M1** Phasen messen nur über zwei Messungen: Abstand zweier Modelle und Base vollständig
  in einer Fläche. Die Baseform kennt nur `messen.py`. Altbestand: `rule_checks.py` prüft
  Kohärenz und Engagement Range allein über `is_within_contours`. Prüft: nur Text; Auslöser:
  erster Abstand (Etappe 2), dann ein Vertragstest je Baseform und ein Importvertrag
  „`phasen` importiert keine Baseform“.

## Tests
- **T1** Je Anforderung eine Testdatei im Ordner der Anforderungsdatei: AUF-1 in
  `domaene/anforderungen/phasen/aufstellen.md` → `tests/akzeptanz/phasen/aufstellen/auf1Test.py`.
  Für die erste Anforderung genügt die Sammeldatei `tests/akzeptanz/phasen/aufstellenTest.py`.
  Höchstmaß: `prozess/kennzahlen.md`; darüber wird die Anforderung geteilt, nicht der Test.
  Prüft: `rueckverfolgung.py` (die Sammeldatei ist rot, sobald ein offenes Item eines
  freigegebenen Plans eine spätere Anforderung der Datei nennt; ebenso eine fehlende
  Testdatei einer genannten Anforderung, ein Test in der Datei einer fremden Anforderung und
  Sammel- neben Einzeldatei derselben Anforderung), `benennung.py`, `hoechstmassTest.py`.
- **T2** Der Weg vom Kriterium zum Test und zurück wird berechnet, nicht gespeichert: keine
  Links in Anforderung oder Test, die Zuordnung steht nur im Namen. Spur:
  `python3 prozess/pruefungen/rueckverfolgung.py AUF-1.4` (auch Testname oder `pfad:zeile`).
  VS-Code-Versuch `prozess/pruefungen/sprung/`, Klick unerprobt:
  [Anliegen 83](../handoff/anliegen/83-sprungErproben.md).
- `tests/einheit/` spiegelt `arbiter/`: `tests/einheit/domaene/phasen/aufstellenTest.py`
  zu `arbiter/domaene/phasen/aufstellen.py` (Name offen:
  Anliegen 28). Jeder Ordner dort hat eine `__init__.py`; sonst
  kollidiert der Dateiname mit dem Akzeptanztest. Prüft: `pytest technik/tests` bricht ab.
- `arbiter` liegt über den Suchpfad `technik` in `pyproject.toml` im Pfad, ohne
  `sys.path`-Eingriff. Prüft: `konfigurationTest.py`.

## Oberfläche
Auslöser: erstes Item mit Oberfläche. Das Design-System gehört der Technik. Eine lebende
Komponentenseite (HTML mit dem echten CSS) ist Doku, Vorlage für Mockups und Ziel eines
Bildschirmtests. Mockups nutzen nur vorhandene Komponenten; Neues geht als Anliegen an die
Technik. Tot ist eine Komponente, die in keinem Template vorkommt. Messbare
Gestaltungsregeln (Kontrast, Mindestgrößen) werden Prüfungen.
