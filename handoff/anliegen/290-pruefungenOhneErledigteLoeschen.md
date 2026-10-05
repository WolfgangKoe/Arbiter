# Prüflauf löscht keine erledigten Anliegen mehr

290 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Aus [289](289-pruefungenBrechenAmHookDesNachbarnAb.md), angenommen:
`prozess/pruefungen/conftest.py` ruft in `pytest_configure` den Hook `erledigteLöschen` auf.
Ein halber Stand in `anliegenregeln/erledigteLoeschen.py` (oder einem seiner Importe) bricht
damit jeden Prüflauf jeder Rolle ab, bevor ein Test läuft; jeder Lauf, auch der einer
Lese-Rolle, löscht erledigte Anliegen im gemeinsamen Arbeitsbaum. Die Regel
([Ablauf, Anliegen](../../prozess/ablauf.md#anliegen): `erledigt` löscht die Datei, ohne
eigenen Lauf) ist mit pre-commit und SubagentStop erfüllt; der Prüflauf als Auslöser trägt
nichts bei, was diese beiden nicht schon tun.

**Kosten.** Solange ein Lauf der Kette Hook-Code ändert, läuft in den anderen Strängen kein
Test; Rot in den eigenen Dateien fällt erst beim Commit auf.

**Gegenvorschlag.**
1. `prozess/pruefungen/conftest.py`: Aufruf und Import von `erledigteLöschen` entfernen; die
   Datei bleibt, weil sie den Importpfad stellt (289); Docstring nach der neuen Aufgabe.
2. `anliegenregeln/erledigteLoeschenTest.py`: `testDerPrüflaufRuftErledigteLöschenVorDemSammelnAuf`
   umkehren: `conftest.py` importiert kein Hook-Modul.
3. `prozess/regeln.md`, Zeile zu `erledigteLoeschen.py`: „Lauf von
   `python3 -m pytest prozess/pruefungen`“ streichen.

Kein Hook-Code ([Ablauf, Gleichzeitige Läufe](../../prozess/ablauf.md#gleichzeitige-läufe),
Bedingung 3): `conftest.py` startet `.claude/settings.json` nicht. Der Lauf passt in
Strang 3 der [Moderation](../moderation.md), sobald `conftest.py` und
`erledigteLoeschenTest.py` frei sind; beide ändert gerade ein Nachbar (Fixture `gitRepo`).

Erledigt, wenn ein `NameError` in `erledigteLoeschen.py` den Prüflauf nicht mehr abbricht
und nur dessen eigene Tests rot werden.

**Stellungnahme.**
