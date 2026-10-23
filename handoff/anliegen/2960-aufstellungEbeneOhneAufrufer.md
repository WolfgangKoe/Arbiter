# Aufstellung.ebene hat keinen Aufrufer mehr

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: angenommen
Wartet auf: Technikphase

## Runde 1
**Befund.** Seit Anliegen 1651 fragen die Aufrufer `ganzeEinheitIstEbene` und `modellIstEbene`.
Die Durchreichung `Aufstellung.ebene`
([`__init__.py`](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py):79–80) ruft niemand
mehr auf, weder Produkt noch Akzeptanztests; nur
[auswahlTest.py](../../technik/tests/einheit/domaene/phasen/aufstellen/auswahlTest.py) prüft
`Auswahl.ebene` selbst. Nach [Ich 3](../../prozess/praemissen/ich.md) wartet das: keine Prüfung
rot, Ablage einer Hilfsfunktion.

**Kosten.** Wer die Schnittstelle der `Aufstellung` liest, hält die alte Frage per `is` für
erlaubt; der nächste Aufrufer greift wieder zu ihr statt zur benannten Frage (Es, SOLID I).

**Gegenvorschlag.** `Aufstellung.ebene` streichen. `Auswahl.ebene` bleibt, solange ihr Test sie
braucht, oder fällt mit, wenn die beiden benannten Fragen ihn tragen.

Erledigt: `Aufstellung.ebene` gestrichen, Tests grün.

**Stellungnahme.** Angenommen und umgesetzt: `Aufstellung.ebene` und, wie in 2821, auch
`Auswahl.ebene` sind gestrichen; auswahlTest.py fragt die beiden benannten Fragen.
