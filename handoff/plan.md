# Plan · Zyklus 6

Etappe: [1 · Aufstellen](../domaene/etappen/01-aufstellen.md). Grundlage: [Review 5](review.md)
und deine Kommentare: nur dein Happy Path wie in ArbiterMap.

## Dein Happy Path nach Zyklus 6
1. Arbiter startet mit verteilten Zonen, Spieler 2 ist *an der Reihe*. (gebaut)
2. Er klickt eine *Einheit* in seiner *Ablage* an: goldener Rahmen, nur sie ist
   *ausgewählt*. (Item 1)
3. Er klickt in seine Zone: Die *Einheit* steht dort als *Formation*, ragt sie hinaus,
   rückt Arbiter sie hinein; sie bleibt *ausgewählt*. (Item 1)
4. Er hält ein *Modell* gedrückt und zieht: Die *Einheit* wandert mit (Item 2) und hält
   schon beim Ziehen am Rand der Zone und vor fremden *Bases* an (Item 3).
5. Ein Klick auf ein *Modell* wählt nur dieses, er zieht es allein, ein weiterer Klick
   darauf wählt wieder die *Einheit* (Item 2); es hält ebenso an (Item 3).
6. „Aufstellen der Einheit beenden“: Der andere ist *an der Reihe*, wer fertig ist, wird
   übersprungen. (gebaut)

Keine Knöpfe in der *Ablage*, kein „in Aufstellung“. Ein *Grund* nur, wenn ein Klick, ein Zug
oder das Beenden gerade nicht geht (995).

## Items
1. [Setzen per Klick](../domaene/items/setzenPerKlick.md): Schritte 2, 3. Vorab der Test zur
   Zugschwelle ([622](anliegen/622-zugschwelleUngeprueft.md)).
2. [Einheit und Modell verschieben](../domaene/items/einheitVerschieben.md): Schritte 4, 5.
3. [Anhalten an Bases](../domaene/items/anhaltenAnBases.md): Risiko des Zyklus.

Testautor: Ein *gesperrtes* *Modell* (AUF-9.3, 12.1, 17.1, QUE-3.5) entsteht in den Tests ab
Item 1 per Ziehen auf ein *gesetztes* (AUF-8.2), ab Item 2 mit der *Ebene* *Modell*; mit
Item 3 gehen die Tests zu „zurück“ (17.1) auf AUF-10.3 über.
Reihenfolge 1, 2, 3: Jedes baut auf dem vorigen auf. Klemmt Item 3, siehst du 2 bis 5
trotzdem (996). Gleichzeitig: Verträge zu 1 und 2 in einem Lauf, der Architekt probiert das
Anhalten neben Item 1 aus.

## Randfälle, Plan 7
„gemeinsam übergehen“ (AUF-13, QUE-5), *zurücklegen* (AUF-23), AUF-22, *ruhige Karte*
(QUE-7), AUF-16.7, Klick auf ein *Modell* einer nicht *ausgewählten* *Einheit*, Klick, dessen
*Formation* fremde *Bases* überdecken würde (AUF-18.7, 27; dazu Etappe 1, 999); bis Item 3
ein Block, auf fremden *Bases* losgelassen. Danach ist Etappe 1 erreicht.

## Empfehlung
Gib die drei Items frei, wenn der Happy Path deinem Bild entspricht.

## Offene Anliegen
An dich, an den Anforderungsautor, Vorschläge von ihm: keine. Sonst: [Moderation](moderation.md).

## Fortschritt
- [ ] Architekt: Vertrag zu Item setzenPerKlick, bei beiden Hälften
- [ ] Testautor: Tests zu Item setzenPerKlick
- [ ] Fachkritiker: Kritik an den Tests zu Item setzenPerKlick
- [ ] Architekt: Kritik an den Tests zu Item setzenPerKlick
- [ ] Implementierer: Tests zu Item setzenPerKlick grün
- [ ] Architekt: Kritik am Code zu Item setzenPerKlick
- [ ] Reviewer: Kritik am Code zu Item setzenPerKlick
- [ ] Fachkritiker: Item setzenPerKlick abgenommen
- [ ] Planer: Item setzenPerKlick gelöscht
- [ ] Architekt: Vertrag zu Item einheitVerschieben, bei beiden Hälften
- [ ] Testautor: Tests zu Item einheitVerschieben
- [ ] Fachkritiker: Kritik an den Tests zu Item einheitVerschieben
- [ ] Architekt: Kritik an den Tests zu Item einheitVerschieben
- [ ] Implementierer: Tests zu Item einheitVerschieben grün
- [ ] Architekt: Kritik am Code zu Item einheitVerschieben
- [ ] Reviewer: Kritik am Code zu Item einheitVerschieben
- [ ] Fachkritiker: Item einheitVerschieben abgenommen
- [ ] Planer: Item einheitVerschieben gelöscht
- [ ] Architekt: Vertrag zu Item anhaltenAnBases, bei beiden Hälften
- [ ] Testautor: Tests zu Item anhaltenAnBases
- [ ] Fachkritiker: Kritik an den Tests zu Item anhaltenAnBases
- [ ] Architekt: Kritik an den Tests zu Item anhaltenAnBases
- [ ] Implementierer: Tests zu Item anhaltenAnBases grün
- [ ] Architekt: Kritik am Code zu Item anhaltenAnBases
- [ ] Reviewer: Kritik am Code zu Item anhaltenAnBases
- [ ] Fachkritiker: Item anhaltenAnBases abgenommen
- [ ] Planer: Item anhaltenAnBases gelöscht
- [ ] Reviewer: DoD über das Inkrement
- [ ] Reviewer: Review geschrieben
- [ ] Stakeholder: Freigabe Review 6

