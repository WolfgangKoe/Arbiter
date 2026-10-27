# Was geschieht beim Loslassen außerhalb der Bewegungsphase

Form: Fragen
Von: Testautor
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** QUE-10.5: „Gegeben eine *Phase* außer der *Bewegungsphase*, wenn jemand ein
*Modell* zieht und loslässt, dann steht jedes *Modell* danach, wo es vor dem Ziehen war.“
Das Kriterium nennt keine *Sperre* und keinen *Grund*. Offen ist, ob die Handlung
stillschweigend nichts ändert oder mit einer *Sperre* ohne *Grund* abbricht. Der Test
prüft vorerst, dass `modellLoslassen` ohne Ausnahme zurückkehrt und jede *Stelle* gleich
bleibt.

**Kosten.** Wirft der Implementierer eine *Sperre*, wird der Test rot, obwohl das Kriterium
nach seinem Wortlaut erfüllt wäre. Auch die Seite zeigt je nach Lesart eine Meldung oder nicht.

**Gegenvorschlag.** QUE-10.5 ergänzt: „… und Arbiter nennt keinen *Grund*“ (keine *Sperre*).
Alternative: ein eigener *Grund* (etwa ‚falsche Phase‘) mit Eintrag im Glossar.

**Fragen.** Empfehlung: keine *Sperre*, Handlung ohne Wirkung. Das Kriterium verlangt nur
den unveränderten Stand, und nach „Es steht nur da, was ich verlangt habe“ (Absicht 3)
kommt kein neuer *Grund* dazu.

**Stellungnahme.** Angenommen: keine *Sperre*, die Handlung bleibt ohne Wirkung.
[QUE-10.5](../../domaene/anforderungen/querschnitt/schlachtrunden.md) endet jetzt mit „und
Arbiter nennt keinen *Grund*“, wie AUF-16.7 und 16.8. Grund: Laut Anliegen 07 ist eine leere
*Phase* eine ohne Spielhandlung, und Arbiter versetzt außerhalb der *Bewegungsphase* nichts. Eine
*Sperre* könnte man *gemeinsam übergehen*, und das Modell würde doch versetzt; genau das schließt
Anliegen 07 aus. Ein neuer *Grund* entfällt (Absicht 3). Die Kennung bleibt, weil der bestehende
Test schon so prüft. Damit die Datei unter 1.200 Zeichen bleibt, trägt der Zweck die Quelle
Anliegen 07 nicht mehr doppelt (sie steht an QUE-10.5) und sagt „durch die *Phasen* der
*Schlacht*“ statt „bis zum Ende der *Schlacht*“; QUE-10.4 deckt das Ende ab.
