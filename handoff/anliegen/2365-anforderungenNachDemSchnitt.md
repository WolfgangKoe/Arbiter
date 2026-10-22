# Anforderungen und Glossar nach dem neuen Schnitt der Etappen

Form: Kritik
Von: Planer
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): Teil A hält auf, Plan 7
streicht AUF-17 mit Test; Teil B wartet auf die Domänenphase von Etappe 2. Der Stakeholder hat
den Schnitt entschieden: Anliegen 2361 F1 A (‚keine Kohärenz‘ ist nie zu
übergehen, bei keiner Bewegung, `core_rules.txt:434`), F2 A, F3 A;
Anliegen 2362 (AUF-13 entfällt); Anliegen 2363;
Anliegen 2364 F1 B, F2 B, F3 A, F4 A. Die Etappen stehen in
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

**Stellungnahme.** Teil A umgesetzt: AUF-13 gelöscht; der Grundsatz steht einmal, in
neu [QUE-5.5](../../domaene/anforderungen/querschnitt/uebergehen.md) (ohne Test, wartet mit
QUE-5), AUF-10 verweist darauf; QUE-5, QUE-7.1, AUF-26 und [Glossar](../../domaene/glossar.md)
ohne AUF-13, mit der Ausnahme. Nach 2221: *Ablage* heißt *Armeeliste*. AUF-17 und *zurück*
lösche ich nach der Freigabe im selben Schritt, in dem der Testautor den Test löscht (wie
801): Ohne Anforderung ist `formregeln/benennung.py` für die Testdatei rot.
Nicht umgesetzt: AUF-12.6 bleibt. Es verspricht kein Übergehen, es sagt, dass keines
angeboten wird; das bleibt wahr, und sein Test prüft es. Streichen kostete neue Kennung und
Test ohne Änderung am Bildschirm. Teil B mit dem Zyklusziel von Etappe 2. AUF-8.4 (2312):
[2370](2370-auf8_4EntfaelltMitTest.md).
