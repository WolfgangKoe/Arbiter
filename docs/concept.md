# Arbiter — Konzept & Name

## Der Name

**Arbiter** trägt zwei Bedeutungsschichten, die das Projekt präzise beschreiben:

### Schiedsrichter der Regeln

Ein Arbiter ist eine neutrale Instanz, die Recht und Regelwerk korrekt durchsetzt.
In WH40k bedeutet das: keine Regelfehler, keine Vergesslichkeit, keine Interpretation nach Belieben.
Die App übernimmt die Regelverantwortung — Phasenkorrektheit, Zustandsübergänge, Eligibility-Checks.
Der Spieler spielt; der Arbiter entscheidet, was erlaubt ist.

### Autorität des Spielgeschehens

Gleichzeitig ist der Arbiter keine passive Uhr, sondern eine aktive Begleitinstanz —
er gibt das Tempo vor, strukturiert die Partie und hält beide Spieler im Fluss.
Er ist der unsichtbare dritte Spieler am Tisch.

---

## Vision

Arbiter ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition.
Er führt zwei Spieler durch eine vollständige Partie: Phasen anzeigen, Einheitenstatus verwalten,
Würfe eingeben und validieren.

Ziel ist kein vollständiges Regelwerk-PDF in App-Form — sondern ein präziser, schneller Begleiter,
der die taktisch relevanten Zustände verwaltet und Fehler verhindert, ohne dem Spieler das Denken abzunehmen.

---

## Designprinzipien

| Prinzip | Bedeutung |
|---|---|
| **Kein Auto-Würfeln** | Der Spieler würfelt physisch — die App nimmt die Ergebnisse entgegen |
| **Kein Board-State** | Keine Positionen, keine Reichweitenberechnung — das bleibt auf dem Tisch |
| **Aktionen nur kontextuell** | Jede Aktion erscheint nur, wenn die betreffende Einheit ausgewählt ist |
| **Zwei Spieler, ein Bildschirm** | Beide Seiten auf einem Gerät — sichtbar, fair, transparent |
| **Regelkonformität über Komfort** | Wenn ein Zug nicht erlaubt ist, wird er gesperrt — kein "quick override" |
