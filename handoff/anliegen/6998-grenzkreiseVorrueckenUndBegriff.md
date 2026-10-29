# Grenzkreise: Ring beim Vorrücken und neuer Begriff

Form: Fragen
Von: Anforderungsautor
An: Stakeholder
Runde: 2/3
Status: offen

## Runde 1
**Befund.** Deinen Wunsch aus [Anliegen 6410](6410-grenzkreiseNahkampfUndBewegung.md) beschreibt
neu [BEW-11](../../domaene/anforderungen/phasen/bewegung/grenzkreise.md): Ist in der
*Bewegungsphase* eine *Einheit* des *Spielers* *am Zug* *ausgewählt*, zeigt die *Karte* um jedes
ihrer *Modelle* einen Kreis, bis wohin seine *Base* ziehen kann, und um jedes *Modell* des
anderen *Spielers* einen Kreis 1″ um seine *Base*, die *Nahkampfreichweite*. An einer Stelle
weiche ich vom Vorbild ab.

Neuer Begriff, Freigabe mit Plan 9: *Grenzkreis* (kein Regelbegriff), ein leicht gezeigter
Kreis, der eine Grenze für eine *Base* zeigt ([Glossar](../../domaene/glossar.md)).

**Kosten.** Ohne Antwort zeichnet Ux das Mockup und baut Plan 9 nach der Annahme unten.

**Gegenvorschlag.** Antworten; „.“ heißt, die Empfehlung gilt.

**F1 · Welche Kreise zeigt Arbiter beim Vorrücken?** ArbiterMap zeichnet zum Kreis der
*Bewegungsweite* alle sechs möglichen Ringe +1″ bis +6″ vor, weil man dort den Wurf nicht
eingibt (`ArbiterMap/docs/spec/interaction_map.md:550`). Bei uns wählst du den *Vorrückwurf*
vorher ([BEW-5](../../domaene/anforderungen/phasen/bewegung/vorruecken.md)), und Arbiter hält
das *Modell* genau dort an.
A: Vor der Wahl nur der Kreis der *Bewegungsweite*; nach der Wahl statt seiner einer,
um den *Vorrückwurf* größer (BEW-11.2). Je *Modell* ein Kreis, auch bei 20 Boyz lesbar.
B: Wie ArbiterMap: solange *Vorrücken* angeboten ist, zusätzlich die sechs Ringe, damit
man vor dem Würfeln sieht, was jeder Wurf bringt. Sieben Kreise je *Modell*, bei großen
*Einheiten* unübersichtlich; ein weiteres Kriterium.
Empfehlung: A; der gewählte Wurf legt die Grenze fest, die sechs Ringe zeigen dann nichts mehr.
Annahme: A.
Antwort: Ich würde es so machen, dass alle 6 Kreise angezeigt werden. Dann klickt oder tippt man auf einen der Kreise, womit dann implizit der Wert des Wurfs "eingegeben" ist. Diese Eingabe muss zur Korrektur zurückgenommen werden können (ähnlich wie beim Aufstellen von Einheiten), falls man sich verklickt hat. Ist das verständlich?

**Stellungnahme.**

## Runde 2
**Befund.** Ja, verständlich; zusammen mit deinen Kommentaren in 6410 und 7000 steht es so da:
Du *wählst* eine *Einheit* *aus*, die *Karte* zeigt die *Einhüllende* ihrer *Grenzkreise*
([BEW-11.5](../../domaene/anforderungen/phasen/bewegung/grenzkreise.md)), bei einem einzelnen
*Modell* als *Ebene* nur dessen *Grenzkreis* (11.1). Ein Knopf „Vorrücken“
([BEW-5](../../domaene/anforderungen/phasen/bewegung/vorruecken.md)), dann sechs weitere Kreise
+1″ bis +6″; ein Klick auf einen ist der *Vorrückwurf*
([BEW-13](../../domaene/anforderungen/phasen/bewegung/grenzkreiseBeimVorruecken.md)), danach
stehen zwei: *Bewegungsweite* und *Bewegungsweite* plus Wurf. „Vorrücken zurücknehmen“
([BEW-12](../../domaene/anforderungen/phasen/bewegung/vorrueckenZuruecknehmen.md)) macht es
rückgängig, auch nach einem Verklicken; dann wieder „Vorrücken“. Zwei Stellen sagst du nicht.

Neuer Begriff, Freigabe mit Plan 9: *Einhüllende* (dein Wort, kein Regelbegriff), Rand der
Fläche, die mehrere *Grenzkreise* zusammen bedecken ([Glossar](../../domaene/glossar.md)).
Folge für den Plan: Vorrücken braucht jetzt die Kreise; das klärt der Planer (Anliegen 6999).

**Kosten.** Ohne Antwort gelten die Annahmen; F2 B kostet ein Kriterium mehr.

**Gegenvorschlag.** Antworten; „.“ heißt, die Empfehlung gilt.

**F2 · Wo stehen die Modelle nach „Vorrücken zurücknehmen“?** A: Wo sie zu Beginn der
*Bewegungsphase* standen, wie „Einheit zurücklegen“ die *Einheit* von der *Karte* nimmt (AUF-23,
dein „ähnlich wie beim Aufstellen“). B: Sie bleiben stehen; wer weiter als seine
*Bewegungsweite* steht, hält beim nächsten Ziehen dort an (neu). Empfehlung: A. Meist nimmst du
gleich nach dem Verklicken zurück, bevor jemand zieht; B ließe ein *Modell* regelwidrig stehen,
ohne dass Arbiter es sperrt.
Annahme: A (BEW-12.2).
Antwort: .

**F3 · Nahkampfreichweite des Gegners: je Einheit eine Einhüllende?** A: Ja, je *Einheit* des
anderen *Spielers* eine (dein Grundsatz aus 6410 Punkt 2). B: Je *Modell* ein Kreis wie bisher
(ArbiterMap `interaction_map.md:532`). Empfehlung: A; bei 10 Necron Warriors sonst zehn Kreise.
Annahme: A (BEW-11.3).
Antwort: .

**Stellungnahme.**
