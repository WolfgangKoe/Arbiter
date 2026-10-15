# Wer schreibt den Backlog, und gilt „wie ArbiterMap“ für alle?

687 · Fragen · von Organisationsentwickler → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.**
1. Nach deiner Antwort in Anliegen 630 (F1 A) kommt Feinschliff, der nichts aufhält, in den
   Backlog der Perspektive ([Ich 3](../../prozess/praemissen/ich.md)). Einen Backlog für die
   Technik gibt es nicht, den der Domäne (`domaene/backlog.md`) darf nur der Planer
   schreiben; die Kritiker dürfen keinen. Rechte legt nur du fest.
2. Dreimal hast du gesagt, Bedienung und Aussehen sollen ArbiterMap und Arbiter-old folgen,
   ihr Code nicht: Kommentar zu Plan 5 („so wie es ArbiterMap gemacht hat“), Anliegen 366
   (Griff wie ArbiterMap), Anliegen 683 („Ich meine, dass ich das immer wieder gesagt
   habe“). Geschrieben steht es nur bei [UX](../../.claude/agents/ux.md); Anforderungsautor,
   Planer und Implementierer lesen es nicht. Wiederholte Entscheidungen schlage ich als
   Prämisse vor ([Ablauf, Prozessphase](../../prozess/ablauf.md#prozessphase)).

**Kosten.** Ohne 1 geht Feinschliff verloren oder wird doch ein Anliegen. Ohne 2 fällt eine
fehlende Bedienung wieder erst dir am Bildschirm auf (Anliegen 685).

**Gegenvorschlag.** Bestehende Regeln (Ich 4): Ich 3, die Schreibpfade in `.claude/agents/`,
DoR 6 im [Ablauf](../../prozess/ablauf.md#dor-item-bereit) (UX vergleicht die Gesten).

**F1 · Wer schreibt Feinschliff in den Backlog?**
A: Wer in der Perspektive arbeitet oder sie kritisiert, darf ihren Backlog schreiben:
`domaene/backlog.md` neu für Anforderungsautor, Ux, Architekt, Fachkritiker;
`technik/backlog.md` neu für Architekt, Testautor, Implementierer, Reviewer, Fachkritiker.
Wer einen Punkt erledigt, löscht ihn. Höchstmaß wie heute, 3.000 Zeichen.
B: Kein Backlog: Feinschliff, der nichts aufhält, entfällt.
Empfehlung: A. Der Punkt kostet nichts, wenn die Datei ohnehin geändert wird.
Antwort: .

**F2 · Gilt „Bedienung und Aussehen wie ArbiterMap und Arbiter-old“ für jede Rolle?**
A: Ja, als Absatz direkt unter dem Ziel in der [Root-CLAUDE.md](../../CLAUDE.md), die jede
Rolle lädt: „Vorbild: Bedienung und Aussehen folgen ArbiterMap und Arbiter-old, soweit Ziel
und Regeln nichts anderes verlangen. Ihr Code ist kein Vorbild; die Codegrundlage bleibt
wartbar nach [Es](prozess/praemissen/es.md).“
B: Nein, nur UX wie heute.
Empfehlung: A. Wer die Anforderung schreibt, kennt das Vorbild dann schon.
Antwort: .

**Stellungnahme.**
