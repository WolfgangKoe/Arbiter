# Zustand der Aufstellung liegt offen in den Spielobjekten

49 · Kritik · von Reviewer (Technik) → Architekt · Runde 1/3 · offen

## Runde 1
**Befund.** [`spielobjekte.py`](../../technik/arbiter/domaene/spielobjekte.py) trägt
`Einheit.aufgestellt` und `Armee.hatEinheitenZumAufstellen`, beides nur von der Aufstellung
gebraucht. [`architektur.md`](../../technik/architektur.md), Grundschnitt: „Was eine Phase
einführt, liegt dort, bis eine zweite Phase es braucht.“ Zudem sind `Modell.gesetzt`,
`Einheit.aufgestellt` und die Felder von `Aufstellung` (`gewinner`, `anDerReihe`,
`einheitInAufstellung`, `beendet`) frei schreibbar. D2 („die `Sperre` fällt vor der ersten
Änderung“) gilt nur, wenn Änderungen durch die Handlungen gehen; `modell.gesetzt = True` von
außen umgeht jede *Sperre* und jedes spätere Protokoll. Die Akzeptanztests lesen diese Namen,
die Schnittstelle kommt also aus den Tests, nicht vom Implementierer.

**Kosten.** Mit `web/` und `speicher/` wächst die Zahl der Stellen, die Zustand setzen
könnten; ein Übergehen ohne Protokoll fällt dann keinem Test auf. Jede weitere Phase legt
ihre Flags in `spielobjekte.py` ab, das Modul wird zum Sammelbecken.

**Gegenvorschlag.** Eine Regel in `architektur.md`, Regeln im Domänencode: Zustand ändern nur
Handlungen; außen lesbar über Properties (`aufgestellt`, `anDerReihe`), gespeichert in
`_`-Feldern. Dazu entscheiden, ob `aufgestellt` als Menge in `Aufstellung` liegt
(`aufstellung.istAufgestellt(einheit)`) oder bewusst am Spielobjekt bleibt, weil spätere
Phasen es lesen; im zweiten Fall den Grundschnitt um diesen Fall ergänzen. Ändert sich die
Schnittstelle, gehen Anliegen an Testautor und Implementierer. Prüfung später: semgrep-Regel
„keine Zuweisung an Domänenattribute außerhalb `arbiter/domaene/`“.

**Stellungnahme.**
