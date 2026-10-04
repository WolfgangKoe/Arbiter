# QUE-2, AUF-4: Begriffe Karte und Ablage, Namen der Spieler

195 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 1/3 · angenommen

## Runde 1
**Befund.** Für die erste Oberfläche (Plan 2, „Danach“; Anliegen 145,
Schnitt in Anliegen 146) stehen [QUE-2 · Karte](../../domaene/anforderungen/querschnitt.md) und
[AUF-4 · Anzeige der Aufstellung](../../domaene/anforderungen/phasen/aufstellen.md), die
Begriffe im [Glossar](../../domaene/glossar.md). Die Kriterien sagen, was die *Spieler* sehen;
Anordnung, Farben und Aussehen schlägt das Mockup vor (145 F1, 151 F1). Ohne Handlung prüft ein
Test von AUF-4.4, AUF-4.6 und QUE-2.4 nur den Anfang (keiner *an der Reihe*, keine Zone farbig,
kein *Modell* auf der *Karte*); den Rest zeigen erst Wählen und *Setzen*.

**Kosten.** Ohne Antwort fehlen der ersten Oberfläche zwei Wörter, mit denen Anforderung,
Mockup und Code dasselbe meinen, und die Beschriftung, an der die *Spieler* sich erkennen.

**F1 · Neue Begriffe.** Ohne Regelbegriff: *Karte* (aus dem Ziel: Abbild des *Spielfelds* mit
*Aufstellungszonen* und *gesetzten* *Modellen*, maßstäblich) und *Ablage* (aus Etappe 1: Ort
neben der *Karte*, je *Spieler* einer, mit seinen nicht *aufgestellten* *Einheiten* und
deren nicht *gesetzten* *Modellen*, nach Anliegen 199). A: so
freigeben. B: Du nennst andere Wörter.
Empfehlung A: Beide Wörter stehen schon in Ziel, Etappe 1 und Plan 2; die Ablage ist der
Bestand „Noch nicht aufgestellt“ aus ArbiterMap.

Antwort: .

**F2 · Wie heißen die Spieler?** Die *Ausgangslage* kennt nur zwei *Armeen*, keine Namen. Ohne
Namen kann Arbiter nicht zeigen, wer *an der Reihe* ist oder wem eine *Ablage* gehört.
- A: „Spieler 1“ führt die erste *Armee* aus `ausgangslage.yaml` (Boyz, Warboss), „Spieler 2“
  die andere (AUF-4.2).
- B: Der Name der Fraktion, etwa „Orks“ und „Necrons“; dazu kommt er in die *Ausgangslage*.
- C: Die *Spieler* geben Namen ein, bevor die *Aufstellung* beginnt.
Empfehlung A: So stehen sie in deinen Skizzen („Player 1“, „Player 2“, `Screen
Architecture.pdf`, S. 1) und in Arbiter-old (`Arbiter-old/docs/spec/setup.md:136`), dort mit
Absicht fraktionsneutral (`Arbiter-old/docs/spec/architecture_invariants.md:68`). B und C
brauchen Daten oder eine Eingabe, die Etappe 1 nicht verlangt.

Antwort: Rückfrage: Beim Rolloff wird ja über "Angreifer" und "Verteidiger" entschieden. Könnten dies nicht die Namen der Spieler sein? Das wäre regelkonform und damit würde sich auch alles weitere ergeben. 
