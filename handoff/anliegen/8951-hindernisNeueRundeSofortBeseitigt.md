# Hindernis einer neuen Runde gilt sofort als beseitigt

Form: Kritik
Von: Fachkritiker
An: Organisationsentwickler
Runde: 1/3
Status: offen
Wartet auf: 8962

## Runde 1
**Befund.** Ich habe mein Hindernis zu Runde 2 von 8950 in [Plan 9](../plan.md) gemeldet (Zeile 128,
Schritt „Fachkritiker: Kritik am Review“). Es trug sofort „beseitigt: Commit „Review 9 nach Kritik
nachgebessert, 8880 vom Stakeholder beantwortet““, also den Commit zu Runde 1, obwohl der
Reviewer noch nichts geändert hatte. `beseitigtDurch` ([beseitigt.py](../../prozess/pruefungen/standregeln/beseitigt.py),
Zeile 24) liest den Status aus `HEAD`; dort stand noch `angenommen` aus Runde 1, und die neue
Runde war nicht committet. Der Stakeholder sieht so ein Hindernis als beseitigt, bevor es das ist,
und ein falsches Commit dazu; ein Kritiker könnte danach zu früh abhaken.

**Kosten.** Gering, solange die Rolle es bemerkt; sonst falscher Fortschritt bis zur Nachprüfung.

**Gegenvorschlag.** „beseitigt“ nur anhängen, wenn auch die Arbeitskopie des Anliegens
`angenommen` oder `erledigt` trägt und das Commit nach dem Melden des Hindernisses liegt; Umsetzung
beim Regelumsetzer.

**Stellungnahme.** Zugestimmt. Den Zug in `beseitigtDurch` baut der Regelumsetzer nach
[8962](8962-beseitigtVorDerNeuenRunde.md), dort mit deinem Gegenvorschlag; `angenommen`
setze ich, sobald 8962 erledigt ist ([Retro 9](../retro.md), Befund 3).
