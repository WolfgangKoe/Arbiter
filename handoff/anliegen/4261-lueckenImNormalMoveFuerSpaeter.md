# Lücken in Normal Move und Schlachtrunden für später

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Wartet (Ich 3: Lücken abseits des Happy Path, *Sperren*, die nur der Regeltext
verlangt, Namen). Damit sie nicht mit Anliegen 4220 verschwinden:
1. ‚keine Kohärenz‘ ist umgehbar: Wer statt *Bewegung der Einheit beenden* „Phase beenden“
   klickt oder ein *Modell* einer anderen eigenen *Einheit* zieht (BEW-1.1 macht sie zur
   *Einheit in Bewegung*), lässt die erste ohne *Kohärenz* stehen. Das Ziel nimmt genau diese
   *Sperre* vom Übergehen aus (`domaene/ziel.md`, `core_rules.txt:730`).
2. ‚schon bewegt‘: Nach *Bewegung der Einheit beenden* beginnt ein neuer *Normal Move* mit
   leerem *Weg*; damit läuft auch ‚weiter als M‘ ins Leere (`core_rules.txt:734`).
3. Ein *Modell* des anderen *Spielers* in der *Bewegungsphase* ziehen: BEW-1.1 regelt nur
   eigene, QUE-10.5 nur die übrigen *Phasen*.
4. „Phase beenden“ vor dem *ersten Zug* und nach dem Ende der *Schlacht*: QUE-10.2 sagt
   nicht, ob der Knopf dann da ist.
5. *Weg* ist jetzt ein Begriff im Glossar; AUF-8.7, 21.1, 26.1 und 29.1 sagen „Weg“ für die
   Strecke eines Zugs oder des Zeigers (Wir 2).
6. ArbiterMap zeigt bei der ausgewählten *Einheit*, wie weit sie gezogen ist
   (`ArbiterMap/frontend/static/js/model_selection.js:443`, „bewegt: x″“); in Arbiter sieht
   der *Spieler* sein *M* erst an der *Sperre*.

**Kosten.** Keine in Zyklus 8; der Happy Path aus Plan 8 läuft ohne sie. Bleiben sie
liegen, ist ‚keine Kohärenz‘ in einer echten Partie umgehbar.

**Gegenvorschlag.** 1 und 2 mit dem Zurücksetzen und der Wahl Normal Move, Advance oder
stehen bleiben im nächsten Zyklus von Etappe 2 (`core_rules.txt:734`); 3 und 4 je ein
Kriterium dort; 5 im Glossar oder in den AUF-Kriterien ein eigener Begriff; 6 als Frage an
den Stakeholder mit ArbiterMap als Quelle.

**Stellungnahme.**
Kommentar: Bitte auf die Umbenennung von "Normal Move" achten!
Stellungnahme: Beachtet: Die neuen Kriterien sagen *Normale Bewegung*, für Advance schlage ich
*Vorrücken* vor (Anliegen 7000). Zu den Punkten:
1 löst BEW-4.1 (siehe 5520 Punkt 5). 2 entfällt nach 7000 F1 A. 3:
[BEW-10.1](../../domaene/anforderungen/phasen/bewegung/fremdeModelle.md). 6: 7000 F3.
4 und 5 kommen mit dem Zurücksetzen; bis 7000 beantwortet ist, wartet das Anliegen.
Stellungnahme: 7000 ist beantwortet. 2 entfällt endgültig: Korrigieren bleibt, kein ‚schon
bewegt‘ (7000 F4 A); die *Bewegungsweite* hält Arbiter, weil die *Distanz* vom Beginn der
*Bewegungsphase* zählt (BEW-1.6). 4 jetzt doch gleich als
[QUE-11.1](../../domaene/anforderungen/querschnitt/phaseBeenden.md): „Phase beenden“ nur, wenn
ein *Spieler* *am Zug* ist; einplanen tut es der Planer. 5 entfällt: *Weg* ist kein Begriff des
Glossars mehr, „Weg“ in AUF-8.7, 21.1, 26.1, 29.1 ist gewöhnliches Wort. 6: Der Stakeholder hat
7000 F3 mit A beantwortet, die Anzeige an einer gezogenen *Einheit* kommt mit dem Zurücksetzen
und einem Mockup ([Plan 9](../plan.md), „Danach“).
