# Höchstmaß der Moderation

73 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Der Stakeholder hat die Rolle [Moderator](../../.claude/agents/moderator.md)
eingesetzt (Anliegen 65, F1). Sie schreibt `handoff/moderation.md`, höchstens 4.000 Zeichen,
damit der Koordinator sie lesen kann (`lesegrenze.py`). `hoechstmassTest.py` prüft die Datei
nicht.

**Kosten.** Wird die Datei länger, liest der Koordinator sie nicht, und die Freigabevorlage
nennt die Sortierung ohne Inhalt.

**Gegenvorschlag.** In `hoechstmassTest.py` ein Fall `handoff/moderation.md` mit 4.000
Zeichen, wenn die Datei existiert; Scheiter-Test wie `testZuLangesAnliegenWärRot`.

**Stellungnahme.** Umgesetzt in `hoechstmassTest.py`: `handoff/moderation.md` höchstens 4.000 Zeichen, wenn sie existiert; Scheiter-Test `testZuLangeModerationWärRot`.
