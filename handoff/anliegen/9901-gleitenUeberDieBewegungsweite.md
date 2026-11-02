# Gleiten an einer Base über Bewegungsweite, Kante und Nahkampfreichweite hinaus

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik am Plan 10, Item anhaltenAufDemWeg, hält auf (eine Sperre fehlt, die ein
Kriterium verlangt; Schritt 4 des Happy Path, „gleitet entlang“).
[BEW-17.1](../../domaene/anforderungen/phasen/bewegung/anhaltenVorFremdenBases.md) prüft nur,
ob die *Stelle* nach BEW-1.5 eine fremde *Base* *überdecken* würde, und zeigt dann wie AUF-29.1
und 29.2. Die nach AUF-29.2 verschobene *Stelle* prüft keine Regel mehr: Sie kann über der
*Bewegungsweite*, in *Nahkampfreichweite* eines Gegners oder über der Kante liegen, denn sie ist
die Ecke des Rechtecks aus voriger und neuer *Stelle*, nicht ein Punkt dazwischen. BEW-17.2
*setzt* dort „statt nach BEW-1.5“ und nennt keinen *Grund*, also ohne BEW-3.1, 6.1, 6.2 und
ohne *gemeinsam übergehen*.
Beispiel: Boy, *Bewegungsweite* 5″, vorige *Stelle* (0, 0). Die *Karte* zeigt ihn bei (0; 4,9).
Der Zeiger rückt, BEW-1.5 ergäbe (3,5; 3,5), 4,95″ weit, dort *überdeckte* er einen Boy einer
anderen *Einheit*, waagrecht allein nicht: Die *Karte* zeigt (3,5; 4,9), rund 6″ weit, Loslassen
*setzt* ihn dort. Der Regeltext verbietet das (`core_rules.txt:745` Move und Engagement Range,
`:729` Kante). Offen ist auch die Reihenfolge: [BEW-6.3](../../domaene/anforderungen/phasen/bewegung/anhaltenVorDerGrenze.md)
nimmt die kürzeste Strecke nur aus 3.1, 6.1, 6.2; BEW-6.4 und BEW-17.1 sagen beide, was die
*Karte* zeigt. ArbiterMap baut die Gleitkandidaten aus schon geklemmten Koordinaten
(`ArbiterMap/frontend/static/js/model_drag.js:1508`, `:1516`).

**Kosten.** Ein Satz in BEW-17.1 (noch ohne Test, darf neu gefasst werden), dazu ein Test mit
einem Boy, der nahe seiner *Bewegungsweite* entlanggleitet. Ohne: In der Partie steht ein Boy
6″ weit, ohne Anhalten, ohne *Eintrag*; genau den Fehler soll Arbiter verhindern (Ziel). Der
Testautor kann zu BEW-17 nicht eindeutig testen.

**Gegenvorschlag.** BEW-17.1 so fassen: Die *Karte* zeigt die verschobene *Stelle* nach
AUF-29.2 nur, wo BEW-3.1, 6.1 und 6.2 nicht anhalten würden, sonst nach AUF-29.1 auf dem
geraden Weg; und ein Kriterium, dass bei BEW-17.1 zusammen mit 3.1, 6.1 oder 6.2 die kürzeste
Strecke gilt wie BEW-6.3 (6.3 hat Tests, also neu). Keine Frage an den Stakeholder nötig, der
Regeltext entscheidet.

**Stellungnahme.** Angenommen in
[BEW-17](../../domaene/anforderungen/phasen/bewegung/anhaltenVorFremdenBases.md), ohne Frage:
- Reihenfolge: BEW-17.1 prüft die *Stelle*, an der die *Karte* nach BEW-1.7 und 6.4 zeigen
  würde, also erst Anhalten, dann Überdecken.
- Nach AUF-29.2 zählt ein Teil nur, wenn BEW-3.1, 6.1 und 6.2 auf ihm keines anhalten; sonst
  der andere Teil oder 29.1. In deinem Beispiel zählt der waagrechte Teil nicht.
- Neu BEW-17.3: nach 29.1 gilt mit 3.1, 6.1, 6.2 die kürzeste Strecke wie BEW-6.3.
BEW-17.2 nur kürzer gefasst. Folgen für das Item: 9940.

**Nachprüfung.** In Ordnung. BEW-17.1 prüft das *Überdecken* an der nach BEW-1.7 und 6.4
angehaltenen *Stelle*, ein Teil nach AUF-29.2 zählt nur ohne Anhalten aus BEW-3.1, 6.1 und 6.2,
BEW-17.3 nimmt auf dem Weg nach AUF-29.1 die kürzeste Strecke wie BEW-6.3. Im Beispiel zeigt die
*Karte* den Boy nicht mehr bei (3,5; 4,9). BEW-17 hat noch keinen Test, also keine Folgekosten.
