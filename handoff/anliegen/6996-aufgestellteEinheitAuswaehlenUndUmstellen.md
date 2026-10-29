# Aufgestellte Einheit in der Aufstellung auswählen und umstellen

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Der Stakeholder hat in Anliegen 5181 F2 B gewählt: In der *Aufstellung* wählt ein
Klick auf ein *Modell* einer *aufgestellten* *Einheit* sie aus, die *Karte* kennzeichnet ihre
*Modelle*. Ziehen sperrt ‚nicht wählbar‘; die *Spieler* können *gemeinsam übergehen*, dann
steht sie, wo losgelassen, die eigene *Aufstellungszone* hält sie fest (AUF-26), und das
*Protokoll* nennt es. *zurücklegen* geht nicht (AUF-23.4). Anlass: Er will eine *aufgestellte*
*Einheit* beiseiteschieben können, damit die *Einheit in Aufstellung* Platz hat; der Regeltext
kennt kein Umstellen (`core_rules.txt:2322`), darum der Weg über die *Sperre* (Ziel). Bis dahin
gilt die Annahme aus 5181: Der Klick wählt sie aus, Ziehen bleibt gesperrt ohne Übergehen.
Danach sind veraltet oder offen:
1. [AUF-20.6](../../domaene/anforderungen/phasen/aufstellen/ebene.md) gilt wörtlich, auch für
   eine *aufgestellte* *Einheit*; der Code wählt sie heute nicht (`modellAnklicken`,
   [6300](6300-anklickenUndFremdesModellLoslassen.md) Punkt 1). Ob die *Einheit in Aufstellung* und
   *an der Reihe* dabei gleich bleiben, sagt nur AUF-5.8, und das für die *Armeeliste*.
2. [AUF-12.6](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md) bietet
   *gemeinsam übergehen* bei ‚nicht wählbar‘ nicht an;
   [AUF-21.1](../../domaene/anforderungen/phasen/aufstellen/einheitVerschieben.md) verschiebt
   nur die *Einheit in Aufstellung*.

**Kosten.** Ohne 1 widerspricht der Code AUF-20.6, und der Mutant aus 6300 bleibt ohne Test.
2 sind zwei, drei Kriterien mit Tests und setzen QUE-5 voraus.

**Gegenvorschlag.**
1. In der Domänenphase 9, mit 6300 Punkt 1: ein Kriterium, dass der Klick nach AUF-20.6 auch
   eine *aufgestellte* *Einheit* wählt, und was dabei gleich bleibt (wie AUF-5.8). Den
   Vertrag V3 ([Aufstellen](../../technik/architektur/vertrag/aufstellen.md)) ziehe ich in der
   Technikphase 9 nach.
2. Das Übergehen beim Ziehen einer *aufgestellten* *Einheit* nach
   [Etappe 7](../../domaene/etappen/07-ansichtenAusArbiterOld.md), zu den Randfällen des
   Aufstellens (Anliegen 2361 F2): AUF-12.6 und AUF-21.1 erweitern; ein *Modell*, nach dem die
   *Einheit* nicht in *Kohärenz* ist, springt zurück, ‚keine Kohärenz‘ ist nie zu übergehen
   (QUE-5.5).

**Stellungnahme.** 1 umgesetzt als
[AUF-30.1](../../domaene/anforderungen/phasen/aufstellen/aufgestellteEinheitAuswaehlen.md)
(eigene Datei, `ebene.md` hat keinen Platz mehr): In der *Aufstellung* wählt der Klick eine
*aufgestellte* *Einheit* mit der ganzen *Einheit* als *Ebene*, *an der Reihe*, *Einheit in
Aufstellung* und *Modelle* bleiben gleich, wie AUF-5.8. Zugleich Antwort auf 6300 Punkt 1.
2 angenommen: Die Kriterien zum Ziehen und Übergehen einer *aufgestellten* *Einheit* schreibe
ich mit den Randfällen des Aufstellens; dass das Item sie mitnimmt, habe ich dem Planer in
Anliegen 7011 geschrieben.
