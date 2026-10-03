# Wie heißen die zwei Aufstellungszonen?

58 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 2/3 · offen

## Runde 1
Anlass: [43](43-aufstellungszoneNamen.md). Der Implementierer hat `nord` und `süd` ohne Quelle
gesetzt; die *Spieler* sehen den Namen, wenn der *Gewinner* seine *Aufstellungszone* wählt
([AUF-1.2](../../domaene/anforderungen/phasen/aufstellen.md)).

**F1 · Namen der Aufstellungszonen.** Die Regel nennt keine: Die Mission zeigt die Zonen nur auf
ihrer Karte, einem Bild (`core_rules.txt:2182`), und spricht von „one of the two deployment
zones“ (`:2322`). Etappe 1 legt sie als 9″-Bänder an die beiden langen Kanten des Spielfelds
44″ × 60″ ([09](09-fragen-freigabe-etappen.md) F10 B).
A: Nord und Süd, fest am Spielfeld; dreht sich die Ansicht, bleibt der Name.
B: Oben und Unten, nach der Lage auf dem Bildschirm; der Name folgt der Ansicht.
C: Keine Namen; die *Spieler* tippen die Zone auf der Karte an. Bis zur Karte (nicht in
Zyklus 1) braucht der Code trotzdem zwei Werte ohne fachlichen Namen.
Empfehlung A: Ein Name, der an der Karte hängt, gilt auch für Protokoll und spätere Regeln
(„enemy's battlefield edge“, `:3324`), unabhängig von Gerät und Drehung; `nord` und `süd`
stehen schon im Code. Nach deiner Antwort kommen die zwei Namen mit Code-Bezeichner ins
Glossar.

Antwort: Es ist regeltechnisch falsch, hier konkrete Namen zu vergeben. Die Aufstellungszonen werden durch die Mission vorgegeben (Führe nochmals eine Recherche durch). Die Missionen müssen daher die Namen enthalten. Wir brauchen ggf. eine Klasse Mission oder Spielart (Matched, Open, Crusade), welche Missionen mit Spielart-typischen Parametern enthält, der Name wäre dann ein entsprechendes Objekt. Bitte meine Idee kritisch bewerten!

## Runde 2
**Recherche.** Die Mission legt die Zonen auf ihrer Karte fest (`core_rules.txt:2182`); einen
Namen trägt eine Zone nur dort, wo die Karte ihn zeigt. Open Play: Zone des Angreifers und des
Verteidigers (`open_play.txt:235`). Narrative Play: so, oder „Player A’s“ und „Player B’s“
(`narrative_play.txt:2001`). Matched Play: Der Verteidiger wählt eine von zwei unbenannten
(`matched_play.txt:540`). Only War: Der *Gewinner* wählt eine von zwei unbenannten
(`core_rules.txt:2322`). Sonst nennen die Regeln eine Zone nur vom *Spieler* aus: „your“ oder
„your opponent’s deployment zone“ (`matched_play.txt:1604`, `:1635`).

**Bewertung.** Richtig: Die Zonen gehören der Mission, `nord`/`süd` fällt
([63](63-zonenOhneErfundeneNamen.md) an den Implementierer). Drei Einwände:
1. Auch eine Mission Only War hätte keinen Namen für ihre Zonen; ihn aus dem Objekt zu holen,
   hieße ihn dort zu erfinden. Die *Spieler* erkennen ihre Zone an der Lage auf der Karte und
   als eigene.
2. Spielarten unterscheiden sich im Ablauf, nicht nur in Parametern: Matched Play bestimmt
   Angreifer und Verteidiger, Reserven und Nebenziele als eigene Schritte
   (`matched_play.txt:533`–`563`). Etappen 1 bis 7 kennen nur Only War; eine Spielart lohnt
   erst mit der zweiten, das entscheidet der Planer.
3. „Klasse“ ist Technik; die Domäne sagt *Mission* und Karte, die Form im Code wählt der
   Architekt.

**F2 · Begriffe.** A: Ins Glossar `Mission | mission | Mission` und `Aufstellungskarte |
deployment map | Aufstellungskarte` (`core_rules.txt:2182`); Only War steht als einzige Mission
mit den zwei Zonen der Etappe in `domaene/daten/`, ohne Namen; Kriterien sagen „eigene
*Aufstellungszone*“ und „die des Gegners“. Namen wie Angreifer und Verteidiger kommen mit der
ersten Mission, die sie zeigt. B: zusätzlich jetzt `Spielart` (Open, Narrative, Matched Play).
Empfehlung A.

Antwort:
