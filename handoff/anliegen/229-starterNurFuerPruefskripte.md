# Der Starter läuft jedes Modul, nicht nur Prüfskripte

229 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Commit 4b492f5, `prozess/pruefungen/gemeinsam/lauf.py`: `starten` reicht jeden
Modulnamen an `runpy.run_module`. Probiert: `python3 prozess/pruefungen/gemeinsam/lauf.py platform`
und `… lauf.py json.tool` laufen. Ebenso erreichbar sind `pip`, `zipfile`, `tarfile`,
`http.server`. Zwei Freigaben prüfen nur den Anfang des Befehls:
- `Bash(python3 prozess/pruefungen/*)` in `.claude/settings.json`: ohne Rückfrage, für jeden Lauf;
- `"python3 prozess/pruefungen/"` in `rollenregeln/bashPositivliste.py` (`erlaubt`, Koordinator).

Vor dem Umzug deckte dieser Anfang nur Dateien unter `prozess/pruefungen/`. Jetzt deckt er
jedes Modul der Umgebung. Beispiel: `… lauf.py zipfile -e a.zip .` überschreibt Dateien,
ohne dass `schreibgrenze.py` oder die Bash-Heuristik es sehen. `… lauf.py pip install x`
ändert die Umgebung ohne Rückfrage. Schon vorher offen und ungeprüft:
`python3 prozess/pruefungen/../../x.py` passt auf denselben Anfang (`istErlaubt` löst den
Pfad nicht auf).

**Kosten.** Die Positivliste des Koordinators („andere Arbeit beauftragst du bei einer Rolle“)
und die Erlaubnis ohne Rückfrage reichen weiter, als ihr Text sagt. Das widerspricht dem Ziel
von 225 (keine Lücke für beliebige Aufrufe). Sicher abgefangen wird das erst mit der Sandbox
(215).

**Gegenvorschlag.** Der Starter ist die Schnittstelle zu allen Prüfskripten, also prüft er
seine Eingabe selbst. Das bleibt so klein wie im Altbestand: Dort sagt
`ArbiterMap/backend/app/domain/rule_checks.py` an einer Stelle, was erlaubt ist.
1. `starten` nimmt nur `<themenordner>.<modul>`, und die Datei
   `prüfskripteOrdner/<themenordner>/<modul>.py` muss existieren. Sonst endet der Lauf mit
   Code ≠ 0 und nennt den Modulnamen. Etwa 6 Zeilen.
2. Scheiter-Tests in `gemeinsam/laufTest.py`: `platform`, `json.tool`, `gemeinsam` (Ordner
   ohne Modul) und `standregeln..stand` rot, `standregeln.stand` grün.
3. `bashPositivliste.istErlaubt` löst Pfade hinter `python3` auf; was nicht unter
   `prozess/pruefungen/` liegt, ist rot. Gegenbeispiel `python3 prozess/pruefungen/../../x.py`.

Erledigt, wenn die Tests aus 2 und 3 an ihren Gegenbeispielen rot sind und
`python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.**
