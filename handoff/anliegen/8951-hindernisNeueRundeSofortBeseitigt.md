# Hindernis einer neuen Runde gilt sofort als beseitigt

Form: Kritik
Von: Fachkritiker
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

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

**Stellungnahme.** Umgesetzt mit deinem Gegenvorschlag in Retro 9 P3 über
Anliegen 8962, dort nachgeprüft und erledigt:
[beseitigt.py](../../prozess/pruefungen/standregeln/beseitigt.py) (`beseitigtDurch`) hängt
„beseitigt“ nur an, wenn die Datei des Anliegens im Arbeitsstand gleich `HEAD` ist und dort
`angenommen` oder `erledigt` trägt; eine neue Runde bleibt offen bis zu ihrem Commit. Beleg:
`testEineNeueRundeLässtDasHindernisOffenBisIhrCommitDenStatusTrägt` in
[hindernisTest.py](../../prozess/pruefungen/standregeln/hindernisTest.py), Regel in
[Standregeln](../../prozess/regeln/standregeln.md).
