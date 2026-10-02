# Rollen für die Technikphase

23 · Vorschlag · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Plan 1 ist freigegeben, der Stand nennt den Testautor. Für die Schritte der
[Technikphase](../../prozess/ablauf.md) fehlen Testautor, Fachkritiker, Implementierer und
Reviewer; der Koordinator kann sie nicht beauftragen. Die DoD, die der Reviewer prüft, steht
nicht in `prozess/`.

**Kosten.** Je Rolle eine Definition und ein Eintrag beim Koordinator; Grundlast nur, wenn
sie läuft. Schritte 1–6 sind 7 Rollenläufe, mit diesem und dem Einsetzen 9 von 10.

**Gegenvorschlag.** Startbesetzung nach E25 und E27 (`VORGEHEN.md`); die Aufgaben sind die
Schritte in `ablauf.md`. Werkzeuge Read, Write, Edit, Bash; keine Rolle startet Agenten.

| Rolle | Art, Modell | Schritt | Schreibpfade |
|---|---|---|---|
| Testautor | Technik, ausführend, Sonnet | 1 | `technik/tests/akzeptanz/` |
| Fachkritiker | Domäne, prüfend, Opus | 2, 5 | – |
| Implementierer | Technik, ausführend, Sonnet | 3 | `technik/arbiter/`, `technik/tests/einheit/`, `pyproject.toml` |
| Reviewer | Technik, prüfend, Opus | 4, 6 | `handoff/review.md` |

Alle dazu `handoff/anliegen/`.
- Testautor: eine Datei je Anforderung, Ordner wie `anforderungen/`
  (`akzeptanz/phasen/test_auf_1.py`), je Kriterium mindestens ein Test
  (`test_auf_1_3_<satz>`), Namen aus dem Glossar (Leitbild in `VORGEHEN.md`).
- Akzeptanztests sind für den Implementierer gesperrt (`schreibgrenze.py`); hält er einen für
  falsch, schreibt er ein Anliegen an den Testautor (E34).
- Der Reviewer hat `/code-review` vorgeladen (`skills:`, Werkzeug `ReportFindings`).
- Keine Skills vorab: `akzeptanztest-schreiben` und die Prüfliste des Reviewers entstehen in
  der Retro aus dem ersten echten Beispiel (E24, E30). Kein Regel-Nachschlager ohne Bedarf.

**F1 · Diese vier Rollen einsetzen?** A: wie oben. B: ohne Fachkritiker, der Architekt prüft
auch fachlich. Empfehlung A: Sonst prüft niemand aus der Domäne, ob der Test das Kriterium
trifft.

Antwort: .

**F2 · Welche DoD gilt in Zyklus 1?** A: die Punkte 1, 2, 5 und 6 der DoD in `VORGEHEN.md`
(Beziehungen); 3 (Mutation) und 4 (Oberfläche) erst, wenn es sie gibt. B: nur Tests grün.
Empfehlung A, in `ablauf.md`, Mechanismus „nur Text“, bis der Regelumsetzer die Prüfung baut.

Antwort: .

**Stellungnahme.**
