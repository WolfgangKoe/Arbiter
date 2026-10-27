# Vier Annahmen zur Bewegungsphase

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 2/3
Status: offen

## Runde 1
**Befund.** Vier Fälle ohne Anforderung.

**Kosten.** Je Frage.

**F1 · Wann steht „Bewegung der Einheit beenden“ da?** A: bei *Einheit in Bewegung*
(Mockup bew-1). B: immer (neu). Empfehlung: A.
Antwort: Hmm, ich gebe mal meine Vorstellung wieder. Die Bewegungsphase beginnt. Ich wähle eine Einheit und bewege diese nicht, soweit wie ich möchte bis zum maximalen Bewegungswert. Einen Knopf "Bewegung beenden" braucht es nicht. Ich wähle einfach die nächste Einheit. Es braucht eher eine Art Markierung, dass sich die Einheit bewegt hat, bzw. welche Art der Bewegung sie in der Bewegungsphase ausgeführt hat (Es gibt m.W. drei, wenn man "Stationär" nicht als vierte Art mitzählt).

**F2 · Wo zeigt die Karte ein Modell beim Ziehen über B?** A: an der letzten *Stelle* ohne
*Sperre* (V10). B: vor dem Ziehen (BEW-2.3). Empfehlung: A.
Antwort: Ich bin mir nicht sicher, ob ich die Frage richtig verstehe. Normalerweise sollte ich eine Einheit nicht über das B der einzelnen MOdelle ziehen können. ALles andere wäre eine bewusst gesetzte ÜBersteuerung, die vermutlich nur dann geschieht, wenn man beispielsweise auf dem Tisch misst, dass eine Einheit in Angriffsreichweite ist, die App diesen Zustand aber nicht abbildet. ANsonten würde ich erwarten, dass die Einheit in der Bewegung am maximalen Wert stoppt.

**F3 · Ein Modell zur Ebene machen, auch in der Schlacht?** A: Nein (AUF-20.6). B: Ja
(AUF-25, ArbiterMap). Empfehlung: A.
Antwort: B, es ist wie in der Aufstellungsphase

**F4 · Was geschieht, wenn ein Klick doppelt ankommt?** A: Er wirkt einmal (V5). B: Jeder
wirkt (neu). Empfehlung: A.
Antwort: A

**Gegenvorschlag.** F1 bis F4 beantworten.

**Stellungnahme.**

## Runde 2
**Befund.** F4 gilt, so ist es gebaut. F1 bis F3 ändern Anforderungen. Ich verstehe F1: kein
Knopf, die Bewegung endet mit der nächsten *Einheit*; Arbiter zeigt, wie sich jede bewegt
hat (*Normale Bewegung*, Advance, Fall Back, stationär, `core_rules.txt:710`). Hält auf: F5
bis F7 ändern Schritt 3 von Plan 8; bis dahin baut niemand Knopf und *Sperre* über *B*.

**Kosten.** Je Frage; Produktcode dazu gibt es noch nicht.

**F5 · Wann endet die Normale Bewegung?** A: wenn jemand ein *Modell* einer anderen
*Einheit* zieht und loslässt oder „Phase beenden“ wählt; ist die *Einheit in Bewegung* nicht
in *Kohärenz*: *Sperre* ‚keine Kohärenz‘ (Regeltext). B: schon beim Klick auf eine andere
eigene *Einheit* (Regeltext). Empfehlung: A. Ein Klick wählt auch zum Ansehen aus
(AUF-20.6); eine *Sperre* dabei überrascht.
Antwort: .

**F6 · Wo bleibt ein Modell, das du über sein B hinaus ziehst?** A: Es hält auf der
geraden Strecke an, wo sein *B* aufgebraucht ist (auf 1/100″), und bleibt beim Loslassen
dort, ohne *Grund*; der Block hält, sobald eines sein *B* erreicht (Anliegen 5180, AUF-29).
B: Es springt beim Loslassen mit ‚weiter als B‘ zurück (BEW-2.3). Empfehlung: A, so
erwartest du es. Weiter erst mit *gemeinsam übergehen* (Plan 8: noch nicht).
Antwort: .

**F7 · Wann kommt das?** A: F5 und F6 jetzt in Plan 8, die Markierung und F3 in der
Domänenphase 9 (Anliegen 5180). B: alles in Domänenphase 9 (Plan 8). Empfehlung: A, sonst
baut Zyklus 8 Knopf und Zurückspringen, die Zyklus 9 abreißt. Bei A heißt Schritt 3: „…zieht
eine *Einheit*, dann die nächste. Am *B* hält Arbiter an; über eine fremde *Base* sperrt er
beim Loslassen, ohne *Kohärenz* beim Ziehen der nächsten oder bei ‚Phase beenden‘.“
Anforderungsautor und UX fassen BEW-1, BEW-2, Mockups neu, etwa 15 Tests ändern sich. Die
Markierung braucht „jede *Einheit* nur einmal“ und Advance, F3 einen neuen Schlüssel im
Spielstand; bis dahin ziehst du ein *Modell* allein nach einem Klick auf eine andere
*Einheit* (AUF-20.4).
Antwort: .

**Gegenvorschlag.** F5 bis F7 beantworten; „.“ heißt, die Empfehlung gilt. Danach
beauftragt der Koordinator Anforderungsautor und UX, ich ziehe den Vertrag nach.

**Stellungnahme.**
