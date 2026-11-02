# Einhüllende eines Grenzkreises

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wartet (Lücke abseits des Happy Path, keine Prüfung rot). Der Code nennt jeden
Eintrag, den die *Karte* zeigt, `Einhüllende`, wie
[V21](../../technik/architektur/vertrag/bewegung/grenzkreise.md) „je *Grenzkreis* oder
*Einhüllende* ein Eintrag“ (Anliegen 8600 Punkt 2). Das [Glossar](../../domaene/glossar.md)
definiert die *Einhüllende* aber als Rand der Fläche, die „mehrere *Grenzkreise*“ bedecken.
Bei BEW-11.1 (ein *Modell* als *Ebene*) und bei einem Gegner mit einem *gesetzten*
*Modell* (11.3) liefert der Code eine `Einhüllende` mit einem *Grenzkreis*; nach dem
Glossar ist das keine.

**Kosten.** Am Bildschirm nichts. Bleibt es, sagen Glossar und Code bei einem *Modell*
Verschiedenes; der Reviewer prüft Glossar gegen Code im Urteil (Wir 2). Änderung: ein
Halbsatz im Glossar.

**Gegenvorschlag.** Definition der *Einhüllenden*: „Rand der Fläche, die ein oder mehrere
*Grenzkreise* zusammen bedecken; bei einem ist sie dieser *Grenzkreis*“. Geometrisch stimmt
das, und die Anforderungen können bei „*Grenzkreis* oder *Einhüllende*“ bleiben.

**Stellungnahme.** Umgesetzt im [Glossar](../../domaene/glossar.md): „Rand der Fläche, die ein
oder mehrere *Grenzkreise* zusammen bedecken …; bei einem ist sie dieser.“
