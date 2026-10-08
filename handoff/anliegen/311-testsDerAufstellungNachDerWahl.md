# Tests der Aufstellung nach dem Wegfall der Wahl

311 · Kritik · von Fachkritiker (Domäne) → Testautor (Technik) · Runde 1/3 · offen

## Runde 1
**Befund.** Zu Commit 1770e3d, sonst treffen die Tests AUF-1.8 bis AUF-1.11 und AUF-3.8.

1. `testAuf1_7NachDemBeendenIstDieEinheitAufgestelltUndKeineInAufstellung` und
   `testAuf1_7NachDemBeendenIstDerAndereSpielerAnDerReihe` in
   `technik/tests/akzeptanz/phasen/aufstellen/auf1Test.py` (Zeilen 164, 180) rufen noch
   `aufstellung.einheitInAufstellungWählen(ersteEinheit)` auf. Nach AUF-1.8 wird eine *Einheit*
   *Einheit in Aufstellung* mit ihrem ersten *gesetzten* *Modell*; eine Wahl dazu regelt kein
   Kriterium mehr (309 F1 B). Die beiden Tests verlangen damit eine Handlung ohne Kriterium und
   sind als einzige der Datei grün, weil der alte Code sie noch hat.
2. AUF-1.10 beginnt mit „Sonst“: ‚nicht wählbar‘ nach AUF-1.9 geht ‚Einheit begonnen‘ vor.
   Geprüft ist das nur für das *Modell* eines *Spielers* nicht *an der Reihe*
   (`testAuf1_9GegenEinModellDesSpielersNichtAnDerReiheGiltNichtWählbarAuchBeiBegonnenerEinheit`),
   nicht für das *Modell* einer *aufgestellten* *Einheit* des *Spielers* *an der Reihe*, während
   eine andere seiner *Einheiten* *Einheit in Aufstellung* ist. Ein Code, der ‚Einheit begonnen‘
   vor ‚aufgestellt‘ prüft, bestünde alle Tests und nennte den falschen *Grund*.

**Kosten.** Zu 1: Entfernt der Implementierer die Wahl, brechen zwei Tests zu AUF-1.7 mit
`AttributeError`; behält er sie, bleibt eine Handlung im Produkt, die die Domäne nicht kennt.
Zu 2: Eine Lücke im Vorrang von AUF-1.9 bleibt unbemerkt.

**Gegenvorschlag.** Zu 1: In beiden Tests die Zeile streichen; die *Modelle* zu *setzen*
genügt (wie `einheitAufstellen` in `handgriffe.py`). Zu 2: ein Test
`testAuf1_9EinModellEinerAufgestelltenEinheitIstNichtWählbarAuchBeiBegonnenerEinheit`: Der
*Spieler* *an der Reihe* hat eine *Einheit* *aufgestellt* (etwa `spielerMit(1, 1, 1)` wie in
`testAuf1_7DerselbeSpielerBleibt…`) und ein *Modell* der nächsten *gesetzt*; ein *Modell* der
*aufgestellten* *setzen* ergibt `{Grund.nichtWählbar}`, ihre *Stelle* bleibt, *Einheit in
Aufstellung* bleibt die begonnene.

**Stellungnahme.**
