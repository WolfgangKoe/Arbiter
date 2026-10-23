# Ein Unit-Test legt fest, was AUF-27.2 anders regelt

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: angenommen
Wartet auf: Technikphase

## Runde 1
**Befund.** Kritik am Code zu Anliegen 1710, Punkt 8. Der neue
Test `testEineSchonÜberdeckendeBaseHältDenWegAmAnfangAnAuchWennSieSichEntfernt`
([messenTest.py](../../technik/tests/einheit/domaene/messenTest.py)) legt fest: Überdeckt eine
*Base* schon am Anfang des Wegs eine andere, bleibt sie stehen (Anteil 0), auch wenn sie sich
entfernt und erst am Ende eine dritte überdecken würde.

- Der Fall liegt außerhalb des Vertrags: [V10](../../technik/architektur/handlungen.md) nennt
  ihn Vorbedingung bis AUF-27 („Am Anfang des Wegs *überdeckt* keine *Base* eine, gegen die
  angehalten wird“).
- [AUF-27.2](../../domaene/anforderungen/phasen/aufstellen/formationOhneFreieStelle.md)
  (Plan 7) regelt ihn umgekehrt: An einer schon überdeckten *Base* hält Arbiter nicht an. Im
  Beispiel des Tests hielte die *Base* vor der dritten an (Anteil um 3/4), nicht am Anfang.
- Innerhalb des Vertrags überdeckt beim Schritt 0 nichts, der erste überdeckende Schritt ist
  mindestens 1; `max(…, 0)` in `anteilBisZurBerührung` ändert dort nie ein Ergebnis. Der
  Mutant `max(…, 1)` ist gleichwertig unter der Vorbedingung, wie der Reviewer annahm. Der
  Test fängt ihn nur, indem er Verhalten außerhalb des Vertrags zusagt.

Vorbild im Bestand: `testEineAufgestellteEinheitAuswählenIstEineVorbedingungsverletzung`
prüft an einer Vorbedingung, dass sie greift (`ValueError`), nicht, was danach geschieht.

Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet. Keine Prüfung ist rot, der
Happy Path ist unberührt, A1, M1 und S3 sind eingehalten. Spätestens mit AUF-27.2 in der
nächsten Technikphase wird der Test rot.

**Kosten.** Bis dahin liest man im Test eine Zusage, die die Domäne schon anders entschieden
hat; wer AUF-27.2 baut, muss erst klären, ob der Test eine Regel schützt. In
Anliegen 1632 zählt der Mutant als gefangen, obwohl er
gleichwertig ist.

**Gegenvorschlag.** Mit AUF-27.2 den Test löschen; der Test zu AUF-27.2 tritt an seine Stelle
und fängt `max(…, 0)`, falls die Zeile dann noch gebraucht wird. Bis dahin führt 1632 den
Mutanten als gleichwertig unter der Vorbedingung von V10. Allgemein dazu:
Anliegen 1751.

**Stellungnahme.** Angenommen. Der Test bleibt, bis AUF-27.2 gebaut wird; AUF-27 hat
noch keinen Akzeptanztest, und ein jetzt gelöschter Test ließe den Mutanten `max(…, 1)` in
1632 ungefangen. Wer AUF-27.2 baut, löscht ihn dann zusammen mit dem Test zu AUF-27.2.
