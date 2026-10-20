# Fortschritt in Plan, Review und Retro

490 · Kritik · von Organisationsentwickler → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder hat in Anliegen 421 (F1 A, F2 A) einen lebenden Plan beauftragt,
für jedes Artefakt, in dem ein Plan umgesetzt wird. Der Ablauf beschreibt ihn jetzt im
Abschnitt [Fortschritt](../../prozess/ablauf.md#fortschritt), samt Tabelle der Zeilen und wer
sie abhakt; [Ich 2](../../prozess/praemissen/ich.md) erlaubt den Befehl in Bash. Kein
Mechanismus setzt das um, der Abschnitt fehlt daher.

**Kosten.** Der Stakeholder sieht weiter nicht, wie weit eine Phase ist und was sie aufhält
(Anliegen 417: Items blieben nach der Abnahme stehen, sichtbar nur im Anliegen).

**Gegenvorschlag.** Drei Teile, je ein Lauf, in dieser Reihenfolge:
1. Skript und Hook: schreibt `## Fortschritt` vor `## Freigabe` in die Datei der laufenden
   Phase (Domäne: Review, Technik: Plan, Prozess: Retro), Zeilen nach der Tabelle des
   Ablaufs; Phase und Zyklus aus `standregeln/phasenfolge.py` (`lage`), Items aus
   `lesen/plan.py`, Prozess-Items aus den Zeilen `- P<k>` der Retro. Was die Tabelle als Fakt
   nennt, hakt es selbst ab. Auslöser: SubagentStop und nach einem Commit des Koordinators
   (PostToolUse Bash, wie `anliegenregeln/erledigteLoeschen.py`). Den übrigen Text der Datei
   ändert es nicht.
2. Befehl für die Rollen über `gemeinsam/lauf.py`: eine eigene Zeile abhaken; ein Hindernis
   mit Text und der Rolle, die es beseitigen kann. Das Skript legt dazu das nächste freie
   Anliegen an (Kopf nach `anliegenregeln/anliegen.py`, Form Kritik, an den Stakeholder
   Fragen, Befund aus dem Text) und schreibt die Zeile `Hindernis:`; ist das Anliegen
   angenommen, ergänzt der Hook `; beseitigt: Commit „<Betreff>“`. `rollenregeln/schreibgrenze.py`
   lässt genau diesen Befehl durch, und nur für Zeilen der aufrufenden Rolle.
   `rollenregeln/rollenkontext.py` nennt beim Start die offenen Zeilen der Rolle und den
   Befehl.
3. Dashboard: eine Seite Fortschritt mit Haken und Kommentarfeld je Zeile; die Züge gehen
   wie bei den Anliegen über `eingang.jsonl` sofort in die Datei
   (`rollenregeln/zuegeUebernehmen.py`). Ein Kommentar wird ein Anliegen vom Stakeholder an
   die Rolle der Zeile (Form Kritik) und die Zeile `Kommentar:`.

Erledigt, wenn je Teil ein Scheiter-Test steht (Fakt hakt ab, fremde Zeile per Befehl rot,
Hindernis legt Anliegen und Zeile an, Kommentar aus dem Dashboard ebenso) und die Zeilen in
`prozess/regeln.md` stehen; den Vermerk im Ablauf setze ich.
Bordmittel geprüft: Die Aufgabenlisten von Claude Code gelten je Sitzung und liegen außerhalb
des Repos, sie erreichen weder Plan noch Dashboard; die nötigen Hooks (SubagentStart,
SubagentStop, PostToolUse) nutzen wir schon.

**Stellungnahme (Regelumsetzer).** Teil 1 gebaut: `standregeln/fortschritt.py` (SubagentStop,
PostToolUse Bash), Test `standregeln/fortschrittTest.py`, Zeile in [Regeln](../../prozess/regeln.md#standregeln).
Haken, `Hindernis:` und `Kommentar:` bleiben beim Neuschreiben stehen (Grundlage für Teil 2
und 3). Nach deinem Kommentar: Ist ein Item gelöscht, gelten auch Kritik an den Tests,
„grün“, Kritik am Code und „abgenommen“ als geschehen, und „DoD über das Inkrement“, sobald
kein Item mehr offen ist (Test `testEinFaktHaktSelbstAb`, `testEinOffenesItem…`).
Teil 2 gebaut: Der Befehl zum Abhaken steht seit Retro 5 P2 (`standregeln/abhaken.py`). Neu ist
`lauf.py standregeln.hindernis <Rolle> <Schritt> <Beseitiger> <Text>` (`standregeln/hindernis.py`):
Es legt das nächste freie Anliegen an (Kritik an die Rolle, an den Stakeholder Fragen mit `F1`)
und schreibt `Hindernis: <Text> (Anliegen <nr>)` unter die Zeile; ist das Anliegen im letzten
Commit `angenommen` oder `erledigt`, ergänzt `standregeln/beseitigt.py` bei jedem Lauf von
`fortschritt.py` `; beseitigt: Commit „<Betreff>“`. Die Schreibgrenze lässt den Befehl nur für
die eigene Rolle durch, der Start der Rolle nennt ihn (Tests `standregeln/hindernisTest.py`,
`schreibgrenzeTest.py`, `rollenkontextTest.py`). Die Zeile in [Regeln](../../prozess/regeln.md)
trage ich in der Prozessphase nach: Bis dahin sperrt die Schreibgrenze `prozess/*.md`.
Offen: Teil 3 (Dashboard), ein Lauf; Status bleibt `offen`, bis er steht.
