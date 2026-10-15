# Wohin Feinschliff, was hält auf, und gilt „wie ArbiterMap“ für alle?

687 · Fragen · von Organisationsentwickler → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.**
1. Nach deiner Antwort in Anliegen 630 (F1 A) kommt Feinschliff, der nichts aufhält, in den
   Backlog der Perspektive ([Ich 3](../../prozess/praemissen/ich.md)). Einen für die Technik
   gibt es nicht; `domaene/backlog.md` ist die Liste der Items des Planers, nur er schreibt
   sie. Feinschliff hat eine andere Form und andere Schreiber (Anliegen 690). Rechte legt
   nur du fest.
2. Dreimal hast du gesagt, Bedienung und Aussehen sollen ArbiterMap und Arbiter-old folgen,
   ihr Code nicht: Kommentar zu Plan 5 („so wie es ArbiterMap gemacht hat“), Anliegen 366
   (Griff wie ArbiterMap), Anliegen 683 („Ich meine, dass ich das immer wieder gesagt
   habe“). Geschrieben steht es nur bei [UX](../../.claude/agents/ux.md); Anforderungsautor,
   Planer und Implementierer lesen es nicht. Wiederholte Entscheidungen schlage ich als
   Prämisse vor ([Ablauf, Prozessphase](../../prozess/ablauf.md#prozessphase)).
3. Ich 3 nennt nicht als aufhaltend: einen fachlichen Fehler (Test trifft sein Kriterium
   nicht, Code weicht von der Fundstelle ab; Anliegen 690) und einen Verstoß gegen eine
   Regel der Architektur, die nur Text prüft, etwa dass das Frontend den Zustand nicht an
   den Sperren vorbei ändert (Anliegen 691). Beides ginge als Feinschliff durch; die
   [Technikphase](../../prozess/ablauf.md#technikphase) hält beim falschen Test dagegen an.

**Kosten.** Ohne 1 geht Feinschliff verloren oder wird doch ein Anliegen. Ohne 2 fällt eine
fehlende Bedienung wieder erst dir am Bildschirm auf (Anliegen 685). Ohne 3 gälte ein Item
mit falscher oder fehlender Sperre als abgenommen.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): Ich 3, die Schreibpfade in `.claude/agents/`,
DoR 6 im [Ablauf](../../prozess/ablauf.md#dor-item-bereit), Technikphase Schritte 2 und 4.

**F1 · Wohin kommt Feinschliff, und wer schreibt ihn?**
A: Je Perspektive `feinschliff.md`, getrennt von den Items: je Punkt Datei und ein Satz,
höchstens 3.000 Zeichen. `domaene/feinschliff.md` schreiben Anforderungsautor, Ux,
Architekt, Fachkritiker; `technik/feinschliff.md` Architekt, Testautor, Implementierer,
Reviewer, Fachkritiker; für den Prozess bleibt `prozess/backlog.md`. Wer einen Punkt
erledigt, löscht ihn. Ich 3 sagt dann `feinschliff.md` statt Backlog.
B: Keine Liste: Feinschliff, der nichts aufhält, entfällt.
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

**F3 · Halten auch fachliche Fehler und Verstöße gegen die Architektur auf?**
A: Ja, die Klammer in Ich 3 lautet dann: „(Kriterium unklar, Test nicht schreibbar, nicht
grün zu machen oder fachlich falsch: trifft sein Kriterium nicht oder lässt einen geregelten
Fall aus, Kriterium oder Code weicht von der Fundstelle ab)“, und statt „gegen Es“ steht
„gegen Es oder eine Regel der Architektur“.
B: Wie heute.
Empfehlung: A. So decken sich Ich 3 und die Technikphase.
Antwort: .

**Stellungnahme.**
