# Kritik an 3e61977: Testdatei je Anforderung, Enum-Erkennung, Archiv der Anliegen

87 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
Gegenstand: 3e61977 (P9, Anliegen 52, 60, 62, 53, 76, 77, 78) und 5166eb6 (Hooks P2, P3).
In Ordnung: 5166eb6 ohne Befund; `python3 -m pytest prozess/pruefungen` 359 grün; der Stand
braucht 0,14 s; `plan.py`, `sprung/`, `codekritik.py` ohne Befund. Lesbarkeit: 86.

**Befund.**
1. [`rueckverfolgung.py`](../../prozess/pruefungen/rueckverfolgung.py),
   `anforderungenMitTestdatei`: Geprüft wird nur, wo die Testdatei der Anforderung schon da
   ist. Nennt ein offenes Item eines freigegebenen Plans `AUF-2` und `aufstellen/auf2Test.py`
   fehlt, bleibt `verstöße` leer und `wartende` nennt nichts (nachgestellt mit `umfasst` =
   wahr). Vor 52 deckte die eine Testdatei alle Anforderungen der Datei ab.
2. Ebenda, `anforderungsVerstöße`: Ergänzt der Anforderungsautor in `aufstellen.md` ein
   `### AUF-2`, ist `aufstellenTest.py` sofort eine Sammeldatei und der Prüflauf rot („teilen
   nach Anforderung“), bevor ein Plan AUF-2 nennt (nachgestellt).
3. [`glossar.py`](../../prozess/pruefungen/glossar.py), `istEnum` und `enumWerte`:
   `class Aufstellungszone(enum.Enum)` (Attribut statt Name), `Flag`, `IntFlag` und ein Wert
   mit Annotation (`nord: int = 1`) gehen ohne Meldung durch (nachgestellt).
4. [`erledigteLoeschen.py`](../../prozess/pruefungen/erledigteLoeschen.py): `git ls-files`
   nennt, was im Index steht, nicht, was committet ist. Der Test `versionieren` macht nur
   `git add -A` und nennt das „wie ein Commit es täte“. Der Gegenvorschlag in 78 war hier zu
   ungenau.

**Kosten.** Zu 1: Ein Kriterium im Plan ohne jeden Test erfüllt die DoD (Kriterium ↔ Test),
und niemand bemerkt es. Zu 2: Der Commit des Anforderungsautors scheitert an einer Aufgabe
des Testautors. Das widerspricht 62. Zu 3: Mit einer gängigen Schreibweise lässt sich P9
umgehen. Zu 4: Scheitert der Commit nach `erledigteLoeschen` (der pre-commit-Rahmen wertet
eine gelöschte Datei als Änderung durch den Hook), ist die Datei nur noch im Index. Das
nächste `git add -A` streicht sie, ohne dass sie je committet war: Das war der Fall in 78,
Punkt 3.

**Gegenvorschlag.**
1. Jede Anforderung, die ein offenes Item eines freigegebenen Plans nennt, braucht ihre
   Testdatei. Fehlt sie, ist das rot („<pfad> fehlt“), sonst nennt `wartende` die
   Anforderung. Scheiter-Test: Plan nennt AUF-2, `auf2Test.py` fehlt, Ergebnis rot.
2. Die Sammeldatei ist erst rot, wenn ein freigegebener Plan eine zweite Anforderung der
   Datei umfasst. Bis dahin gilt sie für AUF-1, und der Stand nennt das Teilen als wartend.
   Scheiter-Test: AUF-2 ohne Plan bleibt grün.
3. In `istEnum` auch `ast.Attribute` prüfen (`basis.attr`), dazu `Flag` und `IntFlag`. In
   `enumWerte` auch `ast.AnnAssign` mit Wert. Scheiter-Tests zu `enum.Enum` und `nord: int = 1`.
4. Bekannt ist eine Datei, wenn `git ls-tree -r --name-only HEAD -- handoff/anliegen` sie nennt.
   Scheiter-Test: eine erledigte Datei, die nur gestaged ist, bleibt liegen.

**Stellungnahme.** Umgesetzt. 1 Fehlt die Testdatei einer von einem offenen Item des freigegebenen Plans genannten Anforderung, ist das rot („<pfad> fehlt“), sonst nennt der Stand die Anforderung als wartend; Scheiter-Tests `testFehlendeTestdateiEinerUmfasstenAnforderungIstRot`, `…NichtUmfasstenAnforderungWartet`. 2 Die Sammeldatei gilt der ersten Anforderung und ist erst rot, wenn ein freigegebener Plan eine spätere nennt; vorher wartet die spätere (Stand: „AUF-2 wartet auf den Testautor“); `testSammeldateiBleibtGrünBisEinPlanEineSpätereAnforderungUmfasst`. 3 `istEnum` erkennt `enum.Enum`, `Flag`, `IntFlag`, `enumWerte` auch `nord: int = 1`; drei Tests in `glossarTest.py`. 4 Bekannt ist, was `git ls-tree -r HEAD` nennt; `versionieren` in `erledigteLoeschenTest.py` committet jetzt, `testNurVorgemerktesErledigtesBleibtLiegen`.
