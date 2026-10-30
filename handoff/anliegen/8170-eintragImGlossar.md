# Eintrag des Protokolls fehlt im Glossar

Form: Kritik
Von: Implementierer
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** QUE-5.1 sagt „einen Eintrag mehr“ im *Protokoll*, das [Glossar](../../domaene/glossar.md)
führt aber nur *Protokoll*, keinen *Eintrag*. Der [Vertrag V18](../../technik/architektur/vertrag/schlacht/uebergehen.md)
nennt `Eintrag(einheit, spieler, gründe)`; die Klasse steht in
[uebergehen.py](../../technik/arbiter/domaene/querschnitt/uebergehen.py), und der Glossar-Test
(`formregeln/glossar.py`) meldet „Klasse Eintrag steht nicht im Glossar“. Alle Tests von
[uebergehenTest.py](../../technik/tests/akzeptanz/querschnitt/uebergehenTest.py) sind grün; nur
DoD 2 ist rot.

**Kosten.** Ohne Begriff bleibt der Glossar-Test rot und die DoD des Items offen.

**Gegenvorschlag.** Eine Zeile `Eintrag | – | Eintrag | Zeile des *Protokolls*: die *Einheit*, der
die *Sperre* galt, ihr *Spieler* und jeder übergangene *Grund* (QUE-5.1).` Erledigt, wenn der
Glossar-Test grün ist.

**Stellungnahme.** Angenommen. Das [Glossar](../../domaene/glossar.md) führt jetzt *Eintrag*
nach dem Gegenvorschlag, mit „je *gemeinsam übergehen*“ und der Quelle Anliegen 362 F4 A. In
[QUE-5](../../domaene/anforderungen/querschnitt/uebergehen.md) stehen *Eintrag* und *Einträge*
in 5.1, 5.2 und 5.4 nun kursiv; der Wortlaut bleibt gleich. `formregeln.glossar` ist grün.
