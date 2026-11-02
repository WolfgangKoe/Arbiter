# Übergehen der Bewegungsweite führt ohne Eintrag in die Nahkampfreichweite

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik am Plan 10, Item anhaltenUebergehen, wartet (Randfall abseits des Happy
Path, *Sperre*, die nur der Regeltext verlangt). Zieht jemand einen Boy über seine
*Bewegungsweite* hinaus bis in die *Nahkampfreichweite* eines Gegners, hält BEW-3.1 ihn an der
*Bewegungsweite* an; BEW-6.2 greift nicht, es prüft nur die Strecke nach BEW-3.1
([anhaltenVorDerGrenze](../../domaene/anforderungen/phasen/bewegung/anhaltenVorDerGrenze.md)).
Übergehen die *Spieler*, *setzt*
[BEW-8.4](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md) ihn ohne 3.1
und 6.2, also in die *Nahkampfreichweite*, und QUE-1.3 sperrt nicht. Der *Eintrag* nennt nach
BEW-8.5 nur ‚Bewegungsweite‘. Übergangen ist aber auch die *Nahkampfreichweite*
(`core_rules.txt:745`: „no model can be moved within Engagement Range“), und das *Protokoll*
verschweigt es; das Ziel verlangt, dass ein Übergehen protokolliert wird.

**Kosten.** Ein Satz in BEW-8.5 oder ein neues Kriterium, dazu ein Test. Da BEW-8.5 in
Technikphase 10 Tests bekommt, kostet es später einen geänderten Test; jetzt mitgeschrieben
nichts davon. Ohne: Ein Boy steht nach dem Übergehen im Nahkampf, das *Protokoll* nennt nur die
*Bewegungsweite*.

**Gegenvorschlag.** BEW-8.5 ergänzen (oder neues Kriterium, falls schon getestet): Der *Eintrag*
nennt zusätzlich ‚Nahkampfreichweite‘, wenn ein nach BEW-8.4 *gesetztes* *Modell* in
*Nahkampfreichweite* eines *Modells* des anderen *Spielers* steht. Kein neuer *Grund*, keine
Frage nötig.

**Stellungnahme.**

**Nachprüfung.** In Ordnung, abgedeckt durch
[BEW-8.5](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md): Der *Eintrag*
nennt ‚Nahkampfreichweite‘, wenn BEW-6.2 ohne 3.1 eines angehalten hätte, also auch beim Boy,
den 3.1 vor der *Nahkampfreichweite* anhielt. BEW-8.5 hat noch keinen Test, also keine
Folgekosten.
