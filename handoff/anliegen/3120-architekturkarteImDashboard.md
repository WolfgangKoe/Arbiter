# Das Dashboard zeigt die Architektur als Karte

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Der Stakeholder hat in [2740](2740-gemesseneUndBeschriebeneArchitektur.md)
F1 mit A entschieden und „Setze es mal um“ kommentiert: Das Dashboard zeigt die
Architektur als Bild wie die Belegung. Es fehlt. Die erlaubten Importe stehen heute nur
verstreut: A1 als Code in `formregeln/importvertrag.py`, A2, A4 und W5 nur als Text in der
[Architektur](../../technik/architektur.md#abhängigkeiten-zeigen-nach-innen).

**Kosten.** Ohne Karte sieht der Stakeholder eine falsche Abhängigkeit oder eine Schicht mit
viel Code und wenig Beschreibung nur, wenn er Code und Architektur liest. Hält nicht auf.

**Gegenvorschlag.** Als Prozess-Item der Retro 7:
- Kästen: Seite (`technik/frontend/`), Web, Anwendung, Katalog, Speicher, Domäne (je
  `technik/arbiter/<ordner>/`), Start (`technik/arbiter/__main__.py`).
- Pfeile: Importe aus Dateien eines Kastens in Module eines anderen, mit Anzahl der
  Importzeilen. Heute: Web → Domäne 11, Katalog → Domäne 2, Start → Domäne, Katalog, Web.
  Seite → Web ist fest gezeichnet, Aufschrift „HTTP“, ohne Zahl.
- Erlaubt, einmal als Tabelle, die Importvertrag und Karte lesen: Start → alle (W5);
  Web → Anwendung (A4), Web → Domäne nur, solange `anwendung/` fehlt; Anwendung → Domäne
  (A4); Katalog → Domäne (A2); Speicher → Anwendung (P1); Domäne → keiner (A1). Jeder
  andere Pfeil ist rot. Der Importvertrag nimmt A1 aus der Tabelle; weitere Prüfungen
  entstehen nicht, die Karte zeigt nur.
- Je Kasten: Zeichen Code (Seite: `.html`, `.css`, `.js`; sonst `.py`, ohne
  `__pycache__`) gegen Zeichen Architektur, das ist `technik/architektur/<ordner>.md`
  (Seite: `frontend.md`), nach der Gliederung aus 2570. Fehlt die Datei, steht „keine
  Datei“; bis zum Umordnen in Plan 8 ([3051](3051-architekturUmordnenInPlan8.md)) gilt das
  für Seite, Katalog und Domäne. Eine Zeile unter der Karte nennt die Zeichen der Übersicht
  (`technik/architektur.md`) und des Vertrags (`technik/architektur/vertrag/`).
- Ein Kasten ohne Code ist gestrichelt; heute Anwendung und Speicher.

Bestehende Regel, die das abdeckt: [Regeln](../../prozess/regeln/rollenregeln.md), Zeile
„Dashboard“, erweitert um die Karte; Vorbild für das Bild `rollenregeln/dashboardDiagramm.py`.
Der Code zählt als Prüfcode gegen die [Kennzahl](../../prozess/kennzahlen.md#kennzahlen).
Erledigt, wenn ein Test an einem Baum unter `/tmp` einen verbotenen Pfeil rot und einen
Kasten ohne Code gestrichelt zeigt, `importvertragTest.py` grün bleibt und das Dashboard
heute keinen roten Pfeil zeigt.

**Stellungnahme.**
