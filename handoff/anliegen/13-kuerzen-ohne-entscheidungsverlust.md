# Etappen 2 bis 7 kürzen, ohne Entscheidungen zu verlieren

13 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Nach E53 schrumpfen die Etappen 2 bis 7 auf je eine Zeile (200 Zeichen,
`test_hoechstmasse.py`, derzeit rot). Ihre Texte tragen Entscheidungen des Stakeholders, die
sonst nirgends stehen, etwa in [Etappe 2](../../domaene/etappen/02-bewegen.md): gerade
Teilstrecken mit Summe höchstens M, „Bewegung der Einheit beenden“ mit Kohärenzprüfung,
„Bewegungsphase beenden“, kein Normal Move nach übergangener Sperre in Engagement Range
(F5 bis F7, Anliegen 02 und 04, beide nur noch in git).

**Kosten.** Wird Etappe 2 aktuell, formuliert der Planer sie neu aus der einen Zeile. Findet
er die Entscheidungen nicht, fragt er erneut oder erfindet; dasselbe Muster wie F8 ohne Ort
(Anliegen 06, git). Für die Technik zählt Punkt 1: Die Abstandsprüfung je Teilstrecke formt
die Schnittstelle des Bewegens; eine Umkehr trifft Fachlogik, Dienst und Karte
(Altbestand `movement_service.py:269-285`, Anliegen 02).

**Gegenvorschlag.** Kürzen wie E53, Dateinamen bleiben. Wer eine Etappe ausformuliert, liest
zuerst `git log -p --follow` ihrer Datei und übernimmt die dort getroffenen Entscheidungen.
Kein neues Artefakt, git bleibt das Archiv. Die Arbeitsanweisung gehört in die Definition des
Planers; das wäre ein Anliegen an den Organisationsentwickler, falls du zustimmst.

**Stellungnahme.**
Angenommen und umgesetzt: Etappen 2 bis 7 je eine Zeile, Dateinamen bleiben. Ergänzung: Die
Entscheidungen stehen nicht nur in den Etappen, sondern auch in Anliegen (F4 und F11 sind in
Anliegen 09 zurückgestellt). Wer eine Etappe ausformuliert,
liest daher `git log -p --follow` ihrer Datei und `git log -p -- handoff/anliegen/`, gefiltert
nach der Etappe. Die Arbeitsanweisung für die Definition des Planers steht in
Anliegen 14, dort erledigt; sie steht in der [Definition des Planers](../../.claude/agents/planer.md).
