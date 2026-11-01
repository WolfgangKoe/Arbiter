# Base nicht überdecken: anhalten statt sperren

Form: Kritik
Von: Stakeholder
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Ihr Wortlaut:
„Die Funktion "Base überdeckt" finde ich so nicht gut. Die Base sollte nicht überdeckt werden können. ArbiterMap hat dies durch "Klemmen" gelöst. Das ist deutlich besser und intuitiver. Die Möglichkeit das zu übersteuern, macht es eher schlimmer als besser. Die Übersteuerung sollte ermöglicht werden, um die Position einer Einheit oder von die von Modellen korrigieren zu können, um den Gamestate auf dem Tisch herzustellen. Aber es ist sehr unwahrscheinlich, dass es jemals dazu kommt, dass Bases überdeckt werden können. Das ist noch nicht gut gelöst und das Zurückspringen an der Stelle ebenfalls nicht.“
Screenshot: rotes *Modell* über fremden *Bases*, „Base überdeckt“, „gemeinsam übergehen“.

**Kosten (Anforderungsautor).** Heute sperren QUE-1.2 und BEW-2.5 beim Loslassen, BEW-2.6 springt zurück, BEW-8 bietet *gemeinsam übergehen*. ArbiterMap hält beim Ziehen an und gleitet entlang (`interaction_map.md:401`), Arbiter nur in der *Aufstellung* (AUF-29). Etwa ein Item.

**Gegenvorschlag (Anforderungsautor).**
1. Keine *Base* *überdeckt* je eine fremde: Arbiter hält beim Ziehen davor an wie AUF-29, in jeder Phase, auch beim Übergehen (`core_rules.txt:729`, `:884`).
2. Übergehen heißt: eine Position auf den Stand am Tisch korrigieren, so über die *Bewegungsweite* hinaus (BEW-3), in *Nahkampfreichweite* (BEW-6.2) oder eine *aufgestellte* *Einheit*.
3. Wann was kommt, entscheidet der Planer.

**Stellungnahme.**
Kommentar: Eine Klärung zum Begriff "übergehbar". Bezieht sich das nur auf das Überdecken von Bases? Denn das sollte niemals passieren. Wenn es darum geht, dass ein Modell mal weiter als Bewegungsweite gezogen werden können soll, oder eine Einheit verschoben werden soll, deren Aufstellung bereits abgeschlossen ist oder auf dem Tisch ist eine Einheit in Angriffsreichweite, in der App ist das aber nicht so. In allen diesen Fällen sollte die Position einer Einheit oder eines Modells verändert im Sinne von "übergehen" werden können, um den Status auf dem Tisch nachzubilden. Dennoch sollten sich Bases selbst in diesen Fällen nicht überdecken können. Bei Fähigkeiten wie "Fliegen" sollte eine Einheit Bases anderer Einheiten bei der Bewegung ignorieren können. Beim Loslassen darf die Bases aber dennoch nicht auf anderen Bases stehen bleiben. Man darf es dann nur darüber hinwegziehen. Vielleicht sind hier die Anforderungen am Anfang nicht klar gewesen, aber bevor hier etwas umgesetzt wird, bitte nochmal genau mit mir klären.
Stellungnahme: Gegenvorschlag 1 und 2 nach Ihrem Kommentar.

**F1 · Gegenvorschlag 1 und 2?** A Ja, Satz in `ziel.md` (Ihr Kommentar) · empfohlen; B Nein (neu)
Antwort: Ja

**F2 · Übergehen?** A *gemeinsam übergehen* nach dem Loslassen (QUE-5) · empfohlen; B Schalter „korrigieren“ (ArbiterMap)
Antwort: .

**F3 · Entlanggleiten?** A Ja (ArbiterMap) · empfohlen; B Nein (Anliegen 2363)
Antwort: Ja

**F4 · „Fliegen“: *Modell* über fremder *Base* losgelassen?** Hinwegziehen ja, darauf enden nein (`core_rules.txt:884`).
- A: *setzt* an die nächste *Stelle* ohne Überdeckung (ArbiterMap `interaction_map.md:675`) · empfohlen: kein Zurückspringen
- B: *setzt* an die letzte freie *Stelle* des Weges (neu)

Antwort: A
Kommentar: Ich folge bei Fragen F2 und F3 deiner Empfhelung. Du nutzt hier kein A,B und C, daher ist es etwas schwierig, einfach deine Fragen zu beantworten.
Stellungnahme: F1 bis F3 gelten als A; ab jetzt steht vor jeder Antwortmöglichkeit ein Buchstabe. Offen ist F4 (A oder B), dann schreibe ich um und stelle das Anliegen an den Planer. Ihr Schritt aus F1 (`domaene/ziel.md` ändern nur Sie): den letzten Satz dort ersetzen durch „Ausnahmen: ‚keine Kohärenz‘ und überdeckte Bases können nicht übergangen werden.“
Stellungnahme: Umgesetzt: BEW-17, BEW-8, AUF-31, QUE-1.4, BEW-18, Glossar; BEW-2 fort. Offen: 9270, Plan: 9271.
