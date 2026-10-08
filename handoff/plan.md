# Plan · Zyklus 4

Etappe: [1 · Aufstellen](../domaene/etappen/01-aufstellen.md)

Grundlage: Zyklusziel aus [Review 3](review.md), Wählen per Klick (Gewinner, Zone, Einheit) mit
Speicher. Abweichung nach deiner Wahl in Anliegen 308 (F1 A, F2 A, git): Arbiter startet mit
gewähltem Gewinner und gewählter Zone, Plan 4 bringt nur die Wahl der Einheit. Ein Klick wählt
sie aus, ohne Handlung; Einheit in Aufstellung wird sie erst mit dem ersten gesetzten Modell
(Anliegen 309, git).

## Items
1. [Vorläufiger Start](../domaene/items/vorlaeufigerStart.md): AUF-6.1
2. [Auswählen in der Ablage](../domaene/items/auswaehlenInDerAblage.md): AUF-5.3 bis
   AUF-5.10, QUE-3.1, nach Item 1
3. [Stand behalten](../domaene/items/standBehalten.md): QUE-3.2, QUE-3.3, nach Item 2

Mockups (DoR 5): [Start](../domaene/mockups/auf-6.html) zeigt gefärbte Zonen, „Spieler 2
an der Reihe“, volle Ablagen, nur aus vorhandenen Komponenten. [Auswahl](../domaene/mockups/auf-5.html)
zeigt dazu den Warboss von Spieler 1 ausgewählt und die Necron Warriors von Spieler 2 in
Aufstellung und ausgewählt, mit drei gekennzeichneten Modellen. Das Kennzeichen „ausgewählt“
(Umriss in Spielerfarbe an der Karte in der Ablage, heller Ring am Modell) hat der Architekt in
Anliegen 316 entschieden (git); es steht in `vorschlag.css`, in den Komponenten erst nach der
Technikphase.

**Hindernis:** Ob das für DoR 5 genügt, fragt der Architekt dich in
[317](anliegen/317-neueKomponenteVorDerFreigabe.md). Bis zu deiner Antwort sind Item 2 und
damit Item 3 nicht bereit; Item 1 ist es.

## Empfehlung
Beantworte 317 mit A, wie der Architekt empfiehlt (Begründung dort). Dann sind alle drei Items
bereit und du gibst sie zusammen frei. Mit B startet
der Koordinator vorher den Implementierer, danach Freigabe. Item 1 allein empfehle ich nicht:
gefärbte Zonen ohne Handlung.

Mit allen drei Items startest du Arbiter und siehst gefärbte Zonen und Spieler 2 an der
Reihe; ihr klickt oder tippt Einheiten in beiden Ablagen an und ab; auf der Karte ändert sich
nichts. Neu laden zeigt dieselbe Auswahl, neu starten wieder den Start. Setzen könnt ihr noch
nicht.

Reihenfolge nach Abhängigkeit: Item 1 legt fest, wer an der Reihe ist, und ändert das Bild,
auf dem Item 2 klickt. Item 2 ist die erste Handlung am Bildschirm, Item 3 der Speicher dazu
(Neuland, [speicher.md](../technik/architektur/speicher.md)). Reicht der Zyklus nicht, fällt
Item 3: Die Auswahl ändert am Spielstand nichts (AUF-5.8), Neuladen verliert nur sie.

Die Krücke: Solange AUF-6 steht, ist Etappe 1 nicht erreicht. Ihr Test geht mit ihr, wenn ihr
Gewinner und Zone am Bildschirm wählt (Plan 6).

Vor dem Testautor (Ablauf, Technikphase 1), Architekt: Vertrag für den Klick in
[web.md](../technik/architektur/web.md), Wegwerf-Versuch zum Wiederholen der Handlungen
(speicher.md, Neuland).

## Danach, nach Abhängigkeit
Plan 5: Setzen, Umsetzen und Zurücklegen durch Ziehen mit Maus und Touch, Sperre mit Grund ·
Plan 6: Gewinner und Zone am Bildschirm, AUF-6 entfällt; zurück, gemeinsam übergehen und
Protokoll · Beenden mit fehlenden Modellen und Kohärenz. Damit ist Etappe 1 erreicht.

## Offene Anliegen
An dich: [317](anliegen/317-neueKomponenteVorDerFreigabe.md), siehe Hindernis.
Deine Antworten, eingearbeitet: 308 F1 A, F2 A ·
309 Runde 2 F1 B, F2 B, Runde 3 F1 A, Runde 1 F2 A (git, vom Anforderungsautor eingetragen).
Vom Anforderungsautor steht kein Vorschlag offen; aus 307 bleiben F2 (Wahl der Zone) und der
Begriff Spielaktionsbereich für Plan 6 (git).

Die übrigen offenen Anliegen betreffen den Prozess
([Moderation](moderation.md)).

## Freigabe
Freigabe: offen
Kommentar: .
