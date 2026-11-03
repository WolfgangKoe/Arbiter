# Glossar: Gezeigt

Form: Kritik
Von: Implementierer
An: Anforderungsautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf (Hook, `glossarTest.py`), Item loslassenNebenDerKarte. Der Vertrag
([Ziehen](../../technik/architektur/vertrag/aufstellen/ziehen.md)) nennt die Klasse `Gezeigt`
(die *Stellen*, die eine Abfrage beim Loslassen nennt); sie steht in
[setzen.py](../../technik/arbiter/domaene/querschnitt/setzen.py), aber nicht im
[Glossar](../../domaene/glossar.md).

**Kosten.** Ohne Zeile bleibt der Hook rot und der Code uncommittet.

**Gegenvorschlag.** Zeile `Gezeigt | – | Gezeigt | …` mit der Erklärung: die *Stellen*, an
denen die *Modelle* stehen würden, wenn der Spieler jetzt losließe (AUF-24.3, 28).

**Stellungnahme.** Angenommen, leicht erweitert: Die Zeile `gezeigt | – | Gezeigt` im
[Glossar](../../domaene/glossar.md) nennt beide Aussagen des Vertrags, die *Stellen* je bewegt
gezeigtem *Modell* und ob AUF-29 es angehalten hat, mit den Kriterien der *Aufstellung* und
der *Bewegungsphase* (BEW-17.2, 20.1), die dasselbe zeigen. Unabhängig vom Ort, den der
Architekt für die Klasse festlegt. Nicht Teil dieses Anliegens: `Weiterrücken` aus demselben
Vertrag steht noch nicht im Glossar; wird es eine Klasse, braucht es ein eigenes Anliegen.
