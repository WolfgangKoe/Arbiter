# Plan · Zyklus 3

Etappe: [1 · Aufstellen](../domaene/etappen/01-aufstellen.md)

Grundlage: Review 2 hat noch kein „Nächstes Vorgehen“; es gilt „Danach“ aus Plan 2. Abweichung:
Die Ablage wird gezeigt, Ziehen und Zurücklegen kommen später. Sie brauchen Handlungen über
HTTP und damit den Speicher (153 F1); der Architekt schneidet erst Anzeige, dann Wählen per
Klick, dann Ziehen (Anliegen 146, git).

## Items
1. [Karte im Browser](../domaene/items/karte-im-browser.md): QUE-2.1 bis QUE-2.6
2. [Anzeige der Aufstellung](../domaene/items/anzeige-der-aufstellung.md): AUF-4.2 bis
   AUF-4.7, nach Item 1

## Empfehlung
Freigeben mit beiden Items, sobald die Mockups verlinkt sind. Danach startest du Arbiter mit
einem Befehl und siehst die Ausgangslage: Spielfeld, Zonen ohne Farbe, beide Ablagen, keinen
an der Reihe, kein Modell auf der Karte; handeln kannst du noch nicht. Die Zustände mit
Spieler an der Reihe, gesetzten Modellen und farbigen Zonen zeigen die Bilder des
Bildschirmtests im Review; die Tests stellen sie mit den Handlungen der Domäne her (Anliegen
Anliegen 198 A). Reihenfolge nach Abhängigkeit: AUF-4 steht neben der Karte und färbt
ihre Zonen. Reicht der Zyklus nicht, fällt Item 2. Start, Komponentenseite und Bildschirmtest
füllen allein einen Zyklus (146); mehr als die reine Anzeige passt nicht.

Noch nicht bereit:
- DoR 5: Die Mockups fehlen. UX schreibt je Anforderung eins mit CSS-Vorschlag, du siehst sie
  vor der Freigabe (145 F1). Die Rolle wartet auf die Leitplanken des Organisationsentwicklers
  ([151](anliegen/151-rolleUxFuerDieErsteOberflaeche.md)).
- DoR 4: [195](anliegen/195-karteUndAblageBegriffeUndNamen.md) ist offen; die Freigabe
  beantwortet F1 und F2. Mit F2 B oder C ändert sich AUF-4.2.

Vor dem Testautor (Technik, 146 Punkt 4): der Aufbau aus
[153](anliegen/153-frontendBackendUndDatenbank.md) in der Technik, Voraussetzung 159,
Wegwerf-Versuch zum
Bildschirmtest, Komponentenseite aus dem CSS der Mockups. Keine Datenbank (153 F1).

## Aufbau der Oberfläche
Deine Antwort zu 145 F1 als Vorgabe für die Mockups; Einzelheiten schlägt UX vor:
- Oben der gameHeader aus Arbiter-old: wer an der Reihe ist (AUF-4.4).
- Links und rechts je Spieler die armyCard mit unitCards aus Arbiter-old: die Ablage
  (AUF-4.3, AUF-4.5); Spalten wie in `Arbiter-old/docs/spec/ui_layout.md`, Abschnitt 1.
- In der Mitte, wo Arbiter-old die gameActionsArea hat, die Karte aus ArbiterMap (QUE-2).
- Die gameActionsArea zieht nach unten, wo ArbiterMap das Datenblatt von unten einfährt
  (`ArbiterMap/frontend/CLAUDE.md:443`); ihre Knöpfe kommen mit dem Wählen.
- Farben, Icons, Schrift aus Arbiter-old; für die Karte, die Arbiter-old nicht hat, aus
  ArbiterMap (QUE-2.6, AUF-4.6, AUF-4.7).

Dein „SOLID und lesbar“ für den Unterbau trägt die Technik: Aufbau 153, Regel D4
(Anliegen 152); beide warten auf Platz in der Technik
(Anliegen 159).

## Danach, nach Abhängigkeit
Wählen per Klick (Gewinner, Zone, Einheit) mit Speicher · Setzen, Umsetzen und Zurücklegen
durch Ziehen mit Maus und Touch, Sperre mit Grund · Zurück, gemeinsam übergehen und Protokoll
(16 F4) · Beenden mit fehlenden Modellen und Kohärenz (16 F3). Damit ist Etappe 1 erreicht.

## Offene Anliegen
An dich, wirken auf Plan 3:
- [195](anliegen/195-karteUndAblageBegriffeUndNamen.md) (Anforderungsautor): Begriffe *Karte*
  und *Ablage*, Namen der Spieler.
- [153](anliegen/153-frontendBackendUndDatenbank.md) F1 (Architekt): Datenbank erst mit der
  ersten Handlung.
- Anliegen 159, [151](anliegen/151-rolleUxFuerDieErsteOberflaeche.md):
  beantwortet, der Organisationsentwickler liefert Optionen und Leitplanken nach.

Zwischen Rollen: Anliegen 155 und 152 warten
auf 159.

## Freigabe
Freigabe: offen
Kommentar: .
