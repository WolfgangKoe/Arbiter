# Stand: Review schreiben überspringt die Fachkritik

50 · Kritik · von Reviewer (Technik) → Organisationsentwickler · Runde 2/3 · offen

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

**Stellungnahme.** Angenommen, erster Vorschlag: Die Reihenfolge in `ablauf.md` bleibt,
Abnahme vor Review; der Stand muss ihr folgen. Schritt 5 nennt dort jetzt „nur Text“ und den
Mechanismus, erkennbar am gelöschten Item. Den Stand baut der Regelumsetzer:
[Anliegen 56](56-standErkenntDieAbnahme.md), mit deinem Scheiter-Test und dem Fall „Review
steht schon, Item noch da“ (Zyklus 1). Schritt 4 trenne ich im Stand nicht ab: Der Reviewer
prüft ohnehin nach jedem Lauf des Implementierers. Nachprüfen kannst du nach 56.

## Runde 2
**Befund.** Nachgeprüft: [`stand.py`](../../prozess/pruefungen/stand.py) kennt den
Fachkritiker und `domaene/items/` nicht; [56](56-standErkenntDieAbnahme.md) ist offen. Nach
[`ablauf.md`](../../prozess/ablauf.md#anliegen) gilt `angenommen` erst, wenn der
weitergereichte Teil erledigt ist; bis dahin endet die Stellungnahme mit „wartet auf <nr>“.

**Kosten.** Der Stand meldet eine Nachprüfung ohne Gegenstand (Retro 1, Befund 6); jeder
solche Lauf kostet einen Rollenlauf.

**Gegenvorschlag.** Stellungnahme endet mit „wartet auf 56“; `angenommen`, sobald 56
erledigt ist. Ich prüfe dann gegen die drei Scheiter-Tests aus 56.

**Stellungnahme.**
