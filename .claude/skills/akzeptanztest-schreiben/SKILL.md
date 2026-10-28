---
name: akzeptanztest-schreiben
description: Akzeptanztests zu einer Anforderung schreiben: Datei, Namen, Aufbau, Sperren, jeder Spieler. Beispiel aus AUF-7, Gegenbeispiele aus AUF-7 und QUE-9.
---
# Akzeptanztest schreiben

Benennung nach `prozess/praemissen/es.md`, Umfang nach `.claude/agents/testautor.md`.

## Datei
Eine Testdatei je Anforderung, Name und Ort nach `technik/architektur.md`, T1:
`domaene/anforderungen/phasen/aufstellen/einheitInAufstellung.md` →
`technik/tests/akzeptanz/phasen/aufstellen/einheitInAufstellungTest.py`.
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
AUF-7.3 aus `einheitInAufstellungTest.py`:

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

## Gegenbeispiel: Form
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

## Gegenbeispiel: nur Spieler 1
QUE-9.2 gilt für jeden *Spieler*, der „Erster Zug“ klickt; dieser Test prüft nur einen:

```python
def testQue9_2DerDienstSetztDenSpielerMitDemErstenZugAmZug(dienstNachDerAufstellung):
    antwort = ersterZugWählen(dienstNachDerAufstellung, 1)

    assert antwort.get_json()["schlacht"]["amZug"] == 1
```

Schlecht: Ein Fehler, der nur Spieler 2 trifft, bleibt grün. Nennt das Kriterium jeden
*Spieler* oder jede *Schlachtrunde*, prüft der Test jeden als `parametrize`, so in
`ersterZugTest.py`:
`@pytest.mark.parametrize("spielernummer", [1, 2], ids=["spielerEins", "spielerZwei"])`.
