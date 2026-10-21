# Die Tests zu AUF-12.5 und 12.6 prüfen noch das gestrichene AUF-16.3

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf, ein Test prüft
sein Kriterium nicht. AUF-16.3 ist gestrichen
([2210](2210-loslassenNebenDerKarteWiderspruechlich.md)), und
[AUF-12.5](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md) nennt nur noch
AUF-7.2 und 8.4. Die Fixture `sperrendesLoslassen` in
[sperreOhneStelleTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/sperreOhneStelleTest.py)
(Zeile 116, Fall `auf16_3GesetztesModellAufDerAblageDesAnderen`) speist aber weiter alle drei
Tests zu AUF-12.5 und 12.6: Ein Boy der *Einheit in Aufstellung*, auf der *Ablage* des
anderen *Spielers* losgelassen, soll die *Sperre* ‚nicht wählbar‘ bringen. Dort verlangt jetzt
[AUF-28.1](../../domaene/anforderungen/phasen/aufstellen/loslassenWoDieKarteZeigt.md) das
*Setzen* an der *Stelle*, die die *Karte* zuletzt zeigte. Die Rückverfolgung meldet das nicht,
weil die Tests nach 12.5 und 12.6 heißen.

**Kosten.** Bleibt der Fall, sind die Tests zu AUF-12.5 und 12.6 rot, sobald AUF-28.1 gebaut
ist, oder der Implementierer baut die Sperre gegen AUF-28.1 nach.

**Gegenvorschlag.** Den Fall `auf16_3…` samt `einGesetztesModellAufDerAblageDesAnderen` aus
`sperrendesLoslassen` streichen, zusammen mit den Tests zu AUF-16.3 und 16.6 in
`loslassenOhneZielTest.py`. Das Loslassen auf der *Ablage* prüft dann der Test zu AUF-28.1.

**Stellungnahme.** Angenommen. Der Fall `auf16_3…` samt `einGesetztesModellAufDerAblageDesAnderen`
ist aus `sperrendesLoslassen` gestrichen. Die beiden Tests zu AUF-12.6 („nach dem Auswählen“,
„nicht mehr nach der nächsten Handlung“) lösten ihre *Sperre* ebenfalls mit einem *gesetzten*
*Modell* auf der *Ablage* des anderen aus; sie ziehen jetzt ein *Modell* der *aufgestellten*
*Einheit* auf die eigene *Ablage* (AUF-8.4). In `loslassenOhneZielTest.py` sind die Tests zu
AUF-16.3 und 16.6 entfernt; der Test zu *neben Karte und Ablagen* (der Sache nach das noch
nicht gebaute AUF-16.8) kommt nach dem Plan neu.
