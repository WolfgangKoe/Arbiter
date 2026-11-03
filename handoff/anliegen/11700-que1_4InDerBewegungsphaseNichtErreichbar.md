# QUE-1.4 in der Bewegungsphase nicht erreichbar

Form: Kritik
Von: Testautor
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [QUE-1.4](../../domaene/anforderungen/querschnitt/setzen.md) verlangt: nach
einer *Sperre* nach QUE-1.2 bietet Arbiter *gemeinsam übergehen* nie an. Seit
[BEW-17.1](../../domaene/anforderungen/phasen/bewegung/anhaltenVorFremdenBases.md) gleitet
Arbiter in der *Bewegungsphase* vor jeder fremden *Base*, auch beim *gemeinsam übergehen*
([V18](../../technik/architektur/vertrag/schlacht/uebergehen.md)). Mit den Eingaben, die die
Seite schickt, entsteht dort keine *Sperre* nach QUE-1.2 mehr. Erreichbar ist sie nur mit
Eingaben, deren `zuvor` schon eine fremde *Base* *überdeckt*; die schickt die Seite nie.

**Kosten.** Ohne Antwort hat QUE-1.4 keinen Test, die Rückverfolgung bleibt rot.

**Gegenvorschlag.** A (Empfehlung): Test am Dienst mit V5, `zuvor` auf der *Base* eines Boys,
Ziel weiter als die *Bewegungsweite* auf der *Base* eines anderen Boys, so dass BEW-3.1
anhält und QUE-1.2 sperrt; geprüft: 409 mit ‚Base überdeckt‘, kein *Angebot*. Vorteil: prüft
das Kriterium mit den Eingaben des Vertrags. Nachteil: ein Fall, den die Seite nie erzeugt.
B: QUE-1.4 streichen, weil BEW-17.1 diese *Sperre* in der *Bewegungsphase* ausschließt.
Vorteil: kein Test für einen unerreichbaren Fall. Nachteil: Fällt das Gleiten (etwa beim
*Fliegen*), fehlt die Regel.

**Stellungnahme.** Angenommen: A, QUE-1.4 bleibt unverändert. Das Kriterium gilt in jeder
Phase, nicht nur in der *Bewegungsphase*. Das Ziel schließt das Übergehen überdeckter *Bases*
aus ([Ziel](../../domaene/ziel.md)), und von der Seite aus wird der Fall spätestens mit
[AUF-27](../../domaene/anforderungen/phasen/aufstellen/formationOhneFreieStelle.md) (Etappe 7)
erreichbar: Dort stehen *Modelle* schon überdeckt, wenn jemand sie zieht. Bis dahin prüft dein
Test am Dienst die Regel mit den Eingaben, die der Vertrag zulässt. In der Domäne ändert sich
nichts.
