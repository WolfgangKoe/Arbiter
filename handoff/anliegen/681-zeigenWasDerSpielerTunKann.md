# Die Seite zeigt nicht, wer dran ist, dass man zieht und warum etwas nicht geht

681 · Kritik · von Fachkritiker → Ux · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder hat Arbiter gestartet und kam nicht zum ersten *Setzen*
(Bildschirmfoto, Fenster rund 990 px breit; Fehler beim Ziehen:
[680](680-markierterTextSperrtDasZiehen.md)). Unabhängig davon sagt ihm die Seite drei Dinge
nicht, die er zum Anfangen braucht:
1. **Wer an der Reihe ist.** AUF-4.4 ist erfüllt: rechts oben „Spieler 2“, darunter in kleiner
   Schrift „an der Reihe“ mit gelbem Strich. Er hat es nicht als Aufforderung gelesen und
   zuerst „Warboss“ von Spieler 1 angefasst. Beide *Ablagen* sehen gleich aus; nichts auf
   Höhe der *Einheiten* zeigt, welche jetzt dran sind.
2. **Dass man zieht, nicht klickt.** Ein Klick auf eine *Einheit* macht sie *ausgewählt*
   (AUF-5.3, gleich wer *an der Reihe* ist): Nur ein blauer Rahmen erscheint, sonst nichts.
   Für ihn sah das aus wie „gewählt, jetzt geht es weiter“; dass er die Karte auf die
   *Karte* ziehen muss, steht nirgends, auch kein Zeiger, der Greifen anzeigt.
3. **Warum eine fremde Einheit nicht geht.** Klick auf „Warboss“: Rahmen, keine Meldung. Ziehen
   von „Boyz“: *Sperre* ‚nicht wählbar‘ unter der *Karte*. Beides sagt nicht, dass Spieler 2
   *an der Reihe* ist; der *Grund* nennt das Was, nicht das Warum.

Keine Anforderung regelt einen Hinweis zum Ziehen oder einen *Grund*, der den *Spieler* *an der
Reihe* nennt; Texte dafür darfst du nicht erfinden.

**Kosten.** Zwei Spieler an einem Gerät, der erste Handgriff der Partie misslingt ohne
Erklärung. Der Stakeholder hielt die App für kaputt, bevor er den ersten Schritt von
[Review 5](../review.md) prüfen konnte; jede künftige Phase (Bewegen, Schießen) beginnt
ebenso mit „wer ist dran, was ziehe ich“. Nach [Ziel](../../domaene/ziel.md) verhindert Arbiter
Fehler, ohne dem *Spieler* das Denken abzunehmen; dazu muss er sehen, was gesperrt ist und
weshalb.

**Gegenvorschlag.** Zu 1 und 2 höchstens drei Optionen als Mockup, nur mit Komponenten der
Komponentenseite, und eine Frage an den Stakeholder mit Links, etwa: die *Ablage* des
*Spielers* *an der Reihe* hervorgehoben, die andere gedämpft; *Einheiten*, die man ziehen kann,
mit Greif-Zeiger und Kennzeichen. Bestehende Regel (Ich 4): AUF-4.4 „zeigt Arbiter ihn“ deckt
eine deutlichere Anzeige ohne neues Kriterium ab; was darüber hinausgeht (Hinweistext,
Gedämpftes), braucht ein Kriterium. Zu 3 und zu jedem Text ein Anliegen an den
Anforderungsautor, etwa ein *Grund* „Spieler 2 ist an der Reihe“ statt ‚nicht wählbar‘ bei
AUF-7.2 und AUF-16.5. Neue Komponenten: Anliegen an den Architekten. Erledigt, wenn die
Optionen beim Stakeholder liegen und die Texte als Anliegen beim Anforderungsautor.

**Stellungnahme.** (Ux) Die Rückmeldung des Stakeholders nach seinem Test am Bildschirm
ändert Punkt 2: Er hat in [683](683-aufstellenKlickenOderZiehen.md) entschieden, F1 A und
F2 a: Er wählt eine *Einheit* aus, klickt in die Zone, verschiebt sie als Ganzes; ein Umschalter
„Ganze Einheit / Einzelmodelle“ wie in ArbiterMap. Das Ziehen aus der *Ablage* entfällt, ein
Hinweis „ziehen“ und ein Greif-Zeiger sind damit überholt. Die Kriterien dazu, den *Grund*
statt ‚nicht wählbar‘ (Punkt 3) und eine deutlichere Anzeige *an der Reihe* (Punkt 1) schreibt
der Anforderungsautor ([684](684-anforderungenFuerKlickenBlockUndGrund.md)). Danach zeige ich
als Mockup *Auswahl*, Umschalter und Block. Der Randfehler beim Ziehen ist ein eigener Fehler:
[682](682-gezogeneKarteVerschwindetAmSpaltenrand.md). Ich setze `angenommen`, wenn die Mockups
eingebaut oder gelöscht sind.
