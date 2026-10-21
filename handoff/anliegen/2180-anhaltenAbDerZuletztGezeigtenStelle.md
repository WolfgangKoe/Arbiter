# AUF-29: V10 hält ab der gesetzten Stelle an, nicht ab der zuletzt gezeigten

Form: Kritik
Von: Architekt
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Nachzug zu Anliegen 2090: [V10](../../technik/architektur/handlungen.md) und
[S3](../../technik/architektur.md#stelle-und-rechnen) verweisen jetzt auf AUF-24.3, 26.5,
28.2 und 29.1 statt auf die gestrichenen 24.1 und 26.2 bis 26.4. Eine Umbenennung reicht nicht
für alles: Die Abfrage `stellenBeimLoslassen(modell, stelle)` rechnet den Weg von der
*gesetzten* *Stelle* bis zum Zeiger, [AUF-29.1](../../domaene/anforderungen/phasen/aufstellen/anhaltenAufDemWeg.md)
ab der zuletzt gezeigten. Beides stimmt nur beim ersten Weiterrücken überein. V10 deckt also ab:
- AUF-24.3, 26.5 und 29.3 ganz (fremd ist beim Block nur eine *Base* einer anderen
  *Einheit*);
- AUF-29.1 und 28.2 nur für ein Weiterrücken ab der *gesetzten* *Stelle*.

Es fehlen:
1. AUF-29.1 über mehrere Weiterrücken: Zieht jemand um eine *Base* herum und dann hinein,
   hält V10 auf der geraden Strecke vom Start an, nicht vor der zuletzt gezeigten *Stelle*.
2. AUF-29.2 (Entlanggleiten): weder Vertrag noch Code.
3. AUF-28.2 nach mehreren Weiterrücken: `modellLoslassen` rechnet aus dem Punkt des Zeigers
   neu und *setzt* dann womöglich anders, als die *Karte* zuletzt zeigte.

Das wartet nach [Ich 3](../../prozess/praemissen/ich.md): Der Happy Path (ein Zug an einer
*Base* vorbei) läuft, keine Prüfung ist rot. Eine neue Schnittstelle gehört in die
Technikphase.

**Kosten.** Bis dahin prüft der Testautor 29.1 nur mit einem Weiterrücken (so steht es in V10,
Prüft). Tests zu 29.2 und zu mehreren Weiterrücken bleiben rot, bis ein Item sie umsetzt.

**Gegenvorschlag.** In der nächsten Technikphase ein Item zum Rest von AUF-29 (1 bis 3). Den
Vertrag dazu entscheide ich dort; meine Empfehlung: Die Seite schickt mit jeder Abfrage und
beim Loslassen die zuletzt gezeigte *Stelle* des gezogenen *Modells* mit (`vonX`, `vonY`), die
Domäne bleibt ohne Zustand: `stellenBeimLoslassen(modell, gezeigt, stelle)`. Eine *Stelle*
reicht, weil der Block um denselben Weg rückt. So hält es auch das Vorbild: Es rechnet je
Schritt ab dem vorigen (`ArbiterMap/…/model_drag.js:887`).

**Stellungnahme.** Das Item nehme ich an, den Zeitpunkt nicht. Es steht als
[Anhalten auf dem Weg](../../domaene/items/anhaltenAufDemWeg.md) (AUF-29, 28.2) bereit, für
Plan 8, nicht für die nächste Technikphase:
1. Plan 7 hat drei Items, das Höchstmaß: davor Item 1 (deine 1654 und 1655, dazu 1541), dann
   die drei Schritte des Zyklusziels aus Review 6 (*zurücklegen*, „gemeinsam übergehen“,
   Loslassen über der Kante).
2. AUF-29.2 hat ein offenes Anliegen, [2212](2212-entlanggleitenOhneFortschritt.md); das Item
   wäre nicht bereit (DoR 4).
3. Der Happy Path läuft, wie du schreibst; bis Plan 8 prüft der Testautor 29.1 mit einem
   Weiterrücken (V10, Prüft).

AUF-28.1 (Loslassen neben der *Karte*) ist in Plan 7, Item 2. Braucht es dafür schon die
zuletzt gezeigte *Stelle* (`vonX`, `vonY`), entscheidest du das im Vertrag zu Item 2; dann
schrumpft das Item in Plan 8.
