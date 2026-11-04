# Fliegen: Spinne nach dem Übergehen auf einem fremden Modell

Form: Fragen
Von: Anforderungsautor
An: Stakeholder
Runde: 2/3
Status: erledigt

## Runde 1
**Befund.** Aus Anliegen [12985](12985-fliegenUngeregelteFaelle.md), Fall 3. Die Spinne hat
*Fliegen*: Beim Ziehen zeigt die *Karte* sie auch über fremden *Bases*
([BEW-18.1](../../domaene/anforderungen/phasen/bewegung/fliegen.md)). Hält Arbiter sie an der
*Bewegungsweite* oder vor der *Nahkampfreichweite* an und wählen beide *Spieler* *gemeinsam
übergehen*, *setzt* Arbiter sie an den Punkt des Loslassens (BEW-8.4). Dort kann sie auf
einem fremden *Modell* stehen. Der Regeltext sagt nur: Sie darf nicht darauf enden
(`core_rules.txt:884`); vom Übergehen weiß er nichts. Lässt man sie ohne Übergehen auf einem
fremden *Modell* los, schiebt Arbiter sie an die nächste freie *Stelle* (BEW-18.2).

**Kosten.** A: ein Kriterium (BEW-18.4, steht schon), in der Technik gering, ein bis zwei
Tests. B: kein Kriterium, BEW-18.4 entfällt; die Spieler ziehen die Spinne neu.

**Gegenvorschlag.**
**F1 · Was tut Arbiter, wenn die Spinne nach dem Übergehen auf einem fremden Modell stünde?**
A: Er schiebt sie wie beim Loslassen an die nächste freie *Stelle* im *Spielfeld*, ohne
*Bewegungsweite* und *Nahkampfreichweite* zu beachten, die ja übergangen sind; der *Eintrag*
im *Protokoll* bleibt (ArbiterMap, Anliegen 8840).
B: *Sperre* ‚Base überdeckt‘: Die Spinne steht wieder, wo sie vor dem Ziehen war (QUE-1.2).
Empfehlung: A, Sie schrieben in 8840, Klemmen sei „deutlich besser und intuitiver“ als eine
Sperre; mit B bekämen die Spieler nach ihrem Übergehen eine Sperre, die sie nicht übergehen
können.
Annahme: BEW-18.4 steht nach A; bei B lösche ich es.
Antwort: Es soll auf die nächste freie Stelle geschoben werden. Aber die Bewegungsweite und Nahkampfreichweite muss beachtet werden. Hat die Spinne damit keinen Platz, kann sie nicht bewegt werden. IRgendwie muss die Base aus in Schnittflächen "passen". Bitte erklär mir, was du mit "Übergehen" in diesem Zusammenhang meinst.

**Stellungnahme.**

**Klärung.** „Übergehen“ ist der Knopf *gemeinsam übergehen* (BEW-8), nicht das Fliegen über
fremde *Modelle*: Arbiter hält die Spinne an ihrer *Bewegungsweite* von 6″ an, am Tisch steht
sie aber 6,5″ weit; beide *Spieler* klicken „gemeinsam übergehen“, die Spinne steht bei 6,5″,
und das *Protokoll* hält es fest. Ebenso vor der *Nahkampfreichweite*.
Ohne Übergehen gilt Ihre Antwort schon: Auf einem fremden *Modell* losgelassen, schiebt
Arbiter die Spinne an die nächste freie *Stelle* innerhalb 6″ und außer *Nahkampfreichweite*
(BEW-18.2). Platz findet er immer, zumindest dort, wo sie vor dem Ziehen stand. Keinen gibt
es erst ab Etappe 7, wenn sie schon auf einem fremden *Modell* aufgestellt wurde (AUF-27.1)
und ringsum alles belegt ist; dann kann sie nicht bewegt werden (BEW-18.6, Anliegen 13020).
Mit Übergehen heißt Ihre Antwort: Bei 6,5″ steht ein Boy, Arbiter schiebt die Spinne zurück
auf höchstens 6″. Das Übergehen wirkt dann nicht, die *Karte* zeigt nicht, was am Tisch steht.
Umgesetzt nach Ihrer Antwort in [BEW-18.5](../../domaene/anforderungen/phasen/bewegung/fliegen.md);
das bisherige 18.4 (ohne 6″ und *Nahkampfreichweite*) ist gestrichen, seine Tests entfallen.

