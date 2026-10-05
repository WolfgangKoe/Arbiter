# Schichten der Prüfskripte: es.md und ablauf.md verweisen auf Vergangenes

282 · Kritik · von Reviewer (Technik) → Organisationsentwickler (Prozess) · Runde 1/3 · angenommen

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

**Stellungnahme.** Befund 2 umgesetzt in [Ablauf](../../prozess/ablauf.md), dazu weitere alte Pfade aus 253 P2: Z. 19 `lesen/plan.py`; Z. 23 `standregeln/phasenfolge.py` (`domänenphase`, `planOhneFreigabe`); Z. 173 f. `anliegenregeln/freigabeSperre.py` (Write, Edit) statt `statusrecht.py`, `pfadsperren.py` (`istFreigabeArtefakt`); Z. 185 `rollenregeln/freigabeCommit.py`; Z. 287 und 306 `anliegenregeln/anliegenDran.py` (`eskaliert`, `beantwortetDurchFreigabe`); Z. 325 `standregeln/belegung.py`. Z. 180 bleibt: `standregeln/freigabeKommentare.py` (`hatKommentarOhneStellungnahme`) trägt „Autor dran“; der Freigabe-Verstoß steht in Z. 173. Jeder Pfad im Ablauf existiert (per Skript geprüft). Dieselben Reste in `prozess/regeln.md` und eine Prüfung dagegen: [284](284-pfadverweiseAufPruefskripte.md). Befund 1 betrifft eine Prämisse: F1. Erledigt erst nach F1.

**F1 · es.md, SOLID D, Satz zu den Prüfskripten ersetzen durch „in den Prüfskripten nach den Schichten in [Regeln](../regeln.md). Mechanismus: `formregeln/importvertrag.py`, `formregeln/schichten.py`.“?** A ja (Empfehlung: Anliegen 253 wird gelöscht, die Schichten stehen genau einmal in `regeln.md`, wir.md 3 und 4), B nein.
Antwort: .
