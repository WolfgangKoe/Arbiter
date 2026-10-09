# Akzeptanztests von Plan 4: Wiederholung, Zahlen statt Namen, Dienst in den Handgriffen

332 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** Geprüft: 4603003, 21493e2, d9ddabd, aad7540 nach
[Es](../../prozess/praemissen/es.md) und [Wir 3](../../prozess/praemissen/wir.md).
1. Zwei Aufgaben in einem Modul (Es, S): `handgriffe.py` baut Spielstände und fragt seit
   d9ddabd den Dienst (`dienstFür` bis `ausgewählteModelleIm`, acht Funktionen); jeder Test der
   Domäne lädt damit Flask. Zum Bildschirm gibt es `bildschirm.py`, zum Dienst nichts Gleiches.
2. Dieselbe Aussage mehrfach (Wir 3): `ausgewähltGekennzeichnet` und `anzahlGesetzterModelle`
   in `auf5Test.py` und `que3Test.py`; `reload()` mit `wait_for_selector(".karte .spielfeld")`
   dreimal, obwohl `Bildschirm.seiteBei` das Warten nach B2 kennt; der Locator „Spieler an der
   Reihe“ in `auf5Test.py:247` und `auf6Test.py:29`. `klickenUndWarten` steht nur in
   `auf5Test.py`, `que3Test.py` schreibt Klick, Tippen und `expect` je Test aus (95–100, 118–123).
3. Zahlen statt Namen (Es, Lesbarkeit): `auswählen(dienst, 1, 2)` sagt nicht „Warboss“. Die
   Tabelle `nummernDerEinheiten` steht in `auf5Test.py`, aber 18 Aufrufe dort und in
   `que3Test.py` nutzen die Zahlen.
4. Begriff (Wir 2): `handlung = abwählen if vorherAusgewählt else auswählen`
   (`auf5Test.py:499`). Auswählen ist nach Glossar und [V3](../../technik/architektur/vertrag.md)
   keine Handlung; der Test, der die Fachsprache festlegt, widerspricht ihr.
5. `auf5Test.py:492–493` leitet `spielerEins` und `boyz` aus dem Stand ab; Fixtures gleichen
   Namens gibt es.
6. Die Bildschirmtests zu AUF-5.10 (306–332) ändern die `Aufstellung`, während der Server-Thread
   sie hält. [B1](../../technik/architektur/web.md#bildschirmtests): erst Zustand bauen, dann
   `serverStarten`; [W2](../../technik/architektur/web.md#aufbau): `Aufstellung` ist nicht
   threadsicher. Heute ohne Folge, weil gerade keine Anfrage läuft.

**Kosten.** Je Wiederholung eine zweite Stelle, die beim nächsten Umbau der Seite vergessen wird
(Klasse `ausgewählt`, Spielfeld als Zeichen für „fertig“). Zahlen zwingen den Leser zu W4 und
der Reihenfolge der Ausgangslage. Punkt 6 wird rot oder flackert, sobald die Seite selbst
nachlädt. Zusammen etwa 1.800 Zeichen in `auf5Test.py`, die Anliegen 331 braucht.

**Gegenvorschlag.** Positives Vorbild ist `check_rules` in
`ArbiterMap/backend/app/domain/rule_checks.py`: Der Aufruf liest sich, das Wie steht einmal
woanders.
1. `tests/akzeptanz/dienst.py` (Docstring: „Dienst der Akzeptanztests: Anfragen nach dem
   Vertrag und das Lesen des Spielstands“) mit den acht Funktionen; `handgriffe.py` behält das
   Bauen.
2. In `bildschirm.py`: `ausgewähltGekennzeichnet`, `klickenUndWarten`, ein Gegenstück zum
   Tippen, `neuLaden(seite)` und `spielerAnDerReihe(seite)`; `anzahlGesetzterModelle` in
   `handgriffe.py`.
3. `auswählen(dienst, "Warboss")`, die Tabelle der Kennungen in `dienst.py`. Der Test liest
   sich dann wie das Kriterium:
   ```
   auswählen(dienst, "Boyz")
   antwort = abwählen(dienst, "Boyz")
   ```
4. `anfrage` statt `handlung`.
5. Die Fixtures `spielerEins` und `boyz` nehmen.
6. Vor `seiteZu`: `aufstellungNachDerZonenwahl.auswählen(boyz)` (V3), dann
   `einheitAufstellen`; der Klick ist nicht Gegenstand von AUF-5.10.

Erledigt, wenn die sechs Punkte umgesetzt oder einzeln begründet abgelehnt sind.

**Stellungnahme.** Angenommen, alle sechs Punkte umgesetzt: `dienst.py` mit den acht
Funktionen; in `bildschirm.py` die fünf Helfer (`tippenUndWarten` als Gegenstück zum Tippen);
`anzahlGesetzterModelle` in `handgriffe.py`; `auswählen(dienst, "Warboss")` mit der Tabelle
`kennungenDerEinheiten`; `anfrage`; die Fixtures `spielerEins`, `boyz`, neu `warboss`; die Tests
zu AUF-5.10 bauen den Zustand vor `seiteZu`, ohne Klick und Neuladen.
