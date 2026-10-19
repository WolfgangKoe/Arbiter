# Dein Happy Path beim Aufstellen: Reserve, verbotene Stelle, eine Einheit auswählen

960 · Fragen · von Planer → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** Dein Kommentar zu [Plan 6](../plan.md): Nach dem *Roll-off* stellen die *Spieler*
abwechselnd je eine ganze *Einheit* mit einem Klick in ihre Zone, verschieben sie oder einzelne
*Modelle*, klicken „Aufstellen der Einheit beenden“, bis alle *Einheiten* auf dem Feld oder in
Reserve stehen; alles andere sind Randfälle. Drei Punkte lässt er offen.

**Kosten.** Ohne Antwort arbeiten Anforderungsautor und UX mit den Empfehlungen; antwortest du
anders, ändern sich Kriterien und Mockups vor dem Test.

**Gegenvorschlag.**

**F1 · Gehört die Reserve in Etappe 1?**
[Etappe 1](../../domaene/etappen/01-aufstellen.md) kennt keine Reserve. Die Regel heißt
Strategic Reserves: Wer *Einheiten* dorthin stellt, wählt sie vor der Schlacht, nicht beim
abwechselnden Aufstellen, zahlt Befehlspunkte und braucht eine Battle-forged-Armee
(`core_rules.txt:3276`); die *Einheit* kommt erst in der Bewegungsphase aufs Feld.
- A · Nein: Etappe 1 endet, wenn alle *Einheiten* auf dem Feld stehen. Die Reserve kommt mit
  dem Ankommen aus der Reserve, frühestens in Etappe 3 (Schlachtrunden). Empfehlung: Sie
  verlangt Befehlspunkte und Ankommen, die Etappe 1 nicht hat.
- B · Ja: In Etappe 1 gibt es je *Einheit* einen Knopf „in Reserve“; sie gilt dann als
  aufgestellt, ohne Befehlspunkte.

Annahme: A, Etappe 1 bleibt.
Antwort: A, nein gehört sie nicht.

**F2 · Was geschieht, wenn ein Modell an einer verbotenen Stelle landet?**
Etwa auf einer anderen *Base*, zu nah am Gegner oder, einzeln gezogen, aus der Zone.
- A · Wie gebaut: Eine *Formation* oder einen Block rückt Arbiter in die Zone; was dann noch
  verboten steht, bleibt blass stehen, darunter der *Grund* und „zurück“. Sonst erscheint nichts.
  Empfehlung: Das [Ziel](../../domaene/ziel.md) verlangt eine *Sperre*, die ihr gemeinsam
  übergehen könnt; auf deinem Happy Path siehst du davon nichts; es kostet nichts Neues.
- B · Wie ArbiterMap: Arbiter hält jedes *Modell* und jeden Block an der letzten erlaubten Stelle
  an, ohne *Grund* und Knopf. Dann gibt es nichts zu übergehen; das Gleiten hat in ArbiterMap
  mehrere Sitzungen gekostet (`ArbiterMap/docs/spec/interaction_map.md:401`), gebaute Kriterien ändern sich.

Annahme: A.
Antwort: A

**F3 · Wie viele Einheiten sind beim Aufstellen ausgewählt?**
Heute bis zu zwei; dann sperrt ein Klick auf die *Karte* mit ‚mehrere ausgewählt‘ (deine Antwort
in Anliegen 800, F1 B).
- A · Höchstens eine: Ein Klick auf eine andere *Einheit* in der *Ablage* wählt nur sie; der
  Hinweis ‚mehrere ausgewählt‘ entfällt. Empfehlung: So macht es ArbiterMap
  (`ArbiterMap/frontend/static/js/deployment.js:408`), und es fällt ein Randfall weg.
- B · Bis zu zwei wie entschieden; ‚mehrere ausgewählt‘ kommt mit den Randfällen in Plan 7.

Annahme: A.
Antwort: A

**Stellungnahme.**
