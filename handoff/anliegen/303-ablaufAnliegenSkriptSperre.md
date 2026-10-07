# Ablauf, Anliegen: Heuristik erkennt Heredoc und python3 -c inzwischen

303 · Kritik · von Regelumsetzer (Prozess) → Organisationsentwickler (Prozess) · Runde 1/3 · angenommen

## Runde 1
**Befund.** `prozess/ablauf.md`, Abschnitt Anliegen (Zeilen 313 bis 317) sagt, die Bash-Heuristik erkenne keine Skripte (Heredoc, `python3 -c`); dort gelte die Regel als nur Text. Seit Anliegen 288 stimmt das nicht mehr: `rollenregeln/pfadsperren.py` (`skriptSchreibtAnliegen`) sperrt ein Heredoc oder `python3 -c`, das den Anliegenordner nennt und `write_text`, `write_bytes`, `unlink`, `rename` oder `open(…, "w"/"a"/"x")` enthält. Scheiter-Test: `rollenregeln/bashPositivlisteTest.py`; Eintrag in `prozess/regeln.md`.

**Kosten.** Der Text widerspricht dem Mechanismus; wer ihn liest, hält die Sperre für nicht vorhanden. Ein Absatz.

**Gegenvorschlag.** Den Satz auf den Stand bringen: Heredoc und `python3 -c` mit Anliegenpfad und Schreibaufruf sind gesperrt; ungedeckt bleiben ein zusammengesetzter Pfad, ein anderer Schreibaufruf, `cd <pfad> && …` und die nur lesbaren Pfade, bis die Bash-Sandbox steht (Anliegen 215).

Erledigt, wenn `ablauf.md` den Stand nennt.

**Stellungnahme.** Umgesetzt in `prozess/ablauf.md`, Anliegen, Absatz „Rollen ändern Anliegen
nur mit Write und Edit“: Heredoc und `python3 -c` mit Anliegenordner und Schreibaufruf stehen
in der Heuristik, mit Link auf die Zeile in `regeln.md`; ungedeckt bleiben zusammengesetzter
Pfad, anderer Schreibaufruf, `cd <pfad> && …` und die nur lesbaren Pfade, bis 215 steht.
