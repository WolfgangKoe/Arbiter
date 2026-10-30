# Der Vertrag der Aufstellung ist voll

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** In Anliegen 2570 hast du F2 C gewählt: je Phase eine Vertragsdatei zu 6.000
Zeichen, „nichts kürzen“. Beim Umordnen (Plan 8) wurde
[aufstellen.md](../../technik/architektur/vertrag/aufstellen/) doch gekürzt, keine Regel
ging verloren, aber zwei Einzelheiten: die Namen der Abfragen zur *Auswahl* in V3 samt ihren
Kriterien und zwei erklärende Halbsätze zu V10 (Befund des Fachkritikers, Anliegen 5000).
Heute hat die Datei 5.991 von 6.000 Zeichen,
[querschnitt.md](../../technik/architektur/vertrag/querschnitt.md) 5.882. Item 3 von Plan 9
(AUF-30: Klick wählt eine *aufgestellte* *Einheit* aus) ändert den Vertrag der *Aufstellung*;
dafür ist kein Platz.

**Kosten.** Ohne Entscheidung muss ich beim Vertrag zu Item 3 wieder Einzelheiten weglassen;
die stehen dann nur noch in Tests und Code, Testautor und Implementierer raten.

**Gegenvorschlag.** Siehe F1.

**Stellungnahme.**

**F1 · Wie wächst der Vertrag einer Phase über 6.000 Zeichen?**
A: Eine volle Vertragsdatei wird ein Ordner, darin je Abschnitt eine Datei zu 6.000, ohne
Summe; für die *Aufstellung* `vertrag/aufstellen/` mit `auswahl.md`, `handlungen.md`,
`seite.md`, `ziehen.md`, die gekürzten Einzelheiten kommen zurück (Anliegen 2570 F1, wie die
Architektur je Ordner eine Datei). Folge: Wer an der *Auswahl* baut, liest knapp 2.000
Zeichen statt 6.000; ein Link mehr je Abschnitt.
B: Je Phase eine Datei, Höchstmaß 12.000 wie ein Code-Modul (Kennzahlen). Folge: einfach,
aber jede Rolle lädt den ganzen Vertrag, etwa doppelt so viele Token; voll in einigen Items.
C: Wie heute, je Item kürzen (Anliegen 2570 F2 A). Folge: Einzelheiten nur in Tests und Code.
Empfehlung: A. Den Satz in den [Kennzahlen](../../prozess/kennzahlen.md#höchstmaße) schreibt
danach der Organisationsentwickler um.
Annahme: Ohne Antwort bis zum Vertrag zu Item 3 teile ich `aufstellen.md` nach A.
Antwort: A
Kommentar: Eine zu groß gewordene Datei aufzuteilen scheint mir meistens das sinnvollste. Es muss nur sichergestellt sein, dass die Einzelteile am Ende an der richtigen Stelle sind und über den PFad einfach zu finden. Außerdem sollte es nicht zu viele Ebenen geben. Alles bis 3 Ebenen sehe ich als unproblematisch an. Die Frage ist aber immer, was am meisten Sinn hat.

**Nachprüfung.** Umgesetzt nach A. Die [Übersicht](../../technik/architektur.md#schichten)
verlinkt je Phase einen Ordner, darin heißt jede Datei wie ihr Abschnitt:
- *Aufstellung*: `vertrag/aufstellen/` mit
  [auswahl.md](../../technik/architektur/vertrag/aufstellen/auswahl.md) (V2, V3, V9),
  `handlungen.md`, `seite.md`, `ziehen.md` (V10). Zurück sind die Namen der Abfragen in V3
  samt Kriterien und die Halbsätze zu V10 (Anliegen 5000).
- *Schlacht* (5.965 von 6.000, voll): `vertrag/schlacht/` mit `tuer.md` (V11),
  `spielstand.md`, `uebergehen.md` (V18), `handlungen.md` (V12, V13), `seite.md`.
- *Bewegungsphase*: `vertrag/bewegung/` mit `auswahl.md` (V14, V19), `handlungen.md` (V15
  bis V17), `ziehen.md`, `seite.md`, `grenzkreise.md` (V20, V21). Sie hatte schon eine Datei
  im Ordner neben `bewegung.md`; so ist jede Phase gleich gebaut.

Ebenen: unter `technik/` drei Ordner (`architektur/vertrag/aufstellen/`), ab dem Projekt
vier. Flacher ginge nur mit Namen wie `vertrag/aufstellenAuswahl.md`; dann suchte man die
Abschnitte einer Phase zwischen denen der anderen. Die Beispiele (`*.json`) bleiben, wo die
Tests sie lesen. Die Summe der Architektur steht damit bei 24.000 von 24.000
([7090](7090-architekturVollFuerZusagenAus6995.md)). Den Satz in den Kennzahlen:
[7080](7080-kennzahlenVertragAlsOrdner.md).
