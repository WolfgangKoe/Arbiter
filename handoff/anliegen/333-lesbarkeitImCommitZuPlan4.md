# Lesbarkeit im Commit zu Plan 4

333 · Kritik · von Reviewer (Technik) → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Fünf kleine Stellen aus 6bea166, nach [Es](../../prozess/praemissen/es.md):
1. `_spieler` in [darstellung.py](../../technik/arbiter/web/darstellung.py): Der Parameter
   `nummer` ist die Spielernummer, die Comprehension darunter bindet `nummer` neu als
   Einheitennummer. Richtig nur, weil die Comprehension einen eigenen Gültigkeitsbereich hat.
2. [anwendung.py](../../technik/arbiter/web/anwendung.py): `# Regel: web.md, V4` nennt die
   falsche Fundstelle; V4 steht in `technik/architektur/vertrag.md`. Der Modul-Docstring nennt
   nur „Dateien und Spielstand liefern“, nicht mehr alles, was das Modul tut (S).
3. `auswahlSenden` in [seite.js](../../technik/frontend/seite.js) liest jede Antwort als JSON.
   Bei 404 oder 400 liefert Flask HTML: `antwort.json()` wirft, die Ablehnung bleibt
   unbehandelt, die Seite zeigt den alten Stand ohne Hinweis.
4. [anwendungTest.py](../../technik/tests/einheit/web/anwendungTest.py):
   `testEinePfadOhneEinheitInDerAblageIstNichtGefunden` (Grammatik: „Ein Pfad“).
5. Ebenda wählt `next(iter(aufstellung.ausgangslage.tiefen))` eine *Aufstellungszone* über
   die Reihenfolge eines Mappings, wo `Aufstellungszone.erste` gemeint ist.

**Kosten.** 1 und 4: Der Name trägt nicht die Bedeutung, ein Leser verwechselt die beiden
Kennungen. 2: Wer die Regel sucht, findet sie unter der Fundstelle nicht. 3: Spätestens mit
der ersten *Handlung* über HTTP (W3: 409 mit Gründen) muss die Seite andere Antworten als 200
behandeln; dann wächst der Fehler mit jeder Route. 5: Ein Umweg, der eine Reihenfolge
voraussetzt, die nirgends zugesichert ist.

**Gegenvorschlag.**
1. In `_spieler` `einheitennummer` (wie in `anwendung.py`), oder den Parameter `spielernummer`.
2. `# Regel: vertrag.md, V4 (…)`; Docstring etwa „Flask: liefert das Frontend, den Spielstand
   und nimmt die Auswahl an (web.md, W1, W2; vertrag.md, V2)“.
3. Nur bei `antwort.ok` die Antwort zeichnen, sonst den Spielstand nach V1 neu holen und
   zeichnen. Wenn du es lieber mit W3 in Plan 5 löst, sag es in der Stellungnahme.
4. `testEinPfadOhneEinheitInDerAblageIstNichtGefunden`.
5. `Aufstellungszone.erste`.

**Stellungnahme.**
Angenommen, alle fünf. 1 `spielernummer`/`einheitennummer` in `_spieler`; 2 Fundstelle und Docstring; 3 die Seite zeichnet nur bei `antwort.ok` die Antwort, sonst den neu geholten Spielstand (V1); 4 und 5 im Test.
