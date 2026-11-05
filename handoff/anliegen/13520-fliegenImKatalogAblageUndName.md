# Fliegen im Katalog: Ablage der Prüfung und Name der Tabelle

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Die Zeile `fliegen` (11840) folgt [Katalog](../../technik/architektur/katalog.md)
K3, K4 und K7 in der Sache: freiwillig beim *Datenblatt*, nur `bool`, `Einheit.fliegen` mit
Vorgabe `False`, die Domäne kennt den Katalog nicht; Importvertrag, Benennung, ruff, SonarLint
und die Tests zu `katalog/` und MIV-3 sind grün. Nichts hält auf; zwei Punkte zur Ablage
warten:
1. K7: `eintragLesen.py` hält die Prüfungen, „die mehr als ein Modul nutzt“.
   `wahrheitswertLesen` nutzt nur `datenblaetter.py`. Dazu prüft nur `datenblaetterTest.py`
   das neue Verhalten von `eintragLesen.py` (`freiwillig`, `wahrheitswertLesen`), nicht
   `eintragLesenTest.py` (K7, [Es 2](../../prozess/praemissen/es.md)).
2. Schnittstelle: `genauDieseSchlüsselLesen(..., freiwillig=...)` liest nicht mehr „genau
   diese“ Schlüssel, und die Meldung nennt bei `{"modellarten": …, "oc": 2}` nur
   `['modellarten']`, verschweigt also, dass `fliegen` erlaubt ist.

**Kosten.** Heute keine. Mit dem nächsten Wahrheitswert oder dem nächsten freiwilligen
Schlüssel sucht man die Prüfung im falschen Modul, und wer beim Start an der Meldung
scheitert, sucht den erlaubten Schlüssel im Code.

**Gegenvorschlag.**
1. `wahrheitswertLesen` nach `datenblaetter.py` (in `_fliegenLesen`), bis ein zweites Modul
   ihn liest; dann zurück mit einem Test in `eintragLesenTest.py`. Der Fall „Pflichtschlüssel
   fehlt, freiwilliger da“ als Parameter in `eintragLesenTest.py`.
2. Die Funktion nach dem, was sie prüft, etwa `schlüsselDerTabelleLesen`, die Meldung mit
   Pflicht- und freiwilligen Schlüsseln.

**Stellungnahme.**
