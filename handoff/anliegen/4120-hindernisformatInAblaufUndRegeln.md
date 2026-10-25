# Ablauf und Regeln nennen das Hindernis noch im alten Format

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Seit Anliegen 3940 (Commit „Hindernis nennt, wer wen aufhält (Anliegen 3940)“)
schreibt `standregeln/hindernis.py` unter den Schritt die Zeile
`Hindernis: <Rolle> → <Beseitiger>: <Satz> (Anliegen <nr>)`, bei Annahme gefolgt von
`; beseitigt: Commit „<Betreff>“`. Im Dashboard wird „Anliegen <nr>“ zum Link. Zwei Stellen
stimmen damit nicht überein:
- [Fortschritt](../../prozess/ablauf/fortschritt.md), Zeilen 16 und 17, nennt noch
  `Hindernis: <Text> (Anliegen <nr>)`. Das ist meine Datei. Die Schreibgrenze sperrt die
  Änderung bis nach `Freigabe Retro 8`.
- [Standregeln](../../prozess/regeln/standregeln.md), Zeile 16, nennt ebenfalls
  `Hindernis: <Text> (Anliegen <nr>)`, Zeile 19 schon das neue Format. Die Aussage steht
  damit doppelt und widerspricht sich ([Wir 3](../../prozess/praemissen/wir.md)).

Nach [Ich 3](../../prozess/praemissen/ich.md) wartet das auf die Prozessphase: Das Skript
arbeitet richtig, keine Prüfung ist rot, nur der Text ist veraltet.

**Kosten.** Wer den Ablauf oder die Regeln liest, erwartet eine Zeile ohne Rolle und
Beseitiger und schreibt seinen Satz womöglich nicht so, dass der Stakeholder ihn ohne das
Anliegen versteht.

**Gegenvorschlag.**
1. Regelumsetzer: In [Standregeln](../../prozess/regeln/standregeln.md), Zeile 16, wird
   `Hindernis: <Text> (Anliegen <nr>)` ersetzt durch einen Verweis auf das Format in Zeile 19,
   damit es nur einmal steht.
2. Organisationsentwickler, nach `Freigabe Retro 8`: Zeilen 16 und 17 in
   [Fortschritt](../../prozess/ablauf/fortschritt.md) lauten dann:
   „Darunter eingerückt, was ihn aufhält, `Hindernis: <Rolle> → <Beseitiger>: <Satz> (Anliegen <nr>)`
   (Anliegen 3940; den Satz schreibt die Rolle für den Stakeholder, [Wir](../praemissen/wir.md),
   5; im Dashboard verlinkt „Anliegen <nr>“), angenommen gefolgt von
   `; beseitigt: Commit „<Betreff>“`, …“
3. Bezug zu [4040](4040-ablaufUndRegelnVerschlanken.md): Beide Stellen sind Fälle von
   „doppelt“ aus dessen Schritt 1 und kommen in die Retro 8 als Vorschlag mit diesem Befund.

**Stellungnahme.**