## Freigabe
Freigabe: ja.
Kommentar: Wenn ich mir die Mockups so anschauen, dann sehe ich da so viele Hinweise und Buttons als ich es aus Arbitermap kenne. Ich möchte in der Aufstellungsphase, dass die Spieler nach dem Rolloff abwechselnd ihre Einheiten komplett in ihrer Aufstellungszone aufstellen (indem sie in die Aufstellungszone klicken) und dort noch verschieben können bzw. einzelne Modelle verschieben können. Dann "Aufstellen beenden" und der andere Spieler ist dran. Das geht dann so weiter bis alle Einheiten auf dem Feld oder in Reserve stehen. ALles andere sind Randfälle. Ich kann den Plan so nicht freigeben, weil ich nicht glaube, dass hier meine Vorstellungen umgesetzt werden.
Stellungnahme: Neu geschnitten auf deinen Happy Path, Randfälle in Plan 7.
Kommentar: 1. Die zwei "Knöpfe" in der einheitenKarte möchte ich nicht!!! Die kommen weg! So wie es jetzt ist, sieht es an sich okay aus. Ich wähle die Einheit in der armeeListe, die bekommt dann den goldenen Rahmen, dass sie "ausgewählt" ist. Dann klicke ich auf die Aufstellungszone und sie erscheint dort. Wenn ich die Einheit verschieben will, halte ich auf einem Modell gedrückt und die ganze Einheit lässt sich ziehen. Möchte ich ein Modell der Einheit ziehen, muss ich nochmal auf das einzelne Modell klicken. Das Modell erscheint ausgewählt, die anderen der Einheit nicht. Dann kann ich dieses Modell mit der Maus halten (so wie es aktuell ist) und verschieben. Das ist alles schon in ArbiterMap umgesetzt. Warum wird hier neuer Kram erfunden?! - So keine Freigabe des Plans! 2. Der Ablaufplan soll in plan.md erscheinen. Warum erstellst du hierfür eine HTML? Das war nicht, was ich mit "Ausnahme" wollte. Warum verstehst du mich nicht? Oder warum kannst du dich in den Anliegen nicht verständlich ausdrücken?
Stellungnahme: 1. Die Knöpfe kommen weg, Schritte 4 und 5 sind deine Bedienung aus ArbiterMap. Ich hatte sie aus der Beschreibung statt aus dem Gebauten; das war falsch. Kriterien 980, Mockups 981. 2. Wer je Item was tut, zeigt jetzt der Abschnitt Fortschritt über der Freigabe; ihn schreibt das Skript ([982](anliegen/982-fortschrittDerTechnikphaseVorDerFreigabe.md)). Meine Prosa dazu ist weg, unter Items steht nur, was nur der Plan weiß ([983](anliegen/983-plan6FortschrittStattProsaUndParallel.md)). Die HTML-Datei ist gelöscht (981).
Kommentar: Und nochmals in der unitCard braucht es keinen Hinweis "in Aufstellung". Auch "Base überdeckt" oder "in Nahkampfreichweite" sind faktisch völlig unsinnige Randfälle. ArbiterMap hat Baseüberdeckung durch Klemmen blockiert. Tu endlich, was ich will!
Stellungnahme: Umgesetzt. Das Wort „in Aufstellung“ fällt mit Item 1 weg. ‚Base überdeckt‘ und ‚Nahkampfreichweite‘ sind aus dem Happy Path: Block und *Modell* klemmen beim Ziehen wie in ArbiterMap am Rand der Zone und vor fremden *Bases* (Schritte 4, 5, Item 3); einen *Grund* nennt der Happy Path. [Etappe 1](../domaene/etappen/01-aufstellen.md) sagt dasselbe. Kriterien: [984](anliegen/984-klemmenStattSperreUndOhneAbzeichen.md), Mockups: [988](anliegen/988-mockupsOhneInAufstellungUndOhneSperrbildFuerBaseUndNahkampf.md).
Kommentar: Auch Rolloff gewonnen ist hier nicht erforderlich. Wir gehen bis auf Weiteres davon aus, dass Spieler 2 diesen gewonnen hat, es also "an der Reihe" anzeigt. Außerdem scheinen viele Mockups identisch zu sein. Wozu sind diese dann gut?
Stellungnahme: „Gewinner und Zone“ entfällt, Schritt 1 ist der gebaute Start (deine Antwort A in Anliegen 990), ebenso in [Etappe 1](../domaene/etappen/01-aufstellen.md). Gleiche Mockups hat Ux gestrichen (988), jedes übrige zeigt einen anderen Schritt.
