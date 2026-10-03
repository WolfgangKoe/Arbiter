# Sprung zwischen Kriterium und Test: nicht eingeplant

46 · Fragen · von Architekt (Technik) → Stakeholder · Runde 1/3 · offen

## Runde 1
Deine Frage: Springt jedes Kriterium in `aufstellen.md` zu seinen Tests in
`aufstellenTest.py`, und kommt man aus dem Test zurück?

**Befund.** Eingeplant ist es nicht. Was gilt:
- Die Zuordnung steht im Namen, nicht als Link: `- AUF-1.4` ↔ `testAuf1_4…`
  ([`wir.md`](../../prozess/praemissen/wir.md) Nr. 3 und 4).
  [`rueckverfolgung.py`](../../prozess/pruefungen/rueckverfolgung.py) prüft beide Richtungen
  (jedes Kriterium hat einen Test, jeder Test ein Kriterium), zeigt aber keine Stelle.
- Heute findet man den Gegenpart nur per Suche in VS Code (Strg+Umschalt+F, regulärer
  Ausdruck `AUF-1\.4|Auf1_4`), weil Kennung und Testname verschieden geschrieben sind.
- Links in den Dateien selbst verbieten zwei Regeln: Anforderungen enthalten keine Technik
  ([`domaene/CLAUDE.md`](../../domaene/CLAUDE.md)), Kommentare im Code nur als `# Regel:`
  oder `# Warum:` (`wir.md` Nr. 8).

**Kosten.** Ohne Sprung prüft der Fachkritiker jedes Kriterium per Suche; bei mehreren
Anforderungsdateien wächst der Aufwand mit.

**F1 · Welcher Weg?**
- A: Suche wie heute. Kostet nichts, kein Klick.
- B: Spur-Befehl. `python3 prozess/pruefungen/rueckverfolgung.py AUF-1.4` gibt das
  Kriterium und alle seine Tests als `pfad:zeile` aus, ebenso mit einem Testnamen als
  Eingabe. Im Terminal von VS Code ist `pfad:zeile` per Strg+Klick ein Sprung. Rund 30 Zeilen
  im vorhandenen Skript, das beide Dateien schon liest; die Zuordnung steht weiter nur an
  einer Stelle, nichts veraltet.
- C: Klick im Editor. Eine kleine VS-Code-Erweiterung macht `AUF-1.4` in der Anforderung und
  `testAuf1_4…` im Test zu Links; sie fragt die Stelle bei B ab. Technisches Neuland:
  Installation aus dem Repo und Pflege sind unerprobt, also erst ein Wegwerf-Versuch.
- D: Gespeicherte Links, z. B. `[Test](…/aufstellenTest.py#L161)` hinter jedem Kriterium,
  von einem Hook nachgeführt. Abgeraten: Technik in der Anforderung, jede Teständerung
  verschiebt Zeilennummern und ändert Domänendateien, die Rückrichtung braucht einen
  verbotenen Kommentar.

Empfehlung B, danach C nur, wenn dir das Terminal im Alltag nicht reicht. B ist billig und
Voraussetzung für C. Vorbild im Altbestand: `ArbiterMap/backend/app/domain/rule_checks.py`
rechnet Kohärenz bei jedem Aufruf aus den Positionen (`check_rules`), statt ein Ergebnis zu
speichern, das veralten kann; ebenso rechnet B den Sprung aus
den Namen, statt Links zu speichern. Mit F1 = A aus
[Anliegen 44](44-akzeptanztestDateiZuLang.md) gehört `### AUF-1` zu genau einer Datei.

Antwort: B auf jeden Fall. Versuche C ebenfalls umzusetzen. Mit einem ersten Test für C wäre ich zufrieden, um es auszuprobieren, wenn es neu ist. Ansonsten ist der Aufwand hoffentlich überschaubar, wenn der Versuch von C schief geht.

**F2 · Nutzt du VS Code?** Im Repo liegt `.vscode/`, installiert ist 1.140. Für B genügt
jedes Terminal mit Pfad-Links, C setzt VS Code voraus.

Antwort: Ja.

**Nach deiner Antwort.** B baut der Regelumsetzer mit Scheiter-Test; ich lege ihm das
Anliegen an und trage die Regel in `technik/architektur.md` (Tests) ein.

**Stellungnahme.**
