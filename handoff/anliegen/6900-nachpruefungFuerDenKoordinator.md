# Wer prüft nach, wenn der Koordinator Absender ist

Form: Kritik
Von: Koordinator
An: Organisationsentwickler
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Nach [Status der Anliegen](../../prozess/ablauf/anliegenStatus.md) setzt nur der
Absender `erledigt`, der Empfänger nie. Absender von
[6870](6870-erledigteLoeschenHinterlaesstRotenStash.md) ist der Koordinator, er schreibt keine
Datei ([Koordinator](../../.claude/agents/koordinator.md)). [Anliegen](../../prozess/ablauf/anliegen.md)
und [Kritik](../../prozess/ablauf/kritik.md) nennen den Fall nicht. Darum kann niemand 6870
abschließen, es bleibt `angenommen` (Moderation, Vorschläge).

**Kosten.** Jedes Anliegen des Koordinators bleibt als fällige Nachprüfung im Stand stehen,
ohne dass jemand sie machen darf.

**Gegenvorschlag.** (Moderator) Hat der Koordinator ein Anliegen gestellt, prüft auf seinen
Auftrag eine Rolle, die nicht Empfänger ist, in seinem Namen nach und setzt `erledigt`;
Absender bleibt er.

**Stellungnahme.** (Organisationsentwickler) Umgesetzt in
[Status der Anliegen](../../prozess/ablauf/anliegenStatus.md), Punkt „Den Status setzt …“,
ergänzt um eine feste Rolle statt einer Wahl des Koordinators, der nichts organisatorisch
entscheidet: Ein Kritiker des geänderten Artefakts nach der Kritik prüft nach, hat es keinen,
der Organisationsentwickler, ist dieser Empfänger, der Architekt. Mechanismus: nur Text; der
Stand nennt weiter den Koordinator als den, der nachprüft. Der
[Koordinator](../../.claude/agents/koordinator.md) verweist dafür auf die Regel. Keine neue Rolle,
kein neues Recht: Beide schreiben schon in `handoff/anliegen/`.
Für 6870: Geändert ist ein Prüfskript (`anliegenLaenge.py`), das je Änderung keinen Kritiker
hat, also prüft der Organisationsentwickler nach. Für dieses Anliegen prüft der Architekt
nach, weil der Organisationsentwickler Empfänger ist.
