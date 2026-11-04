# Nach dem Anhalten auf dem Weg kürzt die Bewegung ab zuvor statt nach V16

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** `Bewegungsphase._gezeigt`
(`technik/arbiter/domaene/phasen/bewegung/__init__.py`, `start = zuvor if
weiter.angehaltenAufDemWeg else ebene`): Mit `angehaltenAufDemWeg` hält es auf der Strecke von
zuvor zum Punkt nach BEW-3.1, 6.1 und 6.2 an und prüft 17.1 dort.
[Ziehen](../../technik/architektur/vertrag/bewegung/ziehen.md) und BEW-17.1 nehmen die
*Stellen* nach V16 ab der *Stelle* vor dem Ziehen und halten auf der Strecke von zuvor dorthin
nur zudem nach 6.2 an (17.4). Probe `/tmp/rev12700probe/probe.py` (Base 25 mm,
*Bewegungsweite* 5″, Beginn (0, 0), zuvor (0, 3), Zeiger (20, 3), nichts im Weg): gezeigt
(4, 3), nach Vertrag (4,94, 0,74). Kein Test entscheidet das (Probe in `/tmp/rev12700`: mit dem
Vertrag bleiben alle Tests zu BEW-17 grün).

**Kosten.** Code und Vertrag sagen für dieselbe Abfrage verschiedene *Stellen*; 12620 hatte
gerade Code und Tests an den Vertrag gebracht. Ob 17.1 greift, entscheidet mit
`angehaltenAufDemWeg` eine andere *Stelle*, als das Kriterium nennt.

**Gegenvorschlag.** Halt immer nach V16 ab `ebene`; bei `angehaltenAufDemWeg` danach auf der
Strecke von zuvor zu diesem Halt nur `anteilBisZurNahkampfreichweite`; das Angebot nach BEW-8.3
aus demselben Anteil. Ein Einheitstest mit den Zahlen oben. Hältst du das jetzige Verhalten für
richtig (es bleibt auf der Strecke zum Zeiger), dann Anliegen an den Architekten, den Vertrag
zu ändern; der Test entfällt nicht.

**Stellungnahme.** Angenommen, wie vorgeschlagen umgesetzt: `Bewegungsphase._gezeigt`
(`technik/arbiter/domaene/phasen/bewegung/__init__.py`) hält immer nach V16 ab `ebene` an; bei
`angehaltenAufDemWeg` kürzt `_gekürztAnDerNahkampfreichweite` danach die Strecke von zuvor zu
diesem Halt nur um `anteilBisZurNahkampfreichweite`; das Angebot nach BEW-8.3 folgt aus beiden
Anteilen. Einheitstest mit den Zahlen der Probe, (4,94; 0,74):
`technik/tests/einheit/domaene/phasen/bewegung/bewegungsphaseTest.py`. Alle Tests zu BEW grün.
