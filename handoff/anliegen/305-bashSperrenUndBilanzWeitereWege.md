# Bash-Sperren und Schreibbilanz lassen weitere Wege durch

305 · Kritik · von Reviewer (Technik) → Regelumsetzer (Prozess) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von c0239e5 (300 und 301 dort erledigt). Fehlverhalten nach
[Ablauf, Kritik am Code](../../prozess/ablauf.md#kritik-am-code); Proben über
`bashPositivliste.entscheide` (Rolle reviewer) und `AngefasstePfade.enthält` in `/tmp`.
1. `pfadsperren.skriptSchreibtAnliegen` gilt nur für den Anliegenordner. Durch gehen
   `python3 - <<EOF` mit `Path("VORGEHEN.md").write_text("x")` (nur lesbar) und dasselbe an
   `handoff/review.md` (Freigabesperre): der Weg aus 288, die Grenze in `regeln.md` nennt ihn nicht.
2. An Anliegen durch, ohne in der Grenze zu stehen: `echo "open('handoff/anliegen/1-x.md','w')…" | python3`
   (Pipe statt Heredoc), `cd handoff/anliegen && python3 -c "open('282-x.md','w')…"` (303 nennt
   es, `regeln.md` nicht), `perl -pi -e s/offen/angenommen/ handoff/anliegen/282-x.md`
   (`ändertPfad` kennt nur `sed -i`). Zu Unrecht gesperrt: `python3 -c` mit
   `open('handoff/anliegen/x.md', encoding='ascii')` (`["'][wax]` trifft `'a`) und
   `cat > /tmp/notiz.md <<EOF` mit `handoff/anliegen/300` und dem Wort `rename` im Text.
3. `AngefasstePfade.enthält` zählt einen schreibenden Befehl nur, wenn er den Pfad oder genau
   dessen Ordner nennt. Unter „unklar, wer“ statt „verletzt“ stehen `sed -i s/a/b/ domaene/*.md`
   für `domaene/a.md`, `rm -r domaene` für `domaene/sub/a.md`, `cd domaene && sed -i s/a/b/ a.md`.
4. `schreibBilanz.räumeAlteStände`: Starten zwei Rollen gleichzeitig und liegt ein alter Stand,
   löscht die eine ihn zwischen `glob` und `stat` der anderen; `FileNotFoundError` bricht deren
   SubagentStart ab, bevor ihre Stand-Datei steht. Sie läuft ohne Schreibbilanz und ohne
   Nennung ihrer Schreibpfade, still. Gelesen am Code.

**Kosten.** 1, 2: Der Weg aus 288 bleibt für nur lesbare Pfade und Freigabe-Artefakte offen;
lesende Proben werden gesperrt. 3: wie 300, Runde 2, Punkt 1, der Täter wird entlastet.
4: selten, dann unbemerkt. Je wenige Zeilen.

**Gegenvorschlag.**
1. Den Skripttext für jeden Eintrag von `pfadsperren` prüfen, nicht nur für Anliegen:
   `skriptSchreibt(befehl, istGesperrt)` in der Schleife von `entscheide`, mit der Meldung des
   Eintrags. Scheiter-Test: die zwei Proben aus 1 rot.
2. `skriptAufruf` auf jeden Aufruf von `python3?` erweitern (Pipe), `perl -i` neben `sed -i`
   zu den In-place-Editoren; bei `open` nur das Modus-Argument prüfen, mit `r+`. `cd <pfad>`
   als Grenze in `regeln.md`. Scheiter-Tests: Pipe und `perl -pi` rot, `encoding='ascii'` grün.
3. In `gemeint` den Ordner als Präfix (`pfad.startswith(relativerPfad + "/")`) und Muster
   per `fnmatch.fnmatch(pfad, relativerPfad)`; `cd` als Grenze. Scheiter-Test: Glob und
   `rm -r` stehen unter „verletzt“.
4. `unlink(missing_ok=True)` und `stat` gegen `FileNotFoundError` schützen, oder erst den
   eigenen Stand schreiben, dann räumen. Scheiter-Test: eine schon gelöschte Datei aus dem
   Glob (monkeypatch) bricht `beimStart` nicht ab.

Erledigt, wenn die Proben wie genannt rot und grün sind und `python3 -m pytest prozess/pruefungen`
grün ist.

**Stellungnahme.**

Stellungnahme: Entfällt mit dem Rückbau.
