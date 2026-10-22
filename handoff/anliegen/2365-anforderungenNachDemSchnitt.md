# Anforderungen und Glossar nach dem neuen Schnitt der Etappen

Form: Kritik
Von: Planer
An: Anforderungsautor
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): Teil A hält auf, Plan 7
streicht AUF-17 mit Test; Teil B wartet auf die Domänenphase von Etappe 2. Der Stakeholder hat
den Schnitt entschieden: [2361](2361-schnittDerEtappen.md) F1 A (‚keine Kohärenz‘ ist nie zu
übergehen, bei keiner Bewegung, `core_rules.txt:434`), F2 A, F3 A;
[2362](2362-etappenVorschlag.md) (AUF-13 entfällt); [2363](2363-schnittBewegungsformenZuerst.md);
[2364](2364-fahrzeugMoralSiegpunkte.md) F1 B, F2 B, F3 A, F4 A. Die Etappen stehen in
[domaene/etappen/](../../domaene/etappen/). Damit sind diese Anforderungen veraltet:

Teil A, für Plan 7:
1. [AUF-13](../../domaene/anforderungen/phasen/aufstellen/gesperrtesBeenden.md) und
   [AUF-17](../../domaene/anforderungen/phasen/aufstellen/zurueckOhneSperre.md) streichen;
   ihre Kennungen kommen nicht wieder.
2. [AUF-10](../../domaene/anforderungen/phasen/aufstellen/beenden.md) hält fest, dass
   ‚keine Kohärenz‘ nicht zu übergehen ist.
3. AUF-13 und *zurück* herausnehmen aus [QUE-5](../../domaene/anforderungen/querschnitt/uebergehen.md)
   (Zweck), [QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md), AUF-12.6
   („bietet *gemeinsam übergehen* nicht an“), AUF-26 (Zweck „ohne ‚zurück‘“) und dem
   [Glossar](../../domaene/glossar.md): *zurück* streichen; *gemeinsam übergehen*, *Protokoll*
   und *Sperre* nennen die Ausnahme ‚keine Kohärenz‘ und nicht mehr Etappe 1.

Teil B, neu für [Etappe 2](../../domaene/etappen/02-bewegen.md), wenn ihr Zyklusziel sie
verlangt:
4. Phasenfolge: sieben Phasen, Schlachtrunde, Spieler am Zug; eine nicht begleitete Phase ist
   leer und endet ohne Spielhandlung (Anliegen 07, dort dir zugedacht); Ende nach der fünften
   Schlachtrunde (`:2337`).
5. Erster Zug: Wer am Tisch den Roll-off gewinnt, wählt am Bildschirm (`:2329`, 2361 F3 A).
6. Normal Move und Advance (`:738`), Wurf als Zahl (Anliegen 09 F4, Empfehlung A); *Sperren*:
   über M oder M plus Wurf, über eine fremde *Base*, über die Kante, in Engagement Range, am
   Ende ohne *Kohärenz*. Zurücksetzen bis zum Ende der Bewegungsphase: Die *Einheit* steht wie
   vorher und darf neu bewegen (2364 F4 A). Vorbild für das Ziehen: ArbiterMap.
7. *Gemeinsam übergehen* beim Bewegen, jede *Sperre* außer ‚keine Kohärenz‘ (QUE-5).
8. Ausgangslage: ein Ork-Psioniker und eine Canoptek-Spinne, sofern ihre *Base* rund ist,
   sonst mit den Fahrzeugen in Etappe 4 (2364 F1).

**Kosten.** Ohne Teil A kann der Testautor den Test zu AUF-17 nicht streichen, und Glossar und
Kriterien versprechen ein Übergehen, das es beim Aufstellen nicht mehr gibt.

**Gegenvorschlag.** Wie oben. Empfehlung zu 2: Der Grundsatz steht einmal, in QUE-5 (‚keine
Kohärenz‘ bietet *gemeinsam übergehen* nie an), AUF-10 verweist darauf ([Wir 3](../../prozess/praemissen/wir.md));
so gilt er in Etappe 2 ohne neues Kriterium auch beim Bewegen.
Erledigt, wenn Teil A umgesetzt ist; Teil B nimmst du mit dem Zyklusziel von Etappe 2 auf.

**Stellungnahme.**
