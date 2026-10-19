# Die Zeile unter dem Grund ist kein zweiter Grund

921 · Kritik · von Architekt → Ux · Runde 1/3 · angenommen · wartet auf die Technikphase

## Runde 1
**Befund.** [auf-22](../../domaene/mockups/auf-22.html) zeigt „Spieler 2 ist an der Reihe“ als
zweites `<li class="sperrmeldungGrund">`. Nach [V7](../../technik/architektur/handlungen.md)
steht je *Grund* ein `sperrmeldungGrund`, und
[AUF-3.9](../../domaene/anforderungen/phasen/aufstellen/sperrenBeimSetzen.md) verlangt, dass
‚nicht an der Reihe‘ der einzige *Grund* ist. Ein Bildschirmtest findet Elemente über ihre
Klasse (B2, [Web](../../technik/architektur/web.md#bildschirmtests)): Er zählt zwei *Gründe*.
Übernimmt der Implementierer das Markup ohne Umschreiben (O3), zeigt die Seite einen Satz als
*Grund*, den die Domäne nie nennt.

Einordnung nach Ich 3: hält auf. Der Klick auf eine *Einheit* des anderen *Spielers* steht im
Plan auf dem Happy Path, und der Test zu AUF-22.1 oder AUF-3.9 könnte sein Kriterium nicht
prüfen.

**Kosten.** Eine Klasse mehr in `vorschlag.css`, ein `<li>` im Mockup geändert.

**Gegenvorschlag.** Entschieden (DoR 5): Die Zeile ist `<li class="sperrmeldungZusatz">`, in
derselben `sperrmeldung` direkt unter ihrem *Grund*. Ein Zusatz gehört zum *Grund* darüber
und ist selbst keiner; gezählt werden nur `sperrmeldungGrund`.
- Warum keine Klasse wie `sperrmeldungAnDerReihe`: Der Name sagt, was die Zeile ist, nicht
  was in ihr steht; die nächste Erläuterung zu einem *Grund* braucht keine neue Klasse.
- Warum kein `<span>` im `sperrmeldungGrund`: Dann trüge der *Grund* den Satz in seinem Text,
  und der Test fände ‚nicht an der Reihe‘ nicht mehr wörtlich.
- Für dich in `vorschlag.css`: Aussehen wählst du, Farben nur aus `:root`. Den Satz baut die
  Seite aus `anDerReihe` des Spielstands (AUF-4.2); das trage ich in der Technikphase in V7 ein.

Erledigt, wenn auf-22 die Zeile als `sperrmeldungZusatz` zeigt und die Regel in
`vorschlag.css` steht.

**Stellungnahme.** Einverstanden. [auf-22](../../domaene/mockups/auf-22.html) zeigt die Zeile als
`sperrmeldungZusatz`; die Regel steht in `vorschlag.css` (gedämpfte Farbe aus `:root`).
