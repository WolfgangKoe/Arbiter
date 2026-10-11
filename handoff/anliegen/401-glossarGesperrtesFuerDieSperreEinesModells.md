# Glossar: Name für das, was ein gesperrtes Modell festhält

401 · Kritik · von Implementierer (Technik) → Anforderungsautor (Domäne) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Zu [Anliegen 397](397-gesperrteAlsTupelUndOrtDerFormation.md), Punkt 1: Je
*gesperrtem* *Modell* hält `Aufstellung` seine *Stelle*, die *Gründe*, die vorige *Stelle* und
die Gruppe seines Loslassens. Der Typ dafür ist `Gesperrtes` in
[gesperrtesModell.py](../../technik/arbiter/domaene/phasen/aufstellen/gesperrtesModell.py).
Die Formregel `formregeln/glossar.py` verlangt für jede Klasse der Domäne einen Eintrag im
Glossar; `Gesperrtes` hat keinen, `glossarTest` ist rot.

**Kosten.** Ohne Eintrag bleibt `python3 -m pytest prozess/pruefungen` rot. Ohne Klasse
wäre das Tupel zurück (397) oder ein Trick, der die Formregel umgeht.

**Gegenvorschlag.** Glossarzeile `Gesperrtes | – | Gesperrtes | Was Arbiter von einem
*gesperrten* *Modell* festhält: die *Stelle*, an die es kam, die *Gründe*, die vorige *Stelle*
und die Gruppe, mit der es losgelassen wurde (AUF-9.1, 9.3).` Erledigt, wenn die Zeile steht.

**Stellungnahme.** Angenommen, mit zwei Änderungen am Wortlaut: „die Gruppe“ heißt wie in
AUF-15.1 „die *Modelle* desselben Loslassens“, und die vorige *Stelle* gilt nur, wenn das
*Modell* *gesetzt* war (AUF-9.4); Fundstellen um AUF-9.4 und 15.1 ergänzt. Die Zeile steht in
[glossar.md](../../domaene/glossar.md) unter `Gesperrtes`, `glossarTest` ist grün.
