# Die Architektur ist länger, als sie sein darf

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Erlaubt sind je Datei 6.000 Zeichen, zusammen 24.000
([Kennzahlen](../../prozess/kennzahlen.md#höchstmaße)). Die Architektur hat 31.446:
[architektur.md](../../technik/architektur.md) 6.459,
[handlungen.md](../../technik/architektur/handlungen.md) 7.811. Eine Prüfung gibt es nicht.

**Kosten.** Jede Rolle liest die Architektur, bevor sie baut; je länger, desto eher
überliest sie eine Regel.

**Gegenvorschlag.** Darin stehen zwei Arten Text. *Regeln* gelten für allen Code, etwa A1
„Die Domäne importiert nur die Standardbibliothek“; sie wachsen kaum. Der *Vertrag* nennt je
Handlung Knopf, Adresse und Antwort, etwa „Einheit zurücklegen“ → `PUT /api/zurücklegen`;
er wächst mit jeder Handlung. Heute: Vertrag 12.444 Zeichen
([vertrag.md](../../technik/architektur/vertrag.md), handlungen.md), Regeln 19.002.

**F1 · Wie gliedert sich die Architektur?**
Empfehlung: wie die Technik. Eine Übersicht, dazu je Ordner in `technik/` eine Datei:
Domäne, Anwendung, Katalog, Speicher, Web, Seite, Tests. Heute stehen die Regeln der Domäne
in der Übersicht, die der Seite verteilt auf drei Dateien. Folge: Wer am Web baut, liest
Übersicht und `web.md`; ein neuer Ordner bringt eine neue Datei.
Antwort: Machen wir so

**F2 · Welche Grenzen gelten?**
- A: wie bisher, je Datei 6.000, zusammen 24.000. Folge: Vor Etappe 2 (Bewegen) fallen 7.500
  Zeichen weg, vor allem im Vertrag; Einzelheiten stehen dann nur in Tests und
  JSON-Beispielen, das Warum dazu fällt weg.
- B: je Datei 6.000, zusammen 6.000 je Datei aus F1. Folge: Jede Datei bleibt lesbar, aber
  nichts zwingt mehr, Regeln allgemein zu fassen; die Summe wächst mit jedem Ordner.
- C, Empfehlung: Regeln je Datei 6.000, zusammen 24.000; der Vertrag je Phase eine Datei
  (Aufstellen, Bewegen …) zu je 6.000, ohne Summe. Folge: Die Regeln bleiben knapp, denn
  eine neue Handlung braucht keine neue Regel; der Vertrag wächst mit dem Spiel, gelesen
  wird nur die Phase, an der gebaut wird. Heute hieße das: handlungen.md teilen, nichts
  kürzen.

Die Kennzahl schreibt danach der Organisationsentwickler um.
Antwort: C, das war doch die Empfehlung, oder?

**F3 · Wann ordne ich um?**
Empfehlung: in Plan 8 als erstes Item, ohne sichtbare Änderung; bis dahin trage ich nur
ein, was ein Item verlangt. Was Plan 7 streicht („zurück“, AUF-8.4), fällt dabei weg.
Antwort: Okay

**Stellungnahme.**
Kommentar: Mir fehlt schon wieder Kontext und Klarheit im Blick auf die Konsequenzen der Entscheidungen ich hier treffe. Wir sollten hier Limits setzen. Gleichzeitig kann eine Architektur für ein ständig wachsendes System nicht auf eine Datei beschränkt bleiben. Es muss die Struktur der Technik abbilden. Denk nochmal genau darüber nach. Mach auch mal eine Recherche nach der "mammutmap", die hilft die Beziehungen zwischen Dateien zu visualisieren. Das könnte helfen, die tatsächliche Architektur zu "messen" und mit der dokumentierten zu vergleichen.

**Klärung.** Die Fragen oben sind neu gefasst: F1 bildet die Struktur der Technik ab, F2
setzt Grenzen, die mit dem System mitwachsen, wo es nötig ist, und jede Wahl nennt ihre
Folge. Die Summe von 24.000 trifft vor allem den Vertrag, der mit jeder Handlung wächst;
deshalb trenne ich ihn von den Regeln. Mammutmap und der Vergleich mit dem gemessenen Code:
[2740](2740-gemesseneUndBeschriebeneArchitektur.md).
