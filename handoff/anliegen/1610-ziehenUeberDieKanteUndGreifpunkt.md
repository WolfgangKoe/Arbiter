# Ziehen über die Kante der Karte und Greifpunkt anders als in ArbiterMap

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Fachliche Abnahme der Items [einheitVerschieben](../../domaene/items/einheitVerschieben.md)
und [anhaltenAnBases](../../domaene/items/anhaltenAnBases.md), am laufenden Arbiter mit der Maus
nachgespielt. Beide sind abgenommen. Einordnung nach [Ich 3](../../prozess/praemissen/ich.md):
wartet. Schritte 4 und 5 aus [Plan 6](../plan.md) sind machbar, alle Akzeptanztests sind grün. Was
folgt, weicht von ArbiterMap ab, betrifft aber nur Fälle, die kein Kriterium der Items regelt.
1. Über die Kante gezogen: Spieler 2 zieht seine Necron Warriors aus der Mitte seiner Zone
   nach rechts und kommt mit dem Zeiger über die Kante der *Karte* hinaus. Beim Halten zeigt die
   *Karte* den Block an der Kante angehalten, so wie Schritt 4 es verspricht. Lässt er dort los,
   springt der Block an seine Stelle vor dem Ziehen zurück. Das verlangt
   [AUF-16.6](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md). Was die *Karte*
   beim Halten zeigt, ist dann nicht das, was das Loslassen *setzt* (AUF-24.1, 26.4 setzen das
   voraus). ArbiterMap *setzt* beim Loslassen dort, wo die Vorschau zuletzt stand, gleich wo der
   Zeiger ist (`ArbiterMap/frontend/static/js/model_drag.js:1536`, Gruppe `:1605`). Jede
   *Aufstellungszone* liegt an einer Kante, und gleich daneben liegt die eigene *Ablage*.
   Mit [AUF-23](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md) (Plan 7)
   würde ein Loslassen dort die *Einheit* *zurücklegen*.
2. Greifpunkt: Arbiter setzt den Mittelpunkt des gezogenen *Modells* unter den Zeiger (AUF-8.2
   „*Stelle* des Loslassens“). Fasst man eine *Base* am Rand, springt sie um bis zu einen
   Radius. ArbiterMap behält den Abstand zwischen Zeiger und Mittelpunkt bei
   (`model_drag.js:1479`, B12).
3. Zum Vormerken für Anliegen Anliegen 1320: Den
   Overlord habe ich gerade nach oben durch zwei Necron Warriors gezogen. Er ist in eine freie
   Lücke dahinter gesprungen, so wie AUF-26.2 es verlangt. Der Zweck von
   [AUF-26](../../domaene/anforderungen/phasen/aufstellen/anhaltenAnEinerBase.md) sagt dagegen
   „an der ersten *Base*, an die es stößt“ und beschreibt damit nicht, was gebaut ist
   ([DoD 3](../../prozess/ablauf.md#dod-item-fertig)). ArbiterMap hält auf der Strecke an und
   gleitet an der *Base* entlang (`model_drag.js:887`, `:964`).

**Kosten.** Zu 1: Wer seine *Einheit* an die Kante schiebt, kommt mit dem Zeiger leicht darüber.
Er sieht dann, dass sie angehalten wird, und nach dem Loslassen steht sie wieder am Anfang. Ab
Plan 7 wäre sie dabei sogar *zurückgelegt*. Der Stakeholder will die Bedienung von ArbiterMap,
das hat er bei der Freigabe von Plan 6 deutlich gesagt. Zu 2: Ein kleiner Sprung beim Greifen,
den ArbiterMap nicht hat. Zu 3: Der Zweck verspricht mehr, als gebaut ist.

**Gegenvorschlag.** In der Domänenphase je eine Frage an den Stakeholder, mit Empfehlung:
1. Empfehlung wie ArbiterMap: Ein *gesetztes* *Modell*, das über die Kante der *Karte* hinaus
   gezogen und dort losgelassen wird, *setzt* Arbiter an die *Stelle*, die die *Karte* zuletzt
   zeigte. AUF-16.6 gilt dann nur noch für das, was nicht *gesetzt* ist. AUF-23 grenzt du davon
   ab, etwa so: Zurückgelegt wird nur, wenn man auf der *Einheitenkarte* der *Einheit* loslässt,
   nicht irgendwo in der Spalte der *Ablage*.
2. Empfehlung wie ArbiterMap: AUF-8.2 und 21.1 *setzen* um den Weg des Zeigers, nicht an den
   Punkt des Zeigers.
3. Das schreibst du in die Neufassung von AUF-26, die der Stakeholder in 1320 für Zyklus 7
   vormerkt. Der Zweck sagt bis dahin „nur wenn die *Stelle* am Ende eine *Base* überdecken
   würde“.

**Stellungnahme.** Angenommen. 1: AUF-28.1, *zurücklegen* per Knopf
([2210](2210-loslassenNebenDerKarteWiderspruechlich.md)). 2: AUF-8.7. 3: AUF-29 (1820).
