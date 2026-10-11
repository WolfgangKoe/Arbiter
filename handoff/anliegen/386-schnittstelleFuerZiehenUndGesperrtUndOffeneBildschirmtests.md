# Schnittstelle für Ziehen und Gesperrt, offene Bildschirmtests

386 · Fragen · von Testautor (Technik) → Architekt (Technik) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Die Domänentests zu Plan 5 legen diese Schnittstelle von `Aufstellung` fest; bitte prüfen:
- `modellLoslassen(modell, stelle)` und `einheitLoslassen(einheit, stelle)`: *setzen* wie `modellSetzen`; sperrt die *Stelle* (QUE-1.2, QUE-1.3, AUF-3.2), wird das *Modell* `gesperrt` statt `Sperre` zu werfen (AUF-9.1). Sperren der Handlung (AUF-7.2, 7.3, 12.1) werfen `Sperre` mit unverändertem Zustand (AUF-12.2). `einheitLoslassen`: AUF-8.5, 8.6, 14.1, 16.1.
- `modellZurücklegen(modell, spieler)`: `spieler` ist der Besitzer der *Ablage*, auf die losgelassen wird (AUF-8.3, 8.4, 16.3).
- `zurück()`; Abfragen `gesperrt(modell)`, `stelleDesGesperrten(modell)`, `gründeDesGesperrten(modell)`, `inKohärenz(einheit)`.
- Neue `Grund`-Werte: `modelleFehlen`, `keineKohärenz`, `modellGesperrt`.
- `inKohärenz` liegt nach dem Grundschnitt in `querschnitt/kohaerenz.py`; die Tests rufen sie über `Aufstellung`.

Es fehlen noch, weil der Vertrag fürs Ziehen und Beenden (W3, Plan: Vorarbeit des Architekten) nicht in [Web](../../technik/architektur/web.md) oder [Vertrag](../../technik/architektur/vertrag.md) steht: die Bildschirm- und Dienst-Tests zu QUE-3.4, QUE-3.5, AUF-9.1 (Kennzeichen am Bildschirm), AUF-10.1 (Klick), AUF-12.3, AUF-12.4, AUF-16.2.

**Kosten.** Ohne sie bleibt `rueckverfolgungTest` rot (QUE-3.4, QUE-3.5 ohne Test).

**Gegenvorschlag.** Du trägst den Vertrag ein (Routen, Antwort bei *Sperre*, Anzeige von *Grund* und *gesperrt*); danach schreibe ich die Bildschirmtests nach B1 (Maus und Finger über CDP `Input.dispatchTouchEvent`).

**Stellungnahme.** Schnittstelle geprüft, sie gilt: eine Tür (`Aufstellung`), Abfragen statt
Felder (D3), `inKohärenz` über die Tür nach dem Grundschnitt. Zwei Hinweise an den
Implementierer: `modellLoslassen` nutzt die Tabelle aus D4 (Gründe gegen die *Stelle* →
*gesperrt*, Wächter werfen), kein `try` um `modellSetzen`; den Parameter von
`modellZurücklegen` nennt er `spielerDerAblage`, wie deine Tests die Variable (positional,
kostet keinen Test). Vertrag eingetragen: [Handlungen](../../technik/architektur/handlungen.md)
V5 bis V8 (Routen, 409 mit `gründe` und `spielstand`, Anzeige von *Grund*, `gesperrt` und
Knöpfen, Ziehen), V1 erweitert ([Vertrag](../../technik/architektur/vertrag.md):
Kennung `einheit`, `nummer`, `gesperrt`, `gründeDerGesperrten`; `spielstand.json` nachgezogen,
neu [sperre.json](../../technik/architektur/vertrag/sperre.json)), W3 und B5 in
[Web](../../technik/architektur/web.md#bildschirmtests). Zwei Annahmen bis zur Antwort in 389
(*Einheit* auf *Ablage*, „zurück“ ohne *gesperrtes*); Knopf in Mockups: 388.
