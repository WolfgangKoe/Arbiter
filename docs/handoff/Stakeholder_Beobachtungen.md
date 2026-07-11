STATUS: STANDING

# Stakeholder-Beobachtungen — stehender Eingangskanal

**Diese Datei wird NIE gelöscht, auch nicht wenn sie leer ist.**

Regeln:

- **Zweck:** Eingangskanal des Stakeholders. Er schreibt hier Beobachtungen als
  Bulletpoints (keine Nummerierung nötig), gern mit Screenshot-Verweis — Screenshots
  liegen daneben in `docs/handoff/`.
- **Lifecycle je Beobachtung:** Bei Session-Start liest der Planner diese Datei. Jede
  neue Beobachtung wird mit **explizitem Vorgehen** nach `docs/goals/backlog.md`
  (oder direkt in den Session-Plan) überführt und **danach aus dieser Datei
  entfernt** — die Datei selbst bleibt bestehen.
- **Screenshots:** bleiben in `docs/handoff/`, bis das zugehörige Finding DONE ist —
  erst dann löschen.

## Beobachtungen (Eingang)

- Die Karte von "Cut them down" erstreckt sich auf beiden Spielerflächen. Das sollte aber nur auf einer Seite sein (s. Bildschirmfoto vom 2026-07-11 11-46-32). Könntest du bitte mal GO-Card oder das UI-Layout generell prüfen. Es sind doch laut Vereinbarung nur zwei Möglichkeiten der Anzeige und der Anker. Das hier sollte eigentlich "verboten" sein. An anderen Stellen hatte es doch funktinoiert. → S139-Planungsgegenstand.
- Die Badges für die Schlüsselwörter in der unitCard können dieselbe Farbe haben wir z.B. "Stationary". Man erkennt es einfach nicht. (Farbteil = Backlog **B14**; der Fraktions-Keyword-Teil derselben Beobachtung ist erledigt, s. u. „Zuletzt überführt".)
- Ich finde das Design des Rahmens der unitCard sehr schön. Ein heller Streifen auf der linken Seite, ansonsten ist der Rest des Randes dunkler (s. Bildschirmfoto vom 2026-07-11 11-54-31). Ist es möglich dieses "Design des Randes" beim zweiten Spieler vertikal zu spiegeln? Also dass der helle gelbe Rand rechts statt links ist? Und könnte man dieses Prinzip auf die Gos übertragen. Die sind zwar so grundsätzlich gut, aber ich empfinde es als zu grell. → S139-Planungsgegenstand (Rand-Design-Konzept).
- Außerdem stelle ich immer wieder fest, dass die GO-Karten keine Schlüsselwörter zeigen, obwohl der Regeltext welche vorgibt. Bitte einplanen, dass ein Subagent diese Schlüsselwörter systematisch in der YAML-Struktur nachpflegt. → S139-Planungsgegenstand (GO-Keyword-Nachpflege in YAML).
- Die Beobachtungen aus Bildschirmfoto vom 2026-07-09 21-29-43 und Bildschirmfoto vom 2026-07-09 21-36-36 scheinen noch nicht für die Umsetzung geplant zu sein. → Backlog B7/B8 (`docs/goals/backlog.md` §2).
- Ist schon irgendwo eingeplant, dass wir das UI-Konzept der heroischen Intervention (s. Bildschirmfoto vom 2026-07-11 12-03-17) ausarbeiten, um es in allen anderen Phase auszurollen? → Backlog GO-UI-Design-System Paket 6 (`docs/goals/backlog.md` §2).

## Zuletzt überführt

- S138: leere Ork-Badge in der unitCard (Powerklaw-/Fall-Back-Badge-Fix) → S138 erledigt.
- S138: Fraktions-Keyword „Ork" in der unitCard (Loader-Platzhalter-Fold-Fix) → S138 erledigt.
- S138: „Unfall" Conquering-Tyrant-Hinweis in gameActionsArea → S138 erledigt (Aura-Hinweis entfernt).
- S138: „Call da WAAAGH"-Endstand endet nie → S138 erledigt (Stufen-Anker + Once-per-Battle-Ledger).
- S137: alle Beobachtungen vom 2026-07-10/11 —
  - **Command-Reroll bei Attackzuweisung** (Screenshot 2026-07-10 21-17-14): S136-Fix
    bestätigt; Folge-Befund Stikkbomb (Inline-Angebot fehlt trotz D6-Attacken) →
    Untersuchung `docs/handoff/S137_stikkbomb_befund.md`.
  - **GO-„used"-Zustand** (Advance-/Command-Reroll; inkl. Inline-Angebot OHNE Undo +
    Once-per-Phase-Erzwingung mit „used" in Wound/Save nach Hit-Einsatz) →
    Backlog **B12** + Konzept `docs/handoff/S137_B12_konzept.md`.
  - **GO-Card-Keyword-Badges** (Screenshot 2026-07-11 09-52-56) → Backlog **B13**.
  - **Badge-Kontrast** (STATIONARY heller, ggf. weitere) → Backlog **B14**.
  - **unitCard: Zustands-/Buff-Badges trennen + CAST-Badge** → direkt in S137
    umgesetzt (P2-1, `unitCard.py`).
  - **Leerzeile zwischen Wound- und Save-Wurf** (Screenshot 2026-07-11 10-31-30) +
    **Power-Claw-Anzeigefehler** (Bezeichnungen falsch, doppelte Badges, Screenshot
    2026-07-11 10-35-44) → Untersuchung `docs/handoff/S137_attack_ui_befund.md`.
- S134: alle Beobachtungen vom 2026-07-09 (B1–B10) → `docs/goals/backlog.md` §2,
  Block **„Stakeholder-Beobachtungen S131"** (je Punkt mit explizitem Vorgehen);
  Entscheidungs-/Diskussionspunkte dazu in `docs/handoff/S134_offene_punkte.md`.
