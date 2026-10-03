# Rundenzähler der Anliegen durchsetzen

115 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Entscheidung des Stakeholders: Nach Runde 3/3 wird ein Anliegen an ihn eskaliert,
er entscheidet über das weitere Vorgehen, auch über das Zurücksetzen auf Runde 1/3. Der Zähler
soll verhindern, dass zwei Rollen endlos diskutieren. Die Regel steht in
[Ablauf, Anliegen](../../prozess/ablauf.md#anliegen). `anliegen.py` prüft nur, dass die Runde
zwischen 1 und 3 liegt. Eine Rolle kann heute die Runde von 3 auf 1 senken, `eskaliert`
zurücknehmen oder in Runde 3 nach `abgelehnt` wieder `offen` setzen, also eine vierte Runde
ohne Zähler führen. Aufgefallen ist die Lücke an [83](83-sprungErproben.md) (Moderation vor
Freigabe Plan 2).

**Kosten.** Ohne Sperre hängt der Zähler am guten Willen genau der zwei Rollen, die er bremsen
soll; die Eskalation erreicht den Stakeholder nie.

**Gegenvorschlag.** `statusrecht.py` (PreToolUse, Write und Edit) sperrt für Rollen, mit
Meldung, was stattdessen gilt:
1. die Runde im Kopf zu senken (`Runde 3/3` → `Runde 1/3`);
2. einen Kopf mit `eskaliert` in einen anderen Status zu ändern;
3. in Runde 3/3 von `abgelehnt` auf einen anderen Status als `eskaliert` oder `erledigt` zu
   wechseln.
Die Meldung nennt: „Runde 3/3 ist die letzte; setze `eskaliert`, der Stakeholder entscheidet.“
Der Stakeholder ändert Anliegen von Hand, ihn trifft der Hook nicht. Scheiter-Test je Fall in
`statusrechtTest.py`, dazu je ein erlaubter Gegenfall (Runde erhöhen, `abgelehnt` →
`eskaliert` in Runde 3). Eintrag in `prozess/regeln.md`; den Vermerk in `ablauf.md` setze ich.

Den Ort des Moduls bestimmt die Ordnung aus [114](114-pruefskripteOrdnenUndLesbarMachen.md);
kommt 115 vorher, zieht es mit 114 um.

Erledigt, wenn die drei Fälle gesperrt sind, die Gegenfälle durchgehen und
`python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.** Angenommen wie vorgeschlagen, alle drei Fälle in `statusrecht.py`, Meldung nennt die letzte Runde. Scheiter-Test je Fall und erlaubter Gegenfall in `statusrechtTest.py`. Eintrag in `prozess/regeln.md`; Vermerk in `ablauf.md` setzt der Organisationsentwickler. Das Modul zieht mit 114 um.

**Nachprüfung.** In Ordnung: `rundenVerstoß` sperrt alle drei Fälle, die Gegenfälle gehen
durch (`statusrechtTest.py`), Eintrag in `prozess/regeln.md` steht, Vermerk in `ablauf.md`
gesetzt. Der Docstring von `statusrecht.py` nennt nur `erledigt`; das fällt unter die
Lesbarkeit aus 114.
