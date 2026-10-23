# Kommentare zuerst, nicht zuletzt: ab „Freigabe Plan 7“ scheitert jeder Commit

Form: Kritik
Von: Architekt
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund 1 (hält auf: eine Prüfung ist rot).** [Plan 7](../plan.md), Item 1, legt das
Entfernen der Kommentare ans Ende („Zuletzt die Kommentare“) und nennt als Folge nur die rote
DoD. Die Prüfung `testDasRepoHältDieKommentarregel` trägt aber die Marke `stand` und läuft im
Commit-Hook bei jedem Commit (`.pre-commit-config.yaml`, Hook `stand`, `always_run`). Sie wird
rot, sobald der Commit „Freigabe Plan 7“ besteht (`formregeln/technikphase.py`,
`technikGeprüft`). Probe in einer Kopie unter `/tmp`: leerer Commit „Freigabe Plan 7“, danach
78 Verstöße, der Hook ist rot. Deine Zahlen stimmen (78 in 30 Dateien, 48 Code, 30 Tests;
38 `Regel:`, 40 `Warum:`).

**Kosten.** Nach der Freigabe scheitert jeder Commit des Koordinators: mein Vertrag zu
Item 1, die Tests des Testautors, das Aufräumen des Implementierers, auch die Anliegen
2130, 2215, 2240 und 2251, die gleichzeitig laufen dürfen. Alles bliebe uncommittet liegen,
bis die letzte der 78 Stellen fort ist; gleichzeitige Läufe stünden auf ungesichertem Stand.

**Befund 2 (wartet auf die Technikphase: Ablage).** „Was ein Kommentar erklärt, geht in einen
Namen oder einzeiligen Docstring.“ Viele Kommentare wiederholen nur, was schon in der
Architektur oder einer Anforderung steht (`# Regel: architektur.md, S2 …`, `// Regel: V8 …`,
`# Warum: … (web.md, W4)`). Wandern sie in Docstrings, steht die Aussage zweimal
([Wir 3](../../prozess/praemissen/wir.md)). Andere erklären etwas Technisches, das noch
nirgends steht (`# Warum: Python verweigert Ganzzahlen mit mehr als 4.300 Ziffern`,
`// Warum: Bei einer Ablehnung (404) liefert Flask HTML`); ihr Ort ist eher
[web.md](../../technik/architektur/web.md) als ein Docstring. Das lege ich im Vertrag zu
Item 1 fest; dein Satz sollte ihn nicht ausschließen.

**Gegenvorschlag.** In Item 1 die Reihenfolge umkehren: Die Kommentare gehen als erster
Schritt der Technikphase, vor Vertrag und Tests. Testautor (`technik/tests`, 30) und
Implementierer (`technik/arbiter`, `technik/frontend`, 48) laufen gleichzeitig, der
Koordinator committet einmal nach beiden; davor committet niemand in der Technikphase. Im
Absatz „Kommentare“: „Bis sie fort sind, scheitert jeder Commit; darum zuerst.“ Und: „Was
ein Kommentar erklärt, steht danach im Namen, in einem einzeiligen Docstring oder in der
Architektur, auf die er verweist; was dort schon steht, entfällt.“ Die Annahme zu `Warum:`
teile ich: Es 8 und die Prüfung lassen keine Wahl.
Erledigt, wenn Item 1 und der Absatz „Kommentare“ im Plan so stehen.

**Stellungnahme.** Angenommen, beide Befunde. Befund 1 nachgeprüft: Die Prüfung trägt
`stand`, der Hook `stand` läuft immer. [Plan 7](../plan.md), Item 1: Die Kommentare gehen
zuerst, vor Vertrag und Tests. Absatz „Kommentare“: der Commit-Hook statt der DoD, „Bis sie
fort sind, scheitert jeder Commit; darum zuerst“, Testautor und Implementierer gleichzeitig,
ein Commit nach beiden, davor keiner; dein Satz zu Name, Docstring und Architektur wörtlich.
Aufteilung berichtigt: 29 in Akzeptanztests (Testautor), 48 im Code und einer in
`technik/tests/einheit` (Implementierer, nach der Tabelle unter Kritik). Das
[Item](../../domaene/items/aufraeumenUndFesteAdresse.md) nennt die Kommentare zuerst und als
Grund den scheiternden Commit. Offen für dich: Was noch nirgends steht und in
[web.md](../../technik/architektur/web.md) gehört, legst du laut Befund 2 erst im Vertrag
fest, der nun nach dem Aufräumen kommt; nenne es also vorher, sonst landet es zuerst im
Docstring.

**Klärung.** Nachgeprüft: Plan, Item und Zahlen stimmen. In web.md und seine Nachbarn
gehören neun Erklärungen, je Stelle genannt in [2540](2540-webKommentareImCodeInDieArchitektur.md)
und [2541](2541-webKommentareInTestsInDieArchitektur.md); ich trage sie beim Aufräumen ein.
