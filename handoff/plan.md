# Plan · Zyklus 3

Etappe: [1 · Aufstellen](../domaene/etappen/01-aufstellen.md)

Grundlage: Review 2 hat noch kein „Nächstes Vorgehen“; es gilt „Danach“ aus Plan 2. Abweichung:
Die Ablage wird gezeigt, Ziehen und Zurücklegen kommen später. Sie brauchen Handlungen über
HTTP und damit den Speicher (153 F1); der Architekt schneidet erst Anzeige, dann Wählen per
Klick, dann Ziehen (Anliegen 146, git).

## Items
1. [Karte im Browser](../domaene/items/karte-im-browser.md): QUE-2.1 bis QUE-2.6,
   [Mockup](../domaene/mockups/que-2.html)
2. [Anzeige der Aufstellung](../domaene/items/anzeige-der-aufstellung.md): AUF-4.2 bis
   AUF-4.7, nach Item 1, [Mockup](../domaene/mockups/auf-4.html)

Beide Mockups bringen ihr CSS als [Vorschlag](../domaene/mockups/vorschlag.css) mit; eine
Komponentenseite gibt es noch nicht (DoR 5). Sie folgen deinem Aufbau aus Anliegen 145 F1
(git): oben der gameHeader, links und rechts je Spieler die armyCard mit unitCards (Ablage),
in der Mitte die Karte. Die gameActionsArea fehlt, ihre Knöpfe kommen mit dem Wählen. Die
Mockups zeigen einen Zustand mit Spieler 1 an der Reihe und gesetzten Modellen, damit du
Farben und Abzeichen siehst.

## Empfehlung
Freigeben mit beiden Items und den Antworten unten. Danach startest du Arbiter mit einem
Befehl und siehst die Ausgangslage: Spielfeld, Zonen ohne Farbe, beide Ablagen, keinen an der
Reihe, kein Modell auf der Karte; handeln kannst du noch nicht. Die Zustände aus den Mockups
zeigen die Bilder des Bildschirmtests im Review; die Tests stellen sie mit den Handlungen der
Domäne her (Anliegen 198 A, git). Reihenfolge nach Abhängigkeit: AUF-4 steht neben der Karte
und färbt ihre Zonen. Reicht der Zyklus nicht, fällt Item 2. Start, Komponentenseite und
Bildschirmtest füllen allein einen Zyklus (146); mehr als die reine Anzeige passt nicht.

Noch nicht bereit: Nach DoR ist nichts offen. Vor der Freigabe fehlt die Kritik (Ablauf,
Domänenphase Schritt 6): Architekt an Plan, Items und Mockups (nur vorhandene Komponenten),
Fachkritiker an den Mockups gegen QUE-2 und AUF-4.

Vor dem Testautor (Technik, 146 Punkt 4): der Aufbau aus
[153](anliegen/153-frontendBackendUndDatenbank.md) in `technik/architektur/web.md` und
`speicher.md`, Wegwerf-Versuch zum Bildschirmtest, Komponentenseite aus
[vorschlag.css](../domaene/mockups/vorschlag.css). Keine Datenbank (153 F1 A). Dein „SOLID
und lesbar“ für den Unterbau trägt dieser Aufbau.

## Danach, nach Abhängigkeit
Wählen per Klick (Gewinner, Zone, Einheit) mit Speicher · Setzen, Umsetzen und Zurücklegen
durch Ziehen mit Maus und Touch, Sperre mit Grund · Zurück, gemeinsam übergehen und Protokoll
(16 F4) · Beenden mit fehlenden Modellen und Kohärenz (16 F3). Damit ist Etappe 1 erreicht.

## Offene Anliegen
Fragen an dich, die Freigabe beantwortet sie mit der Empfehlung:
- [153](anliegen/153-frontendBackendUndDatenbank.md) F1 (Architekt): Datenbank erst mit der
  ersten Handlung (A). Dort steht auch deine Nachprüfung des Aufbaus an, bevor er in die
  Technik geht.
- Anliegen 151 F2 (Organisationsentwickler, git): UX schreibt einbaufähig nach
  `domaene/mockups/`, der Implementierer übernimmt Markup und CSS ohne Umschreiben (A). Die
  Mockups oben sind so geschrieben.

Vom Anforderungsautor liegen keine offenen Vorschläge vor; Anliegen 195 ist erledigt
(F3 A: „Spieler 1“, „Spieler 2“, git). Die übrigen offenen Anliegen betreffen den Prozess und
wirken nicht auf die Items.

## Freigabe
Freigabe: offen
Kommentar: .
