# Frontend und Backend parallel, mit Vertrag und Integrationstest

241 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Dein Auftrag aus Anliegen 238 (git): prüfen, ab wann Frontend und Backend
parallel laufen, mit Integrationstests. Heute läuft die
[Technikphase](../../prozess/ablauf.md#technikphase) nacheinander; gleichzeitig laufen nur
Rollen, die ausschließlich Anliegen schreiben. Claude Code kann Rollen gleichzeitig starten,
auch in eigener Arbeitskopie (`isolation: worktree`, code.claude.com/docs/en/sub-agents).

Parallel geht, wenn vor beiden Hälften drei Dinge stehen:
1. Vertrag: Der Architekt legt die HTTP-Schnittstelle zwischen `web/` und `frontend/` fest
   (`technik/architektur/web.md`): Pfade und je Antwort ein JSON-Beispiel.
2. Tests aus einer Quelle, vom Testautor, rot: Das Backend prüft der Flask-Testclient gegen
   das Beispiel; das Frontend prüft ein Bildschirmtest, in dem Playwright dasselbe Beispiel
   statt des Servers liefert. Sind beide grün, passen die Hälften zusammen, so weit der
   Vertrag reicht.
3. Integrationstest: derselbe Bildschirmtest gegen den echten Flask-Server. Er ist der
   Akzeptanztest des Items, grün erst mit beiden Hälften; danach prüft der Reviewer (DoD 1).

Dazu getrennte Schreibpfade, damit sich zwei Läufe nicht überschreiben.

Nicht in Zyklus 3: Den Vertrag gibt es noch nicht, ihn bringt erst der Wegwerf-Versuch des
Architekten ([Plan 3](../plan.md), Voraussetzung 3), und Item 2 baut auf Item 1. Erster
Kandidat ist „Wählen per Klick mit Speicher“ (Plan 3, Danach): eine Handlung über HTTP im
Backend, ihre Anzeige im Frontend.

**Kosten.** Gewonnen wird Wartezeit, nicht Belegung: Die Token bleiben, dazu kommt der
Vertrag. Ohne Vertrag rät jede Hälfte die Schnittstelle, der Fehler zeigt sich erst im
Integrationstest. Startet man den Implementierer zweimal, hat jeder Lauf beide Pfade;
`schreibgrenze.py` trennt sie nicht. Eigene Arbeitskopien trennen, brechen aber heute die
Hooks (`.git` ist dort eine Datei) und müssen zusammengeführt werden; Bedarf sehe ich nicht.

**Gegenvorschlag.**

**F1 · Ab wann laufen Frontend und Backend parallel?**
- A: Ab dem ersten Item, dessen Vertrag vor dem Testautor feststeht, frühestens Plan 4.
  Zyklus 3 bleibt nacheinander.
- B: Schon in Zyklus 3, nach dem Wegwerf-Versuch des Architekten.
- C: Gar nicht vorbereiten, erst wenn eine Retro Wartezeit als Befund zeigt.
Empfehlung: A. In Zyklus 3 entsteht der Vertrag erst; teilen hieße raten.
Antwort: .

**F2 · Wer baut die zweite Hälfte?**
- A: Ein Frontend-Implementierer mit `technik/frontend/`; der Implementierer gibt den Pfad
  ab. Neuer Auslöser der Rolle ([Rollen mit Auslöser](../../prozess/ablauf.md#rollen-mit-auslöser)):
  ein Item des freigegebenen Plans hat einen Vertrag und Tests beider Hälften.
- B: Der Implementierer zweimal, je mit Auftrag „nur Frontend“ oder „nur Backend“.
Empfehlung: A. Nur getrennte `schreibpfade` setzen die Trennung durch, bei B ist sie nur
Text. Bis zum Auslöser gilt 238 F1 A.
Antwort: .

Nach deiner Antwort, bei A und A: Ich ergänze den Auslöser und die Technikphase (Vertrag vor
Schritt 1, Schritt 3 für beide Hälften gleichzeitig) und lege die Rollendefinition vor, wenn
der Auslöser eintritt. Mechanismen baut der Regelumsetzer: Der Stand nennt beide
Implementierer zugleich (`standregeln/stand.py`); eine Prüfung, dass jedes Beispiel des
Vertrags in einem Test beider Hälften vorkommt. Der Koordinator committet jeden Lauf nach
seinen Pfaden, damit die Kritik am Code je Commit bleibt.

**Stellungnahme.**
