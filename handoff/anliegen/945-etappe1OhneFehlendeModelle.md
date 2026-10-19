# Verlangt Etappe 1 noch „Beenden mit fehlenden Modellen“?

945 · Fragen · von Planer → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** [Etappe 1](../../domaene/etappen/01-aufstellen.md) verlangte: „Aufstellen der
Einheit beenden“ sperrt, solange *Modelle* fehlen; übergeht ihr die *Sperre*, gelten sie als
*vernichtet* (deine Antwort A in Anliegen 11, git). Seit deinen Antworten in 683 und
[890](890-zuruecklegenInGanzeEinheit.md) fehlt aber nie ein *Modell*: Ein Klick *setzt* die
ganze *Formation* ([AUF-18.2](../../domaene/anforderungen/phasen/aufstellen/setzenPerKlick.md)),
*zurücklegen* nimmt die ganze *Einheit* vom Tisch
([AUF-23](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md)), und ohne
*gesetztes* *Modell* gibt es keine *Einheit in Aufstellung* (AUF-7.1). Steht ein *Modell*
*gesperrt*, sperrt AUF-12.1 vorher. Der Anforderungsautor hat das in
[932](932-plan6NachZuruecklegenUndBlock.md) gefunden: AUF-10.2 ‚Modelle fehlen‘ und AUF-10.5
(*vernichtet*) erreicht am Bildschirm niemand mehr.

**Kosten.** Bleibt es in der Etappe, ist sie erst erreicht, wenn ihr etwas vorführt, das am
Bildschirm nicht geht, oder wir bauen eine Sperre ohne Weg dorthin.

**Gegenvorschlag.**

**F1 · Bleibt „Beenden mit fehlenden Modellen“ in Etappe 1?**
- A · Nein: Die Etappe verlangt beim Beenden nur noch die *Kohärenz*; AUF-10.2, 10.4 und 10.5
  kann der Anforderungsautor löschen. Empfehlung: Die Regel stellt *Einheiten* ganz auf
  (`core_rules.txt:2322`), und genau das erzwingt jetzt die Bedienung.
- B · Ja: Der Anforderungsautor beschreibt einen Weg, auf dem ein *Modell* fehlt, etwa wenn
  eine *Formation* nicht ganz in die Zone passt.

Annahme: A, so steht es in Etappe 1, und [Plan 6](../plan.md) nennt AUF-10.5 nicht mehr für
Plan 7.
Antwort: A

**Stellungnahme.** (Stakeholder) Rückfrage: Was ist die eigentliche Frage?

**Klärung.** Die Frage war nur: Muss der Knopf „Aufstellen der Einheit beenden“ noch melden
können, dass *Modelle* fehlen? Nach deiner Beschreibung nie, denn ihr stellt immer die ganze
*Einheit* auf und verschiebt danach nur. Das ist A: Beim Beenden prüft Arbiter nur noch die
*Kohärenz*. So steht es in Etappe 1, den Rest räumt der Anforderungsautor in
[961](961-plan6NurHappyPath.md) auf. Setze `angenommen`, wenn das stimmt.
