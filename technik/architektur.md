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
- **A1** `arbiter.domaene` importiert nur die Standardbibliothek und sich selbst: kein
  Flask, keine Datenbank, nichts aus `web`, `speicher`, `katalog`. Prüft: nur Text;
  Auslöser: der zweite Ordner unter `arbiter/`, dann ein Importvertrag (import-linter).
- **A2** `web`, `speicher` und `katalog` kennen die Domäne, nie umgekehrt. Braucht die
  Domäne Speicherung, beschreibt sie eine Schnittstelle (`typing.Protocol`) in
  `arbiter/domaene/`; `speicher/` setzt sie um, `web/` verdrahtet beides. Prüft: wie A1.
- **A3** Der Spielstand liegt nur in der Datenbank, Katalogdaten nur als YAML in
  `domaene/daten/` und importiert in der Datenbank. Prüft: nur Text; Auslöser: erster
  Spielstand, der eine Sitzung überlebt.

Beispiel aus dem Altbestand: `ArbiterMap/backend/app/domain/rule_checks.py` importiert
nichts außer der eigenen Geometrie; `app/services/` übersetzt Datensätze in `ModelState`,
bevor die Prüfung sie sieht. So lässt sich die Regel ohne Flask und Datenbank testen.

## Grundschnitt der Domäne
`arbiter/domaene/` gliedert sich wie `domaene/anforderungen/`:
- `spielobjekte.py`: `Spieler`, `Armee`, `Einheit`, `Modell` und was mehr als eine Phase
  braucht.
- `phasen/<phase>.py`: heißt wie die Anforderungsdatei, `phasen/aufstellen.py` zu
  `domaene/anforderungen/phasen/aufstellen.md`. Was eine Phase einführt, liegt dort, bis
  eine zweite Phase es braucht; dann zieht es nach `spielobjekte.py`. Darum liegt
  `Aufstellungszone` heute in `phasen/aufstellen.py`.
- `querschnitt/`: Fähigkeiten und Modifikatoren, mit der ersten Anforderung dort.
- `sperre.py`: `Sperre` und `Grund`; jede Phase sperrt, Übergehen und Protokoll gelten für
  alle (`domaene/ziel.md`).
- `messen.py`: die zwei Messungen (M1), mit dem ersten Abstand.
- `spielablauf/` gibt es nur unter `tests/akzeptanz/`: Szenarien über mehrere Phasen.

Ein Modul wird zum Paket, ohne dass sich ein Import ändert. Prüft: die Importe der
Akzeptanztests; Spiegel im Code: nur Text (DoD 2).

Für AUF-1:
```python
from arbiter.domaene.spielobjekte import Armee, Einheit, Modell, Spieler
from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone
from arbiter.domaene.sperre import Grund, Sperre
```

## Regeln im Domänencode
- **D1** Spielobjekte haben Identität: Vergleich mit `is`, Gleichheit nicht überschrieben
  (`@dataclass(eq=False)`). Zwei Einheiten mit gleichen Modellen sind verschiedene
  Einheiten. Prüft: die Akzeptanztests, deren Spieler gleiche Armeen haben
  (`testAuf1_4EinModellDesGegnersIstNichtInAufstellung`).
- **D2** Eine Handlung prüft erst alle Sperren, dann ändert sie den Zustand; die `Sperre`
  fällt vor der ersten Änderung. So kann ein späteres Übergehen dieselbe Prüfung
  überspringen und protokollieren. Prüft: jeder Akzeptanztest einer Sperre prüft den
  unveränderten Zustand.
- **M1** Phasen messen nur über zwei Messungen: Abstand zweier Modelle und Base vollständig
  in einer Fläche. Die Baseform kennt nur `messen.py`; eine neue Form (Etappe 6) ändert
  keine Phase. Altbestand: `rule_checks.py` prüft Kohärenz und Engagement Range allein über
  `is_within_contours`. Prüft: nur Text; Auslöser: erster Abstand (Etappe 2), dann ein
  Vertragstest je Baseform und ein Importvertrag „`phasen` importiert keine Baseform“.

## Tests
- `tests/akzeptanz/<pfad>Test.py` spiegelt `domaene/anforderungen/<pfad>.md`. Prüft:
  `rueckverfolgung.py`, `benennung.py`.
- `tests/einheit/` spiegelt `arbiter/`: `tests/einheit/domaene/phasen/aufstellenTest.py`
  zu `arbiter/domaene/phasen/aufstellen.py` (Name offen:
  [Anliegen 28](../handoff/anliegen/28-benennungOffenePunkte.md)). Jeder Ordner unter
  `tests/einheit/` hat eine `__init__.py`; sonst kollidiert der gleiche Dateiname mit dem
  Akzeptanztest. Prüft: `python3 -m pytest technik/tests` bricht sonst beim Sammeln ab.
- Code findet `arbiter` über den Suchpfad `technik` in `pyproject.toml`, ohne
  `sys.path`-Eingriff. Prüft: `konfigurationTest.py`.

## Oberfläche
Auslöser: erstes Item mit Oberfläche. Das Design-System gehört der Technik, die Domäne
kritisiert es. Eine lebende Komponentenseite (HTML mit dem echten CSS) ist Doku, Vorlage für
Mockups und Ziel eines Bildschirmtests. Mockups nutzen nur vorhandene Komponenten; Neues geht
als Anliegen an die Technik. Tot ist eine Komponente, die in keinem Template vorkommt.
Messbare Gestaltungsregeln (Kontrast, Mindestgrößen) werden Prüfungen.
