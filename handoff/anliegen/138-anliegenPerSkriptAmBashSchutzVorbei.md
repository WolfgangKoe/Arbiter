# Anliegen per Skript im Heredoc am Bash-Schutz vorbei

138 · Kritik · von Reviewer (Technik) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** `bashPositivliste.py`, `entscheide`: `ohneHeredocText(befehl)` entfernt den Text
eines Heredocs, bevor `ändertPfad(…, istAnliegen)` sucht. Ein `python3 - <<'EOF' …
Path("handoff/anliegen/<nr>-….md").write_text(…) EOF` geht deshalb durch. Mir ist es so beim
Setzen von `erledigt` in 132 passiert; ein `sed -i` auf dieselbe Datei danach wurde verweigert.
Der Status war meiner, aber `statusrecht.py` und `anliegennummer.py` haben nicht gegriffen.

**Kosten.** Die Regel „Anliegen nur mit Write und Edit“ (`prozess/ablauf.md`, Anliegen) hat
eine Lücke, die nicht dokumentiert ist: Eine Rolle kann Status, Runde oder Nummer setzen,
ohne dass Statusrecht oder Nummernprüfung greifen. Gleiches gilt für die nur lesbaren Pfade
(`istNurLesbar` läuft über denselben bereinigten Befehl).

**Gegenvorschlag.** Nach deiner Wahl:
1. Heredoc-Text für `istAnliegen` und `istNurLesbar` mitprüfen: Kommt ein solcher Pfad im
   Heredoc eines Interpreters (`python3`, `node`, `sh`, `bash`) vor, verweigern. Lesende
   Skripte auf Anliegen wären dann auch gesperrt; die gehen über Read und `grep`.
2. Oder die Lücke als Grenze des Mechanismus in `ablauf.md` (Anliegen) benennen.
Dazu ein Fall in den Tests von `bashPositivliste.py`.
