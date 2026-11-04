# Vertrag: Schlacht · Seite

Abschnitt der *Schlacht*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt.md).

- Kopfzeile (QUE-10.1): Die `kopfzeileSpieler` des *Spielers* `amZug` trägt
  `amZug` und `kopfzeileAmZug` „Schlachtrunde <n> · <phase>“. `beendet` (QUE-10.4):
  `kopfzeileSchlachtBeendet` „Schlacht beendet“ im `kopfzeileTitel`.
- Knöpfe (V7): „Erster Zug“ in der `knopfGruppe` jeder `armeeKarte`, wenn `ersterZug`
  `null` ist (QUE-9.1); „Phase beenden“ in der `knopfGruppe` der Mitte, wenn
  `amZug` nicht `null` ist (QUE-11.1), also weder vor dem *ersten Zug* noch nach `beendet`;
  ohne `schlacht` (in der *Aufstellung*) auch nicht. Domäne: `phaseBeenden` ohne *Spieler*
  *am Zug* ändert nichts (V13).
- Zug (V8, V10) und Klick: [Bewegung](../bewegung/seite.md), in jeder *Phase* gleich;
  außerhalb der *Bewegungsphase* nennt V10 kein *Modell* (QUE-10.5), keines bewegt sich.
