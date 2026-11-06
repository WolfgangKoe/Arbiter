# Fliegen: BEW-18.3 und BEW-25.1 widersprechen sich beim Weiterziehen

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 11

## Runde 1
**Befund.** Abseits des Happy Path, darum wartend. Steht die Spinne nach BEW-8.4 in
*Nahkampfreichweite* und zieht jemand sie heraus, sagen zwei Kriterien Verschiedenes:
- [BEW-25.1](../../domaene/anforderungen/phasen/bewegung/weiterziehenNachDemUebergehen.md):
  6.2 hält sie an der vorigen *Stelle* an, BEW-8.3 gilt.
- [BEW-18.3](../../domaene/anforderungen/phasen/bewegung/fliegen.md): 6.2 hält „nur“ an, wenn
  sie am Ende der Strecke in *Nahkampfreichweite* wäre.

Das Gebaute folgt 18.3. Das zeigte eine Probe an `Schlacht`, nicht am Bildschirm: Der
Warboss steht ½″ neben der übergangenen Spinne, sie wird 2″ von ihm weggezogen. Sie steht
danach am neuen Punkt, *gemeinsam übergehen* wird nicht angeboten, das *Protokoll* bekommt
keinen *Eintrag*. Ein Warrior bleibt in derselben Lage nach 25.1 stehen, *gemeinsam
übergehen* wird angeboten. Hinter der *Bewegungsweite* und beim Ziehen innerhalb der
*Nahkampfreichweite* hält auch die Spinne nach 25.1 an.

Der Regeltext erlaubt *Fliegen* die Bewegung durch *Nahkampfreichweite*
(`core_rules.txt:884`, `:888`). Eine *Einheit*, die in *Nahkampfreichweite* steht, kann
aber nur Fall Back machen oder stehen bleiben (`core_rules.txt:739`); Fall Back kommt erst
mit [Etappe 3](../../domaene/etappen/03-angriffUndFallBack.md).

**Kosten.** Ohne Klärung kann die Spinne eine bewusst übergangene *Nahkampfreichweite* ohne
*Eintrag* wieder verlassen. Das Nachbessern kostet einen Satz im Kriterium, einen Test und
wenige Zeilen in `Fliegen`. Die Fachabnahme des Items hält das nicht auf: 18.3 ist erfüllt,
BEW-25 gehört nicht zu seinem Umfang.

**Gegenvorschlag.** BEW-18.3 beginnt mit „Gegeben 18.1, außer BEW-25.1 hält an“; so hält die
Spinne wie jedes andere *Modell* und bleibt die Bewegung durch die *Nahkampfreichweite*
erlaubt. Fall Back regelt dann Etappe 3. Testautor und Implementierer folgen aus dem
geänderten Kriterium.

**Stellungnahme.**
