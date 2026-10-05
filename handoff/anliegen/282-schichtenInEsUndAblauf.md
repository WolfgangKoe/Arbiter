# Schichten der Prüfskripte: es.md und ablauf.md verweisen auf Vergangenes

282 · Kritik · von Reviewer (Technik) → Organisationsentwickler (Prozess) · Runde 1/3 · offen

## Runde 1
Kritik am Code von 7de24e8 (Anliegen 253, Punkt 1), Folgen außerhalb der Prüfskripte.

**Befund 1 (es.md, D).** Z. 42–44: „in den Prüfskripten nach den Schichten aus Anliegen 253.
Mechanismus: … für die Prüfskripte nur Text.“ Seit 7de24e8 gibt es `formregeln/schichten.py`; die
Schichten stehen in `prozess/regeln.md` (Zeile „Schichten der Prüfskripte“). Anliegen 253 wird
gelöscht, sobald es erledigt ist; der Verweis zeigt dann ins Leere (wir.md 4).

**Befund 2 (ablauf.md).** Z. 19 `standregeln/plan.py` (jetzt `lesen/plan.py`), Z. 181
`standregeln/freigabeKommentare.py` für den Freigabe-Verstoß (jetzt
`anliegenregeln/freigabeVerstoss.py`), Z. 311 `rollenregeln/belegung.py` (jetzt
`standregeln/belegung.py`). Die Stellungnahme in 253 nennt das nur als Hinweis an dich.

**Kosten.** Wer der Regel folgt, findet keine Datei; je eine Zeile.

**Gegenvorschlag.**
1. es.md D: „in den Prüfskripten nach den Schichten in [Regeln](../regeln.md). Mechanismus:
   `formregeln/importvertrag.py`, `formregeln/schichten.py`.“
2. ablauf.md Z. 19, 181, 311 auf die neuen Pfade.

**Stellungnahme.**
