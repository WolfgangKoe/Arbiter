# Retro 8: F1 widerspricht T1, P2 steht schon, P7 zählt ungeregelt

Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf: Der Stakeholder entscheidet F1 vor der Freigabe ohne die Folgen, P2 und
P7 lassen sich nicht ohne Erfinden umsetzen ([Ich 1](../../prozess/praemissen/ich.md)).
1. F1 A „nur der des Moduls, ohne Kennungen“ widerspricht
   [T1](../../technik/architektur/tests.md) (1): Der Docstring der Testdatei ist die
   Überschrift ihrer Anforderung mit Kürzel (`"""AUF-7 · Einheit in Aufstellung."""`),
   `formregeln/spiegel.py` prüft das, der Skill `akzeptanztest-schreiben` verlangt es. Wörtlich
   umgesetzt sind alle 31 Testdateien rot. F1 B nennt nicht, dass T1 (1),
   [Es S](../../prozess/praemissen/es.md) („sein Docstring nennt sie“) und `spiegel.py`
   mitfallen.
2. F1 lässt offen, was Befund 4 zählt: 35 Zeilen `# Warum:` in `pyproject.toml`, die
   Kommentare der Daten-YAML. Die YAML-Kommentare sind die Fundstellen, die die
   [Domäne](../../domaene/CLAUDE.md) verlangt („Katalogwerte mit Fundstelle“,
   `onlyWar.yaml`: `# core_rules.txt:2166`); `# Warum:` begründet je Prüfregel, wie sie die
   Technik einschränkt, das prüfe ich ([Kritik](../../prozess/ablauf/kritik.md), letzte
   Zeile). 6430 fragt nach Kommentaren im Code; die Antwort deckt nur Docstrings.
3. P2 steht schon: „Kein Verhalten ohne Test … fehlt etwas, schreibe ein Anliegen“ steht in
   `.claude/agents/implementierer.md` (Grenzen), nicht nur in der Root-CLAUDE.md
   (Befund 2). „Der Architekt prüft es in der Kritik am Code“ ist heute so: 6101 war mein
   Hindernis, behoben im Zyklus (Commit 98455ec). 6241 ist kein Code vor dem Test:
   BEW-1.5 verlangt „es sperren nur QUE-1 und BEW-2“, QUE-1.3 ist ‚Nahkampfreichweite‘; der
   Implementierer nutzt `befundeDesSetzens` wieder, wie es [Es O](../../prozess/praemissen/es.md)
   will. Es fehlt nur der Test, den 6241 verlangt. „Danach sperrt Arbiter nichts, was der
   Plan unter „Noch nicht“ nennt“ widerspricht BEW-1.5 und 6241 und verlangt aus einem
   Prozess-Item einen Zweig je Phase im Produkt; Plan 8 meint mit *Nahkampfreichweite* das
   Anhalten davor (6400).
4. P7 „jede Anforderung nennt jetzt `Etappe:`“: 15 von 39 nennen sie (11 mit Etappe 2), 24
   nicht, darunter QUE-1, das die *Bewegungsphase* braucht. Das Format steht nicht in der
   Domäne. Wie „Etappe 2: x von y“ eine Anforderung ohne `Etappe:` zählt, ist ungeregelt.

**Kosten.** (1, 2) Der Stakeholder wählt A und bekommt rote Prüfungen oder eine zweite
Fragerunde; löscht jemand die YAML-Kommentare, fehlen die Fundstellen. (3) Eine Zeile mehr
ohne Wirkung, ein Danach, das kein Prozess-Item erfüllen kann; die Retro beauftragt keinen
Mechanismus, also bleibt P2 Text, den es schon gibt. (4) Der Regelumsetzer erfindet die
Zählung oder P7 wartet.

**Gegenvorschlag.**
1. F1 A: „Nur der des Moduls; eine Kennung nur im Docstring der Testdatei nach T1“
   (Architektur T1). B nennt: T1 (1), Es S und `spiegel.py` ändern sich mit (neu).
2. F1 nennt dazu: `# Warum:` in `pyproject.toml` und die Fundstellen der YAML bleiben, Es 8
   nennt beide als erlaubt (Domäne, Kritik). Meine Empfehlung: so.
3. P2 streichen, Befund 2 berichtigen: Die Regel steht in Root und Implementierer, die Kritik
   am Code fing 6101; 6241 ist ein fehlender Test für Technikphase 9. Was keine Prüfung
   fängt, steht in [6471](6471-frontendOhneAbdeckung.md) (wartet).
4. P7 nennt die Zählung: „Etappe 2“ zählt die Kriterien der Anforderungen mit `Etappe: 2`,
   eine ohne `Etappe:` nur unter allen (Etappe 1 ist erreicht, [Domäne](../../domaene/CLAUDE.md):
   Erreichtes wird gelöscht). Die Zeile `Etappe: <n>` gehört ins Format der Domäne
   (Anforderungsautor, Domänenphase 9).

**Stellungnahme.** In der [Retro 8](../retro.md): 1 in Befund 4 und P3; 6431 bleibt, dort
antwortet der Stakeholder gerade. 2 in Befund 4, ohne Zeile in Es 8: Es 8 und `kommentare.py`
(nur `.py`, `.js`, `.mjs`) erfassen beide nicht. 3 in Befund 2, P2 gestrichen. 4 in P7 als
Annahme; das Format: [6500](6500-etappeEinesKriteriums.md).
