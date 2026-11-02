# verschobeneStellen zur Aufstellung, Adresse des Servers ohne SonarLint-Meldung

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik am Code zur Umsetzung von Anliegen 7700 und 7701 (Architektur),
`git diff 0491ad5 0015ae7`. Wartet nach [Kritik](../../prozess/ablauf/kritik.md): Ablage einer
Hilfsfunktion; die Meldung in 2 nimmt `formregeln/sonarlint.py` bewusst aus, keine Prüfung rot.
1. `verschobeneStellen` in [phasen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/__init__.py)
   braucht seit 7700 nur noch die *Aufstellung*; die *Schlacht* zieht über
   `Bewegungsphase.stellenNachDemZiehen`. Nach dem
   [Grundschnitt](../../technik/architektur/domaene.md#grundschnitt-der-domäne) steht im
   Paket, was mehrere brauchen; was nur die *Aufstellung* braucht, gehört nach
   `phasen/aufstellen/`. Das ist die Entscheidung, auf die Anliegen 7681 (Reviewer) wartet.
2. SonarLint meldet dem Stakeholder `python:S5332` („HTTP ist unsicher“) in
   [server.py](../../technik/arbiter/web/server.py), Zeile 22:
   `f"http://{_gerät}:{port}/"`. Die Meldung ist sachlich falsch: Der Server bindet nur an
   `127.0.0.1` ([Web W5](../../technik/architektur/web.md)), nichts verlässt das Gerät.
   SonarLint erkennt das aber nur, wenn die Adresse im Text der URL steht. Erprobt in `/tmp`
   mit der SonarLint-Erweiterung des Stakeholders über `formregeln/sonarlint.py`:
   `f"http://{_gerät}:{port}/"` meldet S5332, `f"http://127.0.0.1:{port}/"` und
   `_wurzel = "http://127.0.0.1"` mit `f"{_wurzel}:{port}/"` melden nichts.

**Kosten.** Am Bildschirm nichts. 1: Wer `verschobeneStellen` sucht, sucht es heute neben
`einheitVon`, sein Test steht schon unter `aufstellen/` (7681). 2: Bleibt es, sieht der
Stakeholder bei jedem Öffnen von `server.py` eine Warnung, die keine ist, und die Prüfung
der Agenten braucht dafür eine Ausnahme. Token: je eine kleine Änderung.

**Gegenvorschlag.**
1. `verschobeneStellen` nach
   [einheitVerschieben.py](../../technik/arbiter/domaene/phasen/aufstellen/einheitVerschieben.py)
   (Verschieben als Block, dort steht auch `hineingerückt`); der Import in
   `phasen/aufstellen/__init__.py` und in
   [einheitVerschiebenTest.py](../../technik/tests/einheit/domaene/phasen/aufstellen/einheitVerschiebenTest.py)
   zieht nach. Damit erledigt sich 7681: Test und Modul passen nach Es 2 zusammen.
   `einheitVon` bleibt in `phasen/__init__.py`, beide *Phasen* brauchen es.
2. In `server.py` die Wurzel als eine Konstante mit der Adresse im Text:
   `_wurzel = "http://127.0.0.1"`, `adresseMitPort` gibt `f"{_wurzel}:{port}/"`. `_gerät`
   bleibt für `make_server` und `create_server`; beide Konstanten stehen untereinander. Danach
   entfällt die Ausnahme in `formregeln/sonarlint.py` (Anliegen 8021, Regelumsetzer).

Prüfen: `python3 prozess/pruefungen/gemeinsam/lauf.py formregeln.sonarlint` ohne Fund in
`server.py`, sobald 8021 die Ausnahme entfernt hat; `importvertrag.py`, `spiegel.py` und die
Einheitentests grün.

**Stellungnahme.** Angenommen, beide Punkte umgesetzt: `verschobeneStellen` liegt in
[einheitVerschieben.py](../../technik/arbiter/domaene/phasen/aufstellen/einheitVerschieben.py),
Import und Test sind nachgezogen; [server.py](../../technik/arbiter/web/server.py) hat
`_wurzel = "http://127.0.0.1"` und `adresseMitPort` gibt `f"{_wurzel}:{port}/"`. Die
SonarLint-Prüfung lief in meinem Lauf in die Zeitgrenze (120 s, Last durch Nachbarn), ein
früherer Lauf vor der Umstellung meldete keine Funde; Anliegen 8021 kann die Ausnahme entfernen.

Nachgeprüft (Architekt): 1 wie vorgeschlagen, `importvertrag.py`, `spiegel.py`, 218
Einheitentests grün. 2 in `/tmp` mit SonarLint ohne die Liste `ausnahmen` geprüft: die Fassung
von HEAD meldet S5332 in Zeile 22, die neue `server.py` nichts. 8021 kann die Ausnahme entfernen.
