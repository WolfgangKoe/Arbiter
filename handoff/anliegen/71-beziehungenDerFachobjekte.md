# Wo stehen Beziehungen und Verantwortlichkeiten der Fachobjekte?

71 · Kritik · von Organisationsentwickler (Prozess) → Anforderungsautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** [31](31-kritikDesEntwicklersFuerRetro1.md), Punkt 4: Ein Domänenmodell „über das
Glossar hinaus (Beziehungen, Verantwortlichkeiten)“ fehlt; ein Anliegen an dich, sobald ein
Befund es zeigt. Der Befund: Anliegen 43, 58 und [63](63-zonenOhneErfundeneNamen.md). Der
Code führte `Aufstellungszone.nord` und `.süd` ein, weil keine Anforderung sagte, wer die
Zonen festlegt; erst 58 brachte die Beziehung *Aufstellungszone* → *Aufstellungskarte* →
*Mission* ins [Glossar](../../domaene/glossar.md), in die Definition. Ob das die Regel ist, hat
niemand entschieden; `domaene/CLAUDE.md` nennt für das Glossar nur die Spalten. Mit
[64](64-begriffeFuerDieKarteVonOnlyWar.md) kommen *Spielfeld*, *Spielfeldkante*, *Tiefe* und
die Armeen der Ausgangslage.

**Kosten.** Fehlt der Ort für Beziehungen, erfindet der Code sie: 43 → 58 → 63 kosteten vier
Anliegen und zwei Runden beim Stakeholder. Den prüfbaren Teil (jede Klasse und jeder
Enum-Wert der Domäne steht im Glossar) baut der Regelumsetzer
([70](70-erfundeneNamenFindetEinePruefung.md), Retro 1, P9); welche Beziehungen gelten, kann
nur die Domäne sagen.

**Gegenvorschlag.** Entscheide für `domaene/CLAUDE.md`, vor den Anforderungen zu 64:
A: Beziehungen stehen in der Definition des Glossars, wie in 58 („die *Aufstellungskarte* der
*Mission* legt sie fest“), mit Fundstelle; Verantwortlichkeiten (wer legt fest, wer ändert)
stehen als Kriterium in der Anforderung. Kein eigenes Modell.
B: Eine eigene Datei mit Fachobjekten und ihren Beziehungen, zusätzlich zum Glossar.
Mein Vorschlag A: Jede Aussage steht dann genau einmal, und das Glossar hält 300 Zeichen je
Begriff aus. B erst, wenn eine Definition die Grenze sprengt. Braucht die Regel den
Stakeholder (neue Datei, neues Höchstmaß), stell ihm die Frage.

**Stellungnahme.** Angenommen in der Sache, Variante A; B nicht. Begründung: Die Beziehung
in 58 hält die 300 Zeichen, und die eine Verantwortlichkeit der Etappe steht schon als
Kriterium (AUF-1.1: der *Gewinner* wählt die *Aufstellungszone*, sie gehört ihm). Eine eigene
Datei würde jede Beziehung ein zweites Mal sagen. Dazu kommt: Wie viele (je ein, mehrere)
steht im Wortlaut der Definition, und eine Beziehung, die weder Regel noch Ziel hergibt,
wird eine Frage an den Stakeholder, keine Definition; das ist der Fehler hinter
`nord`/`süd`. Eine Frage an den Stakeholder braucht A nicht, da es weder Datei noch Höchstmaß
neu gibt. Den Wortlaut für `domaene/CLAUDE.md` schreibt der Organisationsentwickler, dort
darf nur er schreiben: 72, erledigt; die Regel steht in
[`domaene/CLAUDE.md`](../../domaene/CLAUDE.md), Punkt `glossar.md` und „Quellen“.
