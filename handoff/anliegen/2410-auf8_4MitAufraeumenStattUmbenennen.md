# Item 1 benennt Code um, den Etappe 2 löscht

Form: Kritik
Von: Architekt
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet. Kein Schritt des
Happy Path fehlt, keine Prüfung ist rot. Es geht um Kosten und Schnitt, und die sind nur vor
der Freigabe von Plan 7 billig zu ändern; darum `Domänenphase`, die läuft.

[Item 1](../../domaene/items/aufraeumenUndFesteAdresse.md) benennt *Ablage* in Code und Tests
in *Armeeliste* um (2370). Ein Teil dieses Codes dient nur
[AUF-8.4](../../domaene/anforderungen/phasen/aufstellen/ziehen.md), und AUF-8.4 entfällt mit
Test in [loslassenNebenDerKarte](../../domaene/items/loslassenNebenDerKarte.md), Etappe 2:
- `modellAufAblageLoslassen` in der Domäne (`aufstellen/__init__.py`:142), im Dienst
  (`anwendung.py`:84, 151, 182, Route `DELETE …/stelle?ablage=`) und in `seite.js`:97, 224;
- `testAuf8_4…` in `ziehenTest.py`:82, die Fälle `auf8_4…` in `sperreOhneStelleTest.py`:108,
  109, der Helfer in `dienst.py`:108, der Einheitstest `?ablage=3` in `anwendungTest.py`:124;
- die Zeile zu AUF-8.4 in [handlungen.md](../../technik/architektur/handlungen.md).

Plan 7 benennt das also um, Etappe 2 löscht es. Der Kommentar in `__init__.py`:144 nennt
zudem AUF-16.3 und 16.6, die es nicht mehr gibt.

AUF-8.4 wartet nur auf AUF-16.8 (2312, 2370), und AUF-16.8 hat noch keinen Test. Fasst der
Anforderungsautor 16.8 jetzt neu („neben der *Karte*, auch auf einer *Armeeliste*“), muss
kein Test geändert werden. Ohne die Route schickt die Seite beim Loslassen auf der
*Armeeliste* keine Anfrage und zeichnet den letzten Stand (V8). Das *Modell* springt also
still zurück, wie 16.8 es dann verlangt.

**Kosten.** Bleibt es so, wird jede der genannten Stellen zweimal angefasst: in Item 1
umbenannt, in Etappe 2 gelöscht, jeweils mit den Kritiken am Code. Das trifft gerade die
Dateien, an denen Item 1 ohnehin schneidet: `seite.js` liegt über dem Höchstmaß, und in der
Domäne hängt `Aufstellung` an der *Auswahl* (1651). Entfällt AUF-8.4 schon in Item 1, wird
das Item kleiner statt größer. Am Happy Path ändert sich nichts.

**Gegenvorschlag.** In Item 1 „Entfällt mit Test: AUF-17, AUF-8.4“, aus loslassenNebenDerKarte
den Satz dazu streichen. Der Anforderungsautor nimmt im selben Schritt 8.4 aus AUF-12.5 und
dem Zweck von AUF-12 und fasst AUF-16.8 wie oben (Vorgehen wie 801), AUF-16.8 bleibt in
loslassenNebenDerKarte. Die Umbenennung betrifft dann nur, was bleibt, etwa `ablage` im
Spielstand, `ablageNachNummer`, `einheitInDerAblage`.

Erledigt, wenn Item 1 AUF-8.4 nennt oder du begründest, warum es bis Etappe 2 bleibt.

**Stellungnahme.** Angenommen; 2450 ist erledigt: AUF-8.4 ist gelöscht, AUF-12 und AUF-16.8 sind neu gefasst, die Tests dazu löscht der Testautor in Item 1. Keine Antwort des Stakeholders legt fest, wann AUF-8.4
entfällt; 2361 F2 A verschiebt nur AUF-16.8 nach Etappe 2, den Zeitpunkt für 8.4 habe ich
in 2370 gewählt. Ein Modell, das jemand auf eine *Armeeliste* zieht, springt dann schon ab
Item 1 still zurück statt ‚nicht wählbar‘ zu nennen; das ist abseits des Happy Path und
folgt 2220 F4 A.
- [Item 1](../../domaene/items/aufraeumenUndFesteAdresse.md): „Entfällt mit Test: AUF-17
  (*zurück*), AUF-8.4“.
- [loslassenNebenDerKarte](../../domaene/items/loslassenNebenDerKarte.md): der Satz zu
  AUF-8.4 ist gestrichen; AUF-16.8 bleibt dort, mit dem Vermerk „auch auf der *Armeeliste*“.
- [Plan 7](../plan.md) nennt es bei Item 1 und nicht mehr unter der Abweichung.
- AUF-8.4 löschen, AUF-12 und AUF-16.8 neu fassen: an den Anforderungsautor in
  [2450](2450-auf8_4SchonMitItem1.md), dort mit Verweis auf 2440.
