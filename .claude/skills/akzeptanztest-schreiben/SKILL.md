---
name: akzeptanztest-schreiben
description: Akzeptanztests zu einer Anforderung schreiben: Datei, Namen, Aufbau, Sperren. Beispiel und Gegenbeispiel aus AUF-7.
---
# Akzeptanztest schreiben

Benennung nach `prozess/praemissen/es.md`, Umfang nach `.claude/agents/testautor.md`.

## Datei
Eine Testdatei je Anforderung, Name und Ort nach `technik/architektur.md`, T1: AUF-7 →
`technik/tests/akzeptanz/phasen/aufstellen/auf7Test.py`.
Erste Zeile ein einzeiliger Docstring mit Kürzel und Name: `"""AUF-7 · Einheit in Aufstellung."""`.
Gemeinsame Handgriffe (`sperrgründe`, `nachDerWahlDerAufstellungszone`) stehen in
`technik/tests/akzeptanz/handgriffe.py`.
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
AUF-7.3 aus `technik/tests/akzeptanz/phasen/aufstellen/auf7Test.py`:

```python
def testAuf7_3EinModellEinerAnderenEinheitIstEinheitBegonnen(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    begonneneEinheit, andereEinheit = zweiterSpieler.armee.einheiten
    erstesModell, _ = begonneneEinheit.modelle
    modellDerAnderenEinheit, *_ = andereEinheit.modelle
    stelle = stelleDesErstenModells(aufstellung, zweiterSpieler, begonneneEinheit)
    stelleDerAnderenEinheit = stelleDesErstenModells(aufstellung, zweiterSpieler, andereEinheit)
    aufstellung.modellSetzen(erstesModell, stelle)

    gründe = sperrgründe(aufstellung.modellSetzen, modellDerAnderenEinheit, stelleDerAnderenEinheit)

    assert gründe == {Grund.einheitBegonnen}
    assert not aufstellung.gesetzt(modellDerAnderenEinheit)
    assert aufstellung.einheitInAufstellung is begonneneEinheit
```

Gut: Der Name sagt Kriterium und Aussage, die Handlung steht allein, geprüft werden die
Gründe und der unveränderte Zustand, jedes Fachobjekt hat einen Namen aus dem Glossar.

## Gegenbeispiel
AUF-7.2, wie es nicht stehen soll:

```python
def test_auf_7_2_nach_der_aufstellung_ist_kein_modell_wählbar(aufstellung, a, b):
    ...
    for modell in a.armee.einheiten[0].modelle + b.armee.einheiten[0].modelle:
        assert sperrgründe(lambda m=modell: aufstellung.modell_setzen(m, stelle)) == {Grund.NICHT_WÄHLBAR}
```

Schlecht: snake_case, Fixtures `a` und `b`, `einheiten[0]` statt eines Namens, lambda mit
Bindung per Standardargument, die Handlung steckt im Assert, die Schleife verschweigt,
welches Modell scheitert.
