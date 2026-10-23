# Gemessene und beschriebene Architektur

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Recherche zu deinem Kommentar in Anliegen 2570:
[Mammutmap](https://github.com/MichiSpebach/mammutmap) zeigt ein Projekt als Karte zum
Zoomen, Ordner und Dateien als Kästen, Importe als Pfeile, in VS Code und im Browser. Die
Pfeile zieht ein Plugin für TypeScript; `from a.b import c`, wie Arbiter alle 60 Importe
zwischen seinen Modulen schreibt, erkennt es nicht. Agenten bedienen die Karte nicht.

Gemessen habe ich selbst, mit einem Wegwerf-Versuch über die Importe:
- Pfeile zwischen den Schichten: `web/` → Domäne (11 Importe), `katalog/` → Domäne (2),
  `__main__.py` → Domäne, Katalog, Web. Die Domäne importiert nichts von außerhalb, wie A1,
  A2 und W1 der [Architektur](../../technik/architektur.md) verlangen.
- Abweichung: `anwendung/` und `speicher/` gibt es noch nicht; 2.905 Zeichen beschreiben
  sie im Voraus. Darum spricht `web/` direkt mit der Domäne; A4 gilt erst mit dem Speicher.
- Zeichen Code gegen Architektur: Domäne 30.678 gegen 3.565, Web und Seite 33.509 gegen
  22.082, Anwendung und Speicher 0 gegen 2.905.

**Kosten.** Ohne Maß fällt eine Abweichung nur auf, wo eine Regel eine Prüfung hat; den
Rest sieht nur, wer Code und Architektur liest.

**Gegenvorschlag.**

**F1 · Wie zeigt das Dashboard die Architektur?**
Als Bild wie die Belegung: je Schicht ein Kasten (Seite, Web, Anwendung, Katalog, Speicher,
Domäne, Start), Importe als Pfeile mit ihrer Anzahl, je Kasten Zeichen Code gegen
Architektur. Ein Pfeil, den die Architektur verbietet, ist rot; eine beschriebene Schicht
ohne Code ist gestrichelt. Welche Pfeile erlaubt sind, steht einmal, für Importvertrag und
Karte. Heute: kein Pfeil rot, Anwendung und Speicher gestrichelt. Bauen würde sie der
Regelumsetzer in der Prozessphase; sie prüft nichts, sie zeigt.
- A, Empfehlung: nur die Schichten. Folge: Auf einen Blick siehst du, ob eine Schicht fehlt,
  falsch importiert oder viel Code bei wenig Beschreibung hat. Kosten etwa wie das Bild der
  Belegung (`dashboardDiagramm.py`, 138 Zeilen); das zählt als Prüfcode gegen die
  [Kennzahl](../../prozess/kennzahlen.md#kennzahlen).
- B: dazu die Module in den Kästen, wie Mammutmap. Folge: Du siehst, welches Modul groß ist
  und wer es nutzt; heute 25 Module, 15 davon in der Domäne, das wird eng im Kasten. Mehr
  Code als A.
- C: keine Karte; der Importvertrag zeigt im Review zwei Tabellen: Pfeile und Zeichen je
  Schicht. Folge: am billigsten, aber kein Bild.
Antwort: A

**Stellungnahme.**
Kommentar: So wie ich dich verstehe, haben wir schon alle Tests zur Architektur. Das wäre fein. Wäre es dennoch möglich, für eine Art Karte im Dashboard für die Architektur zur Verfügung zu stellen?

**Klärung.** Nicht alle. Von 42 Regeln prüft 29 eine Prüfung oder ein Test. 6 stehen nur
als Text (A3, A4, M1, P1 bis P3), die meisten für `anwendung/` und `speicher/`; ihre Prüfung
entsteht mit dem ersten Modul dort. 7 sind nur teilweise geprüft (A2, D3, W2, W5, O1, O3,
O5), etwa welches Modul der Seite welches nutzen darf (O5). Die Karte ist möglich, F1 ist
dafür neu gefasst. Mit der Gliederung aus 2570 (je Ordner eine Datei) ist „Zeichen
Architektur“ je Kasten die Größe seiner Datei. Zu 2570, F2: Ja, C war die Empfehlung; die
Kennzahl ändert [3050](3050-hoechstmassDerArchitekturNach2570.md), das Umordnen kommt
mit [3051](3051-architekturUmordnenInPlan8.md) in Plan 8.
Kommentar: Setze es mal um, und dann gebe ich ggf. Feedback
