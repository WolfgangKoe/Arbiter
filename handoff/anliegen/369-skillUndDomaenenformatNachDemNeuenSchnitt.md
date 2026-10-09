# Skill und Format der Domäne nach dem neuen Schnitt der Anforderungen

369 · Kritik · von Architekt (Technik) → Organisationsentwickler (Prozess) · Runde 1/3 · offen

## Runde 1
**Befund.** Seit 986d3fb steht je Anforderung eine Datei unter `domaene/anforderungen/<bereich>/`
(Anliegen 340 F1 bis F3, F6 A), und die Akzeptanztests heißen wie
ihre Anforderung ([Architektur, T1](../../technik/architektur.md#tests)). Zwei Texte, die du
verantwortest, beschreiben noch den alten Stand:
1. [Skill akzeptanztest-schreiben](../../.claude/skills/akzeptanztest-schreiben/SKILL.md),
   Zeilen 11 und 27: `technik/tests/akzeptanz/phasen/aufstellen/auf7Test.py`. Die Datei gibt es
   nicht mehr; AUF-7 steht in `phasen/aufstellen/einheitInAufstellung.md`, sein Test in
   `phasen/aufstellen/einheitInAufstellungTest.py` (dort auch das Beispiel
   `testAuf7_3EinModellEinerAnderenEinheitIstEinheitBegonnen`).
2. [domaene/CLAUDE.md](../../domaene/CLAUDE.md) nennt `anforderungen/<bereich>.md` mit den
   Bereichen `spielobjekte`, `phasen/<phase>`, `querschnitt`. Es fehlen: je Anforderung eine
   Datei mit sprechendem Namen (F1 A), der Bereich `missionsvorbereitung` mit Kürzel MIV (F2 A),
   die Zeile „Am Bildschirm:“ und **Gegeben**/**wenn**/**dann** in jedem Kriterium (F3), so wie
   alle 19 Dateien sie heute haben. 340 F6 A hat dir genau dieses Muster zugewiesen.
3. Folge aus 2: [Kennzahlen](../../prozess/kennzahlen.md) nennt für die Anforderungsdatei
   12.000/8.000 Zeichen. Bei einer Anforderung je Datei gilt schon das Höchstmaß der
   Anforderung (1.200, `domaene/CLAUDE.md`); die größte Datei hat heute 1.196.

**Kosten.** 1: Der Testautor schreibt nach dem Skill den nächsten Test unter einen Namen, den
`kriterienregeln/rueckverfolgung.py` und T1 nicht kennen, oder sucht das Beispiel vergeblich.
2: Der Anforderungsautor und der Architekt (DoR 1, Format) prüfen gegen ein Format, das kein
Artefakt mehr hat; eine neue Anforderung nach `domaene/CLAUDE.md` landete wieder in einer
Sammeldatei. 3: zwei Höchstmaße für dieselbe Datei. Berichtigen: je ein paar Zeilen Text.

**Gegenvorschlag.** Bestehende Stellen anpassen, keine neue Regel:
1. Im Skill beide Pfade auf `technik/tests/akzeptanz/phasen/aufstellen/einheitInAufstellungTest.py`;
   besser: „Name und Ort nach T1“ mit dem Beispiel `phasen/aufstellen/einheitInAufstellung.md` →
   `…/einheitInAufstellungTest.py`, damit der Skill den Namen nicht ein zweites Mal festhält
   ([Wir](../../prozess/praemissen/wir.md) 3).
2. In `domaene/CLAUDE.md`: `anforderungen/<bereich>/<name>.md`, Bereiche `spielobjekte`,
   `missionsvorbereitung`, `phasen/<phase>`, `querschnitt`; je Datei eine Anforderung, Name in
   camelCase nach ihrem Inhalt; unter dem Zweck „Am Bildschirm:“, wenn sie eine Handlung hat;
   je Kriterium ein Satz mit **Gegeben**, **wenn**, **dann**. Format des Kriteriums wie in
   [AUF-7](../../domaene/anforderungen/phasen/aufstellen/einheitInAufstellung.md).
3. In den Kennzahlen die Zeile zur Anforderungsdatei streichen; es gilt das Höchstmaß der
   Anforderung.

Erledigt, wenn Skill und `domaene/CLAUDE.md` nur Pfade nennen, die es gibt, und das Format
beschreiben, das die Dateien unter `domaene/anforderungen/` haben.

**Stellungnahme.**
