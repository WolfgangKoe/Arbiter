# Prüfung „schon grün“ nimmt die Kriterien aus der Zeile Abhängigkeit mit

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: erledigt
Wartet auf: Prozessphase

## Runde 1
**Befund.** Wartet auf die Prozessphase: Das Abhaken von „Kritik an den Tests zu Item fliegen“
meldete 15 Tests zu BEW-17.1 als „grün, bevor der Code besteht“ und legte dafür das Hindernis
Anliegen 13101 an. BEW-17.1 gehört nicht zum Item:
[fliegen.md](../../domaene/items/fliegen.md) nennt es nur in der Zeile „Abhängigkeit“, der
Umfang ist BEW-18 und MIV-3. `testkennungenDesItems` in
`prozess/pruefungen/standregeln/testsRot.py` gibt den ganzen Text des Items an `umfasst`
(`kriterienregeln/rueckverfolgung.py`), also auch diese Zeile. Grün sind diese Tests zu Recht:
Der Code des Items anhaltenAufDemWeg erfüllt sie schon. Jedes Item, das eine Abhängigkeit mit
Kennung nennt, löst so ein falsches Hindernis aus, und der Testautor muss es von Hand
beantworten.

**Kosten.** Regelumsetzer: `testsRot.py` liest nur die Zeile „Umfang:“, dazu ein Fall in
`abhakenTest.py`. Ob `rueckverfolgung.py` an seinen anderen Stellen dasselbe braucht, prüft er
mit.

**Gegenvorschlag.** `testkennungenDesItems` gibt `umfasst` nur die Zeile „Umfang:“ des Items.
Warum: Der Umfang nennt die Kriterien, die das Item umsetzt; eine Abhängigkeit ist schon
umgesetzt, ihre Tests sind darum grün.

**Stellungnahme.** Umgesetzt als P3 der [Retro 10](../retro.md): `umfangDes` in
`testsRot.py` gibt nur den Absatz „Umfang:“ weiter, auch an die Zuordnung der Anforderungen;
[Regel](../../prozess/regeln/standregeln.md), Fall in `abhakenTest.py`. Ob
`rueckverfolgung.py` an anderen Stellen dasselbe braucht, ist hier nicht geprüft: Dort
zählen den Umfang die Items des Plans, nicht Abhaken.
