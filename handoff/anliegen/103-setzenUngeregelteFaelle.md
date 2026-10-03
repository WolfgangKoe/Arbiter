# AUF-1.4 und AUF-3: zwei ungeregelte Fälle beim Setzen

103 · Kritik · von Architekt (Technik) → Anforderungsautor · Runde 1/3 · offen

## Runde 1
Gegenstand: [Aufstellen](../../domaene/anforderungen/phasen/aufstellen.md), AUF-1.4 und
AUF-3, für Item `sperren-beim-setzen` in Plan 2.

**Befund.**
1. AUF-1.4 und AUF-3 treffen sich: Ein Modell außerhalb der *Einheit in Aufstellung* an
   einer *Stelle* außerhalb der eigenen Zone hat die Gründe ‚nicht in Aufstellung‘ und ‚nicht
   ganz in der Zone‘. 100 F3 fragt nur nach den drei Gründen aus AUF-3. Mit Item 2 bekommt
   jedes Setzen eine Stelle, auch in den 11 Aufrufen der AUF-1-Tests.
2. AUF-3.1 regelt *Setzen* nur für ein nicht *gesetztes* Modell. Ein gesetztes Modell noch
   einmal setzen wäre Umsetzen; das kommt laut Plan später. Heute nimmt der Code es ohne
   Sperre hin (`modellSetzen` in `technik/arbiter/domaene/phasen/aufstellen.py`), mit Stelle
   würde es das Modell stillschweigend versetzen.

**Kosten.** Zu 1: Der Testautor wählt für die AUF-1.4-Tests eine Stelle; liegt sie falsch,
hängt das Ergebnis von einer Reihenfolge ab, die nur im Code steht. Zu 2: Der Implementierer
erfindet ein Verhalten, oder ein Fall wird verdeckt erlaubt, den Etappe 1 erst mit Ablage und
Zurücklegen regeln will.

**Gegenvorschlag.**
1. In AUF-3 ein Satz: „Die *Sperren* aus AUF-1 gehen vor; dann wird die *Stelle* nicht
   geprüft.“ Begründung: Gilt die Handlung selbst nicht, sagt die Stelle nichts. Kosten: ein
   Satz. Falls du AUF-3.5 (100 F3) ohnehin schreibst, kann er dort stehen.
2. AUF-3.1: „Ein *gesetztes* *Modell* *setzen*: *Sperre* ‚schon gesetzt‘“, bis Umsetzen
   kommt. Alternative: ausdrücklich „regelt Etappe 1 später“, dann bleibt der Fall untestbar
   und der Code darf ihn nicht ändern.
Beides gehört zum Kriterium, nicht zur Technik; die Entscheidung liegt bei dir oder, wenn du
sie für fachlich offen hältst, beim Stakeholder.

**Stellungnahme.**
