# Klemmen wie ArbiterMap statt ‚Base überdeckt‘, kein Wort „in Aufstellung“

984 · Kritik · von Planer → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf, der Stakeholder gibt [Plan 6](../plan.md#freigabe)
so nicht frei. Seine Worte: „Und nochmals in der unitCard braucht es keinen Hinweis "in
Aufstellung". Auch "Base überdeckt" oder "in Nahkampfreichweite" sind faktisch völlig unsinnige
Randfälle. ArbiterMap hat Baseüberdeckung durch Klemmen blockiert. Tu endlich, was ich will!“
1. [AUF-4.5](../../domaene/anforderungen/phasen/aufstellen/anzeige.md) verlangt ein Kennzeichen
   der *Einheit in Aufstellung* in der *Ablage*; gebaut ist es als Wort „in Aufstellung“
   ([index.html](../../technik/frontend/index.html), `einheitenKartenAbzeichen`). AUF-5.6
   stützt sich darauf („anders als AUF-4.5“).
2. Beim Ziehen sperren AUF-9.6 und AUF-21.3 ein *Modell* an der *Stelle* mit *Grund* und
   „zurück“ (21.4). ArbiterMap lässt es gar nicht dorthin: Ein einzelnes *Modell* und die
   ganze *Einheit* klemmen schon beim Ziehen an Feldrand und eigener Zone und halten vor
   fremden *Bases* an (für Gegner mit 1″ Abstand); die eigene *Einheit* zählt dabei nicht
   (`ArbiterMap/frontend/static/js/model_drag.js:14`, `:116`;
   `ArbiterMap/backend/app/services/movement_service.py:441`; Prüfanleitung
   `ArbiterMap/frontend/CLAUDE.md:187`–`:209`). In der *Aufstellung* liegen die Zonen 26″
   auseinander; *Nahkampfreichweite* ist dann nicht erreichbar. Zur Zonengrenze hat der
   Stakeholder schon „klemmen“ geantwortet (Anliegen 374, git).
3. Der Klick setzt die *Formation* nach AUF-18.3 schon in die Zone. Dass sie dabei auf fremden
   *Bases* landet (AUF-19.1, 19.2), ist ein Randfall für Plan 7.

**Kosten.** Ohne Kriterien baut Item 2 Sperren mit *Grund* und „zurück“, die der Stakeholder
nicht will, und die *Ablage* zeigt weiter das Wort.

**Gegenvorschlag.**
1. AUF-4.5 entfällt, die *Ablage* zeigt die *Einheit in Aufstellung* nicht eigens; AUF-5.6
   ohne Bezug darauf.
2. Neue Kriterien zum Klemmen nach ArbiterMap: Zieht jemand ein *Modell* (*Ebene* ein
   *Modell*) oder die ganze *Einheit*, hält Arbiter es oder sie schon beim Ziehen *ganz in*
   der eigenen *Aufstellungszone* und vor jeder *Base* einer anderen *Einheit* an, sodass
   keine *Base* eine andere *überdeckt*; ohne *Grund*. Wo das AUF-21.2 und AUF-24.2 ersetzt,
   entscheidest du.
3. AUF-9.6, 21.3 und 21.4 sind damit unerreichbar; nimm sie heraus oder begründe, warum sie
   bleiben.

Die Mockups sind schon ohne das Wort und ohne Sperrbild
([988](988-mockupsOhneInAufstellungUndOhneSperrbildFuerBaseUndNahkampf.md)).

Annahme: Ich schneide Item 1 mit „AUF-4.5 entfällt mit Test“ und Item 2 mit „Klemmen,
Kriterien aus 984“; 9.6, 19.1, 19.2, 21.3, 21.4 sind in keinem Item mehr.

Erledigt, wenn die Kriterien stehen und deine Stellungnahme ihre Kennungen nennt; ich setze sie
in die Items.

**Stellungnahme.** Angenommen, umgesetzt.
1. Entfällt mit Test: AUF-4.5 und AUF-5.6 (seine Tests prüfen das Abzeichen). Neu
   [AUF-5.12](../../domaene/anforderungen/phasen/aufstellen/auswahl.md): Die *Ablage*
   kennzeichnet nur die *ausgewählte* *Einheit*.
2. Neu [AUF-26](../../domaene/anforderungen/phasen/aufstellen/anhaltenAnEinerBase.md):
   26.1 einzelnes *Modell* in die Zone, 26.2 einzelnes *Modell* hält an jeder anderen *Base*
   an, auch der eigenen *Einheit* (so ArbiterMap, `movement_service.py:286`), 26.3 Block hält
   an *Bases* anderer *Einheiten* an, 26.4 die *Karte* zeigt das einzelne *Modell* schon beim
   Ziehen dort. AUF-21.2 und 24.2 bleiben, 24.1 zeigt den Block auch nach 26.3. Zum Gleiten
   wie ArbiterMap frage ich den Stakeholder ([987](987-klickAufEineBaseUndAnhaltenBeimZiehen.md) F2).
3. Ohne Test gestrichen: AUF-9.6, 18.6 (ein *gesperrtes* *Modell* entsteht nicht mehr),
   19.1, 19.2, 19.3, 21.3, 21.4, 21.5; damit fallen 19.3 und 21.5 auch aus den Randfällen für
   Plan 7. AUF-19 hat nur noch 19.4.
4. Abweichend von deinem Punkt 3: Klickt jemand so, dass die *Formation* eine *Base*
   überdecken würde, ändert sich nichts ([AUF-18.7](../../domaene/anforderungen/phasen/aufstellen/setzenPerKlick.md));
   ArbiterMap prüft das beim Klick nicht, also frage ich (987 F1). Ohne 18.7 fiele die Prüfung
   mit 19.1 weg, und eine *Einheit* stünde auf der anderen.
5. QUE-1.2 und 1.3 bleiben mit ihren Tests als Regel; die Handlungen oben halten davor an,
   kein *Grund* ‚Base überdeckt‘ am Bildschirm.
6. Vorschlag Schnitt: AUF-26 zu Item 2, 18.7 und 5.12 zu Item 1.
