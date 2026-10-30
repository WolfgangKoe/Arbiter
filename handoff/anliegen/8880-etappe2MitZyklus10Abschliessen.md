# Etappe 2 mit Zyklus 10 abschließen?

Form: Fragen
Von: Planer
An: Stakeholder
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Dein Wortlaut: „Wir sollten mit diesem Zyklus Etappe 2 an sich fast abgeschlossen haben. Das bitte nochmal prüfen. Für Zyklus 10 haben wir inzwischen sehr viele Anliegen angesammelt. Vielleicht lohnt es sich Zyklus 10 als Abschluss für Etappe 2 zu planen. Das bitte mal kritisch prüfen.“

Geprüft an [Etappe 2](../../domaene/etappen/02-bewegen.md):
- 57 von 63 Kriterien haben Tests; es fehlen AUF-12.8, 16.7, 16.8, 28.1 ([Loslassen neben der *Karte*](../../domaene/items/loslassenNebenDerKarte.md)), QUE-11.1 (*Phase beenden* nur im Zug), QUE-7.1 ([ruhige *Karte*](../../domaene/items/ruhigeKarte.md)).
- Ohne Kriterium: Zurücksetzen (2364 F4), Ork-Psioniker und Canoptek-Spinne (2364 F1), die Regellücken aus [6986](6986-bewegungLueckenFuerSpaeter.md) (`core_rules.txt:724`, `:745`), [8480](8480-ueberDieKanteHinausLoslassen.md), 7642, 8601.
- 22 Anliegen an die Technikphase 10 räumen Tests und Code auf, ohne Folge am Bildschirm, dazu die Umbenennung aus [7800](7800-karteUndEbeneBenennen.md).

Ergebnis: „fast“ gilt für den Happy Path; Zyklus 10 schließt ab, wenn er auf die Etappe begrenzt bleibt.

**Kosten.** Siehe die Möglichkeiten; jeder Zyklus kostet dazu Plan, Review, Retro, Prozessphase.

**Gegenvorschlag.**
**F1 · Wie planen wir Zyklus 10?**
- A Abschluss, Umfang genau die Etappe (Etappe 2, Anliegen 2364): Zurücksetzen, Loslassen neben der *Karte* mit 8480, *Nahkampfreichweite* auf der ganzen Strecke und kein *Vorrücken* aus ihr, *Phase beenden* nur im Zug, Psioniker und Spinne, ruhige *Karte*. „Schon gezogen“ und *Übergehen* eines Anhaltens kommen in Etappe 3, wo das Ziehen an fremden *Bases* anhält (Anliegen 2363); bis dahin merkt ihr euch, was gezogen hat. Drei bis vier Anforderungen, ein Mockup; Token rund ein Drittel mehr als Zyklus 9, dafür ein Zyklus weniger. Hängt es, rückt die ruhige *Karte* in Zyklus 11. **Empfehlung**: Die Etappe ist erreicht, alles darin dient der Regel.
- B Abschluss mit allem, auch der Anzeige und dem *Übergehen* eines Anhaltens aus dem Zyklusziel von [Review 9](../review.md) (Review 9, Anliegen 7000 F2, F3): acht Items, Token etwa doppelt so viel wie Zyklus 9.
- C Zwei Zyklen wie im Review (Review 9): erst Zurücksetzen, Anzeige, *Übergehen* eines Anhaltens, *Phase beenden* nur im Zug, in Zyklus 11 der Rest.
Antwort: Wir nehmen A, wobe wir die "ruhige Karte" noch mit in Etappe 2 nehmen. Ordne alles so, dass die Feature umgesetzt werden können und die "Aufräumarbeiten" im Anschluss folgen. Dann kann ich die Funktionalitäten schon mal abnehmen, während das Refactoring noch läuft. Ist das so möglich?

**Stellungnahme.**
Kommentar: Und ein weiterer Kommentar. Sobald Etappe 2 inhaltlich abgenommen ist, könnten der Anforderungsautor und ich schon mal Etappe 3 inhaltlich vorbereiten. Die potentiellen Anforderungen könnten im Rahmen von Anliegen schon mal diskutiert werden und in Zyklus 11 wären wir dann startklar, die Anforderungen und Akzeptanzkritierien auszuarbeiten.
Stellungnahme: Geht ohne neue Regel, wer nur Anliegen schreibt, läuft neben der Technikphase ([Gleichzeitige Läufe](../../prozess/ablauf/gleichzeitigeLaeufe.md)). Ab der Abnahme des letzten Items fragt dich der Anforderungsautor in Anliegen zu [Etappe 3](../../domaene/etappen/03-angriffUndFallBack.md) samt den zwei Punkten aus A; ausformuliert wird sie nach Review 10 (Domänenphase 1). Token: in Zyklus 10 statt 11.

**Klärung.** Ja. Plan 10 ordnet: erst die Teile aus A bis zur Abnahme des Fachkritikers, die ruhige *Karte* zuletzt; dann die 22 Anliegen zum Aufräumen und 7800; dann DoD und Review 10. Die ruhige *Karte* bleibt in Etappe 2; hängt sie, endet die Etappe mit Zyklus 11. Ab der Abnahme des letzten Items prüfst du am Bildschirm, Start nach [Web, W5](../../technik/architektur/web.md#aufbau); freigeben kannst du erst Review 10.
Folgen: eine Ausnahme von „erst Bestand abbauen“ (Absicht 2, Anliegen 306) für Zyklus 10. Die neuen Teile bauen auf Code, den 8620, 8121, 8261 und 8641 noch umbauen; das Aufräumen fasst dann auch neuen Code an, etwas mehr Arbeit. Braucht ein Teil ein Anliegen vorher, ziehe ich es vor. Die Teile fasse ich zu höchstens drei Items (Domänenphase 6).
