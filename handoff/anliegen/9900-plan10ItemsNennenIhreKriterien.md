# Plan 10: Items nennen ihre Kriterien, Plan nach dem Stand

Form: Kritik
Von: Fachkritiker
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik am Plan (Domänenphase 7), hält auf: Für Schritt 3 des Happy Path fehlt nach
der Freigabe der Test.
1. [loslassenNebenDerKarte](../../domaene/items/loslassenNebenDerKarte.md) nennt „das Kriterium
   aus Anliegen 8480 (*Bewegungsphase*)“, nicht BEW-20.1;
   [anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md) nennt „(BEW-1.5)“, gemeint ist
   aber [BEW-21.1](../../domaene/anforderungen/phasen/bewegung/sperreBeimLoslassen.md); BEW-1.5
   hat schon Tests. Die Rückverfolgung verlangt nur Tests zu Kriterien, deren Kennung ein Item
   nennt (`kriterienregeln/rueckverfolgung.py`, `nennt`), und ein Item führt im Umfang
   Kriterien-IDs (`domaene/CLAUDE.md`). So bliebe BEW-20.1 ohne Test, gerade der Fall aus
   Schritt 3 in der *Bewegungsphase*, ebenso BEW-21.1.
2. Der Plan steht vor dem Stand: QUE-5.6 (8972), BEW-20.1 (8480) und BEW-21.1 (9421) sind
   geschrieben, 8972 und 9421 erledigt, 9760 F1 beantwortet. Die Empfehlung sagt dir dennoch,
   der Anforderungsautor schreibe sie erst, und „bis dahin sind die Items nicht bereit“;
   „Offene Anliegen“ führt 8972 und 9421, die Items nennen sie als Abhängigkeit. Offen ist nur
   noch 8480 (Nachprüfung von 9760 durch den Anforderungsautor). Du entschiedest über die
   Freigabe auf falscher Grundlage (Absicht 4).
3. Schritt 3 verspricht „auch beim Aufstellen“ ohne Einschränkung. Für ein *Modell* einer schon
   *aufgestellten* *Einheit* gilt dort aber AUF-16.8 (zurück, kein *Grund*), das Item 2 selbst
   baut; nur die *Einheit in Aufstellung* bleibt stehen (AUF-28.1). Du sähest am Bildschirm das
   Gegenteil des Schritts.

**Kosten.** Je Item eine Zeile, im Plan drei Sätze. Sonst ist Item 2 fertig, ohne dass das
Loslassen neben der *Karte* in der *Bewegungsphase* getestet ist, und du prüfst Schritt 3
gegen ein Versprechen, das die Kriterien nicht geben.

**Gegenvorschlag.** Umfang Item 2: „… AUF-12.8, BEW-20.1“; Item 3: „… QUE-1.4, BEW-21.1“;
Item 1 besser „QUE-5.6“ statt „das Kriterium aus Anliegen 8972“. Abhängigkeiten: 8972 und 9421
streichen, Item 2 behält 8480. Empfehlung und „Offene Anliegen“ nach dem Stand: nur noch 8480.
Schritt 3: „… steht es, wo die *Karte* es zuletzt zeigte, beim Aufstellen für die *Einheit in
Aufstellung*.“

**Stellungnahme.** Umgesetzt wie vorgeschlagen:
1. [loslassenNebenDerKarte](../../domaene/items/loslassenNebenDerKarte.md) nennt BEW-20.1 (ohne
   AUF-8.7, das schon Tests hat, 9880), behält 8480;
   [anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md) nennt BEW-21.1 statt
   „(BEW-1.5)“; [anhaltenUebergehen](../../domaene/items/anhaltenUebergehen.md) nennt QUE-5.6.
   8972 und 9421 sind aus den Abhängigkeiten gestrichen.
2. [Plan](../plan.md): Empfehlung und „Offene Anliegen“ nach dem Stand: 8480 (Nachprüfung
   von 9760), dazu die Frage 9941 aus 9881; 7642, 8601 und 9400 sind erledigt und
   gestrichen.
3. Schritt 3: „… steht es, wo die *Karte* es zuletzt zeigte, beim Aufstellen für die *Einheit
   in Aufstellung*.“

**Nachprüfung.** In Ordnung. Die Items nennen BEW-20.1, BEW-21.1 und QUE-5.6, die
Abhängigkeiten nur noch 8480; Empfehlung und „Offene Anliegen“ im Plan nennen 8480 und 9941,
Schritt 3 hat die Einschränkung auf die *Einheit in Aufstellung*.
