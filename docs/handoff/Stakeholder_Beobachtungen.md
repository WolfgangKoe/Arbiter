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

- Orks scheinen eine leere Badge in der unitCard zu haben (S137, s. „Bildschirmfoto
  vom 2026-07-11 11-32-52" in `docs/handoff/`) — in S138 triagieren.
- Die Karte von "Cut them down" erstreckt sich auf beiden Spielerflächen. Das sollte aber nur auf einer Seite sein (s. Bildschirmfoto vom 2026-07-11 11-46-32). Könntest du bitte mal GO-Card oder das UI-Layout generell prüfen. Es sind doch laut Vereinbarung nur zwei Möglichkeiten der Anzeige und der Anker. Das hier sollte eigentlich "verboten" sein. An anderen Stellen hatte es doch funktinoiert.
- Die Badges für die Schlüsselwörter in der unitCard können dieselbe Farbe haben wir z.B. "Stationary". Man erkennt es einfach nicht. AUßerdem bei der Ork-UnitCard sollte das Schlüsselwort "Ork" (vor der leeren Badge) gar nicht in der unitCard angezeigt werden. Es ist ein Fraktionsschlüsselwort und das ist in der armyCard. (s. Bildschirmfoto vom 2026-07-11 11-49-25) Wie kann so etwas noch passieren? Die unitCard sollte Fraktions- und Subfraktionsschlüsselwörter gar nicht mehr zulassen. Bitte nochmal gezielt prüfen, ob das ein Fehler in der unitCard oder in der YAML-Struktur ist.
- Ich finde das Design des Rahmens der unitCard sehr schön. Ein heller Streifen auf der linken Seite, ansonsten ist der Rest des Randes dunkler (s. Bildschirmfoto vom 2026-07-11 11-54-31). Ist es möglich dieses "Design des Randes" beim zweiten Spieler vertikal zu spiegeln? Also dass der helle gelbe Rand rechts statt links ist? Und könnte man dieses Prinzip auf die Gos übertragen. Die sind zwar so grundsätzlich gut, aber ich empfinde es als zu grell. 
- Außerdem stelle ich immer wieder fest, dass die GO-Karten keine Schlüsselwörter zeigen, obwohl der Regeltext welche vorgibt. Bitte einplanen, dass ein Subagent diese Schlüsselwörter systematisch in der YAML-Struktur nachpflegt. 
- Die Beobachtungen aus Bildschirmfoto vom 2026-07-09 21-29-43 und Bildschirmfoto vom 2026-07-09 21-36-36 scheinen noch nicht für die Umsetzung geplant zu sein.
- Ist schon irgendwo eingeplant, dass wir das UI-Konzept der heroischen Intervention (s. Bildschirmfoto vom 2026-07-11 12-03-17) ausarbeiten, um es in allen anderen Phase auszurollen?
- Es scheint einen "Unfall" in den CommandProtocolls für den das Protokoll "Conqueringe Tyrant" zu geben (s. Bildschirmfoto vom 2026-07-11 12-05-42). Der blaue Hinweis wäre eher in der gameActionArea zu erwarten. Aber m.E. kann der verschwinden. Er steht ja in der armyCard. 
- Der State von "Call da WAAAGH" scheint bis zum Ende des Spiels zu gelten. Ist das wirklich regelkonform? Im Test habe ich den WAAAGH in der ersten Runde gespielt. Dann geht alles wie erwartet. In der zweiten Runde kommt dann Stufe 2, doch ab der dritten Runde bleibt der Buff wohl bestehen,in der viereten und fünften Runde sehe ich den Buff immer noch (s. Bildschirmfoto vom 2026-07-11 12-08-32). Das ist m.E. falsch! Da passt der End-State nicht.

## Zuletzt überführt

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
