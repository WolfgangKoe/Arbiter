# Die Standregeln nennen das Hindernis noch im alten Format

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
`; beseitigt: Commit „<Betreff>“`. Im Dashboard wird „Anliegen <nr>“ zum Link.
[Fortschritt](../../prozess/ablauf/fortschritt.md) nennt dieses Format seit P5 der
[Retro 8](../retro.md). In den [Standregeln](../../prozess/regeln/standregeln.md) nennt die
Zeile zu `standregeln/hindernis.py` (Retro 7, P5; Anliegen 2460) noch
`Hindernis: <Text> (Anliegen <nr>)`, die Zeile zu Anliegen 3940 das neue Format. Die Aussage
steht damit dreimal und widerspricht sich ([Wir 3](../../prozess/praemissen/wir.md)).

Nach [Ich 3](../../prozess/praemissen/ich.md) wartet das auf die Prozessphase: Das Skript
arbeitet richtig, keine Prüfung ist rot, nur der Text ist veraltet.

**Kosten.** Wer die Regeln liest, erwartet eine Zeile ohne Rolle und Beseitiger und schreibt
seinen Satz womöglich nicht so, dass der Stakeholder ihn ohne das Anliegen versteht.

**Gegenvorschlag.** Regelumsetzer, mit P6 der Retro 8: Die beiden Zeilen der
[Standregeln](../../prozess/regeln/standregeln.md) nennen das Format nicht mehr selbst, sondern
verlinken [Fortschritt](../../prozess/ablauf/fortschritt.md), wo es einmal steht. Damit ist
auch Punkt 4 aus Anliegen 4040 erledigt.

**Stellungnahme.**
