# Sechs Testläufe zugleich: Der Regelumsetzer muss vor „fertig“ alles prüfen

Form: Fragen
Von: Organisationsentwickler
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Befund des Koordinators in der Prozessphase 10: Zwei Regelumsetzer starteten den
Lauf über alle Prüfungen (`python3 -m pytest prozess/pruefungen`, allein 16 Minuten), obwohl
ihr Auftrag „keinen Gesamtlauf starten“ sagte. Zeitweise liefen sechs Testläufe gleichzeitig
und machten alle langsam.
Bestehende Regeln (Ich 4): Die Rolle hielt sich an ihre Definition, nicht der Auftrag.
- [Regelumsetzer](../../.claude/agents/regelumsetzer.md), Grenzen: „Melde erst fertig, wenn
  `python3 -m pytest prozess/pruefungen` grün ist“; ebenso [Commits](../../prozess/ablauf/commits.md):
  „Alles prüft der Regelumsetzer, bevor er fertig meldet“.
- [Gleichzeitige Läufe](../../prozess/ablauf/gleichzeitigeLaeufe.md): Der Lauf darf neben Rollen
  laufen, ohne Grenze, wie viele.
- Der Commit-Hook prüft bei einer Änderung in `prozess/pruefungen/` schon fast dasselbe: alle
  Tests außer Abdeckung und `vollstaendig`, die beide nur `technik/` betreffen
  ([Formregeln](../../prozess/regeln/formregeln.md), Zeile Commits). Den ganzen Lauf macht
  außerdem der Reviewer je Zyklus in der [DoD](../../prozess/ablauf/dod.md) 2.

Der zweite Teil des Befunds ist gewollt: Zwei Läufe schrieben je eine Zeile in
[Rollenregeln](../../prozess/regeln/rollenregeln.md), die Zeile zu P6 kam mit dem Commit von
P4 (cdd72fb). Der Befehl committet ganze Dateien, und
[Gleichzeitige Läufe](../../prozess/ablauf/gleichzeitigeLaeufe.md) sagt: „die Zeile eines
Nachbarn in `prozess/regeln/` geht mit“. Der Haken im Fortschritt folgt dem Betreff, nicht
der Datei. Einziger Nachteil: Nimmt man P4 zurück, fehlt auch die Zeile zu P6. Ich schlage
dazu nichts vor.

**Kosten.** A: zwei Sätze Text, kein Code; ein Lauf des Regelumsetzers endet etwa
16 Minuten früher, und es laufen nur noch die Prüfungen der Commits gleichzeitig. Nachteil:
Bricht eine Änderung etwas, das nur der ganze Lauf findet, merkt es erst der Reviewer in der
nächsten Technikphase. B: kein Aufwand, aber jeder Lauf des Regelumsetzers dauert 16 Minuten
und mehr, parallel deutlich mehr. C: Hook-Code; Läufe warten aufeinander statt sich zu
bremsen, der zweite dauert so 32 Minuten.

**Gegenvorschlag.** A, in dieser Prozessphase, durch mich: Der Regelumsetzer prüft vor
„fertig“ nur die Testdateien der Module, die er geändert hat; den Rest prüft der Commit-Hook.
Dazu ändere ich die Zeile in [Regelumsetzer](../../.claude/agents/regelumsetzer.md) und den
Satz in [Commits](../../prozess/ablauf/commits.md). Mechanismus: nur Text; der Commit-Hook
besteht. Danach schreibt der Koordinator „keinen Gesamtlauf“ nicht mehr in Aufträge, denn
die Regel sagt es dann selbst. Rückweg: Commit zurücknehmen. Ohne Probe: Ich ändere keine
Einstellung und keinen Hook.

**Stellungnahme.**

**F1 · Was prüft der Regelumsetzer, bevor er fertig meldet?**
A: Nur die Tests der Module, die er geändert hat; den Rest prüft der Commit-Hook, alles der Reviewer in der DoD (Commits, DoD 2)
B: Wie bisher alles; der Koordinator schreibt „keinen Gesamtlauf“ nicht mehr in seine Aufträge (Regelumsetzer, Gleichzeitige Läufe)
C: Wie bisher alles, aber ein Hook lässt immer nur einen Lauf über alles zu, die anderen warten (neu)
Empfehlung: A, der Commit-Hook prüft fast dasselbe schon; der ganze Lauf je Regelumsetzer verdoppelt das nur und bremst alle anderen.
Antwort: A
