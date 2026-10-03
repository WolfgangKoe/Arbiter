# Ablauf und Prämisse nach den gebauten Mechanismen

33 · Anliegen · von Regelumsetzer (Prozess) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** Der Regelumsetzer darf `prozess/ablauf.md` und `prozess/praemissen/wir.md` nicht
schreiben. Nach den gebauten Mechanismen ([Regeln](../../prozess/regeln.md)) stimmen dort
einige Angaben nicht mehr:
1. `ablauf.md`, Anliegen: `test_hoechstmasse.py (Wert noch 2.400)` heißt jetzt
   `hoechstmassTest.py`, Wert 4.000.
2. `ablauf.md`: „Mechanismus: nur Text“ ist überholt bei: Anliegen-Kopf maschinenlesbar
   (`anliegen.py`, `anliegenTest.py`), Status `erledigt` rot (`anliegenTest.py`), Stand nennt
   Nachprüfungen mit Rolle (`stand.py`), Budget (`belegung.py`: Meldung ab 120.000, Sperre
   ab 150.000, Freigabe des Stakeholders in `.git/arbiter/belegungsgrenze.txt`; der Stand
   zeigt die Belegung, die Rollenläufe bleiben Kennzahl), DoD 2 für Benennung und
   Kriterium ↔ Test.
3. `wir.md`: Regel 1 bis 5 haben jetzt `benennung.py`, Regel 3 und 4 zusätzlich
   `rueckverfolgung.py`. Regel 6 bis 8 bleiben Text.
4. `ablauf.md` nennt weiter als „nur Text“: der Hook, der nach jedem Rollenlauf die
   geänderten Status und die Belegung der Rolle meldet, die dran ist. Er ist nicht gebaut
   (braucht die Belegung des vorigen Laufs; Auftrag fehlt).
5. Schreibschutz: `VORGEHEN.md`, `handoff/kritik-entwickler.md`, `Arbiter/`, `ArbiterMap/`
   sind für alle nur lesbar (`schreibgrenze.py`, `bashPositivliste.py`); das gehört in den
   Ablauf oder die Root-`CLAUDE.md`.
6. Der Koordinator liest `git show` nur mit `--stat` oder für Dateien unter 4.000 Zeichen.

**Kosten.** Veraltete Vermerke lassen Rollen Regeln für Text halten, die ein Hook schon
durchsetzt, und umgekehrt.

**Gegenvorschlag.** Die Vermerke und Dateinamen nachziehen; die Namensangaben nennen die
Skripte in `prozess/pruefungen/` (camelCase, `…Test.py`).

**Stellungnahme.**
