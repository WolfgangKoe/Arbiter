# Zieht ein Modell durch eine fremde Base hindurch, wenn sein Ziel frei liegt?

1320 · Fragen · von Testautor → Stakeholder · Runde 1/3 · rückfrage

## Runde 1
**Befund.** AUF-26.2 und 26.3 halten ein Modell oder einen Block nur an, wenn die Stelle beim Loslassen eine Base überdecken würde. Ein Modell, dessen gerade Strecke eine Base kreuzt, dessen Ziel aber frei liegt, wird nicht angehalten. Es springt über die Base hinweg. Die Tests sagen das so (`testAuf26_2KreuztDieStreckeNurEineBaseUndLiegtDasZielFreiStehtDasModellAmZiel`, ebenso 26.3). Der Architekt hat es in [V10](../../technik/architektur/handlungen.md) so festgelegt: „Angehalten wird nur, wenn die Stelle am Ende des Wegs eine Base überdecken würde“.

**Kosten.** Am Tisch zieht man ein Modell nicht durch ein anderes. Ob Arbiter es trotzdem erlaubt, bestimmt, wie sich das Ziehen anfühlt. Antwortest du nicht, gilt die Empfehlung.

**F1 · Soll ein Modell auch dann an der ersten Base anhalten, wenn sein Ziel hinter ihr frei liegt?**
Annahme: Die Tests bleiben, wie die Kriterien sie verlangen (Nein).
Empfehlung: Nein, wie in AUF-26.2 und 26.3 geschrieben. Das Ziehen bleibt einfach, und Arbiter setzt ein Modell dorthin, wo der Spieler es loslässt. Ja hieße: Die Strecke zählt, und AUF-26.2, 26.3 und 27.2 müssten umgeschrieben werden. Dein Vorbild in ArbiterMap (`geometry.py:734`) hält an der Strecke an, das müsstest du dann ausdrücklich so wollen.
Antwort: .

**Gegenvorschlag.** Bei Nein bleiben Kriterien und Tests unverändert. Bei Ja ändert der Anforderungsautor AUF-26.2 und 26.3, die Tests folgen.

**Stellungnahme.**
Kommentar: In ArbiterMap gab es dieselbe Frage. Grundsätzlich soll es hier genauso wie dort gelöst werden, bzw. so gelöst werden, wie es dort geplant war. Die Anforderungen würde ich aber erst im nächsten Zyklus anpassen. Bitte vormerken. Was wäre hierzu die richtige Antwort?
