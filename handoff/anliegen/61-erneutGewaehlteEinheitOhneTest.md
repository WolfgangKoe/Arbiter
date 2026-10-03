# AUF-1.6: Test für die erneut gewählte Einheit in Aufstellung

61 · Kritik · von Fachkritiker (Domäne) → Testautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** [AUF-1.6](../../domaene/anforderungen/phasen/aufstellen.md) lautet jetzt „Eine
wählbare *Einheit* wird *Einheit in Aufstellung*, außer eine andere ist es und von ihr ist ein
*Modell* *gesetzt*: *Sperre* ‚Einheit begonnen‘.“ Damit regelt das Kriterium auch den Fall,
dass die *Spieler* die *Einheit in Aufstellung* erneut wählen, nachdem ein *Modell* von ihr
*gesetzt* ist: keine *Sperre*, sie bleibt *Einheit in Aufstellung*. In
[aufstellenTest.py](../../technik/tests/akzeptanz/phasen/aufstellenTest.py) prüfen die beiden
Tests zu AUF-1.6 nur eine andere *Einheit*; für diesen Fall gibt es keinen Test
(Stellungnahme in Anliegen 41, Commit aede801).

**Kosten.** Der Code sperrt den Fall heute:
`technik/arbiter/domaene/phasen/aufstellen.py:73` wirft `Grund.einheitBegonnen`, sobald die
bisherige *Einheit in Aufstellung* begonnen ist, gleich welche *Einheit* gewählt wird. Die
Akzeptanztests sind trotzdem grün, die Abnahme kann den Widerspruch zum Kriterium an nichts
festmachen. Mit Touch ist erneutes Antippen alltäglich; die *Spieler* sähen eine *Sperre*,
die die Regel (`core_rules.txt:2322`) nicht kennt.

**Gegenvorschlag.** Ein Test zu AUF-1.6, etwa
`testAuf1_6DieBegonneneEinheitErneutWählenSperrtNicht`: nach der Wahl, `begonneneEinheit`
wählen, ein *Modell* *setzen*, dieselbe *Einheit* erneut wählen; erwartet keine *Sperre*,
`einheitInAufstellung is begonneneEinheit` und das *Modell* weiter *gesetzt*. Er ist rot,
bis der Implementierer `aufstellen.py:73` anpasst.

**Stellungnahme.** Angenommen. `testAuf1_6DieBegonneneEinheitErneutWählenSperrtNicht` steht; er ist rot, bis der Implementierer `aufstellen.py` anpasst.
