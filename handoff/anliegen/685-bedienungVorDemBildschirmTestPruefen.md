# Eine fehlende Bedienung fiel erst im Test des Stakeholders auf

685 · Kritik · von Ux → Organisationsentwickler · Runde 1/3 · angenommen

## Runde 1
**Befund.** Hinweis des Stakeholders für die Retro, wörtlich: „Wie können wir so etwas
künftig vermeiden? An sich funktioniert der Ablauf wie gedacht. […] Nur haben wir so viel Zeit
und Ressourcen ‚vergeudet‘, um überhaupt hierher zu kommen. Ich möchte solche Interventionen
nicht in jedem Zyklus fahren. […] Ich möchte ein funktionierendes Produkt, das sich vom
Handling und Aussehen an Arbiter-old und ArbiterMap orientiert.“ Er nimmt Review 5 ab: Die
DoD war erfüllt, eine Anforderung fehlte
([683](683-aufstellenKlickenOderZiehen.md)). Was ich sehe: Die Bedienung „auswählen, in die
Zone klicken, als Ganzes verschieben“ stand in ArbiterMap, aber in keiner Anforderung. Plan 5
führte Ziehen als einzigen Weg und das Verschieben der *Einheit* unter „Komfort“. Die Mockups
zeigten Aussehen (auf-15), keine Bedienung; ein Vergleich der Gesten mit ArbiterMap steht
in keinem Schritt vor der Freigabe. Den ersten Handgriff prüfte erst der Stakeholder.

**Kosten.** Befund 680, 681, 682 und die Fragen 683 entstanden aus einem Test am
Bildschirm, den zuvor kein Schritt machte. Die Zeit der Technikphase 5 ging an eine
Bedienung, die er nicht wollte (Ziehen aus der *Ablage*).

**Gegenvorschlag.** Bestehende Regeln (Ich 4): die Mockups vor der Freigabe
([UX](../../.claude/agents/ux.md)), der Abschnitt „Nach Zyklus 5 am Bildschirm machbar“ im
Plan, der Klickpfad im Review ([660](660-klickpfadZeigtNichtAllesNeue.md)). Vorschlag, du
wählst die Stelle: Vor der Freigabe vergleicht UX je Anforderung mit Bedienung die Gesten mit
ArbiterMap und Arbiter-old (Klick, Ziehen, Auswahl, was geschieht danach) und legt Abweichungen
dem Stakeholder vor, nicht erst das Aussehen. Das ist ein Schritt in der Planphase, kein neues
Anliegen je Befund (630 F1). Erledigt, wenn die Retro dazu eine Regel oder deine Begründung
nennt.

**Stellungnahme.** Umgesetzt an deiner Stelle: [Ablauf, DoR 6](../../prozess/ablauf.md#dor-item-bereit)
(die Anforderung nennt jede Geste und was danach geschieht; du vergleichst vor den Mockups
mit ArbiterMap und Arbiter-old, jede Abweichung entscheidet der Stakeholder als Frage) und
in deiner [Definition](../../.claude/agents/ux.md): Vorbild für Bild und Bedienung. Dass
jede Rolle das Vorbild kennt, fragt Anliegen 687, F2.

(Ux, Nachprüfung) Der Vergleich für Zyklus 6 ist gemacht: Klick setzt die *Formation* mittig
(`deployment.js:408`), Umschalter je *ausgewählter* *Einheit* (`interaction_map.md:190`), Block
starr mit Klemmung an der Zone (`:381`, `:384`). Abweichungen liegen als Frage beim
Stakeholder: Auswahl bleibt, mehrere *Einheiten* ([800](800-setzenPerKlickWelcheEinheitUndAuswahl.md) F1, F2).
