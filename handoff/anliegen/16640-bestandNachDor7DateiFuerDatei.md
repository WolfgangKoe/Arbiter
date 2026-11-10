# Bestand nach DoR 7 umschreiben, Datei für Datei

Form: Kritik
Von: Planer
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 11

## Runde 1
**Befund.** 86 von 176 Kriterien in 44 Dateien verstoßen gegen [DoR 7](../../prozess/ablauf/dor.md):
Ein Bezug auf ein anderes Kriterium steht statt eines Satzes (`python3
prozess/pruefungen/gemeinsam/lauf.py kriterienregeln.bezuege domaene/anforderungen`). Der
Stakeholder hat entschieden: Der Bestand wird als Erstes in der Domänenphase 11 umgeschrieben,
Etappe 2 zuerst ([16171](16171-kriterienOhneNachlesenVerstaendlich.md)). Elf dieser Dateien
ändern wartende Anliegen an dich ohnehin fachlich. Schreibst du sie vorher um, schreibst du
ihre Sätze zweimal: BEW-18.7 und BEW-25.1 schrieben dann aus, was BEW-8.4 heute tut, und
15461 fasst BEW-8.4 neu.

**Kosten.** Rund 86 Kriterien; kein Test und kein Produktcode ändern sich. Wartete alles auf
15461, lägen 57 Kriterien in 33 Dateien still, bis der Stakeholder dort fünf Fragen beantwortet
hat.

**Gegenvorschlag.** Je Datei schreibt nur einer zur Zeit:
1. Zuerst, neben den Strängen der [Moderation](../moderation.md): die 33 roten Dateien, die
   unten nicht stehen, Etappe 2 zuerst, je Ordner ein Lauf.
2. Die übrigen elf schreibst du im Lauf mit dem letzten wartenden Anliegen an ihnen ganz nach
   DoR 7 um:
   - `uebergehenBeimZiehen.md`, `weiterziehenNachDemUebergehen.md`, `anhaltenVorDerGrenze.md`,
     `sperreNichtAmZug.md`: nach 15461, 10201, 14320, 10120.
   - `fliegen.md`: erst 16150 (BEW-18.6), dann 14320 (BEW-18.3), dann umschreiben.
   - `sperreBeimLoslassen.md`: erst 16150 (Am Bildschirm), dann 10201 (BEW-21.1), dann
     umschreiben.
   - `formationOhneFreieStelle.md` mit 16150, `ebene.md` mit 15300.
   - `anhaltenAufDemWeg.md`, `anhaltenVorFremdenBases.md` mit 16080, ebenso
     `anhaltenAnDerBewegungsweite.md`, falls 16080 Punkt 3 BEW-3.1 ändert.
   Die Stränge (a) und (b) der Moderation laufen also in `fliegen.md` und
   `sperreBeimLoslassen.md` nicht nebeneinander.
3. `fliegen.md`, `uebergehenBeimZiehen.md` und `anhaltenVorFremdenBases.md` liegen schon über
   1.200 Zeichen ([Domäne](../../domaene/CLAUDE.md)), ausgeschrieben werden sie länger: Teile
   sie im selben Lauf, wie [13842](13842-akzeptanztestdateienUeberDemHoechstmass.md) vorschlägt;
   die Tests teilt der Testautor in der Technikphase 11.
4. `querschnitt/` nicht gleichzeitig mit 16241, das den Ordner verschiebt.

Beim Umschreiben bleiben Sinn und Kennungen (16171); ändert sich doch ein Sinn, fragst du den
Stakeholder. Erledigt, wenn das Skript 0 rote Kriterien meldet, die Akzeptanztests unverändert
grün sind und der Fachkritiker jede Datei einmal gelesen hat, nach ihrer letzten Änderung.

**Stellungnahme.**
