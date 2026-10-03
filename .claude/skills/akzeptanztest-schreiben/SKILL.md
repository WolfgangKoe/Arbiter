---
name: akzeptanztest-schreiben
description: Akzeptanztests zu einer Anforderung schreiben: Datei, Namen, Aufbau, Sperren. Beispiel und Gegenbeispiel aus AUF-1.
---
# Akzeptanztest schreiben

Benennung nach `prozess/praemissen/wir.md`, Umfang nach `.claude/agents/testautor.md`.

## Datei
Eine Testdatei je Anforderungsdatei, im gespiegelten Ordner:
`domaene/anforderungen/phasen/aufstellen.md` → `technik/tests/akzeptanz/phasen/aufstellenTest.py`.
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
AUF-1.6 aus `technik/tests/akzeptanz/phasen/test_auf_1.py`, nach der Prämisse benannt:

```python
def sperrgrund(handlung, *argumente) -> Grund:
    with pytest.raises(Sperre) as sperre:
        handlung(*argumente)
    return sperre.value.grund


def testAuf1_6MitGesetztemModellIstDieEinheitBegonnen(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    begonnene, andere = zweiterSpieler.armee.einheiten
    erstesModell, *weitereModelle = begonnene.modelle
    aufstellung.einheitInAufstellungWählen(begonnene)
    aufstellung.modellSetzen(erstesModell)

    grund = sperrgrund(aufstellung.einheitInAufstellungWählen, andere)

    assert grund is Grund.EINHEIT_BEGONNEN
    assert aufstellung.einheitInAufstellung is begonnene
```

Gut: Der Name sagt Kriterium und Aussage, die Handlung steht allein, geprüft werden Grund und
unveränderter Zustand, jedes Fachobjekt hat einen Namen aus dem Glossar.

## Gegenbeispiel
AUF-1.5 aus `test_auf_1.py`, wie es dort steht:

```python
def test_auf_1_5_nach_der_aufstellung_ist_keine_einheit_wählbar(aufstellung, a, b):
    ...
    for einheit in a.armee.einheiten + b.armee.einheiten:
        assert sperrgrund(lambda e=einheit: aufstellung.einheit_in_aufstellung_wählen(e)) is Grund.NICHT_WÄHLBAR
```

Schlecht: snake_case, Fixtures `a` und `b`, lambda mit Bindung per Standardargument, die
Handlung steckt im Assert, die Schleife verschweigt, welche Einheit scheitert. Ebenso
`b.armee.einheiten[0]` in AUF-1.4: Wer ist `[0]`?
