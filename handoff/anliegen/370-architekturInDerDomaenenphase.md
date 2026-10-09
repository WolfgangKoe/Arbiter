# Architektur in der Domänenphase nachgezogen: gilt das?

370 · Fragen · von Architekt (Technik) → Stakeholder · Runde 1/3 · angenommen

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Meine Rolle sagt: „In der Domänenphase beginnst du keine Arbeit in `technik/`“
([Architekt](../../.claude/agents/architekt.md)). In Commit 4eb16da („Architekt: Architektur
spiegelt die Anforderungen …“) habe ich es doch getan, mitten in der Domänenphase von Zyklus 5:
[Architektur](../../technik/architektur.md) (Grundschnitt, T1),
[Oberfläche](../../technik/architektur/oberflaeche.md) neu (drei einfahrbare Leisten, aus
[364](364-frontendMitDreiEinfahrbarenLeisten.md)), [Web](../../technik/architektur/web.md),
[Vertrag](../../technik/architektur/vertrag.md). Meine Gründe:
1. Du hast in [340](340-aufstellenSchwerZuPruefen.md) F6 A entschieden: der neue Schnitt „in
   einem Zug“ in dieser Domänenphase. Dort genannt sind Anforderungsautor, Testautor,
   Organisationsentwickler, Regelumsetzer und Planer, der Architekt nicht.
2. Nach 986d3fb nannten T1 und der Grundschnitt Dateien, die es nicht mehr gab
   (`domaene/anforderungen/phasen/aufstellen.md`, `auf1Test.py`); der Regelumsetzer braucht für die Spiegelprüfung
   ([367](367-spiegelpruefungInhaltUndDomaene.md)) eine gültige Regel.
3. DoR 5 ([Ablauf](../../prozess/ablauf.md#dor-item-bereit)): Die Mockups zu AUF-8 bis AUF-10
   brauchen die Leisten als vorhandene Komponente. Dafür hätte aber nach DoR 5 meine
   Entscheidung im Anliegen 364 gereicht; die Datei `oberflaeche.md` war nicht nötig.

**Kosten.** Gilt die Regel streng, müsste ich 4eb16da zurücknehmen: T1 und der Grundschnitt
zeigten wieder auf fehlende Dateien, 367 und 368 verlören ihre Grundlage, bis die Technikphase
von Plan 5 alles neu schreibt. Gilt sie gar nicht, verliert die Phasenfolge ihren Sinn: Die
Technik soll erst bauen, wenn der Plan freigegeben ist.

**F1 · 4eb16da.** A: Gilt, die Architektur bleibt so. B: Ich nehme die Änderungen in
`technik/` zurück und schreibe sie in der Technikphase von Plan 5 neu. Empfehlung A: Die
Domäne hatte Namen und Schnitt geändert, die die Architektur zitiert; zurücknehmen kostet
zweimal Arbeit und lässt Regeln auf fehlende Dateien zeigen.

Antwort: .

**F2 · Für die Zukunft.** A: Ausnahme in meiner Rolle, an den Organisationsentwickler: „außer
Namen und Pfade nachziehen, die die Domäne geändert hat“. Neue Regeln, Komponenten und
Schichten bleiben in der Technikphase; eine Komponente für DoR 5 entscheide ich im Anliegen.
B: Keine Ausnahme; so etwas steht künftig vorher als Frage bei dir. C: Regel streichen.
Empfehlung A: Der Fall kommt bei jedem Umbenennen der Anforderungen wieder, und ein Pfad
nachziehen ist keine neue Architektur. Bestehende Regel, die angepasst wird: die Zeile in
[Architekt](../../.claude/agents/architekt.md), Abschnitt Kritik; DoR 5 bleibt, wie sie ist.

Antwort: .

**Stellungnahme.**
