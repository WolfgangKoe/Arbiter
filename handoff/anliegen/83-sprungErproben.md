# Sprung zwischen Kriterium und Test: Klick erproben, behalten oder löschen

83 · Fragen · von Architekt (Technik) → Stakeholder · Runde 3/3 · offen

## Runde 1
**Befund.** Aus Anliegen 53: Weg B, der Befehl `python3 prozess/pruefungen/rueckverfolgung.py
AUF-1.3`, gibt Kriterium und Tests als `pfad:zeile` aus, Strg+Klick im Terminal springt. Weg
C, eine VS-Code-Erweiterung in `prozess/pruefungen/sprung/`, macht `AUF-1.3` und
`testAuf1_3…` zu Links.

**Stellungnahme (Stakeholder).** Muss ich VS Code dafür neu starten? Denn aktuell
funktioniert es nicht.

## Runde 2
**Befund.** Kein Neustart; die Erweiterung ist nicht installiert und wirkt nur in einem
zweiten Fenster, das `code --extensionDevelopmentPath=…` öffnen soll.

**Stellungnahme (Stakeholder).** Das zweite Fenster öffnet sich nicht. Beim Versuch die
Datei in dem zweiten Fenster zu öffnen schaltet mich auf das erste VS Code Fenster zurück
ohne in eine Datei zu springen. Es funktioniert damit nicht!

Ich verstehe ehrlich gesagt auch nicht, warum hierfür ein neues Fenster geöffnet werden muss.
Mit "Sprung" meinte ich, dass die jeweiligen Dateien smart miteinander verlinkt sind. Das
machst du doch an anderer Stelle ganz häufig.

## Runde 3
**Befund.** Das Fenster sprang zurück, weil `Arbiter_Structure` bei dir schon offen ist; ein
VS Code öffnet einen Ordner nur einmal. Wichtiger: Ich habe dich falsch verstanden. Du willst
gewöhnliche Links wie in diesen Anliegen, keine Erweiterung. Die habe ich mit
[T2](../../technik/architektur.md) bisher ausgeschlossen („keine Links in Anforderung oder
Test“), weil Links auf Zeilen veralten, sobald sich eine Datei ändert.

Was ein gewöhnlicher Link leisten kann:
- Anforderung → Tests: In Markdown springt Strg+Klick, mit `#L…` sogar auf die Zeile, wie
  heute schon `[core_rules.txt:2322]` in `aufstellen.md`. Stabil ist ein Link je
  *Anforderung* auf ihre Testdatei, denn die Datei folgt aus T1. Beispiel unter `### AUF-1`:
  `Tests: [auf1Test.py](../../../technik/tests/akzeptanz/phasen/aufstellen/auf1Test.py)`.
  Ein Link je *Kriterium* auf die Zeile des Tests veraltet dagegen mit jeder Änderung am Test.
- Test → Anforderung: In Python-Dateien macht VS Code keinen relativen Pfad klickbar, nur
  Webadressen. Zurück bleibt der Befehl (Weg B) oder Strg+P und der Dateiname.

**Kosten.** Option A unten: ein Link je Anforderung, heute drei; der Anforderungsautor setzt
ihn beim Schreiben, `rueckverfolgung.py` prüft, dass er auf die Testdatei nach T1 zeigt (der
Regelumsetzer, klein); ich ändere T2. Der Link zeigt ins Leere, bis der Testautor die Datei
anlegt; das meldet die Prüfung heute schon als „fehlt“, sobald ein Item die Anforderung
nennt. Die Erweiterung fällt in beiden Fällen weg: Sie braucht ein eigenes Fenster oder ein
Installationspaket, das nach jeder Änderung neu gebaut werden müsste.

**Gegenvorschlag.** Erweiterung löschen, Links je Anforderung einführen.

**F1 · Welcher Sprung?**
- A: Link je Anforderung auf ihre Testdatei, geprüft; zurück per Befehl. Anliegen von mir an
  den Anforderungsautor (Links), an den Regelumsetzer (Prüfung, `sprung/` und
  `sprungTest.py` löschen); T2 ändere ich.
- B: nur der Befehl. Anliegen an den Regelumsetzer: `sprung/` und `sprungTest.py` löschen.
Empfehlung: A; das ist der Sprung, den du gemeint hast, soweit ein Link ihn stabil leisten
kann. Willst du den Link je Kriterium auf die Zeile trotzdem, schreib es dazu; dann müsste
ein Prüfskript die Zeilennummern bei jedem Lauf nachziehen.
Antwort: .
