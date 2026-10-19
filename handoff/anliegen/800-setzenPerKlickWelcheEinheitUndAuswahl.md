# Setzen per Klick: welche Einheit, bleibt die Auswahl, neuer Begriff Ebene

800 · Fragen · von Anforderungsautor → Stakeholder · Runde 2/3 · erledigt

## Runde 1
**Befund.** Nach deiner Entscheidung in [683](683-aufstellenKlickenOderZiehen.md) (F1 A, F2 a)
stehen die Kriterien in [AUF-18](../../domaene/anforderungen/phasen/aufstellen/setzenPerKlick.md),
[AUF-20](../../domaene/anforderungen/phasen/aufstellen/ebene.md) und
[AUF-21](../../domaene/anforderungen/phasen/aufstellen/einheitVerschieben.md). Zwei Punkte sagen
weder Regeln noch ArbiterMap eindeutig, einer weicht von ArbiterMap ab, und ein Begriff ist neu.
In ArbiterMap ist die *Einheit* zum Aufstellen nur eine, getrennt von der *Auswahl* auf der
*Karte*; nach dem Klick ist sie nicht mehr gewählt (`ArbiterMap/frontend/static/js/deployment.js:420`).
Bei uns ist es eine *Auswahl* mit bis zu zwei *Einheiten* je *Spieler* (AUF-5.5), und der
Umschalter „Ganze Einheit / Einzelmodelle“ gilt je *ausgewählter* *Einheit*.

**Kosten.** Ohne Antwort arbeite ich mit den Empfehlungen; ändern sie sich, ändern sich AUF-18.1
und AUF-20.5 samt Tests.

**Gegenvorschlag.**

**F1 · Welche *Einheit* setzt ein Klick auf die *Karte*, wenn mehrere *ausgewählt* sind?**
- A · Die zuletzt *ausgewählte* des *Spielers* *an der Reihe*; hat er keine, die des anderen,
  dann sperrt Arbiter mit „Spieler 2 ist an der Reihe“ (AUF-22.1). Empfehlung: Der letzte Klick
  in der *Ablage* gilt wie in ArbiterMap, und wer die falsche *Ablage* angeklickt hat, erfährt warum.
- B · Ein Klick setzt nur, wenn genau eine *Einheit* *ausgewählt* ist, sonst Sperre.

Annahme: A, so steht es in AUF-18.1.
Antwort: B

**F2 · Bleibt die *Einheit* nach dem Klick *ausgewählt*?**
- A · Ja, bis sie *aufgestellt* ist (AUF-5.10). Empfehlung: Sonst verschwindet der Umschalter
  „Ganze Einheit / Einzelmodelle“ genau dann, wenn du sie verschieben willst, und für den Rest
  ihrer *Modelle* (AUF-18.4) müsstest du sie neu anklicken. Weicht von ArbiterMap ab.
- B · Nein, wie ArbiterMap; zum Verschieben klickst du sie erneut an.

Annahme: A, so steht es in AUF-20.5.
Antwort: A

**F3 · Neuer Begriff *Ebene* (ArbiterMap: „Einheiten-/Modellebene“).**
Was Ziehen bei einer *ausgewählten* *Einheit* verschiebt: „Ganze Einheit“ oder „Einzelmodelle“;
Code `ebene`. Eine neue *Ebene* beginnt mit „Ganze Einheit“ (AUF-20.2), wie der erste Klick in
ArbiterMap (`interaction_map.md:376`).
- A · *Ebene* freigeben. Empfehlung.
- B · Dein Wort.

Antwort: A

**Stellungnahme.**

## Runde 2
**Befund.** F1 B und F2 A stehen in AUF-18.1, [AUF-19.5](../../domaene/anforderungen/phasen/aufstellen/gesperrterKlick.md)
und AUF-20.5. Drei Punkte zu B sagen weder Antwort noch Regeln ([850](850-klickNachAntwortBUndBlockAmZonenrand.md)).
„S“ zu F3 ist keine Option.

**Kosten.** Je Änderung AUF-18.1 oder 19.5; Tests gibt es noch keine.

**Gegenvorschlag.**

**F4 · Wessen *Auswahl* zählt für „genau eine“?**
- A · Beide zusammen, wie deine Antwort. Gehört die eine *Einheit* dem *Spieler*, der nicht
  *an der Reihe* ist, sperrt AUF-22.1 mit „Spieler 1 ist an der Reihe“. Empfehlung.
- B · Nur die des *Spielers* *an der Reihe*; hat er keine, ändert sich nichts.

Annahme: A, so steht es in AUF-18.1 und 19.5.
Antwort: A

**F5 · Klick ohne *Auswahl*?**
- A · Nichts, ohne *Grund*, wie AUF-18.5 (Anliegen 380 F1 A). Empfehlung.
- B · *Sperre* ‚nichts ausgewählt‘.

Annahme: A, so steht es in AUF-18.1.
Antwort: A

**F6 · Welcher *Grund* bei mehr als einer *ausgewählten* *Einheit*?**
- A · ‚mehrere ausgewählt‘, ohne „gemeinsam übergehen“ wie AUF-19.4, denn welche *Einheit*
  gemeint ist, bleibt offen. Empfehlung.
- B · Dein Wortlaut.

Annahme: A, so steht es in AUF-19.5.
Antwort: A

**F7 · Heißt „S“ zu F3: *Ebene* freigegeben?**
- A · Ja. Empfehlung: steht schon in Glossar, AUF-20 und 21.
- B · Dein Wort.

Annahme: A.
Antwort: A

**Stellungnahme.**
