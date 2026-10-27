# Hindernis: Tests zu Item normalMove grün

Form: Kritik
Von: Implementierer
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** testAuf8_2EinModellBleibtBeiWenigerAlsDerZugschwelleAbweichungAnSeinerStelle (ziehenTest.py) fordert, dass eine Bewegung unter der Zugschwelle keine ändernde Anfrage sendet. Sie ist aber ein Klick auf ein gesetztes Modell einer nicht ausgewählten Einheit in der Aufstellung; AUF-20.6 und V14 verlangen dafür PUT …/anklicken (Einheit wird ausgewählt). Beides zugleich ist nicht erfüllbar. Empfehlung: der Test wählt zuvor die Einheit der Boyz aus (dann sendet der Klick nur ebene, auch eine ändernde Anfrage; besser: Test prüft nur, dass die Stellen unverändert bleiben und keine PUT …/stelle gesendet wird) oder nimmt anklicken ausdrücklich aus. Das hält den Schritt „Tests zu Item normalMove grün“ von Implementierer im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis.

**Stellungnahme.** Angenommen. „Keine ändernde Anfrage“ war zu weit: Der Zug ist zugleich ein Klick auf ein gesetztes Modell, und der ist nach AUF-20.6 und V14 eine Handlung (anklicken). Der Test wählt jetzt zuerst die Einheit der Boyz aus (wie in AUF-18.1) und prüft dann nur, was AUF-8.2 betrifft: Kein PUT …/stelle verlässt die Seite, die Stellen aller Modelle bleiben. Die Anfrage der Ebene (PUT …/ebene beim Klick auf ein Modell der ausgewählten Einheit) bleibt erlaubt. Umgesetzt in ziehenTest.py.
