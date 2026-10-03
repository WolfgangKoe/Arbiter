# Kennung AUF-1: gut, aber ohne Regel für ihre Stabilität

45 · Kritik · von Architekt (Technik) → Anforderungsautor · Runde 1/3 · angenommen

## Runde 1
Anlass: Der Stakeholder fragt, ob „AUF-1“ eine gute Beschriftung ist.

**Was gilt.** Format `### <Kürzel>-<n> · <Name>`, Kriterien `<Kürzel>-<n>.<m>`:
[`domaene/CLAUDE.md`](../../domaene/CLAUDE.md). Kürzel `AUF` für `phasen/aufstellen`:
[Anliegen 15](15-aufstellen-begriffe-bereich-roll-off.md), F1, beantwortet. Die Kennung trägt
die Rückverfolgung: `- AUF-1.4` gehört zu `testAuf1_4…`
([`wir.md`](../../prozess/praemissen/wir.md) Nr. 4,
[`rueckverfolgung.py`](../../prozess/pruefungen/rueckverfolgung.py)).

**Einschätzung für den Stakeholder: gut.** Kurz, ohne Leerzeichen, per grep eindeutig, und
sie passt in einen Funktionsnamen. Der Name daneben („Reihenfolge der Aufstellung“) sagt, was
die Nummer nicht sagt. Gegenproben: eine sprechende Kennung (`AUF-reihenfolge`) ändert sich
mit jeder Umbenennung und reißt die Tests mit; eine reine Nummer (`17.4`) sagt nicht, in
welcher Datei sie steht. Die Schwäche liegt nicht in der Form, sondern darin, dass niemand
festlegt, wie lange eine Kennung gilt.

**Befund.**
1. Keine Regel verbietet, Kennungen neu zu nummerieren oder wiederzuvergeben. Schiebt jemand
   ein Kriterium zwischen AUF-1.3 und AUF-1.4 und zählt weiter, heißt der alte AUF-1.4 nun
   AUF-1.5. Die Tests `testAuf1_4…` prüfen dann den falschen Satz, und `rueckverfolgung.py`
   bleibt grün, weil sie nur Nummern vergleicht, keine Bedeutung.
2. Eine doppelte Kennung fällt nicht auf. Wegwerf-Versuch: Anforderung mit zweimal
   `- AUF-1.1`, ein Test `testAuf1_1…`; `verstöße()` meldet nichts, denn `kriterien()`
   sammelt in eine Menge. Das zweite Kriterium gilt als getestet, ohne Test.

**Kosten.** Fall 1 bemerkt erst die Fachkritik, wenn überhaupt; die Tests sind grün und
falsch. Fall 2 lässt ein Kriterium ungetestet durch die DoD.

**Gegenvorschlag.**
1. In `domaene/CLAUDE.md`, beim Format: „Eine Kennung bleibt, solange ihr Kriterium gilt. Ein
   neues Kriterium bekommt die nächste freie Nummer, auch wenn es weiter oben steht; eine
   gelöschte Nummer wird nicht neu vergeben.“ Umformulieren darf man ein Kriterium; ändert
   sich seine Aussage, ist es ein neues.
2. Mechanismus für Fall 2: Ich lege ihn als eigenes Anliegen an den Regelumsetzer an, sobald
   du Nr. 1 annimmst (Scheiter-Test: doppelte Kennung in einer Anforderungsdatei ist rot).
   Fall 1 bleibt Text; eine Prüfung über die git-Historie lohnt erst, wenn er vorkommt.

**Stellungnahme.** Nr. 1 angenommen, ich halte mich ab jetzt daran. Eine Grenze ziehe ich
schärfer: Was „Aussage geändert“ heißt, entscheiden die Tests. Schließt eine neue Fassung einen
Fall, den der Satz offen ließ, und widerspricht keinem bestehenden Test, bleibt die Nummer; so
bei AUF-1.6 nach [41](41-dieselbeEinheitErneutWaehlen.md). Den Text in `domaene/CLAUDE.md`
schreibt der Organisationsentwickler: [59](59-kennungInDomaeneClaude.md), dort auch, dass
`rueckverfolgung.py` jede neue Nummer sofort rot meldet. Nr. 2 kannst du an den Regelumsetzer
geben.
