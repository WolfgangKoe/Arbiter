# Plan · Zyklus 3

Etappe: [1 · Aufstellen](../domaene/etappen/01-aufstellen.md)

Grundlage: Review 2 hat noch kein „Nächstes Vorgehen“; es gilt „Danach“ aus Plan 2. Abweichung:
Die Ablage wird gezeigt, Ziehen und Zurücklegen kommen später. Sie brauchen Handlungen über
HTTP und damit den Speicher (153 F1; Schnitt aus Anliegen 146, git).

## Items
1. [Karte im Browser](../domaene/items/karte-im-browser.md): QUE-2.1 bis QUE-2.6,
   [Mockup](../domaene/mockups/que-2.html)
2. [Anzeige der Aufstellung](../domaene/items/anzeige-der-aufstellung.md): AUF-4.2 bis
   AUF-4.7, nach Item 1, Mockups
   [Ausgangslage](../domaene/mockups/auf-4-ausgangslage.html) und
   [Spieler 1 an der Reihe](../domaene/mockups/auf-4.html)

Die Mockups folgen deinem Aufbau aus Anliegen 145 F1 (git), mit deinen Namen aus 223 F1: oben
die kopfzeile, links und rechts je Spieler die armeeKarte mit einheitenKarten (Ablage), in der
Mitte die Karte. Jede einheitenKarte zeigt die Anzahl ihrer nicht gesetzten Modelle, keinen
Durchmesser (AUF-4.3 nach 239 F1 B). Der spielAktionsBereich fehlt, seine Knöpfe kommen mit dem
Wählen. Die Ausgangslage ist das Bild, das du am Ende des Zyklus siehst; „Spieler 1 an der
Reihe“ zeigt gesetzte Modelle, damit du Farben und Abzeichen siehst.

## Empfehlung
Beide Items wie freigegeben. Danach startest du Arbiter mit einem Befehl und siehst die
Ausgangslage: Spielfeld, Zonen ohne Farbe, beide Ablagen, keinen an der Reihe, kein Modell auf
der Karte; handeln kannst du noch nicht. Die Zustände aus den Mockups zeigen die Bilder des
Bildschirmtests im Review; die Tests stellen sie mit den Handlungen der Domäne her (Anliegen
198 A, git). Reihenfolge nach Abhängigkeit: AUF-4 steht neben der Karte und färbt ihre Zonen.
Reicht der Zyklus nicht, fällt Item 2. Start, Komponentenseite und Bildschirmtest füllen allein
einen Zyklus (146).

Offen, blockiert nicht: Die Kritik des Fachkritikers an den Mockups gegen QUE-2 und AUF-4
(Ablauf, Domänenphase Schritt 6) fehlt, auch nach 223 und 239.

Vor dem Testautor (146 Punkt 4), in dieser Reihenfolge:
1. Flask und Playwright in `pyproject.toml`, Regelumsetzer
   ([234](anliegen/234-flaskUndPlaywrightFehlen.md), umgesetzt, Nachprüfung Architekt).
2. Schreibrecht auf `technik/frontend/` für den Implementierer, Organisationsentwickler
   ([233](anliegen/233-frontendOhneAutor.md), umgesetzt, Nachprüfung Architekt).
3. Aufbau aus [153](anliegen/153-frontendBackendUndDatenbank.md) in `web.md` und
   `speicher.md`, Wegwerf-Versuch zum Bildschirmtest, Architekt. Keine Datenbank (153 F1 A).
   Er trägt dein „SOLID und lesbar“ für den Unterbau.

Die Komponentenseite aus [vorschlag.css](../domaene/mockups/vorschlag.css) ist der erste
Bildschirmtest: Der Testautor schreibt ihn, der Implementierer baut die Seite
(`technik/architektur.md`, Oberfläche).

## Danach, nach Abhängigkeit
Wählen per Klick (Gewinner, Zone, Einheit) mit Speicher · Setzen, Umsetzen und Zurücklegen
durch Ziehen mit Maus und Touch, Sperre mit Grund · Zurück, gemeinsam übergehen und Protokoll
(16 F4) · Beenden mit fehlenden Modellen und Kohärenz (16 F3). Damit ist Etappe 1 erreicht.

## Offene Anliegen
Deine Antworten, eingearbeitet: [223](anliegen/223-mockupsBenennungUndZonenfarbe.md) F1 A mit
deinen Namen · 153 F1 A · 151 F2 A (git) · [238](anliegen/238-implementiererSchreibtFrontend.md)
F1 A · [239](anliegen/239-durchmesserInDerAblageZeigen.md) F1 B, kein AUF-4.8.

An dich: [241](anliegen/241-frontendUndBackendParallel.md) (Organisationsentwickler, aus deiner
Stellungnahme in 238): Frontend und Backend parallel. Plan 3 ändert sich nur bei F1 B. Ich
teile Empfehlung A: Item 2 baut auf Item 1, der Vertrag entsteht erst mit Schritt 3 oben.

Die übrigen offenen Anliegen betreffen den Prozess.

## Freigabe
Freigabe: ja
Kommentar: Ich habe Anliegen kommentiert und Fragen beantwortet. Bitte systematisch durchgehen.
Stellungnahme: Nachgezogen: Mockups (223, 239 B), Vor dem Testautor, Offene Anliegen (neu 241); Items gleich.
