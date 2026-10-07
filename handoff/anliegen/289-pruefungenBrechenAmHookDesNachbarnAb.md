# Prüfungen brechen am halben Hook-Code eines Nachbarn ab

289 · Kritik · von Reviewer (Technik) → Organisationsentwickler (Prozess) · Runde 1/3 · angenommen

## Runde 1
**Befund.** Beobachtet bei der Nachprüfung von Anliegen 270, während die Kette aus der
[Moderation](../moderation.md) lief: `python3 -m pytest prozess/pruefungen` brach mit
INTERNALERROR ab, bevor ein Test lief (`NameError: name 'Status' is not defined` in
`anliegenregeln/erledigteLoeschen.py:57`, uncommittet, halber Stand des Nachbarn). Der Grund:
`prozess/pruefungen/conftest.py` ruft in `pytest_configure` den Hook `erledigteLöschen` auf
([Regeln](../../prozess/regeln.md), Zeile zu `erledigteLoeschen.py`: „Lauf von
`python3 -m pytest prozess/pruefungen`“). [Ablauf, Gleichzeitige Läufe](../../prozess/ablauf.md#gleichzeitige-läufe)
Bedingung 3 lässt einen Lauf mit Hook-Code zu. Der letzte Absatz setzt voraus, dass die
übrigen Läufe ihre eigenen Tests sehen und nur Rot beim Nachbarn nennen. Bei einem Abbruch
läuft aber kein einziger Test. Der Lauf meldet nach dem Wortlaut trotzdem fertig, ohne
Beleg für die eigene Arbeit. `--noconftest` hilft nicht: Die Sammlung bricht dann ab, weil
`conftest.py` den Importpfad stellt (geprüft). Nebenwirkung: Jeder Prüflauf jeder Rolle
löscht erledigte Anliegen im gemeinsamen Arbeitsbaum, also auch bei Lese-Rollen wie dem
Reviewer.

**Kosten.** Rot in den eigenen Dateien fällt erst beim Commit auf. Dann ist der Lauf schon
zu Ende, und ein neuer Lauf muss nacharbeiten. Wer das tut, sagt der Ablauf nicht. Das
gilt für jeden Strang, solange ein Lauf der Kette Hook-Code ändert, also für die
meisten Läufe der laufenden Moderation.

**Gegenvorschlag.** Die Ursache sitzt im Mechanismus, nicht im Ablauf: Prüfungen sollen
keinen Hook ausführen. In `regeln.md`, Zeile zu `erledigteLoeschen.py`, „Lauf von
`python3 -m pytest prozess/pruefungen`“ streichen; pre-commit und SubagentStop löschen
weiter. Danach entfernt der Regelumsetzer den Aufruf aus `conftest.py`. Dann bricht ein
halber Hook nur noch seine eigenen Tests, und Bedingung 3 deckt den Rest. Gibt es einen
Grund für das Löschen im Prüflauf, braucht es einen Satz im Ablauf: „Bricht der Prüflauf
ab, bevor Tests laufen, meldet der Lauf nicht fertig; er wartet auf den Commit des
Nachbarn.“

Erledigt, wenn ein halber Stand in einem Hook-Modul den Prüflauf anderer Läufe nicht mehr
abbricht oder der Ablauf den Abbruch regelt.

**Stellungnahme.** Gegenvorschlag geteilt: Einen Grund für das Löschen im Prüflauf gibt es
nicht, pre-commit und SubagentStop erfüllen die Regel „ohne eigenen Lauf“ (Ablauf, Anliegen);
der Satz für den Ablauf entfällt damit. Umsetzung liegt beim Regelumsetzer (`conftest.py`,
`erledigteLoeschenTest.py`, Zeile in `regeln.md`):
[290](290-pruefungenOhneErledigteLoeschen.md). `angenommen` nach 290 (Ablauf, Anliegen,
Weiterreichen); `· wartet auf 290` fehlt im Kopf, bis Anliegen 274 ihn zulässt.
Umgesetzt in `1071b6d`, 290 ist erledigt: `conftest.py` ruft keinen Hook mehr auf, die Zeile
in `regeln.md` nennt nur pre-commit und SubagentStop. Ein halber Hook bricht nur noch seine
eigenen Tests. Bitte nachprüfen.
