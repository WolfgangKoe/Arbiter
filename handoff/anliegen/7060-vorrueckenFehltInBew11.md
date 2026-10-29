# „Vorrücken“ fehlt im Mockup bew-11

Form: Kritik
Von: Fachkritiker
An: Ux
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf (Kritik, eine Handlung fehlt, die ein Kriterium verlangt).
[bew-11](../../domaene/mockups/bew-11.html) zeigt die *ausgewählten* Boyz, deren *Ebene* ein
Boy ist, in der *Bewegungsphase*. Sie sind weder *vorgerückt*, noch warten sie auf ihren
*Vorrückwurf*. Unter der *Karte* steht aber nur „Phase beenden“. Nach
[BEW-5.1](../../domaene/anforderungen/phasen/bewegung/vorruecken.md) bietet Arbiter in diesem
Zustand „Vorrücken“ an, egal welche *Ebene* gilt; [bew-5](../../domaene/mockups/bew-5.html)
zeigt den Knopf auch, dort mit der ganzen *Einheit* als *Ebene*. Der Implementierer übernimmt
das Markup ohne Umschreiben (Technikphase, Schritt 3). Folgt er bew-11, fehlt „Vorrücken“,
sobald nach Schritt 4 des Happy Path ein Boy die *Ebene* ist, und der Test zu BEW-5.1
widerspricht dem Mockup.

**Kosten.** Eine Zeile `<button class="knopf" type="button">Vorrücken</button>` vor „Phase
beenden“, wie in bew-5. Ohne die Zeile entscheidet der Implementierer zwischen Mockup und
Kriterium.

**Gegenvorschlag.** In bew-11 „Vorrücken“ wie in bew-5 in die `knopfGruppe` aufnehmen.

**Stellungnahme.** Übernommen: [bew-11](../../domaene/mockups/bew-11.html) bietet „Vorrücken“ vor „Phase beenden“ in der `knopfGruppe` an, wie bew-5; BEW-5.1 gilt damit auch mit einem Boy als *Ebene*.
