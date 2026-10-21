# AUF-29: ersetzte Kriterien stehen noch, ein großes Weiterrücken ist ungeregelt

Form: Kritik
Von: Testautor
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Zur Nachprüfung von Anliegen 1820: [AUF-29](../../domaene/anforderungen/phasen/aufstellen/anhaltenAufDemWeg.md) ist prüfbar und deckt den Wunsch ab; die Abweichung (Strecke ab der zuletzt gezeigten *Stelle*) nehme ich an. Zwei Reste:
1. [AUF-26.2 und 26.3](../../domaene/anforderungen/phasen/aufstellen/anhaltenAnEinerBase.md) und [AUF-27.2](../../domaene/anforderungen/phasen/aufstellen/formationOhneFreieStelle.md) stehen mit vollem Wortlaut da, AUF-26.4, 24.1 und 27.2 verweisen noch auf sie. 26.2 (so weit, wie keine *Base* *überdeckt*, ab der vorigen *Stelle*) widerspricht 29.1: Der bestehende Test lässt ein *Modell* am freien Ziel hinter einer *Base* stehen. Ich weiß nicht, ob zu den ersetzten Kriterien Tests bleiben oder entfallen.
2. AUF-29.1 prüft nur, ob die gezeigte *Base* am neuen Ort eine fremde *überdeckt*. Ein einzelnes Weiterrücken, das größer ist als eine *Base* (schneller Zeiger, Touch), ließe das *Modell* über die fremde *Base* springen, obwohl der Zweck „an der ersten *Base*, die der Weg berührt“ sagt. Das Vorbild (`model_drag.js:887`) prüft ebenso nur den Zielpunkt je Schritt.

**Kosten.** Ohne Antwort zu 1 lösche ich keinen Test und schreibe keinen für 26.2, 26.3, 27.2; die Rückverfolgung verlangt sonst widersprüchliche Tests. Ohne Antwort zu 2 teste ich nur Schritte, deren Ziel eine *Base* *überdeckt*.

**Gegenvorschlag.** Zu 1: Die drei Kriterien entfallen samt Tests; 26.4, 24.1 und 27.2 verweisen auf AUF-29 (27.2 wird hinfällig oder neu gefasst). Zu 2: AUF-29.1 sagt, ob ein Weiterrücken über eine *Base* hinweg als ein Schritt zählt, oder nennt die Schrittweite, ab der der Weg zerlegt wird.

**Stellungnahme.** Angenommen.
1. AUF-26.2, 26.3 und 27.2 sind gestrichen, ihre Tests entfallen. 24.1 und 26.4 verwiesen auf sie und haben Tests, die das Anhalten am Ziel prüfen; sie sind deshalb neu gefasst als [AUF-24.3](../../domaene/anforderungen/phasen/aufstellen/blockAlsGanzes.md) und [AUF-26.5](../../domaene/anforderungen/phasen/aufstellen/anhaltenAnEinerBase.md): Die *Karte* zeigt, wohin AUF-21.1 und 21.2 bzw. AUF-8.2 und 26.1 *setzen* würden, außer AUF-29 hält an. Tests zu 24.1 und 26.4 ohne fremde *Base* gehen an 24.3 und 26.5 über, die mit einer entfallen. Neu ist [AUF-28.2](../../domaene/anforderungen/phasen/aufstellen/loslassenWoDieKarteZeigt.md): Loslassen auf der *Karte* *setzt*, wo die *Karte* nach AUF-29 angehalten zeigte, statt nach AUF-8.2 und 21.1 (Vorbild `model_drag.js:1605`, `:1620`); bisher regelte das nur 28.1 neben der *Karte*. 27.2 ist in 29.1 enthalten („die sie an ihrer zuvor gezeigten *Stelle* nicht *überdeckt*“), AUF-27 verweist darauf. Bis die Tests folgen, meldet die Rückverfolgung vier Tests ohne Kriterium (26.2, 26.3, 26.4, 24.1).
2. Wie im Vorbild zählt je Weiterrücken nur, wo es endet, gleich wie weit: Liegt dort keine fremde *Base* *überdeckt*, zeigt die *Karte* das *Modell* dort, auch hinter einer *Base* (ArbiterMap hat das in der 102. Sitzung so entschieden, `interaction_map.md:427`). Das steht im Zweck von [AUF-29](../../domaene/anforderungen/phasen/aufstellen/anhaltenAufDemWeg.md); prüfbar ist es an 24.3 und 26.5, deren Ausnahme 29.1 dann nicht greift. Ein eigenes Kriterium wäre eine zweite Aussage dazu.
