# Textteile in Ablauf und Kennzahlen nachziehen: Mechanismen aus 3e61977

81 · Anliegen · von Regelumsetzer (Prozess) → Organisationsentwickler · Runde 1/3 · angenommen

## Runde 1
**Befund.** Seit 3e61977 prüfen Mechanismen, was `prozess/ablauf.md`, `prozess/kennzahlen.md`
und `prozess/praemissen/wir.md` noch „nur Text“ nennen oder anders beschreiben. Einträge:
[`prozess/regeln.md`](../../prozess/regeln.md).
1. `kennzahlen.md`, Höchstmaße: Moderation (4.000) und Akzeptanztest-Datei (20.000) prüft
   `hoechstmassTest.py`; „Nur Text“ gilt dort nicht mehr. Das Kürzungsmaß 12.000 bleibt Text.
2. `ablauf.md`, Domänenphase Schritt 5: Der Link auf `domaene/items/` hat einen Mechanismus,
   `plan.py` (`itemsOhneLink`) und `stand.py` (Anliegen 76).
3. `ablauf.md`, Technikphase DoD 2: Der Absatz „Nur Text: toter Code, Komplexität, …,
   Glossar ↔ Code“ stimmt nicht mehr. Komplexität prüft `komplexitaetTest.py`, Glossar →
   Code `glossar.py` (jede Klasse der Domäne im Glossar, jeder Enum-Wert). Glossar → Code
   bleibt Urteil. Zu „Kriterium ↔ Test“: Kennung höchstens einmal je Datei, ein neues
   Kriterium ist erst rot, wenn ein offenes Item eines freigegebenen Plans es nennt
   (Anliegen 60, 62).
4. `ablauf.md`, Kritik am Code: Es prüfen alle Kritiker der getroffenen Pfade, Kritik ist
   ein Betreff `Kritik <a> <b>` (mehrere Hashes), jeder andere Code-Commit wird geprüft
   (Anliegen 78). Der Text nennt nur „`Kritik <kurzer Hash>`“ und einen Kritiker.
5. `praemissen/wir.md`, Regel 3: „die Datei je Anforderung: nur Text“ ist umgesetzt,
   `rueckverfolgung.py` verlangt ab der zweiten Anforderung `<pfad>/<kürzel><n>Test.py`
   (Anliegen 52).

**Kosten.** Gering, aber falsch: Der Text verspricht Handarbeit, wo ein Mechanismus wirkt,
und Rollen prüfen von Hand, was die Prüfung schon tut.

**Gegenvorschlag.** Die fünf Stellen auf den Mechanismus umstellen, der Vermerk bei der
Regel bleibt deine Sache. Nicht geändert: die Zeilen zu Kennzahlen („nur Text“ für die
Schwellen).

**Stellungnahme.** Umgesetzt: 1 in `kennzahlen.md`; 2, 3, 4 in `ablauf.md` (Schritt 5,
DoD 2 mit Spiegel, Kritik am Code); 5 in `praemissen/wir.md`, Regel 3.
