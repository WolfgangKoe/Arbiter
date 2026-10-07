# Abhängigkeitstests als Tabelle, Kommentar und Regelzeile zu 09a195e

247 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von 09a195e. Die Prüfungen sind grün (`konfigurationTest.py`, 26
bestanden), `import flask, playwright` läuft (3.1.3, 1.60.0). Drei Punkte:
1. `formregeln/konfigurationTest.py`: `testFlaskIst…` und `testPlaywrightIst…` sind Kopien
   von `testPyYamlIst…`, sie unterscheiden sich nur in Paketname und Gruppe. Nach
   [wir.md](../../prozess/praemissen/wir.md) Regel 9 gehören Fälle, die sich nur in Daten
   unterscheiden, in eine Tabelle. Dazu ist die Gegenprobe („nicht in der anderen Gruppe“)
   eine Teilzeichenkette mit Groß- und Kleinschreibung: `flask==3.1.*` in `entwicklung`
   bleibt grün, obwohl pip Paketnamen ohne Rücksicht auf die Schreibung vergleicht (PEP 503).
   Das Paket stünde dann doppelt.
2. `pyproject.toml`, Kommentar zu `entwicklung`: „1.60 gehört zum Chromium-Build 1223 unter
   ~/.cache/ms-playwright; sonst lädt `playwright install chromium` den passenden.“ Der erste
   Teil beschreibt den Cache dieses Rechners, nicht das Projekt. Auf einem frischen Rechner
   oder nach einem Update des Cache stimmt er nicht mehr, und keine Prüfung merkt es. Der
   zweite Teil ist eine Anleitung zur Einrichtung, kein `Warum`.
3. `prozess/regeln.md`: Flask und Playwright stehen in der Zeile „Importvertrag A1 und A2“.
   Mit dem Importvertrag haben sie nichts zu tun, die Regel kommt aus CLAUDE.md
   (Technik-Rahmen) und aus den Anliegen 146 und 234 (git). Die Spalte
   Mechanismus nennt nur `[project] dependencies`, Playwright steht aber in
   `[dependency-groups] entwicklung`.

**Kosten.** (1) Jede weitere Abhängigkeit, ob eslint, mypy oder eine andere, bringt sechs
kopierte Zeilen, und die Kopien gehen schon jetzt auseinander (PyYAML prüft inline, Flask über
eine Variable). Ein doppelter Eintrag in falscher Schreibung bleibt grün. (2) Der Kommentar
veraltet still und führt den nächsten Leser auf einen Cache, den es bei ihm nicht gibt. (3) Wer
die Regel für Abhängigkeiten sucht, findet sie unter dem Importvertrag nicht, und die Zeile
nennt den Mechanismus für Playwright falsch.

**Gegenvorschlag.**
1. Ein einziger parametrisierter Test, z. B.
   `testAbhängigkeitStehtInIhrerGruppeMitFesterMinorVersion(paket, gruppe)` mit den Zeilen
   `("PyYAML", laufzeit)`, `("Flask", laufzeit)`, `("playwright", entwicklung)`. Die Gegenprobe
   vergleicht den normalisierten Namen vor `==` (klein geschrieben), keine Teilzeichenkette.
2. Kommentar kürzen auf: Playwright mit fester Minor-Version, weil jede Version einen eigenen
   Chromium-Build braucht. Wie man den Browser einrichtet (`playwright install chromium`),
   gehört dorthin, wo die Technik die Einrichtung beschreibt, oder fällt weg, wenn es keinen
   solchen Ort gibt.
3. Eine eigene Zeile in `regeln.md`: „Abhängigkeiten mit fester Minor-Version, je in ihrer
   Gruppe (Laufzeit: PyYAML, Flask; Entwicklung: Werkzeuge, Playwright)“, Mechanismus
   `pyproject.toml` (`[project] dependencies`, `[dependency-groups] entwicklung`), Scheiter-Test
   der parametrisierte Test aus 1. PyYAML bleibt zusätzlich bei A2, falls es dort wegen des
   Katalogs stehen soll.

Erledigt, wenn die drei Punkte umgesetzt oder begründet abgelehnt sind und die Prüfungen
grün sind. Das Inkrement wird dadurch nicht blockiert.

**Stellungnahme.**

Stellungnahme: Entfällt mit dem Rückbau.
