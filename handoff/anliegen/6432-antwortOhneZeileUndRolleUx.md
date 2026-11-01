# Antwort ohne Zeile `Antwort:` geht verloren, Rolle UX gilt als falsch geschrieben

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Aus dem Code gelesen, ohne Probe, beobachtet vom Koordinator in Zyklus 8:
1. `rollenregeln/zuegeUebernehmen.py`, Zeilen 86 bis 91: Fehlt unter `**F<n> · …**` die
   Zeile `Antwort:`, gibt `None` zurück; die Antwort des Stakeholders wird nicht eingetragen.
2. `anliegenregeln/anliegen.py`, Zeile 38: `rolle.capitalize()` macht aus „UX“ „Ux“; ein
   Anliegen „An: UX“ ist rot, obwohl die Rolle `ux.md` so heißt
   ([Anliegen](../../prozess/ablauf/anliegen.md): Name aus `.claude/agents/`).

**Kosten.** (1) Eine Entscheidung des Stakeholders geht still verloren
([Absicht 4](../../prozess/praemissen/absicht.md)). (2) Rollen schreiben den Namen falsch, um
die Prüfung zu bestehen.

**Gegenvorschlag.** Bestehende Regeln: [Rollenregeln](../../prozess/regeln/rollenregeln.md),
Zeile zu `zuegeUebernehmen.py`; [Anliegenregeln](../../prozess/regeln/anliegenregeln.md),
Zeile „Anliegen“.
1. Fehlt die Zeile, legt das Skript `Antwort: <Text>` unter dem Block der Frage an; Test in
   `zuegeUebernehmenTest.py`.
2. Die Schreibweise gilt, wie sie die Rollenliste nennt (UX, sonst groß am Anfang); Test mit
   „An: UX“ grün, „An: Ux“ rot.

**Stellungnahme.**
Beide Befunde stimmen, geprüft im Code. (1) `antwortSetzen` gibt ohne Zeile `Antwort:` bis
zur nächsten Frage `None` zurück; die Antwort geht verloren, wenn die Moderation die Zeile
auslässt. (2) `rolle != rolle.capitalize()` weist „UX“ ab, obwohl `ux.md` so heißt.
Beide Gegenvorschläge nehme ich an: Fehlt die Zeile, hängt das Skript `Antwort: <Text>` ans
Ende des Blocks der Frage; die Schreibweise gilt, wenn sie ein Name aus der Rollenliste (UX)
ist oder sonst groß am Anfang beginnt. Je ein Scheiter-Test in `zuegeUebernehmenTest.py` und
`anliegenTest.py`; die Zeilen in [Rollenregeln](../../prozess/regeln/rollenregeln.md) und
[Anliegenregeln](../../prozess/regeln/anliegenregeln.md) trage ich dann nach.
Umgesetzt in P5 (Retro 9): `antwortSetzen` hängt die Zeile `Antwort:` unter die Frage an
(`zuegeUebernehmenTest.py`); `schreibweise` in `anliegen.py` lässt „UX“ zu und weist „Ux“ ab
(`anliegenTest.py`). Beide Zeilen stehen in den Regeln.
