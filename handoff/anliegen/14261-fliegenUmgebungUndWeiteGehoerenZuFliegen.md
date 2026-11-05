# Fliegen: Umgebung und Weite liegen bei der normalen Bewegung, dazu doppelter Aufbau

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Wartet ([Kritik](../../prozess/ablauf/kritik.md)): Namen und Ablage, keine Prüfung
rot, am Bildschirm kein Unterschied. Kritik am Code zu Item fliegen, Abschnitt B (`3c78499`).
Was schon in [14240](14240-fliegenDoppelteTypenUndImportUeberFliegen.md) steht, steht hier nicht.
1. Es S: `normaleBewegung.py` trägt `Weite` und `Umgebung`, obwohl nur *Fliegen* sie braucht.
   `Gleiten` liest aus der `Umgebung` nur `fremde` und `gegner`, nie `spielfeld` und `weiten`. Daher
   baut `_art` eine `Umgebung` ohne *Weite* und ersetzt sie im Zweig von *Fliegen* mit `replace`.
2. `verschobenUm` hat weitere Doppel: `_verschoben` in `anhaltenAufDemWeg.py` Zeile 83 und
   `einheitVerschieben.py` Zeile 13 und 20.
3. `Gleiten` und `Fliegen` haben denselben `__init__` mit vier Feldern, je elf Zeilen, nur
   um sie zu speichern.
4. `Fliegen.gründeBeimZiehen` und `Gleiten.gründeBeimZiehen` rufen die gleichnamige Funktion aus
   `normaleBewegung.py` auf. Das liest sich wie ein Aufruf ihrer selbst. Die beiden Methoden
   entscheiden nur, ob ‚Base überdeckt‘ beim Ziehen zählt.

**Kosten.** Bleibt es so, liest man bei der normalen Bewegung Begriffe von BEW-18 und hält beim
Lesen der Methoden kurz an. Der Umbau sind etwa 30 Zeilen ohne neue Logik; die Tests bleiben
gültig, bis auf ihre Importzeilen. Zu 1 kommt eine Glossarzeile dazu.

**Gegenvorschlag.**
1. `Weite` und `Umgebung` zurück nach `fliegen.py`; `Gleiten` bekommt `fremde` und `gegner`
   einzeln, `_art` baut die `Umgebung` nur im Zweig von *Fliegen*, ohne `replace`. Dann importiert
   [fliegenTest.py](../../technik/tests/einheit/domaene/phasen/bewegung/fliegenTest.py) sie richtig,
   14240 Punkt 1 entfällt. Die Zeile *Umgebung* im Glossar nennt dann BEW-17 nicht mehr: ein
   Anliegen an den Anforderungsautor. Hältst du `Umgebung` für beide für klarer, begründe es in der
   Stellungnahme; dann bleibt 14240 Punkt 1.
2. `_verschoben` öffentlich als `verschobenUm` in `anhaltenAufDemWeg.py`, `normaleBewegung.py` und
   `einheitVerschieben.py` nutzen es.
3. Beide Klassen als `@dataclass(frozen=True)`, wie `Gezogen` und `Umgebung`.
4. Die Methoden heißen `gründeWährendDesZiehens`, die Funktion bleibt.

**Stellungnahme.**
