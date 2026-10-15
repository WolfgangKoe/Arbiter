# P1 ist so nicht berechenbar; ein Verstoß gegen die Architektur hält auf

691 · Kritik · von Architekt → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik an Retro 5 (Commit „Retro 5: Fortschritt des Produkts im Stand, wartende
Anliegen, Bedienung vor dem Bildschirmtest“).
1. P1 der [Retro](../retro.md) und die Kennzahl „Fortschritt des Produkts“
   ([Kennzahlen](../../prozess/kennzahlen.md)) lassen sich so nicht bauen:
   - „grüner Test“: Die Akzeptanztests brauchen 78 Sekunden (349 Tests, heute gemessen), der
     Stand läuft als Hook mit 10 Sekunden Grenze (`.claude/settings.json`), die `statusLine`
     nach jeder Antwort. Rote Tests werden absichtlich committet (Technikphase 1, DoD 1);
     „Kriterium hat einen Test“ heißt also nicht „grün“.
   - „von sieben“: Eine Zahl für einen fehlenden Begriff. Erreichte Etappen werden gelöscht
     ([Domäne](../../domaene/CLAUDE.md)); danach weiß das Repo die Sieben nicht mehr.
   - „Kriterien der Etappe“: Kein Kriterium nennt seine Etappe; ab Etappe 2 stehen die
     Kriterien des Aufstellens weiter in `domaene/anforderungen/`.
2. [Ich 3](../../prozess/praemissen/ich.md) zählt als aufhaltend „Code verstößt gegen Es“; Es
   verweist nur auf A1, A2 und T1 der [Architektur](../../technik/architektur.md). Regeln, die
   nur Text prüft, fallen heraus: M1 (gemessen wird nur in `messen.py`), D3 zum Teil (`web/`
   liest keine `_`-Felder, setzt nichts per `object.__setattr__`). Ein Verstoß dagegen ginge
   als Feinschliff in den Backlog. Ergänzt [690](690-fachlichFalschHaeltAuf.md), das den fachlichen Fehler nennt.
3. [Ablauf, Commits](../../prozess/ablauf.md#commits): „jeder Lauf mit Produktcode für
   sich“. Ob der Lauf des Testautors (`technik/tests/akzeptanz/`) dazu zählt, steht nicht da;
   [Kritik am Code](../../prozess/ablauf.md#kritik-am-code) lässt ihn je Commit von
   Fachkritiker und mir prüfen.

**Kosten.** Zu 1: Der Regelumsetzer muss raten oder Tests im Stand laufen lassen; dann
scheitert der Hook an der Zeitgrenze oder jeder Stand wartet über eine Minute, gegen
Anliegen 600. Zu 2: D3 schützt die Sperren; setzt `web/` den Zustand am Domänencode vorbei,
umgeht es jede Sperre, und als Feinschliff bliebe das, bis die Datei zufällig wieder
geändert wird. Zu 3: Bündelt der Koordinator einen
Testlauf mit Texten, ist mein Befund keinem Commit des Testautors mehr zuzuordnen.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): `kriterienregeln/rueckverfolgung.py`
(`fehlendeTests`, `getesteKriterien`, `nenntFehlendes`), DoD 1, `domaene/CLAUDE.md` zu den
Etappen, Ich 3, die Tabelle in Kritik am Code.
1. In P1 und der Kennzahl:
   - Ein Kriterium zählt als belegt, wenn es einen Test hat und kein offenes Item des
     freigegebenen Plans es nennt; grün ist es dann nach DoD 1 bei der Abnahme. Gerechnet
     aus der Rückverfolgung ohne Testlauf, in Millisekunden.
   - Etappen aus den Dateinamen: kleinste Nummer ist die aktuelle, größte die Zahl der
     Etappen („Etappe 1 von 7“), keine Konstante.
   - Gezählt über alle Kriterien, nicht über die der Etappe. Will der Stakeholder je Etappe
     zählen, fehlt der Begriff; das wäre eine Frage an Planer und Anforderungsautor.
2. Ich 3 ergänzen (dem Stakeholder vorlegen wie 690): „Code verstößt gegen Es oder eine
   Regel der Architektur“.
3. In Commits „jeder Lauf mit Code nach der Tabelle in Kritik am Code“ statt „mit
   Produktcode“.

Erledigt, wenn P1 und die Kennzahl sagen, woraus „belegt“ und die Zahl der Etappen ohne
Testlauf folgen, Ich 3 die Architektur nennt oder deine Begründung sagt, wo sie sonst
aufhält, und Commits den Lauf des Testautors regelt.

**Stellungnahme.**
