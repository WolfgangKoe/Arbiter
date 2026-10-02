# Etappe 3: Phasen am Tisch ändern den Spielstand an der Karte vorbei

07 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · offen

## Runde 1
**Befund.** [Etappe 3](../../domaene/etappen/03-schlachtrunden.md) lässt Phasen, die Arbiter
noch nicht begleitet, am Tisch spielen. Schießen, Nahkampf und Moral entfernen dort Modelle
(z. B. Flucht, `core_rules.txt:2125`), Charge, Pile In und Consolidate bewegen sie
(`:1768`, `:1939`). Arbiter kann in Etappe 3 weder Modelle entfernen noch außerhalb der
Bewegungsphase versetzen. Nach dem ersten Verlust weicht die Karte vom Tisch ab, gegen das
Ziel („Die Karte bildet den Spielstand ab“); in der nächsten Bewegungsphase sperrt Arbiter dann
nach Modellen, die es am Tisch nicht mehr gibt, oder an Stellen, wo sie nicht mehr stehen.

**Kosten.** Zwei Auswege, beide teuer:
- Ein vorläufiges „Modell entfernen“ und „Modell versetzen“ vor Etappe 5. Das regelgerechte
  Entfernen in Etappe 5 ersetzt es; bis dahin ist es Code ohne Zukunft, wie in Anliegen 04.
- Nichts tun: Die Akzeptanztests prüfen nur die Phasenfolge, aber die Probe am Tisch zeigt
  falsche Sperren, und der Stakeholder kann Etappe 3 nicht am echten Spiel abnehmen.

**Gegenvorschlag.** Etappe 3 sagt ausdrücklich: Nicht begleitete Phasen sind leer. Arbiter
zeigt sie in der Reihenfolge der Grundregeln, die Spieler beenden sie ohne Spielhandlung.
Etappe 3 prüft so Phasenfolge, Zugwechsel, Schlachtrunden und Advance ohne Wegwerfcode; ein
vollständiges Probespiel am Tisch gibt es ab Etappe 5, das ist der Preis. Gewünscht ist das
Probespiel früher, dann kommt das Entfernen von Modellen aus Etappe 5 vor, nicht ein Ersatz.
