# Ist der Domänencode SOLID? Viele if

152 · Kritik · von Stakeholder → Architekt · Runde 1/3 · offen

## Runde 1
**Befund (Stakeholder).** „Eine potentielle Kritik meinerseits an den Architekten bzw.
Implementierer. Ich bin mir nicht sicher, ob der bereits geschriebene Code SOLID ist und die
Kritik-Entwickler in den bisherigen Projekten berücksichtigt. Ich sehe hier auch wieder viele
if statements. Noch geht es, aber das Muster möchte ich nicht fördern. Ich möchte lesen
können, was eine Funktion oder der Produktivcode macht.“ (Offen war
`technik/arbiter/domaene/spielobjekte.py`.)

**Stellungnahme (Architekt).** Zum Teil berechtigt. In `spielobjekte.py` steht kein `if`;
die Datei zeigt das Gegenstück: Spielobjekte ohne Verhalten. Die 22 `if` stehen in
`phasen/aufstellen.py`, Klasse `Aufstellung`. Beides hängt zusammen: Was `Armee` oder
`Aufstellungszone` selbst beantworten könnte, fragt `Aufstellung` mit `if` ab. Das ist der
Befund „Domänenmodell zu implizit“ aus `handoff/kritik-entwickler.md`.

SOLID, kurz:
- S (eine Aufgabe je Klasse): zum Teil verletzt. `Aufstellung` trägt die Regeln der Phase,
  das ist gewollt (Grundschnitt), aber auch Geometrie (`_grenzenInX`) und Fragen an die
  Armee (`_modelleVon`).
- O (Neues ergänzen, ohne Bestehendes zu ändern): verletzt. Jeder neue Grund, als nächster
  die Kohärenz, ist ein weiteres `if` in `_gründeGegenDieStelle`.
- L und I: noch keine Vererbung und keine Schnittstellen; nichts zu prüfen.
- D (Abhängigkeiten nach innen): erfüllt. Die Domäne kennt weder Flask noch Datenbank,
  geprüft von `importvertrag.py` (A1).

Nicht jedes `if` ist ein Problem. Die Wächter am Anfang einer Handlung sind gewollt, je einer
für ein Kriterium; sie lesen sich wie die Anforderung, etwa AUF-1.2 „der Gewinner wird nur
einmal gewählt“: `if self._gewinner is not None: raise Sperre(Grund.nichtWählbar)`.
Drei Stellen dagegen fragen, was Daten oder ein Begriff beantworten sollten:
1. Die Sperren beim Setzen als Kette `if … gründe.add(…)`. Positiv im Altbestand:
   `ArbiterMap/backend/app/domain/rule_checks.py`, je Regel eine kleine Funktion
   (`check_coherency`, `check_engagement_range`); `check_rules` sammelt nur ein.
2. `aufstellungszone(spieler)` leitet die Zone mit drei `if` und `next(…)` aus dem Gewinner
   ab; eine Zuordnung Spieler → Zone, angelegt bei der Zonenwahl, schlägt nur nach.
3. `_modelleVon(spieler)` gehört als `modelle` an die `Armee`, die Grenzen einer Zone nicht
   in die Klasse `Aufstellung`.

Kritik-Entwickler, Stand: kurze Namen (`benennung.py`), Komplexität (complexipy, ruff) und
fachliche Akzeptanztests sind umgesetzt. Die Schwellen messen aber je Funktion; dieser
Befund liegt in der Verteilung auf Klassen, und `wir.md` 9 überlässt ihn dem Urteil des
Reviewers. Darum bekommt die Architektur eine Regel: **D4** Ein Grund ist eine benannte
Prüfung, eine Handlung sammelt die Gründe aus einer Tabelle; ein neuer Grund ändert keine
bestehende Funktion. Sie geht nach architektur.md, sobald dort Platz ist
([155](155-technikBrauchtPlatzUndErstesMockup.md)).

**Gegenvorschlag.** Den Umbau macht der Implementierer zu Beginn der Technikphase von
Zyklus 3, bevor die Oberfläche `Aufstellung` aufruft; Erledigt-Bedingung in Anliegen 154
(in git). Polymorphie nicht um ihrer selbst willen: wenige Fälle bleiben `if` mit frühem
`return` (`wir.md` 9).

Stand: Der Umbau ist erledigt (Commit `b940ef8`, Anliegen 154). Die Sperren beim Setzen
stehen als Tabelle Grund → Prüfung, die Zone schlägt eine Zuordnung nach, `Armee.modelle`
steht in `spielobjekte.py`. Offen ist Regel D4 in der Architektur.

wartet auf 155
