# Das Löschen erledigter Anliegen schreibt „Anliegen Anliegen <nr>“

Form: Kritik
Von: Regelumsetzer
An: Regelumsetzer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** `anliegenregeln/erledigteLoeschen.py` (`linksErsetzen`, Zeile 34) ersetzt jeden
Link auf ein gelöschtes Anliegen durch „Anliegen <nr>“, auch wenn vor dem Link schon
„Anliegen“ steht. Aus „Anliegen [6640](…)“ in [Retro](../retro.md) wurde im Commit 712a634
„Anliegen Anliegen 6640“. Der Text in der Retro ist inzwischen korrigiert (der
Organisationsentwickler); der Fehler im Code besteht.

**Kosten.** Jedes Löschen erledigter Anliegen kann so einen Satz in Retro, Plan oder Ablauf
verderben, den der Stakeholder liest ([Wir 5](../../prozess/praemissen/wir.md)).

**Gegenvorschlag.** Bestehende Regel: [Anliegen](../../prozess/ablauf/anliegen.md), Mechanismus
`erledigteLoeschen.py`. Das Muster `link` um ein optionales vorangehendes „Anliegen “ erweitern
und es mitersetzen, oder bei vorangehendem „Anliegen “ nur „<nr>“ einsetzen. Scheiter-Test in
`erledigteLoeschenTest.py`: ein Link mit vorangestelltem „Anliegen “ ergibt „Anliegen <nr>“. Ein
eigenes Prozess-Item ist nicht nötig; nächster Lauf des Regelumsetzers.

**Stellungnahme.** Behoben: Das Muster `link` in `erledigteLoeschen.py` nimmt ein
vorangehendes „Anliegen “ (auch über einen Zeilenumbruch) mit, das Ergebnis ist „Anliegen <nr>“.
Scheiter-Test: `erledigteLoeschenTest.py`
(`testEinLinkMitVorangestelltemAnliegenGibtKeinDoppeltesAnliegen`).
