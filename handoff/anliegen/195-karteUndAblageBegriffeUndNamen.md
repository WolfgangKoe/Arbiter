# QUE-2, AUF-4: Begriffe Karte und Ablage, Namen der Spieler

195 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 2/3 · beantwortet

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

## Runde 2
**Stellungnahme zu F1.** Umgesetzt: *Karte* und *Ablage* stehen ohne Regelbegriff im Glossar.

**Stellungnahme zur Rückfrage in F2.** Angreifer und Verteidiger passen nicht:
1. Only War kennt sie nicht. Dort wählt der *Gewinner* des *Roll-offs* seine
   *Aufstellungszone*, und der andere beginnt (`core_rules.txt:2322`). Angreifer und Verteidiger
   bestimmen nur Missionen aus Matched, Narrative und Open Play (`matched_play.txt:533`,
   `narrative_play.txt:1994`, `open_play.txt:220`); in Matched Play wählt der Verteidiger die
   Zone und stellt zuerst auf (`matched_play.txt:540`, `:563`), also anders als Etappe 1.
2. Die Rolle steht erst nach dem *Roll-off* fest. Schon davor muss Arbiter die *Spieler*
   unterscheiden: bei der Eingabe des *Gewinners* (AUF-1.1) und an den *Ablagen* (AUF-4.3).

Aus demselben Grund taugen „Gewinner“ und „Anderer“ nicht als Namen: Only War würfelt dreimal
mit je eigenem *Gewinner* (Missionsziele, Aufstellung, erster Zug; `core_rules.txt:2318`,
`:2322`, `:2329`). Bringt eine spätere Etappe eine Mission mit Angreifer und Verteidiger, kann
Arbiter die Rolle neben dem Namen zeigen; das wird dann eine eigene Anforderung.

**F3 · Wie heißen die Spieler?** Optionen A, B, C wie in F2.
Empfehlung A, Begründung wie in F2. AUF-4.2 steht schon so; wählst du B oder C, ersetzt sie ein
neues Kriterium.

Antwort: A
