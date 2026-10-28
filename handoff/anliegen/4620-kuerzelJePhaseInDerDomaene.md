# Kürzel je Phase in der Domäne

Form: Kritik
Von: Anforderungsautor
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Stakeholder hat entschieden: Jede Phase trägt ein eigenes Kürzel, die
Bewegungsphase BEW (Anliegen 4280, F6 A). [Domäne](../../domaene/CLAUDE.md), Zeile 9, nennt
für `phasen/<phase>` aber nur AUF; [BEW-1](../../domaene/anforderungen/phasen/bewegung/normaleBewegung.md)
und [BEW-2](../../domaene/anforderungen/phasen/bewegung/sperrenBeimZiehen.md) widersprechen
ihr damit. Die Datei liegt in deinen Schreibpfaden, nicht in meinen.

**Kosten.** Bleibt die Zeile, liest jede Rolle AUF als Kürzel aller Phasen, und ein Kritiker
kann BEW-1 und BEW-2 zu Unrecht beanstanden. Die Prüfungen erkennen BEW schon.

**Gegenvorschlag.** In Zeile 9 statt „`phasen/<phase>` (AUF)“:
„`phasen/<phase>` je Phase ein Kürzel, `aufstellen` (AUF), `bewegung` (BEW)“. Ein neues
Kürzel schlägt der Anforderungsautor weiter dem Stakeholder vor (Rolle Anforderungsautor).

**Stellungnahme.** Umgesetzt in P3 der [Retro 8](../retro.md):
[Domäne](../../domaene/CLAUDE.md) nennt „`phasen/<phase>` (je Phase ein Kürzel: AUF, BEW)“;
kürzer als dein Vorschlag, sonst überschritte die Datei 1.500 Zeichen. Die Ordnernamen
`aufstellen` und `bewegung` stehen im Baum.
