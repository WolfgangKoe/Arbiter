# Auswahl: Modell anklicken einfacher, Meldung zur aufgestellten Einheit

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Kritik am Code (Lesbarkeit), `git diff 90801c5 819896b`. Wartet nach
[Kritik](../../prozess/ablauf/kritik.md): Namen und Ablage von Hilfsfunktionen, keine Prüfung
rot.
1. [auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py):
   `modellAnklicken` fragt `modellIstEbene` und ruft dann `ebeneAbwählen`, das dieselbe Frage
   noch einmal stellt. Seit die Route der *Ebene* fehlt (8030), rufen `ebeneWählen` und
   `ebeneAbwählen` nur noch `modellAnklicken` und
   [auswahlTest.py](../../technik/tests/einheit/domaene/phasen/aufstellen/auswahlTest.py).
2. [aufstellen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py):
   `auswählen` wirft „Eine aufgestellte Einheit ist nicht auswählbar“, `modellAnklicken`
   derselben Klasse wählt sie nach AUF-30.1 aus. Wer die Meldung liest, glaubt das Gegenteil
   dessen, was die *Aufstellung* tut.

**Kosten.** Am Bildschirm nichts. Bleibt 1, liest man zwei öffentliche Methoden, die nur noch
ein Weg braucht; bleibt 2, sucht ein Leser die Regel an der falschen Stelle.

**Gegenvorschlag.**
1. `modellAnklicken` prüft die Zugehörigkeit einmal und setzt
   `self._modellAlsEbene = None if self.modellIstEbene(modell) else modell`; `ebeneWählen` und
   `ebeneAbwählen` entfallen, ihre Unit-Tests prüfen `modellAnklicken`.
2. Die Meldung nennt den Weg, den sie sperrt (die *Einheitenkarte*). Ist offen, ob die
   *Einheitenkarte* einer *aufgestellten* *Einheit* sie auswählen soll, fragst du den
   Anforderungsautor, statt es im Code zu entscheiden.

**Stellungnahme.** Beide Punkte angenommen und umgesetzt. 1: `modellAnklicken` setzt die
*Ebene* einmal (`None if modellIstEbene else modell`), `ebeneWählen` und `ebeneAbwählen`
entfallen, die Unit-Tests prüfen `modellAnklicken` (siehe 8100). 2: Die Meldung heißt jetzt
„Eine aufgestellte Einheit wählt man nicht über die Einheitenkarte“. Ob die *Einheitenkarte*
einer *aufgestellten* *Einheit* sie auswählen soll, entscheide ich nicht; das Verhalten bleibt
wie bisher gesperrt, und AUF-30 regelt nur den Klick auf ein *Modell*. Ich stelle dazu keine
Frage, solange der Stakeholder den Bildschirm nicht anders verlangt.
