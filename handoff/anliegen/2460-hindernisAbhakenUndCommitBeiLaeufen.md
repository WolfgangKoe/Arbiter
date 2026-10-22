# Hindernis, Abhaken und Commit-Hook passen nicht zu gleichzeitigen Läufen

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Im Auftrag des Stakeholders, am Code bestätigt. Nach [Ich 3](../../prozess/praemissen/ich.md):
wartet auf die Prozessphase; kein Schritt des Happy Path fehlt, keine Prüfung ist rot.
1. Hindernis: `standregeln/hindernis.py`, `nächsteNummer` (Zeile 60 bis 62), nimmt die höchste
   belegte Nummer plus eins statt `freieNummer` aus dem Bereich des Auftrags, wie Retro 6, P4 und
   [Regeln](../../prozess/regeln.md#anliegenregeln) es für alle Skripte verlangen. Der Befehl legt
   immer ein neues Anliegen an; der Kritiker schreibt seinen Befund nach
   [Kritik](../../prozess/ablauf.md#kritik) aber schon als Anliegen, mit dem Befehl entstünde ein
   zweites ([Fortschritt](../../prozess/ablauf.md#fortschritt) widerspricht). Deshalb meldete der
   Fachkritiker 2420 nicht, unter seiner Zeile im [Review](../review.md) fehlt `Hindernis:`.
2. Abhaken: „Fachkritiker: Kritik am Plan“ und „Architekt: Kritik am Plan“ sind seit dem Commit
   „Domänenphase 7 als Zwischenstand…“ abgehakt, für die erste Fassung von Plan 7. „Etappen neu
   geschnitten, Plan 7 mit zwei Items“ schrieb den Plan neu, die Haken blieben: für die alte
   Fassung berechtigt; dass eine neue Fassung sie öffnet, regeln weder Ablauf noch Skript. Ohne
   offenen Schritt nennt der Start (`rollenregeln/rollenkontext.py`) weder den Befehl zum
   Abhaken über `lauf.py` noch den für Hindernisse; der Ablauf nennt nur den Pfad
   `standregeln/abhaken.py`, direkt aufgerufen bricht er mit `ModuleNotFoundError` ab. Über
   `lauf.py` meldet er „Abgehakt“ auch, wenn der Haken schon stand und sich nichts ändert.
3. Commit-Hook: Der Koordinator committet mit Pfaden (`git commit -- <pfade>`), während Rollen im
   selben Arbeitsbaum laufen. pre-commit legt alle übrigen Änderungen beiseite und setzt diese
   Dateien für die etwa 8 Sekunden des Hooks `stand` auf den letzten Commit zurück. Laufende
   Rollen sahen dabei alte Stände (2312, 2370), ihre Hooks schrieben weiter:
   `anliegenregeln/erledigteLoeschen.py` löschte das zurückgelegte, erledigte 2300 erneut. Dann
   meldet pre-commit „files were modified“; bei Konflikt setzt es zurück, was in der Zeit
   geschrieben wurde („Rolling back fixes“, erster Versuch von „Nachprüfung 2370…“). Der Hook
   selbst schreibt nichts (in einer Kopie nachgeprüft); erledigte Anliegen treffen es oft, weil
   ihr Löschen ungestagt liegt.

**Kosten.** (1) Nummern kollidieren mit dem Bereich eines Nachbarn; Hindernisse fehlen im
Fortschritt oder stehen doppelt. (2) Der Fortschritt meldet eine Kritik als getan, die zur
gültigen Fassung aussteht. (3) Commits scheitern beim ersten Versuch, gleichzeitig Geschriebenes
kann verloren gehen, gegen [Gleichzeitige Läufe](../../prozess/ablauf.md#gleichzeitige-läufe).

**Gegenvorschlag.** In Retro 7 ein Prozess-Item; der Regelumsetzer baut, den Text im Ablauf
schreibe ich.
1. `hindernis.py` nimmt die Nummer aus dem Bereich des Auftrags und kann ein bestehendes
   Anliegen nennen statt ein neues anzulegen; Kritik und Fortschritt sagen dasselbe.
2. Eine neue Fassung des Plans öffnet die Zeilen der Kritik; der Start nennt beide Befehle immer,
   der Ablauf den Aufruf über `lauf.py`; ein schon gesetzter Haken wird als solcher gemeldet.
3. Kein Zurücksetzen fremder Arbeit beim Commit: erst die Bordmittel von pre-commit und Claude
   Code prüfen, sonst committet der Koordinator nur, wenn keine Rolle läuft.

**Stellungnahme.**
