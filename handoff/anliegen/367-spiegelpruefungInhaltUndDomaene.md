# Spiegelprüfung: Inhalt der Akzeptanztests und Module der Domäne

367 · Kritik · von Architekt (Technik) → Regelumsetzer (Prozess) · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder will einen Test, der den Spiegel zwischen Anforderungen und
Technik prüft (Anliegen 340, 362 über Anliegen 365).
Die Regeln stehen jetzt in der [Architektur](../../technik/architektur.md):
[T1](../../technik/architektur.md#tests) für die Akzeptanztests (Struktur und Inhalt) und der
[Grundschnitt](../../technik/architektur.md#grundschnitt-der-domäne) für `arbiter/domaene/`.
`spiegelVerstoß` in `formregeln/benennung.py` prüft heute nur den Ort der Testdatei; den
Inhalt und die Module der Domäne prüft niemand. Bestehende Regeln, die das aufnehmen:
`formregeln/benennung.py` (Spiegel) und `kriterienregeln/rueckverfolgung.py` (Kennung im
Testnamen).

**Kosten.** Ohne Prüfung laufen Kriterium und Test still auseinander: Heute steht in
`querschnitt/karteTest.py` QUE-2.7 vor QUE-2.5, weil die Kennung beim Umbenennen wechselte.
Die Prüfung ist eine Funktion je Regel mit Scheiter-Test, ohne Eingriff in den Produktcode.

**Gegenvorschlag.** In `formregeln/benennung.py` oder einem eigenen Modul daneben, je mit
Scheiter-Test auf einer Probe in `tmp_path`:
1. T1 (1): Der Docstring der Testdatei ist die Überschrift ihrer Anforderung ohne `### ` mit
   Punkt. Rot: `"""AUF-7 · Einheit."""` zu `### AUF-7 · Einheit in Aufstellung`.
2. T1 (2): Jede Testfunktion trägt Kürzel und Nummer der Anforderung ihrer Datei. Rot:
   `testAuf3_2…` in `einheitInAufstellungTest.py`.
3. T1 (3): Die Kennungen der Testfunktionen stehen in der Folge der Kriterien der Anforderung;
   gleiche Kennungen beisammen. Rot: `5_3, 5_4, 5_3`; `2_7, 2_5` bei Kriterien 2.5 vor 2.7.
4. Grundschnitt: Jedes Modul unter `technik/arbiter/domaene/` außer `messen.py` und
   `sperre.py` hat einen Spiegel: `<pfad>.py` oder `<pfad>/__init__.py` den Ordner
   `domaene/anforderungen/<pfad>/`, `<pfad>/<name>.py` die Datei `<pfad>/<name>.md`. Rot:
   `phasen/aufstellen/zug.py` ohne `zug.md`; grün: `spielobjekte.py`, `phasen/aufstellen.py`.
   Die Gegenrichtung gilt nicht: Anzeige und Bedienung haben kein Modul.
5. Aufräumen: Der Zweig `geteilt`/`gebündelt` in `spiegelVerstoß` (`<kürzel><n>Test.py` im
   Ordner einer Sammeldatei) hat keine Regel mehr; er fällt mit dem Absturz aus
   [363](363-spiegelpruefungStuerztBeiTestImAkzeptanzordnerAb.md). In
   [Regeln](../../prozess/regeln.md) nennt die Zeile zum Frontend „[Web] O1“; O1 steht jetzt in
   [Oberfläche](../../technik/architektur/oberflaeche.md).

Reihenfolge: 1, 2 und 4 sind am Repo heute grün. 3 ist rot in `auswahlTest.py`,
`karteTest.py`, `sperrenBeimSetzenTest.py` und `bedienungTest.py`, bis der Testautor sie nach
[368](368-akzeptanztestsInDerFolgeDerKriterien.md) ordnet; bis dahin baust du 3 nur mit
Scheiter-Test und schaltest die Prüfung am Repo danach zu. Erledigt, wenn 1 bis 4 mit
Scheiter-Test am Repo grün sind, 5 erledigt ist und `python3 -m pytest prozess/pruefungen`
grün bleibt; ich setze dann in T1 und im Grundschnitt „Prüft“ auf die Prüfung.

**Stellungnahme.**
