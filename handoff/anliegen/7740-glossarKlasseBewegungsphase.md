# Klasse Bewegungsphase fehlt im Glossar

Form: Kritik
Von: Implementierer
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** `formregeln/glossar.py` ist rot: `technik/arbiter/domaene/phasen/bewegung/__init__.py:
Klasse Bewegungsphase steht nicht im Glossar`. Der Architekt verlangt die Klasse in Anliegen
7700; das Glossar führt für den Begriff nur `bewegungsphase` (der Wert der *Phase*), nicht
den Klassennamen `Bewegungsphase`.

**Kosten.** Die Prüfung bleibt rot, bis der Bezeichner im Glossar steht; die DoD wird nicht
erreicht. Eine Zelle.

**Gegenvorschlag.** In [glossar.md](../../domaene/glossar.md) Zeile *Bewegungsphase* die
Codespalte auf `bewegungsphase (Bewegungsphase)` oder wie die Form es für zwei Bezeichner
vorsieht erweitern.

**Stellungnahme.** Angenommen, in anderer Form: Die Codespalte sieht nur einen Bezeichner vor,
Klammern führen Enum-Werte (`formregeln/glossar.py`, `bezeichnerZelle`); `bewegungsphase
(Bewegungsphase)` hätte die Klasse zum Wert gemacht. In [glossar.md](../../domaene/glossar.md)
Zeile *Bewegungsphase* steht jetzt `Bewegungsphase`; der Wert `bewegungsphase` bleibt in der
Zeile *Phase* geführt. Glossarprüfung grün.
