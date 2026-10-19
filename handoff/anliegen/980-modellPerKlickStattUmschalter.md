# Kein Umschalter: Ein Klick auf ein Modell wählt das einzelne Modell

980 · Kritik · von Planer → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf, der Stakeholder gibt Plan 6 so nicht frei
(Kommentar 1 unter [Freigabe](../plan.md#freigabe)). Er will die Knöpfe „Ganze Einheit“ und
„Einzelmodelle“ in der *Ablage* nicht. Er will die Bedienung, die in ArbiterMap gebaut ist:
1. Er klickt eine *Einheit* in der *Ablage* an, sie bekommt den goldenen Rahmen, dann klickt er
   in die Zone, und sie steht dort.
2. Er hält ein *Modell* gedrückt und zieht, dann wandert die ganze *Einheit* mit.
3. Er klickt ein *Modell* an. Dann ist nur dieses *ausgewählt*, die anderen *Modelle* der
   *Einheit* nicht. Er zieht es, und nur dieses *Modell* wandert.

So ist es in ArbiterMap gebaut: Der Zustand hat je Auswahl eine Ebene, „unit“ oder „model“
(`ArbiterMap/frontend/static/js/model_selection.js:110`, 258–266). Ein Klick auf ein *Modell*
der gewählten *Einheit* wählt nur dieses *Modell*. Ein weiterer Klick auf ein *Modell*
derselben *Einheit* wählt wieder die ganze *Einheit* (`ArbiterMap/docs/spec/interaction_map.md:228`–237).
Ziehen bewegt bei „unit“ alle *Modelle* und bei „model“ nur das gezogene (`:381`). Einen
Umschalter hat ArbiterMap nie gebaut (`model_selection.js:59`, `layerToggleTrigger`
unimplementiert). Er stand nur als Vorschlag in der Beschreibung (`interaction_map.md:191`).
Meine Frage 683 F2 a gab ihn als ArbiterMap aus, das war falsch. Darauf beruhen
[AUF-20](../../domaene/anforderungen/phasen/aufstellen/ebene.md) (20.1, 20.3), die Zeile
*Ebene* im [Glossar](../../domaene/glossar.md) und die Wörter „Ganze Einheit“ und
„Einzelmodelle“ in AUF-21, AUF-23, AUF-24 und QUE-7.

**Kosten.** Bleibt AUF-20 so, baut Item 2 zwei Knöpfe, die der Stakeholder ausdrücklich nicht
will, und Plan 6 bleibt ohne Freigabe.

**Gegenvorschlag.** Fasse die *Ebene* nach ArbiterMap neu, ohne Knopf:
1. AUF-20.1 und 20.3 (Umschalter) entfallen. Kein Kriterium und keine Glossarzeile nennt
   einen Knopf für die *Ebene*.
2. Neu: **Gegeben** eine *ausgewählte* *Einheit*, deren *Ebene* die ganze *Einheit* ist,
   **wenn** jemand auf eines ihrer *gesetzten* *Modelle* klickt, ohne zu ziehen, **dann** ist
   nur dieses *Modell* *ausgewählt*. Die *Karte* kennzeichnet nur dieses (AUF-5.7 anpassen).
   *Modelle*, *Einheit in Aufstellung* und *an der Reihe* bleiben gleich.
3. Neu: Ein Klick auf ein *Modell* derselben *Einheit*, während ein einzelnes *Modell*
   *ausgewählt* ist, wählt wieder die ganze *Einheit* (ArbiterMap `:235`). Empfehlung:
   übernehmen, sonst kommt der *Spieler* ohne Knopf nicht zur ganzen *Einheit* zurück.
4. AUF-20.2 und 20.5 bleiben in der Sache: Nach der Wahl in der *Ablage* und nach dem Klick in
   die Zone ist die ganze *Einheit* *ausgewählt*. AUF-20.4 und AUF-21.1 bleiben mit den neuen
   Namen der *Ebene*: Ziehen bewegt nur das *ausgewählte* *Modell* oder die ganze *Einheit*.
5. Glossar: *Auswahl* und *Ebene* sagen, dass auch ein einzelnes *Modell* *ausgewählt* sein
   kann und wie die *Ebene* wechselt.
6. Die Wörter „Ganze Einheit“ und „Einzelmodelle“ in AUF-21, 23, 24 und QUE-7 nachziehen.

Randfall, wartet auf Plan 7: Klick auf ein *Modell* einer nicht *ausgewählten* *Einheit*.
ArbiterMap wählt dann deren ganze *Einheit* (`:228`).

Erledigt, wenn kein Kriterium und keine Glossarzeile einen Umschalter verlangen, Punkt 2 bis 5
ein Kriterium haben und deine Stellungnahme die Kennungen nennt. Dann setze ich sie in
[Einheit verschieben](../../domaene/items/einheitVerschieben.md).

**Stellungnahme.** Umgesetzt. Entfallen: AUF-20.1, 20.3. Neu in AUF-25: 25.1 (2), 25.2 (3),
25.3, 25.4 (*Karte*, „statt AUF-5.7“, 5.7 bleibt). 3 wie gebaut: ein anderes *Modell* wird
*Ebene* (`model_selection.js:343`). Wie die *Ebene* wechselt, sagt AUF-25, nicht das Glossar
(`domaene/CLAUDE.md`). Nachgezogen: 21, 23, 24.1, QUE-7.1.
