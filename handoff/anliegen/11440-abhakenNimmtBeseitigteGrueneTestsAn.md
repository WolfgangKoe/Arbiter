# Abhaken nimmt beseitigte grüne Tests an

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf nach [Kritik](../../prozess/ablauf/kritik.md) (Prüfung hält den Happy
Path auf), aus [11360](11360-abhakenTrotzBegruendetGruenerTests.md):
1. `standregeln/abhaken.py` (`grünVorDemCode`) kennt von der Regel
   [Standregeln, Retro 9 P1](../../prozess/regeln/standregeln.md) nur „rot machen“, nicht „die
   Stelle nennen“. Ein Test, den der Code früherer Items schon erfüllt, bleibt grün; der
   Befehl hakt nie ab und legt bei jedem Versuch ein neues Hindernis an (11263 doppelt zu
   11001). Trifft im Plan die Kritik an den Tests zu anhaltenUebergehen (beide Kritiker) und
   zu loslassenNebenDerKarte (11262).
2. Unter „Architekt: Kritik an den Tests zu Item anhaltenUebergehen“ steht ein Hindernis mit
   Anliegen 11382; die Datei gibt es weder im Ordner noch in git (angelegt, dann vor dem
   Commit entfernt, ersetzt durch 11360). Die Zeile erhält nie `beseitigt` und hält den
   Schritt nach [Fortschritt](../../prozess/ablauf/fortschritt.md) (Befehl) für immer auf.

**Kosten.** Ohne 1 kommt kein Item, das bestehende Tests umbaut, zum Implementierer. Die
Änderung trifft `abhaken.py`, `fortschritt.py` und ihre Tests, keine Regel der Rollen.

**Gegenvorschlag.** Bestehende Regel anpassen, keine neue ([Ich 4](../../prozess/praemissen/ich.md)):
1. `grünVorDemCode` läuft nach `fortschrittSchreiben`, damit `beseitigt` aktuell ist. Ein
   grüner Test zählt nicht, wenn ein Hindernis *desselben Schritts* mit `; beseitigt:` ihn
   nennt: genau sein Name samt Parameter, gelesen mit
   `\btest\w+(?:\[[^\]\s]*\])?` (an plan.md erprobt: 11001 nennt alle 23 grünen Tests aus
   11263). Ein Hindernis eines anderen Kritikers zählt nicht; jeder prüft die Stelle selbst.
   Nennt ein Hindernis des Schritts ohne `beseitigt` schon alle übrigen grünen Tests, legt
   der Befehl kein neues an, endet mit 1 und nennt dessen Anliegen. Das Hindernis nennt nur
   die übrigen.
   Regelzeile: „Ist beim Abhaken von ‚Kritik an den Tests zu Item …‘ ein Test des Items grün,
   den kein beseitigtes Hindernis desselben Schritts nennt, hakt der Befehl nicht ab, endet
   mit 1 und meldet dem Testautor ein Hindernis mit diesen Tests, außer ein offenes des
   Schritts nennt sie schon (rot machen oder die Stelle nennen, die das Kriterium erfüllt;
   die Stelle prüft der Kritiker in seiner Nachprüfung, Anliegen 11360)“.
   Tests in `abhakenTest.py`: grün und im beseitigten Hindernis genannt hakt ab; nur im
   Hindernis des anderen Kritikers genannt meldet eines; im offenen genannt meldet keines
   neu und nennt es; teils genannt meldet nur die übrigen.
2. `fortschritt.py` lässt eine Zeile `Hindernis:` fallen, deren Anliegen weder als Datei noch
   in git besteht. Test in `fortschrittTest.py`: Hindernis mit fehlendem Anliegen
   verschwindet, mit uncommittetem bleibt.

Rückweg: der Commit, der es baut. Den Ablauf ändert das nicht; er sagt schon, dass ein
Kritiker abhakt, wenn kein Hindernis ohne `beseitigt` unter seinem Schritt steht.

**Stellungnahme.** Berechtigt, umgesetzt wie vorgeschlagen.
1. `grünVorDemCode` läuft nach `fortschrittSchreiben`; ein grüner Test zählt nicht, wenn ein
   Hindernis desselben Schritts mit `; beseitigt:` ihn mit Namen samt Parameter nennt. Nennt ein
   offenes Hindernis des Schritts die übrigen schon, legt der Befehl kein neues an, endet mit 1
   und nennt dessen Anliegen; sonst meldet er nur die übrigen.
2. `fortschritt.py` lässt über `verwaisteFallenLassen` (`beseitigt.py`) Zeilen `Hindernis:` fallen,
   deren Anliegen weder Datei noch in git ist.
Tests: `abhakenTest.py` (vier Fälle), `fortschrittTest.py`. Eingetragen in
[Standregeln](../../prozess/regeln/standregeln.md). Rückweg: der Commit, der es baut.
