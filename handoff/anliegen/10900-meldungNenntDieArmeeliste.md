# Meldung zur aufgestellten Einheit nennt die Armeeliste

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik am Code (Lesbarkeit) zur Umsetzung von
Anliegen 8121 Punkt 2, uncommittet. Wartet nach
[Kritik](../../prozess/ablauf/kritik.md): Namen, keine Prüfung rot.
[aufstellen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py),
`Aufstellung.auswählen`, meldet „Eine aufgestellte Einheit wählt man nicht über die
Einheitenkarte“. *Einheitenkarte* steht nicht im [Glossar](../../domaene/glossar.md)
([Wir 2](../../prozess/praemissen/wir.md)); der Weg, den die Sperre schützt, ist die
*Armeeliste*: Die Route ruft `auswählen` nur über `einheitInDerArmeeliste`
([anwendung.py](../../technik/arbiter/web/anwendung.py)), und die *Armeeliste* zeigt nach dem
Glossar nur nicht *aufgestellte* *Einheiten*. Der Begriff kam aus meinem Gegenvorschlag in 8121.

**Kosten.** Am Bildschirm nichts. Bleibt es, sucht ein Leser eine *Einheitenkarte*, die es im
Glossar nicht gibt. Eine Zeile.

**Gegenvorschlag.** Die Meldung nennt den Begriff des Glossars, etwa „Eine aufgestellte Einheit
steht nicht in der Armeeliste“.

**Stellungnahme.** Angenommen, umgesetzt mit Anliegen 10880 Punkt 2: Die Meldung lautet
„Eine aufgestellte Einheit steht nicht in der Armeeliste“.
