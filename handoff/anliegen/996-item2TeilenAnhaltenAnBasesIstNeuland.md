# Item 2 teilen: Anhalten an Bases ist Neuland, der Rest nicht

996 · Kritik · von Architekt → Planer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf. Ich habe in [975](975-plan6KostenVonItem2.md)
gesagt, wie die *Karte* den Block beim Ziehen zeigt: Der Spielstand liefert den Spielraum mit,
ein Rechteck wie `allowed_vector_bounds` in ArbiterMap. Das trägt nur das Hineinrücken in die
Zone. Erst danach kam [AUF-26](../../domaene/anforderungen/phasen/aufstellen/anhaltenAnEinerBase.md)
dazu (984). Wo ein *Modell* an einer *Base* anhält, hängt von der Richtung des Zuges ab, und
das zeigt kein Rechteck.
1. ArbiterMap hat dafür Sperrflächen je *Modell* als Pfad geschickt. Der Browser fragt nur, ob
   ein Punkt darin liegt, und tastet sich halbierend heran (`ArbiterMap/frontend/static/js/model_drag.js:180`
   bis `:215`). Dafür brauchte es die Items 011-B, 030 und 068 und mehrere Reparaturen.
2. Die *Stelle* der Berührung ist im Allgemeinen eine Wurzel. Nach [S2](../../technik/architektur.md)
   rechnet Arbiter aber exakt und ohne Wurzel. Ich brauche also eine Regel wie in
   `technik/arbiter/domaene/phasen/aufstellen/ziehen.py` (auf 1/100″ zur sicheren Seite), bevor
   ein Test AUF-26.2 und 26.3 prüfen kann.
3. „Verträge in einem Lauf, Tests zugleich“ lässt Item 1 auf diesen Versuch warten. Dabei
   braucht Item 1 fast nur Vorhandenes: Die *Formation* und das Hineinrücken setzt schon
   `einheitLoslassen`, und die Anfrage `PUT …/einheiten/<e>/stelle` gibt es (V5).

**Kosten.** Bleibt Item 2 ganz, hängen die einfachen Schritte 4 und 5 am Neuland. Klemmt es
dort, wird das Item nicht grün, also nicht committet, und der Stakeholder sieht im Review auch
die *Ebene* nicht. Item 1 beginnt erst nach meinem Versuch.

**Gegenvorschlag.** Ich 4: Höchstens drei Items je Plan (Ablauf, Domäne 6), dein Happy Path
bleibt, nur die Reihenfolge des Bauens ändert sich, kein Kriterium ändert sich.
- Item 2 „Einheit und Modell verschieben“: AUF-20.2, 20.4, 20.5, 21.1, 21.2, 24.2, 25.1 bis
  25.4, 26.1. Beim Ziehen folgt die *Einheit* dem Zeiger, beim Loslassen gilt die Antwort.
- Item 3 „Anhalten an Bases“: AUF-24.1, 26.2, 26.3, 26.4 (alles „schon beim Ziehen“ und
  „hält vor fremden *Bases* an“), dazu was [997](997-gesperrtesModellOhneUrsprungNachPlan6.md) entfallen lässt. Risiko des Zyklus.
- Gleichzeitig: Vertrag zu Item 1 und 2 in einem Lauf, ohne Versuch; mein Wegwerf-Versuch zu
  Item 3 läuft in `/tmp` neben den Tests und dem Bau von Item 1. Item 2 wird nach Item 1
  gebaut, Item 3 nach Item 2, denn alle drei ändern das Ziehen in `seite.js` und
  `Aufstellung`.

Erledigt, wenn der Plan so schneidet oder deine Stellungnahme begründet, warum Item 2 ganz
bleibt, und der Absatz „Gleichzeitig“ den Versuch neben Item 1 nennt.

**Stellungnahme.** Angenommen, geschnitten wie vorgeschlagen.
- [Einheit und Modell verschieben](../../domaene/items/einheitVerschieben.md): dein Umfang,
  ohne Vorarbeit.
- Neu [Anhalten an Bases](../../domaene/items/anhaltenAnBases.md): AUF-24.1, 26.2 bis 26.4,
  dazu was 997 entfallen lässt (999); Abhängigkeit: Item 2 und dein Versuch.
- [Plan 6](../plan.md): Schritte 4, 5 nennen Item 2 und 3; Reihenfolge 1, 2, 3 mit deiner
  Begründung; „Gleichzeitig“ nennt die Verträge zu 1 und 2 in einem Lauf und deinen Versuch
  neben Tests und Bau von Item 1.
