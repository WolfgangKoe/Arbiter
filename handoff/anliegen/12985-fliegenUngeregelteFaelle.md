# Fliegen: was die Karte zeigt und vier ungeregelte Fälle

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Beim Vertrag [Fliegen](../../technik/architektur/vertrag/bewegung/fliegen.md)
(Item [fliegen](../../domaene/items/fliegen.md)):
1. [BEW-18.1](../../domaene/anforderungen/phasen/bewegung/fliegen.md) zeigt nach BEW-1.7,
   also dort, wo BEW-1.5 beim Loslassen *setzen* würde. Mit 18.2 wäre das schon die
   nächste freie *Stelle*; die Spinne spränge beim Ziehen um jede *Base* herum. Dein Bild
   aus 8840 und Plan Schritt 5 ist anders: darüber hinwegziehen, beim Loslassen rücken.
   Dafür darf QUE-1.2 beim Ziehen nicht sperren, sonst bleibt die *Karte* vor der *Base*
   stehen (V10 409).
2. Findet 18.2 keine freie *Stelle* (selten, etwa nach AUF-27.1), sagt BEW-18 nichts.
3. Nach *gemeinsam übergehen* (BEW-8.4) kann die Spinne auf einer fremden *Base* enden; 18.2
   gilt nur beim Loslassen, also sperrt QUE-1.2, das Angebot bleibt.
4. BEW-18.3 nennt das „Ende der Strecke nach BEW-3.1“. Hält die *Spielfeldkante* früher
   (6.1), läge die Spinne an deren Halt womöglich in *Nahkampfreichweite*.

**Kosten.** Je ein Halbsatz. Bis dahin gilt im Vertrag die Empfehlung: 1 und 4 wie unten, 2
und 3 sperrt QUE-1.2 wie bisher; der Testautor prüft nur, was ein Kriterium nennt.

**Gegenvorschlag.**
1. BEW-18.1: „… zeigt die *Karte* es, wo BEW-1.5 es ohne BEW-17.1 und 18.2 *setzen* würde,
   ohne *Sperre* nach QUE-1.2“ (8840: „nur darüber hinwegziehen“).
2. BEW-18.2: „… gibt es keine, sperrt QUE-1.2“ (bestehende Regel).
3. Frag den Stakeholder, ob 18.2 auch nach BEW-8.4 gilt, dann nur mit 6.1; meine
   Empfehlung: ja, er will Klemmen statt Sperre (8840).
4. BEW-18.3: „am Ende der Strecke nach BEW-6.3 ohne 6.2“.

**Stellungnahme.** Umgesetzt in [BEW-18](../../domaene/anforderungen/phasen/bewegung/fliegen.md),
umformuliert statt neu nummeriert, weil noch kein Test sie prüft; gekürzt, die Datei hält
1.200 Zeichen.
1. Angenommen: 18.1 zeigt, wo BEW-1.5 ohne 17.1, 18.2 und QUE-1.2 *setzen* würde.
2. Angenommen als BEW-18.6 (Etappe 7): erreichbar erst nach AUF-27.1 (Anliegen 13020).
3. Gefragt in Anliegen 13010: 18.2 gilt auch nach BEW-8.4,
   nach F2 ohne BEW-3.1, nach F3 A immer mit 6.2, auch wenn 6.2 vor BEW-8.3 anhielt
   (BEW-18.7; 18.5 und 18.8 gestrichen). 13010 ist erledigt.
4. Angenommen: 18.3 „am Ende der Strecke nach 6.3 ohne 6.2“.
