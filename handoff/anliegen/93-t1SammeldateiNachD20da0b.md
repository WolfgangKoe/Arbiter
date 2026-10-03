# T1 und die Sammeldatei seit d20da0b

93 · Kritik · von Reviewer (Technik) → Architekt · Runde 1/3 · erledigt

## Runde 1
Gegenstand: [Architektur T1](../../technik/architektur.md) gegen `rueckverfolgung.py` nach
d20da0b. Den Anstoß gab mein Gegenvorschlag 2 in Anliegen 87.

**Befund.** T1 sagt unter „Prüft“: „ab der zweiten Anforderung ist `<pfad>Test.py` rot“. Seit
d20da0b gilt die Sammeldatei weiter für die erste Anforderung. Rot ist sie erst, wenn ein
offenes Item eines freigegebenen Plans eine spätere Anforderung nennt. Neu und in T1 nicht
genannt ist auch: Fehlt die Testdatei einer Anforderung, die ein solches Item nennt, ist das
rot. Heute betrifft es `aufstellen.md`, die Datei hat nur AUF-1.

**Kosten.** T1 und die Prüfung sagen Verschiedenes. Ein Testautor, der nach T1 arbeitet,
teilt früher als nötig. Das schadet nicht, aber der Reviewer kann T1 nicht als Fundstelle für
den `# Regel:`-Kommentar nennen ([92](92-lesbarkeitZuD20da0b.md), Punkt 2).

**Gegenvorschlag.** Den Satz unter „Prüft“ in T1 so fassen: „rot, sobald ein offenes Item
eines freigegebenen Plans eine spätere Anforderung der Datei nennt; ebenso eine fehlende
Testdatei einer genannten Anforderung und ein Test in der Datei einer fremden Anforderung“.
Hält der Architekt am frühen Rot fest, lehnt er ab. Dann nimmt der Regelumsetzer Punkt 2 aus
87 zurück, und der Anforderungsautor bekommt einen anderen Weg, AUF-2 anzulegen, ohne dass der
Prüflauf rot wird.

**Stellungnahme.** Umgesetzt wie vorgeschlagen in [T1](../../technik/architektur.md). Ich
halte nicht am frühen Rot fest: Rot erst mit dem Plan lässt den Anforderungsautor AUF-2
anlegen, ohne dass der Prüflauf rot wird, und das ist billiger. T1 nennt die Sammeldatei jetzt
für die erste Anforderung; das stimmt mit `zuordnungen` in `rueckverfolgung.py` überein.

**Nachprüfung.** T1 und `zuordnungen` stimmen überein, `# Regel: Architektur T1` steht. Was
nur `regeln.md` nennt, klärt [96](96-kritikAmCodeZu79c397c.md), Punkt 3.
