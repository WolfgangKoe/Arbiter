# Formation schräg und Kohärenz ohne Gegenfall

387 · Fragen · von Testautor (Technik) → Anforderungsautor (Domäne) · Runde 1/3 · erledigt

## Runde 1
**Befund.**
1. Glossar *Formation*: Benachbarte *Bases* haben den *Abstand* 1,5″, „auch schräg“. Bei Reihen von 3, 4, 3 mit halbem Versatz ist der Reihenabstand ein Vielfaches von √3, nicht rational; die Architektur (S2) rechnet exakt ohne Wurzel. Wie genau gilt 1,5″ schräg?
2. QUE-4 nennt nur, wann eine *Einheit* nicht in *Kohärenz* ist (4.2 bis 4.4) und dass höchstens ein *gesetztes* *Modell* sie hält (4.1). Wann sie in *Kohärenz* ist, steht nicht da; ein Code, der ab zwei *Modellen* immer „nicht“ sagt, besteht alle Tests.

**Kosten.** 1: Ich prüfe 1,5″ nur zwischen *Modellen* derselben Reihe, schräg kein Test. 2: Es gibt keinen Test, der eine *Einheit* in *Kohärenz* verlangt außer 4.1 und dem Beenden in AUF-10.1.

**Gegenvorschlag.** 1: Toleranz oder ein Satz, der die schrägen Paare bestimmt. 2: ein Kriterium „Gegeben keiner der Fälle 4.2 bis 4.4, dann in *Kohärenz*“.

**Stellungnahme.**
1. Angenommen als Satz, ohne Toleranz. Entschieden hat das der Stakeholder in Anliegen 377 F1 A
   (git): Der Abstand der Reihen wird auf 1/100″ aufgerundet. Bisher stand das nur dort. Jetzt
   steht es in [formation.yaml](../../domaene/daten/formation.yaml): *Bases* einer Reihe haben
   genau `abstand`. Die Mittelpunkte benachbarter Reihen liegen um das kleinste Vielfache von
   1/100″ auseinander, bei dem jede *Base* zu jeder *Base* der Nachbarreihe mindestens
   `abstand` hat. Das [Glossar](../../domaene/glossar.md) (*Formation*) nennt das Prinzip
   und verweist auf die Datei. Ein Test prüft exakt im Quadrat: schräg mindestens 1,5″, und
   bei Reihen, die 1/100″ enger stehen, hätte ein Paar weniger. Bei 32 mm sind das 2,40″
   Abstand der Reihen und schräg etwa 1,509″.
2. Angenommen: [QUE-4.5](../../domaene/anforderungen/querschnitt/kohaerenz.md) „Gegeben eine
   *Einheit*, auf die keiner der Fälle QUE-4.2 bis 4.4 zutrifft, dann ist sie in *Kohärenz*“
   (`core_rules.txt:434`). Das Item [Beenden mit Kohärenz](../../domaene/items/beendenUndSperreOhneStelle.md)
   umfasst ganz QUE-4, also auch 4.5. Damit es unter 1.200 Zeichen bleibt, ist die Zeile
   „Am Bildschirm“ weggefallen, denn *Kohärenz* ist ein Zustand und keine Handlung. Der Zweck
   ist kürzer, sagt aber dasselbe.

**Nachprüfung.** Beide Antworten tragen. Zu 1 prüft `testAuf8_5SchrägBenachbarteBasesHabenMindestensEinsKommaFünfZollBeiReihenAufEinHundertstelGenau` in `ziehenTest.py` je Nachbarreihen: kein Paar unter 1,5″, mindestens ein Paar höchstens 1/100″ darüber, Reihenabstand ein Vielfaches von 1/100″. Zu 2 prüft `testQue4_5…` in `kohaerenzTest.py` fünf Fälle in Kohärenz, darunter Gruppen im Abstand von genau 2″. Erledigt.
