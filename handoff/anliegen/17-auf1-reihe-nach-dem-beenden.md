# AUF-1: Wer ist nach dem Beenden an der Reihe, was ist wählbar

17 · Kritik · von Architekt (Technik) → Anforderungsautor · Runde 1/3 · offen

## Runde 1
**Befund.** In [AUF-1](../../domaene/anforderungen/phasen/aufstellen.md):
1. *Widerspruch:* Nach AUF-1.5 ist nach jedem Beenden der andere *Spieler* an der Reihe, nach
   1.6 derselbe, nach 1.7 keiner; was vorgeht, steht nirgends. Offen ist auch, ob danach noch
   eine *Einheit in Aufstellung* besteht; davon hängt ab, ob 1.4 die beendete Einheit sperrt.
2. *Akteur:* Beide teilen ein Gerät, Arbiter sieht nicht, wer tippt. „Der Gewinner wählt“
   (1.1), „Der Spieler an der Reihe wählt“ (1.3), „Setzt ein Spieler“ (1.4) sind so nicht
   prüfbar; prüfbar ist nur der Zustand.
3. *Ungeregelt:* Wahl einer gegnerischen oder aufgestellten *Einheit*; Wechsel der *Einheit
   in Aufstellung* nach einem Fehltipp.

**Kosten.** Bei 1 und 3 erfindet der Testautor Vorrang und Verhalten; beide prägen den
Spielstand. Bei 2 bekäme jede Handlung einen Parameter „welcher Spieler“, den nichts prüfen
kann: Die Schnittstelle wird größer und täuscht eine Prüfung vor.

**Gegenvorschlag.**
1. AUF-1.5 bis 1.7 als ein Kriterium: „Gelingt *Aufstellen der Einheit beenden*, ist die
   *Einheit* aufgestellt und keine *Einheit in Aufstellung*. An der Reihe ist der andere
   *Spieler*; hat er keine nicht aufgestellte *Einheit*, derselbe; hat keiner mehr eine, ist
   die *Aufstellung* beendet.“ Drei Fälle, ein parametrisierter Test.
2. Zustand statt Akteur, etwa 1.3: „Wählbar als *Einheit in Aufstellung* ist nur eine nicht
   aufgestellte *Einheit* des *Spielers* an der Reihe; jede andere Wahl ist eine *Sperre*.“
3. Wechsel, solange kein *Modell* gesetzt ist, sonst über die Ablage ([16](16-aufstellen-ablage-beenden-uebergehen.md)
   F2). `core_rules.txt:2322` schweigt dazu; fehlt die Grundlage, frag den Stakeholder.

**Stellungnahme.**
