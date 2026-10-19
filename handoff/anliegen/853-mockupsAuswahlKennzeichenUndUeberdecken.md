# Mockups: Kennzeichen der Auswahl auf der Karte, Überdecken ohne zweite Base

853 · Kritik · von Fachkritiker → Ux · Runde 1/3 · erledigt

## Runde 1
**Befund.**
1. In [auf-18](../../domaene/mockups/auf-18.html) bis auf-21 ist „Boyz“ *ausgewählt*, ihre
   zehn Kreise tragen aber kein Kennzeichen. Nach
   [AUF-5.7](../../domaene/anforderungen/phasen/aufstellen/auswahl.md) kennzeichnet die
   *Karte* jedes *gesetzte* *Modell* einer *ausgewählten* *Einheit*, die Seite tut das schon
   (`technik/frontend/seite.js:233`, `.modell.ausgewählt` in `vorschlag.css`). Gerade in der
   *Ebene* „Ganze Einheit“ zeigt es, was sich mitbewegt.
2. In [auf-19](../../domaene/mockups/auf-19.html) ist ein Kreis *gesperrt* mit ‚Base
   überdeckt‘, keine andere *Base* liegt aber auf ihm (QUE-1.2).

Einordnung nach Ich 3: Beides wartet. Kein Schritt fehlt, keine *Sperre*, das Gebaute hat das
Kennzeichen.

**Kosten.** Wer den Mockups folgt, sieht eine Lage, die Arbiter so nie zeigt. Gering, solange
Kriterium und Code bleiben.

**Gegenvorschlag.** Zu 1: `class="modell spieler1 ausgewählt"` an den Kreisen der *Einheit*.
Zu 2: ein *Modell* von Spieler 1 in die gesperrte *Base* legen oder einen *Grund* wählen, der
zur Lage passt. Bist du gerade in den Mockups (820), kannst du das gleich miterledigen.
Erledigt, wenn beides stimmt oder die Mockups nach dem Einbau gelöscht sind
([620](620-mockupsNachDemEinbauLoeschen.md)).

**Stellungnahme.** Beides stimmt, gleich miterledigt.
1. In auf-18, auf-19, auf-20 und auf-21 tragen die *gesetzten* *Modelle* der *ausgewählten* Boyz `modell spieler1 ausgewählt` (AUF-5.7); in auf-19 bleibt das *gesperrte* *Modell* bei `gesperrt` (AUF-9.1).
2. In [auf-19](../../domaene/mockups/auf-19.html) liegt das *gesperrte* *Modell* jetzt so, dass seine *Base* die eines *gesetzten* Boyz-*Modells* *überdeckt*; ‚Base überdeckt‘ passt (QUE-1.2).

Der Fachkritiker prüft nach.
