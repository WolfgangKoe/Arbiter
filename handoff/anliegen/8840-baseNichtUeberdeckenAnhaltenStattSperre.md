# Base nicht überdecken: anhalten statt sperren

Form: Kritik
Von: Stakeholder
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 10

## Runde 1
**Befund.** Wortlaut des Stakeholders:
„Die Funktion "Base überdeckt" finde ich so nicht gut. Die Base sollte nicht überdeckt werden können. ArbiterMap hat dies durch "Klemmen" gelöst. Das ist deutlich besser und intuitiver. Die Möglichkeit das zu übersteuern, macht es eher schlimmer als besser. Die Übersteuerung sollte ermöglicht werden, um die Position einer Einheit oder von die von Modellen korrigieren zu können, um den Gamestate auf dem Tisch herzustellen. Aber es ist sehr unwahrscheinlich, dass es jemals dazu kommt, dass Bases überdeckt werden können. Das ist noch nicht gut gelöst und das Zurückspringen an der Stelle ebenfalls nicht.“
Screenshot: *Bewegungsphase*, ein rotes *Modell* über anderen *Bases*, Meldung „Base überdeckt / über eine Base“, Knopf „gemeinsam übergehen“.

**Kosten (Anforderungsautor).** Heute zeigt die *Karte* beim Ziehen das *Modell* auch über fremden *Bases*; beim Loslassen sperren [QUE-1.2](../../domaene/anforderungen/querschnitt/setzen.md) und [BEW-2.5](../../domaene/anforderungen/phasen/bewegung/sperrenBeimZiehen.md), BEW-2.6 stellt alles zurück (das Zurückspringen), [BEW-8](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md) bietet *gemeinsam übergehen* an.
ArbiterMap hält schon beim Ziehen an der ersten fremden *Base* an und gleitet an ihr entlang (`ArbiterMap/docs/spec/interaction_map.md:401`, `:407`). Arbiter hat das als [AUF-29](../../domaene/anforderungen/phasen/aufstellen/anhaltenAufDemWeg.md) nur für die *Aufstellung*, Gleiten erst in Etappe 3 (Anliegen 2363); Kante und *Nahkampfreichweite* hält [BEW-6](../../domaene/anforderungen/phasen/bewegung/anhaltenVorDerGrenze.md) schon an (Anliegen 6400).
Aufwand etwa ein Item wie anhaltenUndAuswahl: drei bis vier neue Kriterien mit Tests, die zu BEW-2 und BEW-8 entfallen; Anhalten ist für die *Aufstellung* gebaut, Gleiten noch nirgends. Folge: In der *Bewegungsphase* bleibt nur die *Sperre* ‚keine Kohärenz‘, nichts zu übergehen.

**Gegenvorschlag (Anforderungsautor).**
1. In der *Bewegungsphase* hält Arbiter vor jeder fremden *Base* an wie AUF-29.1 bis 29.3, schon beim Ziehen; Loslassen *setzt*, wo die *Karte* zeigt. Keine *Sperre*, kein Übergehen, kein Zurückspringen, wie BEW-6.
2. BEW-2.5 bis 2.8 und BEW-8 entfallen, QUE-1.2 gilt nicht in BEW-1.5.
3. Die Bedingung von Etappe 2 („sperrt über fremde Bases“, „Jede Sperre … gemeinsam übergehen“) gehört dem Planer; nach Ihrer Antwort geht ein Anliegen an ihn.

**Stellungnahme.**

Annahme: Bis zur Antwort ändere ich nichts; in der Domänenphase 10 gelten die Empfehlungen.

**F1 · Was kommt in Etappe 2?**
- Anhalten und Entlanggleiten in der *Bewegungsphase* (ArbiterMap) · empfohlen: ohne Gleiten bleibt das *Modell* an der ersten *Base* hängen
- Nur Anhalten an der ersten fremden *Base* wie AUF-29.1, Gleiten in Etappe 3 (Anliegen 2363)
- *Sperre* wie heute bis Etappe 3 (Anliegen 2363)

Antwort: .

**F2 · Anhalten an *Bewegungsweite* oder vor *Nahkampfreichweite* übergehbar machen?** Ich lese: Übergehen dient dem Korrigieren auf den Stand am Tisch; BEW-3 und 6.2 halten heute ohne Übergehen an.
- Nein, die *Karte* bildet den Spielstand ab, nicht den exakten Tisch; BEW-1.6 lässt nachziehen (Ziel, Anliegen 5180 F6 A, 6400) · empfohlen
- Ja, nach dem Loslassen dort bietet Arbiter *gemeinsam übergehen* an und *setzt*, wo losgelassen wurde, mit *Eintrag* im *Protokoll* (neu; Grund: Ihr Wortlaut, Ziel „einvernehmlich übergehen“)

Antwort: .

**F3 · ‚Base überdeckt‘ auch in der *Aufstellung* nicht mehr übergehbar?**
- Nein, dort hält AUF-29.1 schon an, das Übergehen bleibt wie freigegeben (Anliegen 2361 F1 A) · empfohlen
- Ja, nirgends übergehbar; dazu ergänzen Sie im letzten Satz von `domaene/ziel.md` die Ausnahme um ‚Base überdeckt‘ (Ihr Wortlaut)

Antwort: .
