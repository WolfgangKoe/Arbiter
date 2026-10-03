# Stand: Review schreiben überspringt die Fachkritik

50 · Kritik · von Reviewer (Technik) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** [`ablauf.md`](../../prozess/ablauf.md), Technikphase: 4 Reviewer (DoD, Code),
5 Fachkritiker (Abnahme), 6 Reviewer schreibt `handoff/review.md`. Der Stand
([`stand.py`](../../prozess/pruefungen/stand.py), Zeile 96) meldet nach grünen Tests
„Implementierer, dann Reviewer: Tests grün, Review <n>“ und wechselt in die Prozessphase,
sobald `review.md` die Zyklusnummer trägt. Schritt 5 kommt im Stand nicht vor; wer dem Stand
folgt, schreibt das Review vor der Abnahme. So in Zyklus 1: Review 1 steht, die fachliche
Abnahme und das Löschen des Items (DoD 3, 4) fehlen.

**Kosten.** Die Prozessphase beginnt mit offener DoD; die Abnahme hängt an keinem Auslöser
und kann ausfallen. Das Review muss zwei DoD-Punkte als offen führen.

**Gegenvorschlag.** Der Stand trennt die Schritte: nach grünen Tests „Reviewer: Review der
Technik (Schritt 4)“, nach dessen Kritik-Commit „Fachkritiker: Abnahme“, und erst wenn das
Item gelöscht ist (`domaene/items/` ohne Item des Plans), „Reviewer: `handoff/review.md`“.
Erkennbar ist die Abnahme am gelöschten Item. Scheiter-Test: Plan n, Tests grün, Item noch
vorhanden → Stand nennt den Fachkritiker, nicht die Prozessphase. Alternativ Schritt 6 so
umformulieren, dass das Review vor der Abnahme steht und die Abnahme als offener Punkt in
die Prozessphase geht.

**Stellungnahme.**
