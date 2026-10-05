---
name: akzeptanztest-schreiben
description: Akzeptanztests zu einer Anforderung schreiben: Datei, Namen, Aufbau, Sperren. Beispiel und Gegenbeispiel aus AUF-1.
---
# Akzeptanztest schreiben

Benennung nach `prozess/praemissen/es.md`, Umfang nach `.claude/agents/testautor.md`.

## Datei
Eine Testdatei je Anforderung, Name und Ort nach `technik/architektur.md`, T1: AUF-1 →
`technik/tests/akzeptanz/phasen/aufstellen/auf1Test.py`. Heute steht AUF-1 als einzige
Anforderung ihrer Datei in `phasen/aufstellenTest.py`; mit der zweiten wird geteilt.
Erste Zeile ein einzeiliger Docstring mit Kürzel und Name: `"""AUF-1 · Reihenfolge der Aufstellung."""`.
Fixtures in `conftest.py` heißen nach dem, was sie sind (`ersterSpieler`), nicht `a`, `b`.

## Aufbau eines Tests
- Ein Test je Aussage des Kriteriums; der Name ist Kriterium plus Aussage als Satz.
- Drei Blöcke, durch Leerzeilen getrennt: Vorgeschichte, genau eine Handlung, Prüfung.
- Eine Sperre prüft den Grund und dass der Zustand unverändert bleibt.
- Fachobjekte entpacken und benennen statt indizieren; Handlung und Argumente getrennt
  übergeben statt in ein lambda zu wickeln.
- Mehrere Fälle einer Äquivalenzklasse als `pytest.mark.parametrize` mit sprechenden `ids`,
  keine Schleife über Asserts.

## Beispiel
AUF-1.6 aus `technik/tests/akzeptanz/phasen/aufstellenTest.py`:

```python
def sperrgrund(handlung, *argumente) -> Grund:
    with pytest.raises(Sperre) as sperre:
        handlung(*argumente)
    return sperre.value.grund


def testAuf1_6MitGesetztemModellIstDieEinheitBegonnen(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    begonneneEinheit, andereEinheit = zweiterSpieler.armee.einheiten
    erstesModell, *_ = begonneneEinheit.modelle
    aufstellung.einheitInAufstellungWählen(begonneneEinheit)
    aufstellung.modellSetzen(erstesModell)

    grund = sperrgrund(aufstellung.einheitInAufstellungWählen, andereEinheit)

    assert grund is Grund.einheitBegonnen
    assert aufstellung.einheitInAufstellung is begonneneEinheit
```

Gut: Der Name sagt Kriterium und Aussage, die Handlung steht allein, geprüft werden Grund und
unveränderter Zustand, jedes Fachobjekt hat einen Namen aus dem Glossar.

## Gegenbeispiel
AUF-1.5, wie es nicht stehen soll:

```python
def test_auf_1_5_nach_der_aufstellung_ist_keine_einheit_wählbar(aufstellung, a, b):
    ...
    for einheit in a.armee.einheiten + b.armee.einheiten:
        assert sperrgrund(lambda e=einheit: aufstellung.einheit_in_aufstellung_wählen(e)) is Grund.NICHT_WÄHLBAR
```

Schlecht: snake_case, Fixtures `a` und `b`, lambda mit Bindung per Standardargument, die
Handlung steckt im Assert, die Schleife verschweigt, welche Einheit scheitert. Ebenso
`b.armee.einheiten[0]` in AUF-1.4: Wer ist `[0]`?
