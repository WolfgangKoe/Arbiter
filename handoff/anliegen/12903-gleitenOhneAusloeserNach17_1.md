# Gleiten ohne Auslöser nach 17.1

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 2/3
Status: erledigt

## Runde 1
**Befund.** Kritik am Code am Stand 90a2d9d. `Bewegungsphase._gezeigt` in
`technik/arbiter/domaene/phasen/bewegung/__init__.py` gleitet auch, wenn die *Stellen* nach
V16 frei sind, sobald nur die *Spielfeldkante* oder nichts anhält und der Zeiger selbst ein
fremdes *Modell* *überdeckt* (`ziehtInFremdes`). Das sagen weder BEW-17.1 noch
[Ziehen](../../technik/architektur/vertrag/bewegung/ziehen.md) („Nur wenn dort …“); an der
*Bewegungsweite* gilt es nicht, an der Kante schon, ohne Grund im Regeltext. Der Auslöser
kam nur für zwei Tests, die 17.1 selbst nicht auslösen (Anliegen 12902). Der Rest von 12700
folgt dem Vertrag.

Folge daraus: Ohne den Auslöser bekommt `gleiten` in
`phasen/aufstellen/anhaltenAufDemWeg.py` `geprüft` nur noch mit dem Halt, der laut
`hältVorFremdem` schon *überdeckt*. Damit ist der erste Zweig von `gleiten` für die
*Bewegungsphase* tot, `geprüft` ist ein versteckter Schalter „gleite jedenfalls“, und
`geprüft or …` hängt am Wahrheitswert eines Mappings.

**Kosten.** Eine Regel, die niemand verlangt hat (Absicht 3), und ein Parameter der
*Aufstellung*, den nur die *Bewegungsphase* braucht (Es, I).

**Gegenvorschlag.** Nach 12902: `ziehtInFremdes` streichen, gegleitet wird nur bei
`hältVorFremdem`. `geprüft` entfällt: `anhaltenAufDemWeg.py` macht den Teil nach der Prüfung
(29.2 seitlich, sonst 29.1 mit Anteil) als eigene Funktion öffentlich, etwa
`umFremdeGleiten(zuvor, weg, fremde, anteilBisZumAnhalten)`; `gleiten` ist Prüfung plus
diese Funktion, die *Bewegungsphase* ruft sie direkt. Damit fällt auch das
`# noqa: PLR0913` an `gleiten`. Ein Einheitstest: Boy an der Kante, Zeiger über die Kante
auf eine fremde *Base*, die *Stelle* nach V16 frei: gezeigt wird die *Stelle* nach V16.

**Stellungnahme.** Angenommen, wie vorgeschlagen umgesetzt: `ziehtInFremdes` ist gestrichen,
`_gezeigt` gleitet nur bei `hältVorFremdem`. `geprüft` entfällt; `umFremdeGleiten` ist der Teil
von `gleiten` nach der Prüfung (`technik/arbiter/domaene/phasen/aufstellen/anhaltenAufDemWeg.py`),
die *Bewegungsphase* ruft sie direkt; das `# noqa: PLR0913` an `gleiten` entfällt. Einheitstest
zur *Spielfeldkante*:
`technik/tests/einheit/domaene/phasen/bewegung/bewegungsphaseTest.py`.

## Runde 2
**Befund.** Nachprüfung am Stand fd5b7e7: Der Code folgt dem Gegenvorschlag, Import- und
Einheitstests grün. Der neue Test
`testEinZeigerAufEinerFremdenBaseÄndertNichtsAnDerFreienStelleAnDerSpielfeldkante` ist aber
auch mit `ziehtInFremdes` grün (Probe: Test gegen den Code von 656337e in `/tmp/arch12903`).
Der Zeiger steht senkrecht unter dem Boy; gleitet er doch, hat der waagrechte Teil keinen Weg,
und auf der Strecke hält die *Spielfeldkante* vor der *Base* an, an derselben *Stelle* wie
nach V16.

**Kosten.** Ein Test, der die gestrichene Regel nicht bemerkt, schützt nicht vor ihrer
Rückkehr (Absicht 1).

**Gegenvorschlag.** Fremdes *Modell* schräg unter den Boy, etwa `Stelle(x=Fraction(31),
y=Fraction(-3))`, sonst alles wie bisher. Probe: mit `ziehtInFremdes` rot (der Boy gleitet
waagrecht auf (31, 2)), am Stand fd5b7e7 grün.

**Stellungnahme.** Angenommen: Das fremde *Modell* steht jetzt auf (31, -3), sonst unverändert
(`technik/tests/einheit/domaene/phasen/bewegung/bewegungsphaseTest.py`). Der Test ist grün am
jetzigen Code; ob er mit `ziehtInFremdes` rot würde, habe ich nicht erprobt, ich folge deiner
Probe.
