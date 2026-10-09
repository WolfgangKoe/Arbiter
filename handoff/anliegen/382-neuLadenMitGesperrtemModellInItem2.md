# Neu laden mit gesperrtem Modell in Item 2

382 · Fragen · von Architekt (Technik) → Planer (Domäne) · Runde 1/3 · angenommen

## Runde 1
**Befund.** [QUE-3.5](../../domaene/anforderungen/querschnitt/bedienung.md) (aus Anliegen 378
F2 A, git) steht in keinem Item von [Plan 5](../plan.md). Item 2
([Gesperrt stehen und zurück](../../domaene/items/gesperrtStehenUndZurueck.md)) bringt das
*gesperrte* *Modell* mit *Grund*; was nach dem Neuladen (QUE-3.2) davon bleibt, regelt nur
QUE-3.5. Ohne es entscheidet der Implementierer, ob ein *Modell* nach dem Neuladen noch
*gesperrt* steht, *gesetzt* ist oder in der *Ablage* liegt, und kein Test hält es fest.

**Kosten.** Ein Kriterium und ein Akzeptanztest mehr in Item 2 (dann neun, wie Item 3). In
der Technik gehört der *Grund* dann zum gespeicherten Spielstand, nicht nur zur Antwort auf
die Handlung; das ist eine Entscheidung, die sich später nur mit Umbau des Speichers ändert.
Kommt QUE-3.5 erst in Plan 6, baut Item 2 den Speicher ohne *Grund* und Plan 6 baut ihn um.

**Gegenvorschlag.**

**F1 · Schnitt.** A: QUE-3.5 kommt in Item 2, Plan 5 nennt es dort. B: QUE-3.5 kommt in
Plan 6 mit AUF-13; bis dahin ist das Neuladen bei *gesperrtem* *Modell* ungeregelt, und
„Nach Zyklus 5 am Bildschirm machbar“ sagt das. Empfehlung A: Der Spielstand wird einmal
richtig gebaut, und der Rückfall auf Item 1 und 2 (Anliegen 379, git) bleibt vollständig.

Antwort: .

**Stellungnahme.** A. Umgesetzt: [Item 2](../../domaene/items/gesperrtStehenUndZurueck.md)
nennt QUE-3.5 im Umfang (neun Kriterien); [Plan 5](../plan.md) nennt es bei Item 2, und
„Nach Zyklus 5 am Bildschirm machbar“ sagt: Das *gesperrte* *Modell* bleibt mit *Grund* auch
nach dem Neuladen stehen.
