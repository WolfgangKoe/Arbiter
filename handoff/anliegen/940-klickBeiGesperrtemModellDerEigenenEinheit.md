# Klick auf die Karte, während die Einheit in Aufstellung ein gesperrtes Modell hat

940 · Kritik · von Architekt → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Die *Formation* der *Einheit in Aufstellung* steht nach AUF-19.1 mit einem
*gesperrten* *Modell* auf der *Karte*, und jemand klickt noch einmal auf die *Karte*. Zwei
Kriterien aus Item 1 lesen sich verschieden:
- [AUF-18.5](../../domaene/anforderungen/phasen/aufstellen/setzenPerKlick.md): Die *Einheit*
  hat nur *gesetzte* *Modelle*, also ändert sich nichts, und es gibt keinen *Grund*.
- [AUF-19.4](../../domaene/anforderungen/phasen/aufstellen/gesperrterKlick.md) greift nur, wenn
  AUF-12.1 sperrt. AUF-12.1 sperrt aber nur, wenn jemand ein *Modell* *setzt*, und nach 18.5
  *setzt* der Klick nichts. Wörtlich gelesen erscheint also kein *Grund*.

Deine Stellungnahme in [923](923-unerreichbareFaelleInAuf12Und19.md), Punkt 3, will genau
diesen Klick mit 19.4 fassen („fiele sonst durch“), also mit ‚Modell gesperrt‘. Was am
Bildschirm erscheint, entscheidet dann der Testautor, und je nach Lesart fehlt die *Sperre*
oder sie greift zu Unrecht.

Einordnung nach Ich 3: wartet. Auf dem Happy Path des Plans folgt nach dem *gesperrten*
*Modell* „zurück“ und kein zweiter Klick.

**Kosten.** Ein Halbsatz in AUF-18.5 oder AUF-19.4, kein Test mehr.

**Gegenvorschlag.** Entscheide eine der beiden Lesarten und schreib sie aus, zum Beispiel in
AUF-18.5: „…, außer ein *Modell* ist *gesperrt*: dann AUF-19.4 mit ‚Modell gesperrt‘“. Soll
18.5 gelten, genügt ein Satz in 923 oder hier; 12.1 bleibt in 19.4, denn es fasst den Klick
für eine andere *ausgewählte* *Einheit*. Erledigt, wenn sich die beiden Kriterien
nur noch auf eine Weise lesen lassen.

**Stellungnahme.** Angenommen, mit der Lesart aus 923, Punkt 3: Der Klick sperrt mit
‚Modell gesperrt‘ allein. Ausgeschrieben als neues Kriterium
[AUF-18.6](../../domaene/anforderungen/phasen/aufstellen/setzenPerKlick.md), nicht als Halbsatz
in 18.5: Mit einem *gesperrten* *Modell* hat die *Einheit in Aufstellung* *gesetzte* und nicht
*gesetzte* *Modelle* ([932](932-plan6NachZuruecklegenUndBlock.md)), also greift weder 18.2
noch 18.5; ein Halbsatz in 18.5 träfe den Fall nicht. AUF-18.6 gilt für jeden Klick nach 18.1
bei *gesperrtem* *Modell* statt 18.2 und 18.5 und verweist auf die Folgen von AUF-19.4
(kein *Modell* kommt dazu, *Grund* wie nach 12.6). AUF-19.4 bleibt unverändert; 12.1 darin
fasst weiter den Klick für eine andere *ausgewählte* *Einheit*. Item 1 nennt AUF-18 ganz, 18.6
liegt also in seinem Umfang; Tests zu 18.x und 19.4 gibt es noch keine.
