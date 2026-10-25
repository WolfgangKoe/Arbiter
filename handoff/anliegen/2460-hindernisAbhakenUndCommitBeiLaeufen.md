# Hindernis, Abhaken und Commit-Hook passen nicht zu gleichzeitigen Läufen

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Im Auftrag des Stakeholders, am Code bestätigt. Nach [Ich 3](../../prozess/praemissen/ich.md):
wartet auf die Prozessphase; kein Schritt des Happy Path fehlt, keine Prüfung ist rot.
1. Hindernis: `standregeln/hindernis.py`, `nächsteNummer` (Zeile 60 bis 62), nimmt die höchste
   belegte Nummer plus eins statt `freieNummer` aus dem Bereich des Auftrags, wie Retro 6, P4 und
   [Regeln](../../prozess/regeln/anliegenregeln.md) es für alle Skripte verlangen. Der Befehl legt
   immer ein neues Anliegen an; der Kritiker schreibt seinen Befund nach
   [Kritik](../../prozess/ablauf/kritik.md) aber schon als Anliegen, mit dem Befehl entstünde ein
   zweites ([Fortschritt](../../prozess/ablauf/fortschritt.md) widerspricht). Deshalb meldete der
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
kann verloren gehen, gegen [Gleichzeitige Läufe](../../prozess/ablauf/gleichzeitigeLaeufe.md).

**Gegenvorschlag.** In Retro 7 ein Prozess-Item; der Regelumsetzer baut, den Text im Ablauf
schreibe ich.
1. `hindernis.py` nimmt die Nummer aus dem Bereich des Auftrags und kann ein bestehendes
   Anliegen nennen statt ein neues anzulegen; Kritik und Fortschritt sagen dasselbe.
2. Eine neue Fassung des Plans öffnet die Zeilen der Kritik; der Start nennt beide Befehle immer,
   der Ablauf den Aufruf über `lauf.py`; ein schon gesetzter Haken wird als solcher gemeldet.
3. Kein Zurücksetzen fremder Arbeit beim Commit: erst die Bordmittel von pre-commit und Claude
   Code prüfen, sonst committet der Koordinator nur, wenn keine Rolle läuft.

**Stellungnahme.** Umgesetzt in Retro 7, P5, Regeln in [Standregeln](../../prozess/regeln/standregeln.md).
1. `standregeln/hindernis.py` nimmt als letztes Argument den Nummernbereich des Auftrags oder die Nummer eines vorhandenen Anliegens (dann entsteht keines); die Frage, ob das Hindernis bei Kritik unter der Zeile steht, liegt beim Stakeholder (Anliegen 3940, Empfehlung Ja).
2. Ein neu gefasster Plan öffnet „Kritik am Plan“ (`standregeln/planFassung.py`, Merkzettel in `.git/arbiter`; der erste Lauf merkt nur, die bereits abgehakte Kritik an Plan 7 bleibt); der Start nennt beide Befehle immer; `abhaken.py` meldet einen schon gesetzten Haken als solchen. Den Aufruf über `lauf.py` im Ablauf schreibt der Organisationsentwickler.
3. Nicht gebaut: pre-commit bietet kein Mittel, das Beiseitelegen fremder Änderungen abzuschalten; ein eigener Hook statt `.git/hooks/pre-commit` ist ungeprüft und Hook-Code für alle Rollen. Es bleibt dein Rückfall: Der Koordinator committet nur, wenn keine Rolle läuft ([Commits](../../prozess/ablauf/commits.md)), Text für dich.

**Nachprüfung.** Erfüllt (Commit „P5: Läufe und Anliegenkopf“). 1 und 2 am Code bestätigt,
die Tests der Standregeln-Zeilen grün (104); mein Start nannte beide Befehle ohne offenen
Schritt. Im Ablauf stehen jetzt der Aufruf über `lauf.py`, Bereich oder Nummer beim
Hindernis und die neue Fassung des Plans ([Fortschritt](../../prozess/ablauf/fortschritt.md));
3 als Rückfall, nur Text, in [Commits](../../prozess/ablauf/commits.md).
