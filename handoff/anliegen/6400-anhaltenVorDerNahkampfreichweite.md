# Anhalten vor der Nahkampfreichweite statt Zurücksetzen

Form: Auftrag
Von: Stakeholder
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 9

## Runde 1
**Befund.** Wortlaut des Stakeholders:
„Ich habe auch geprüft, ob die Nahkampfreichweite berücksichtigt wird. Das funktioniert gut.
Hierbei sollte die Einheit oder das Modell am besten an der Grenze, wo die
Nahkampfreichweite beginnt, stehen bleiben können. Dass es auf die ursprüngliche Position
zurückgesetzt wird, ist hier nicht intuitiv und wird bestimmt stören.“

Festgehalten vom Anforderungsautor. Stand heute: In der *Bewegungsphase* sperrt
[QUE-1.3](../../domaene/anforderungen/querschnitt/setzen.md) ‚Nahkampfreichweite‘, danach
steht jedes *Modell*, wo es vor dem Ziehen war
([BEW-2.6](../../domaene/anforderungen/phasen/bewegung/sperrenBeimZiehen.md)). Regeltext:
„no model can be moved within Engagement Range of enemy models“ (`core_rules.txt:745`).
Vorbilder für Anhalten statt Sperren:
[BEW-3](../../domaene/anforderungen/phasen/bewegung/anhaltenAnDerBewegungsweite.md)
(*Bewegungsweite*) und [AUF-29](../../domaene/anforderungen/phasen/aufstellen/anhaltenAufDemWeg.md)
(fremde *Base*). Verwandt: Anliegen 6241 Punkt 1 (Test zu QUE-1.3 in der *Bewegungsphase*),
6240 (Abwählen in der *Schlacht*).

**Kosten.** Bleibt es, zieht der Spieler ein *Modell* oder eine *Einheit* nach jeder *Sperre*
von der ursprünglichen *Stelle* erneut und schätzt die Grenze selbst.

**Gegenvorschlag.** In der Domänenphase 9 ein Kriterium wie BEW-3: Würde ein gezogenes
*Modell* in *Nahkampfreichweite* eines *Modells* des anderen *Spielers* *gesetzt*, hält
Arbiter die gezogenen *Modelle* (*Modell* oder ganze *Einheit* als *Ebene*) dort an, wo sie
gerade noch außerhalb sind, statt zu sperren; was Regeltext und Vorbilder offenlassen, als
Frage an den Stakeholder.

**Stellungnahme.**
