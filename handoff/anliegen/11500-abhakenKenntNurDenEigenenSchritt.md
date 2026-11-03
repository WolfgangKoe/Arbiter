# Abhaken kennt nur das Hindernis des eigenen Schritts

Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Wartet nach [Kritik](../../prozess/ablauf/kritik.md): keine Prüfung rot, der
Happy Path geht weiter. [Standregeln, Zeile Retro 9 P1](../../prozess/regeln/standregeln.md)
zählt einen grünen Test nur, wenn ein beseitigtes Hindernis *desselben Schritts* ihn nennt
(`abhakenTest.py`: „Hindernis des anderen Kritikers zählt nicht“). Beim Abhaken von „Kritik an
den Tests zu Item loslassenNebenDerKarte“ entstand so
[11441](11441-hindernisKritikAnDenTestsZuItemLoslassen.md) für sechs Tests zu AUF-16.8, deren
Stelle der Testautor in Anliegen 11262 schon genannt
hat und der Fachkritiker abgenommen hat. Die Tests eines Items haben zwei Kritiker; jeder grüne
Test kostet so zwei Anliegen und zwei Antworten des Testautors mit derselben Stelle.

**Kosten.** Je Item mit vorher grünen Tests ein zweites Hindernis-Anliegen, ein weiterer Lauf
des Testautors und eine Nachprüfung mehr, ohne neuen Befund. Bleibt es, wächst das mit jedem
Item, dessen Kriterien früherer Code schon erfüllt.

**Gegenvorschlag.** Dieselbe Regel (Retro 9 P1) angepasst ([Ich 4](../../prozess/praemissen/ich.md)):
Es zählt ein beseitigtes Hindernis jeder Zeile „Kritik an den Tests zu Item <dasselbe>“, gleich
welches Kritikers; die genannte Stelle prüft jeder Kritiker in seiner eigenen Nachprüfung, er
liest dazu die Stellungnahme im Anliegen des anderen. Der Test „Hindernis des anderen Kritikers
zählt nicht“ kehrt sich um. Rückweg: die Bedingung wieder auf den eigenen Schritt. Ohne Probe in
`/tmp`; die Probe gehört zur Umsetzung durch den Regelumsetzer.

**Stellungnahme.**
