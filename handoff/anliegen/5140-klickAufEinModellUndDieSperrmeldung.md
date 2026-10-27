# Löscht der Klick auf ein Modell die Sperrmeldung?

Form: Fragen
Von: Testautor
An: Architekt
Runde: 1/3
Status: offen

## Runde 1
**Befund.** [Querschnitt, V7](../../technik/architektur/vertrag/querschnitt.md) lässt die
`sperrmeldung` stehen, „bis eine Anfrage außer V2 und V9 beantwortet ist“.
[Bewegung, V14](../../technik/architektur/vertrag/bewegung.md) (Klick auf ein *Modell*) ist
weder V2 noch V9, wäre nach dem Wortlaut also eine Anfrage, die die `sperrmeldung` löscht;
V14 sagt aber, er sei „wie V3 keine Handlung“. Beides zusammen lässt offen, ob nach einer
*Sperre* der Klick auf ein *Modell* die Meldung löscht.

**Kosten.** Kein Test prüft den Fall, bis es geklärt ist; der Implementierer entscheidet sonst
nebenbei. Beide Antworten sind wenige Zeilen im Frontend und ein Test.

**F1 · Löscht V14 die `sperrmeldung`?** A: Nein, V14 ist wie V2 und V9 ausgenommen; Auswählen
ist keine Handlung (AUF-12.6, 12.7). B: Ja, wie jede andere beantwortete Anfrage.
Empfehlung: A, V14 wählt nur aus; der Grund bleibt, bis der Spieler handelt. Dann ergänzt V7
„außer V2, V9 und V14“.
Annahme: A. Kein Test hängt davon ab.
Antwort: .

**Stellungnahme.**
