# Kritik-Commit in der Koordinator-Definition

80 · Fragen · von Organisationsentwickler → Stakeholder · Runde 1/3 · angenommen

## Runde 1
**Befund.** Seit `Freigabe Retro 1` trägt kein Commit `Kritik <Hash>` im Betreff
([79](79-kritikCommitsFehlen.md)). Die Pflicht steht nur in
[Ablauf, Kritik am Code](../../prozess/ablauf.md#kritik-am-code). Diese Datei ist länger als
4.000 Zeichen, der Koordinator darf sie also nicht lesen (`lesegrenze.py`). Seine
[Definition](../../.claude/agents/koordinator.md) nennt den Kritik-Commit nicht. Meine
Änderung dort hat die Berechtigungsprüfung von Claude Code abgelehnt (Selbständerung).

**Kosten.** Ohne die Zeile in der Definition fehlt der Kritik-Commit auch nach dem nächsten
Kritiklauf. Dann meldet der Stand wieder eine fällige Kritik, die schon gemacht ist.

**Gegenvorschlag.** Drei Änderungen in `.claude/agents/koordinator.md`. Die Definition hat
2.492 von 2.500 Zeichen, deshalb rückt „notfalls `--allow-empty`“ an eine Stelle:
1. Zeile 16: „(notfalls `--allow-empty`)“ streichen.
2. Zeile 20: Hinter „Kritik am Code).“ folgt der Satz „Seinen Lauf committest du, der
   Betreff beginnt mit `Kritik <kurzer Hash>`.“
3. Zeile 31: Vor dem Doppelpunkt „(Freigabe und Kritik notfalls `--allow-empty`)“ einfügen.

„Beginnt mit“ passt zu `codekritik.py` heute und nach [78](78-kritikAmCodeZuE15c5d2.md),
Punkt 2.

**F1 · Ändert der Stakeholder die Definition selbst wie im Gegenvorschlag, oder gibt er dem
Organisationsentwickler das Schreibrecht für diese Änderung?** Empfehlung: Der Stakeholder
erlaubt mir die Änderung, ich setze sie in einem Lauf um.
Antwort: .

**Stellungnahme.**
