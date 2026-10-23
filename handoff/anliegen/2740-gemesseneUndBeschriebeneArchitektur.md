# Gemessene und beschriebene Architektur

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: rückfrage

## Runde 1
**Befund.** Recherche zu deinem Kommentar in [2570](2570-architekturUeberDemHoechstmass.md):
[Mammutmap](https://github.com/MichiSpebach/mammutmap) zeigt ein Projekt als Karte zum
Zoomen, Ordner und Dateien als Kästen, Importe als Pfeile; als Erweiterung für VS Code
(0.9.9, 271 Installationen) und im Browser. Die Pfeile zieht ein Plugin aus den Importen,
gebaut für TypeScript. Im letzten öffentlichen Quellcode (0.5.3, 2022, Lizenz „TODO“; heute
liegt nur noch die Beschreibung offen) erkennt das allgemeine Plugin `import a.b`, nicht
`from a.b import c`; so schreibt Arbiter alle 60 Importe zwischen seinen Modulen. Die Karte
legt ihre Kästen als JSON-Dateien im Projekt ab (Ordner `map/`). Agenten bedienen sie nicht:
Sie ist ein Bild für dich, kein Maß.

Gemessen habe ich selbst, mit einem Wegwerf-Versuch (60 Zeilen Python über die Importe):
- Pfeile zwischen den Schichten: `web/` → Domäne (11 Importe), `katalog/` → Domäne (2),
  `__main__.py` → Domäne, Katalog, Web. Die Domäne importiert nichts von außerhalb. Das
  stimmt mit A1, A2 und W1 der [Architektur](../../technik/architektur.md) überein.
- Abweichung: `anwendung/` und `speicher/` gibt es noch nicht; 2.905 Zeichen beschreiben
  sie im Voraus. Darum spricht `web/` direkt mit der Domäne; A4 gilt erst mit dem
  Speicher. Die Seite beschreibt O5 als vier Module, heute ist sie eines (`seite.js`,
  10.776 Zeichen); Item 1 von Plan 7 teilt es.
- Gewicht, Zeichen Code gegen Architektur: Domäne 30.678 gegen 3.565, Web und Seite 33.509
  gegen 22.082, Anwendung und Speicher 0 gegen 2.905. Am meisten beschrieben ist die
  Grenze zwischen Web und Seite, nicht die Domäne.

**Kosten.** Ohne Maß fällt eine Abweichung nur auf, wo eine Regel eine Prüfung hat
(A1, W1: `formregeln/importvertrag.py`); den Rest sieht nur, wer beides liest.

**Gegenvorschlag.**

**F1 · Womit vergleichen wir Code und Architektur?**
Empfehlung: nicht mit Mammutmap. Der Importvertrag liest die Importe schon und prüft A1, A2
und W1; er kann im Review zusätzlich die beiden Tabellen oben zeigen: Pfeile zwischen den
Schichten und Zeichen je Schicht. Das ist eine Ausgabe, keine neue Prüfung; bauen würde sie
der Regelumsetzer in der Prozessphase. Folge: Du siehst in jedem Review, ob Code und
Architektur auseinanderlaufen, ohne Werkzeug. Willst du die Karte trotzdem sehen: die
Erweiterung auf einer Kopie des Projekts, damit `map/` nicht in git landet.
Antwort: .

**Stellungnahme.**
Kommentar: So wie ich dich verstehe, haben wir schon alle Tests zur Architektur. Das wäre fein. Wäre es dennoch möglich, für eine Art Karte im Dashboard für die Architektur zur Verfügung zu stellen?
