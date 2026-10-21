# Für den Knopf zum Zurücklegen fehlt ein Mockup, auf-23-sperre.html ist veraltet

Form: Kritik
Von: Fachkritiker
An: Ux
Runde: 2/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf. Das
Zyklusziel aus [Review 6](../review.md) enthält den Schritt *zurücklegen*. Jede Anforderung
braucht ein Mockup ([Ablauf, DoR 5](../../prozess/ablauf.md#dor-item-bereit)).

Der Stakeholder will einen Knopf neben „Aufstellen der Einheit beenden“, der die Boyz vom
Spielfeld nimmt ([AUF-23](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md),
Anliegen 2062). Bisher zeigt kein Mockup diesen Knopf.
[auf-23-sperre.html](../../domaene/mockups/auf-23-sperre.html) gehört zum alten AUF-23. Dort
legte man die Boyz zurück, indem man sie in die *Ablage* zog, und die Meldung ‚nur ganze
Einheit‘ gibt es nicht mehr.

Wie der Knopf heißt, wann man ihn sieht und ob es neben dem Spielfeld eine *Ablage* oder die
Reserve gibt, klärt der Anforderungsautor gerade in [2220](2220-knopfZuruecklegen.md). Darauf
wartet dieses Anliegen.

**Kosten.** Ohne Mockup kann der Planer den Schritt *zurücklegen* nicht einplanen, und der
Implementierer hat nichts, was er übernehmen kann. Das alte Mockup zeigt eine Meldung, die es
nicht mehr gibt.

**Gegenvorschlag.** Nach 2220 ein Mockup zu AUF-23 nach dessen Fassung: der Knopf neben
„Aufstellen der Einheit beenden“, solange Boyz auf dem Spielfeld stehen, und der Bildschirm
nach dem Klick. auf-23-sperre.html löschen oder durch das neue Mockup ersetzen.
Erledigt, wenn ein Mockup den Knopf vor und nach dem Klick zeigt, wie AUF-23 es beschreibt,
und kein Mockup mehr ‚nur ganze Einheit‘ zeigt.

**Stellungnahme.** Einverstanden, umgesetzt. Zwei neue Mockups zeigen den Knopf:
[vorher](../../domaene/mockups/auf-23-vorher.html) ist die *Einheit in Aufstellung*: Boyz
stehen auf der *Karte*, neben „Aufstellen der Einheit beenden“ steht „Einheit zurücklegen“.
[nachher](../../domaene/mockups/auf-23-nachher.html) ist der Bildschirm nach dem Klick: Die
*Karte* ist leer, die Boyz sind in der Spalte links noch angewählt, beide Knöpfe sind
verschwunden, weil keine *Einheit in Aufstellung* mehr da ist (AUF-23.4). Ein Klick in die
Zone stellt sie neu auf. Das alte Mockup mit ‚nur ganze Einheit‘ ist gelöscht; kein Mockup
zeigt die Meldung noch. Die Spalte heißt im Mockup nur im Hilfetext des Griffs *Ablage*, bis
du [2221](2221-ablageHeisstArmeeliste.md) beantwortest. Die übrigen Mockups bleiben
unverändert.

## Runde 2
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf. Das Mockup
[vorher](../../domaene/mockups/auf-23-vorher.html) passt, ‚nur ganze Einheit‘ ist überall weg.
In [nachher](../../domaene/mockups/auf-23-nachher.html) fehlt aber auch „Aufstellen der
Einheit beenden“. AUF-23.4 lässt nur „Einheit zurücklegen“ verschwinden. „Aufstellen der
Einheit beenden“ bleibt stehen: Klickst du ihn, ohne dass Boyz auf der *Karte* stehen,
meldet Arbiter ‚nicht in Aufstellung‘
([AUF-7.4](../../domaene/anforderungen/phasen/aufstellen/einheitInAufstellung.md), AUF-12.7).
So zeigt ihn auch der laufende Arbiter (`technik/frontend/seite.js:312`), und so stand es in
der Frage an den Stakeholder ([2220](2220-knopfZuruecklegen.md), F3 B: „wie beim Beenden“).

**Kosten.** Der Implementierer übernimmt das Mockup ohne Umschreiben
([Ablauf](../../prozess/ablauf.md), Technikphase, Schritt 3). Dann verschwindet nach dem Zurücklegen auch
„Aufstellen der Einheit beenden“, und die Meldung ‚nicht in Aufstellung‘ wäre am Bildschirm
nicht mehr zu erreichen. Die Spieler sähen eine Änderung, die keiner beschlossen hat.

**Gegenvorschlag.** In auf-23-nachher.html bleibt „Aufstellen der Einheit beenden“ in der
Knopfgruppe stehen, nur „Einheit zurücklegen“ fehlt. Erledigt, wenn nachher genau diesen
einen Knopf zeigt.

**Stellungnahme.** Einverstanden, umgesetzt. Du hast recht: Nur „Einheit zurücklegen“ verschwindet,
„Aufstellen der Einheit beenden“ bleibt stehen, damit die Meldung ‚nicht in Aufstellung‘
erreichbar bleibt. [nachher](../../domaene/mockups/auf-23-nachher.html) zeigt jetzt genau
diesen einen Knopf; sonst ist nichts geändert.
