# W2 kennt das Modul kennungen.py nicht

341 · Kritik · von Reviewer (Technik) → Architekt · Runde 1/3 · erledigt

## Runde 1
**Befund.** Mit c1416e2 (Anliegen 335) hat `web/` ein viertes Modul,
`technik/arbiter/web/kennungen.py`: Es übersetzt die Kennungen nach W4 in *Spieler* und
*Einheiten* der *Ablage*. [Web, W2](../../technik/architektur/web.md) zählt die Module von
`web/` je mit ihrem Grund zur Änderung auf und nennt es nicht; dort vergibt noch
`darstellung.py` „Spieler 1“ und „Spieler 2“ aus der Reihenfolge der Ausgangslage.

**Kosten.** W2 beschreibt `web/` nicht mehr vollständig: Wer die Kennung des *Modells*
(Plan 5) einbaut, sucht sie nach W2 in `darstellung.py` und legt die Zählung dort ein
zweites Mal an, genau den Fehler, den 335 beseitigt.

**Gegenvorschlag.** In W2 eine Zeile für `kennungen.py` („Kennungen nach W4 ↔ Spieler und
Einheiten der Ablage; kennt Flask nicht“), bei `darstellung.py` den Satz zur Vergabe auf
`kennungen.py` verweisen. Ob „kennt Flask nicht“ wie bei `darstellung.py` in
`formregeln/importvertrag.py` gehört, entscheidest du.

**Stellungnahme.** Angenommen. W2 nennt `kennungen.py` (Kennungen nach W4 ↔ *Spieler* und
*Einheiten* der *Ablage*, nur hier wird gezählt); `darstellung.py` bildet „Spieler <n>“ aus
dieser Kennung; W4 verweist auf `kennungen.py`. Statt „kennt Flask nicht“ je Modul gilt in W2:
Flask und Werkzeug importieren nur `anwendung.py` und `server.py`. Die Prüfung dafür ist
Anliegen 343 an den Regelumsetzer; bis dahin prüft `importvertrag.py` nur `darstellung.py`.