**F2 · Beachtet Arbiter nach dem Übergehen beim Schieben 6″ und die Nahkampfreichweite?**
A: Nein: Er schiebt sie an die nächste freie *Stelle*, auch über 6″ weit oder in *Nahkampfreichweite*; das *Protokoll* nennt, was dort regelwidrig ist (ArbiterMap, Anliegen 8840).
B: Ja, wie Ihre Antwort: nächste freie *Stelle* innerhalb 6″ und außer *Nahkampfreichweite*; der *Eintrag* im *Protokoll* bleibt, ohne *Grund* (Anliegen 13010).
Empfehlung: A, die *Spieler* haben bestätigt, dass die Spinne am Tisch weiter steht; B schiebt sie auf höchstens 6″ zurück, und die *Karte* weicht vom Tisch ab.
Annahme: BEW-18.5 bleibt nach B, Ihrer Antwort; bei A fasse ich es als neues Kriterium ohne 6″ und *Nahkampfreichweite*.
Antwort: Nein
Kommentar: Ich verstehe nicht, warum mir diese Frage gestellt wurde. Das war ja der Sinn von "übergehen", dass Bewegungsweite nicht beachtet wird. Die Nahkampfreichweite sollte durchausbeachtet werden, wenn die Phase dies erforderlich macht.
Stellungnahme: Ihre Antwort auf F1 verlangte beim Schieben *Bewegungsweite* und *Nahkampfreichweite*, auch nach dem Übergehen; damit hätte Arbiter das Übergehen zurückgenommen. Das lag an F1: Sie sagte nicht klar, dass die Spinne schon übergangen war. Statt Ihre Antwort still anders zu lesen, habe ich nachgefragt (Ich 1). Umgesetzt in [BEW-18.7](../../domaene/anforderungen/phasen/bewegung/fliegen.md): nach dem Übergehen ohne 6″, mit *Nahkampfreichweite*; BEW-18.5 ist gestrichen. Offen bleibt ein Fall, Runde 2.

## Runde 2
**Befund.** „Wenn die Phase es erforderlich macht“: In der *Bewegungsphase* verlangt es der
Regeltext immer, kein *Modell* darf in *Nahkampfreichweite* enden, auch mit *Fliegen*
(`core_rules.txt:745`, `:884`); nach einem Angriff muss es darin enden, das kommt mit einer
späteren Etappe (`core_rules.txt:1803`). Ungeklärt ist nur der Fall, in dem die *Spieler* gerade die
*Nahkampfreichweite* übergangen haben: Arbiter hielt die Spinne 1″ vor dem Warboss an, am Tisch
steht sie 0,5″ vor ihm, beide wählen *gemeinsam übergehen*. Liegt dieser Punkt zugleich auf der
*Base* eines Necron Warriors, schiebt Arbiter sie an die nächste freie *Stelle*.

**Kosten.** A: kein Kriterium mehr, BEW-18.8 entfällt. B: ein Kriterium (BEW-18.8), ein Test
erwartet die Spinne dann in *Nahkampfreichweite* statt außerhalb.

**Gegenvorschlag.**
**F3 · Beachtet Arbiter beim Schieben die Nahkampfreichweite auch, wenn die Spieler sie eben übergangen haben?**
A: Ja: Er schiebt die Spinne aus der *Nahkampfreichweite* des Warboss, also über 1″ von ihm weg; der *Eintrag* im *Protokoll* bleibt, ohne *Grund* ‚Nahkampfreichweite‘ (Regeltext, `core_rules.txt:884`).
B: Nein: Er schiebt sie nur vom Warrior herunter, sie bleibt in *Nahkampfreichweite*; das *Protokoll* nennt ‚Nahkampfreichweite‘ (Anliegen 13010 F2: Was übergangen ist, beachtet Arbiter nicht).
Empfehlung: B, wie Ihr „Nein“ zur *Bewegungsweite*: Mit A stünde die Spinne auf der *Karte* über 1″ vom Warboss, am Tisch 0,5″. Haben die *Spieler* nur die *Bewegungsweite* übergangen, beachtet Arbiter die *Nahkampfreichweite* in jedem Fall (BEW-18.7).
Annahme: BEW-18.8 steht nach B; bei A lösche ich es.
Antwort: Ja, wobei das eben auf die Phase bzw. die Bewegung ankommt. Die Endposition sollte idealerweise andere Regeln einhalten, selbst wenn Übergehen hier aus pragmatischen Gründen eine Spielregel übergeht. Das bedeutet eben nicht, dass andere Regeln aufgehoben werden müssen. In der Angriffsphase und beim Nachrücken in der Nahkampfphase, dürfen Modelle unter bestimmten Bedingungen die Nahkampfreichweite betreten..

**Stellungnahme.** Nachgeprüft, umgesetzt nach A: BEW-18.8 ist gestrichen. Nach dem Übergehen
schiebt Arbiter die Spinne in der *Bewegungsphase* an die nächste freie *Stelle* außer
*Nahkampfreichweite*, auch wenn die *Spieler* gerade diese übergangen haben
([BEW-18.7](../../domaene/anforderungen/phasen/bewegung/fliegen.md), gilt nur in der
*Bewegungsphase* nach 18.1). Ihr Hinweis zu Angriff und Nachrücken gehört zu Etappe 3
(Charge, Pile In, Consolidate): Dort enden *Modelle* nach dem Regeltext in
*Nahkampfreichweite* (`core_rules.txt:1803`, `:1985`); die Anforderungen dafür schreibe ich
mit Etappe 3, jetzt nichts.
