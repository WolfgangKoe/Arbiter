# AUF-28.1 widerspricht AUF-16.3 und 16.6, AUF-23 folgt nicht deiner Antwort in 2062

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf, zwei Schritte
des Zyklusziels aus [Review 6](../review.md) („über der Kante loslassen setzt, wo die *Karte*
zuletzt zeigte“, „*zurücklegen*“).
1. [AUF-28](../../domaene/anforderungen/phasen/aufstellen/loslassenWoDieKarteZeigt.md) ersetzt
   AUF-16.3 und 16.6 nur im Zweck. Beide stehen in
   [AUF-16](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md) mit vollem
   Wortlaut, ihre Tests auch: Lässt man ein Boy der *Einheit in Aufstellung* auf der *Ablage* des
   anderen los, verlangt 16.3 die *Sperre* ‚nicht wählbar‘, 28.1 das *Setzen*. Lässt man es neben
   *Karte* und *Ablagen* los, verlangt 16.6 Zurückspringen, 28.1 das *Setzen*. AUF-16.3 betrifft
   nur *gesetzte* *Modelle* der *Einheit in Aufstellung*, ist also ganz ersetzt. AUF-12.5 nennt
   16.3 weiter. Das ist derselbe Rest wie in 2090, Punkt 1.
2. AUF-23 und 28.1 folgen deiner Annahme A aus
   [2062](2062-zuruecklegenNurAufDerEigenenEinheit.md). Die Antwort des Stakeholders dort ist
   eine andere: *zurücklegen* per Knopf neben „Aufstellen der Einheit beenden“, kein Zug auf die
   *Ablage*. Damit fehlt der Schritt *zurücklegen*, wie er ihn will. Ändert sich AUF-23, entfällt
   auch die Ausnahme „nicht auf ihrer *Einheit* in der *Ablage*“ in 28.1.

**Kosten.** Zu 1: Der Testautor kann 28.1 nicht prüfen, ohne dass die Tests zu 16.3 und 16.6
rot werden. Die Rückverfolgung verlangt dann widersprüchliche Tests. Zu 2: Plan 7 baut ein
*Zurücklegen*, das der Stakeholder nicht beschreibt. Mit „zurück“ (AUF-13) stünde dann ein
zweiter, ähnlich benannter Knopf daneben.

**Gegenvorschlag.**
1. AUF-16.3 streichen samt Test. AUF-16.6 als neues Kriterium nur noch für das, was 28.1 nicht
   regelt. AUF-12.5 ohne 16.3.
2. Erst 2062 klären. Gilt der Knopf: AUF-23 neu als Klick auf einen Knopf, mit Namen, Zeitpunkt
   und dem, was danach am Bildschirm geschieht (DoR 6). AUF-28.1 dann ohne Ausnahme für die
   eigene *Ablage*. Danach braucht UX ein Mockup zum Knopf.

Nachprüfung zu 1610: Punkte 2 und 3 sind in AUF-8.7 und AUF-29 umgesetzt, Punkt 1 geht hier
weiter. 1610 und 978 hast du als Empfänger selbst auf `erledigt` gesetzt. Das setzt nach
[Ablauf, Anliegen](../../prozess/ablauf.md#anliegen) der Absender.

**Stellungnahme.** Angenommen.
1. AUF-16.3 und 16.6 gestrichen. Neu AUF-16.8 für den Rest: ein *gesetztes* *Modell* einer
   *aufgestellten* *Einheit* neben *Karte* und *Ablagen*. Der Zweck von AUF-16 verweist auf
   AUF-28. AUF-28.1 gilt neben der *Karte*, „auch auf einer *Ablage*“. AUF-12 (Zweck) und 12.5
   ohne 16.3; 12.5 bleibt, weil es nur enger wird und die übrigen Fälle gleich bleiben.
2. 2062 ist geklärt: *zurücklegen* per Knopf. AUF-23 neu: 23.1 Klick auf „Einheit
   zurücklegen“ legt die ganze *Einheit in Aufstellung* zurück, gleich welche *Ebene* sie hat;
   23.2 (‚nur ganze Einheit‘) gestrichen; 23.3 bleibt; 23.4 sagt, wann der Knopf da ist; 23.5
   gilt, wenn es keine *Einheit in Aufstellung* gibt. Zu AUF-23 gab es keine Tests. Name,
   *Ebene* und Zeitpunkt stehen als Annahme in [2220](2220-knopfZuruecklegen.md) F1 bis F3.
   AUF-28.1 hat keine Ausnahme mehr. Neu gefasst sind auch der Zweck von AUF-8 und *zurücklegen*
   im Glossar.

Für den Testautor, nur gelesen: In `loslassenOhneZielTest.py` entfallen `testAuf16_3…` und
die vier `testAuf16_6…`; dort verlangt jetzt AUF-28.1 das *Setzen*. AUF-16.8 hat noch keinen
Test. In `sperreOhneStelleTest.py:116` entfällt der Fall `auf16_3…` aus
`sperrendesLoslassen` (12.5, 12.6). Für den Architekten: `technik/architektur/handlungen.md:27`
und `:57` nennen AUF-16.6. Für UX: Der Knopf (AUF-23.4) braucht ein Mockup.
`domaene/mockups/auf-23-sperre.html` zeigt den gestrichenen *Grund* ‚nur ganze Einheit‘.
1610 und 978 stehen auf `angenommen`.
