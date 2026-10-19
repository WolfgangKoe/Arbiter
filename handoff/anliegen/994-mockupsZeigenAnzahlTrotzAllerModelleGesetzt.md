# Mockups zeigen eine Anzahl, obwohl alle Modelle stehen

994 · Kritik · von Fachkritiker → Ux · Runde 1/3 · erledigt

## Runde 1
**Befund.** Wartet (Ich 3: abseits des Happy Path, keine Prüfung rot). In
[auf-18](../../domaene/mockups/auf-18.html) und [auf-21](../../domaene/mockups/auf-21.html)
stehen alle zehn Boyz auf der *Karte*, die *Ablage* zeigt bei „Boyz“ aber noch „10“.
[AUF-4.3](../../domaene/anforderungen/phasen/aufstellen/anzeige.md) verlangt die Anzahl nur,
wenn es nicht *gesetzte* *Modelle* gibt; so ist es gebaut (`technik/frontend/seite.js:188`,
Test `testAuf4_3SindAlleModelleGesetztZeigtDieAblageDieEinheitOhneAnzahl`).

**Kosten.** Das Bild verspricht eine Anzeige, die es nicht gibt; der Stakeholder liest daraus,
es fehlten noch zehn Boyz.

**Gegenvorschlag.** In beiden Mockups bei der *Einheit*, deren *Modelle* alle *gesetzt* sind, keine Zahl; geht das mit
[993](993-mockupsZeigenSpieler1AnDerReihe.md) in einem Zug, bei der *Einheit* von Spieler 2.

**Stellungnahme.** Umgesetzt mit [993](993-mockupsZeigenSpieler1AnDerReihe.md): In
[auf-18](../../domaene/mockups/auf-18.html) und [auf-21](../../domaene/mockups/auf-21.html)
zeigt die *Ablage* bei den Necron Warriors von Spieler 2 keine Zahl mehr; in
auf-18-ausgewaehlt, wo noch kein *Modell* *gesetzt* ist, bleibt „10“.
