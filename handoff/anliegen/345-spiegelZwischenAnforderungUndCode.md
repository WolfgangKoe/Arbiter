# Spiegel zwischen Anforderung und Domänencode

345 · Fragen · von Architekt (Technik) → Anforderungsautor (Domäne) · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder wünscht in Anliegen 339
und [340](340-aufstellenSchwerZuPruefen.md) einen gemeinsamen Spiegel: Ordner und Namen der
Anforderungen kehren in der Technik wieder, wir beide bauen dieselbe Struktur. Dein Schnitt
aus 340 F1 A (`phasen/aufstellen/reihenfolge.md` …, `querschnitt/setzen.md` …) ist dafür die
Vorlage. Drei Stellen passen aus den Regeln noch nicht:
1. AUF-3.4 *Nahkampfreichweite* steht bei der *Aufstellung*. „Models cannot be set up within
   Engagement Range of enemy models“ steht aber im Abschnitt Engagement Range
   (`core_rules.txt:447`, `:450`), nicht in Deploy Forces (`:2322`), und gilt für jedes
   *Setzen*, auch für Reinforcements (`:800`). Wie QUE-1.2 misst sie den *Abstand* zweier
   *Bases*. In der *Aufstellung* greift sie nur, wenn die Spieler ‚nicht ganz in der Zone‘
   übergehen: Die Zonen liegen 26″ auseinander.
2. Die Auswahl (AUF-5) wird im Code eine eigene Klasse (339, F1 B). Das Glossar kennt nur
   *ausgewählt*; `formregeln/glossar.py` verlangt für jede Klasse der Domäne einen Begriff.
3. `anzeige.md`, `vorlaeufigerStart.md`, `karte.md` und `bedienung.md` tragen keine Regel
   der Domäne; ihr Code liegt in `web/` und `frontend/`.

**Kosten.** Bauen wir verschieden, prüft das Spiegelskript, das der Stakeholder vom
Regelumsetzer will, gegen zwei Strukturen. Bleibt 1, liegt eine allgemeine Regel in der
Phase, die sie am seltensten braucht, und Etappe 2 zieht sie um. Ohne 2 bleibt die Auswahl
in der Klasse `Aufstellung`, und AUF-5.5 wächst hinein.

**Gegenvorschlag.** Den Spiegel schreibe ich so in die Architektur:
- `domaene/anforderungen/<pfad>/<name>.md` ↔ `technik/tests/akzeptanz/<pfad>/<name>Test.py`
  (T1) ↔, wenn sie Regeln der Domäne trägt, `technik/arbiter/domaene/<pfad>/<name>.py`.
- Kein Modul der Domäne ohne gleichnamige Anforderung; Ausnahmen sind die Werkzeuge
  `messen.py` (M1) und `sperre.py`.
- Der Ordner `phasen/aufstellen/` wird Paket; `Aufstellung` liegt in seinem `__init__.py`,
  bleibt die eine Tür zum Stand und setzt sich aus den Modulen zusammen. Importe ändern sich
  nicht (Architektur, Grundschnitt).
- *An der Reihe* bleibt in `reihenfolge` (AUF-1), bis der Nahkampf (`:1941`) dasselbe
  Abwechseln braucht.

**F1 · Spiegel.** A wie oben. B jede Anforderungsdatei auch als Modul der Domäne, auch
Anzeige und Bedienung: leere oder künstliche Module. Empfehlung A.

**F2 · Nahkampfreichweite.** A AUF-3.4 wird QUE-1.3 in `querschnitt/setzen.md`, AUF-3.5
nennt QUE-1.2, QUE-1.3 und AUF-3.2. B sie bleibt bei der *Aufstellung*; der Code folgt.
Empfehlung A.

**F3 · Begriff.** A Glossarzeile *Auswahl*: „Die *ausgewählten* *Einheiten* eines
*Spielers*“; der Code-Bezeichner `Auswahl`. B kein Begriff, die Auswahl bleibt in der
Klasse `Aufstellung`. Empfehlung A.

Umsetzung mit 340 in der nächsten Domänenphase. Einigen wir uns, schreibe ich den Spiegel in
die Architektur und gebe die Prüfung an den Regelumsetzer; sonst geht es an den Stakeholder
zurück (339).

**Stellungnahme.**
