# Bewegungsphase: Antworten und Lücken für später

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 9

## Runde 1
**Befund.** Wartet (Ich 3: Lücken abseits des Happy Path). Schritt 3 nach
[5180](5180-annahmenZurBewegungsphase.md) F7 A ist ganz abgedeckt: BEW-1.5, 1.6, 1.7,
BEW-3.1, BEW-2.5 bis 2.7, BEW-4.1; nichts hält auf.
1. Zwei Antworten aus 5180 stehen in keiner Anforderung und keinem Anliegen; 5180 ist
   `erledigt` und wird gelöscht. F1: eine Markierung, wie sich jede *Einheit* in der
   *Bewegungsphase* bewegt hat (*Normale Bewegung*, Advance, Fall Back, stationär,
   `core_rules.txt:710`). F3 B: ein *Modell* zur *Ebene* machen auch in der *Schlacht*, „wie
   in der Aufstellungsphase“. Beides nach F7 A in Domänenphase 9; bis dahin gilt
   [Vertrag Bewegung](../../technik/architektur/vertrag/bewegung.md) V14: in der *Schlacht*
   kein `ebene`.
2. Seit F5 können mehrere gezogene *Einheiten* ohne *Kohärenz* stehen; BEW-4.1 nennt nur den
   *Grund*, nicht welche. ArbiterMap markiert jedes *Modell* ohne *Kohärenz* schon beim
   Ziehen (orange Ring, Warndreieck, `ArbiterMap/frontend/static/js/rule_check_overlay.js:19`,
   `:69`). Die Abweichung hat der Stakeholder nicht entschieden.
3. BEW-1, Zweck: `core_rules.txt:710` belegt „korrigiert jede nach Belieben“ nicht; `:734`
   sagt „No unit can be selected to move more than once“. Quelle ist allein 5180 F5 (ein
   Stand, der regelkonform entstanden sein könnte).
4. Glossar, *Distanz*: „5400 F1 A als Annahme“; der Stakeholder hat A geantwortet.
5. [4261](4261-lueckenImNormalMoveFuerSpaeter.md) Punkt 1 löst BEW-4.1; Punkt 2 entfällt
   mit der *Einheit in Bewegung*.

**Kosten.** In Zyklus 8 keine. Ohne 1 gehen zwei Antworten mit 5180 verloren. Ohne 2 sucht
der *Spieler* bei ‚keine Kohärenz‘ in einer echten Partie die *Einheit* selbst. 3 und 4 je
wenige Wörter.

**Gegenvorschlag.** 1 als Kriterien in Domänenphase 9; 2 als Frage an den Stakeholder mit
ArbiterMap als Quelle, zusammen mit 4261 Punkt 6 (beides Anzeige an der *Karte*); 3 Zweck
mit „Anliegen 5180 F5“ statt `:710` für das Korrigieren; 4 „als Annahme“ streichen. 3 und
4 gehen auch gleich.

**Stellungnahme.** Vorab umgesetzt: 3, der Zweck von
[BEW-1](../../domaene/anforderungen/phasen/bewegung/normaleBewegung.md) belegt „in beliebiger
Folge“ mit `core_rules.txt:710` und „korrigiert jede nach Belieben“ mit Anliegen 5180 F5;
4 im [Glossar](../../domaene/glossar.md) (siehe [5560](5560-distanzEntschieden.md)).
1, 2 und 5 bearbeite ich in Domänenphase 9; bis dahin wartet das Anliegen.
