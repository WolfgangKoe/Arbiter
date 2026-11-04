# Glossar: Weiterrücken

Form: Kritik
Von: Implementierer
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Vertrag ([Ziehen](../../technik/architektur/vertrag/aufstellen/ziehen.md)) nennt die
Klasse `Weiterrücken`; sie steht in
[anhaltenAufDemWeg.py](../../technik/arbiter/domaene/phasen/aufstellen/anhaltenAufDemWeg.py), aber nicht im
[Glossar](../../domaene/glossar.md).

**Kosten.** Ohne Zeile bleibt der Hook zum Glossar rot, der Code uncommittet.

**Gegenvorschlag.** Zeile `Weiterrücken | – | Weiterrücken | …`: die Eingaben, mit denen der Spieler
ein gezogenes *Modell* weiterzieht (die zuvor gezeigte *Stelle* und ob es schon angehalten hat,
AUF-29, BEW-17).

**Stellungnahme.** Angenommen: Zeile `Weiterrücken` im [Glossar](../../domaene/glossar.md), nach
dem Gegenvorschlag, mit AUF-29.1, BEW-17.1 und 17.4. Die Prüfung zum Glossar meldete aus derselben
Datei auch die Klasse `Geglitten`; dafür steht dort eine Zeile `Geglitten` (AUF-29.1, 29.2,
BEW-17.1). `formregeln.glossar` ist grün.
