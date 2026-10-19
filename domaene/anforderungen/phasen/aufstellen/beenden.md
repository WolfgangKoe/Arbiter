### AUF-10 · Aufstellen der Einheit beenden

Zweck: Die *Spieler* schließen die *Einheit in Aufstellung* ab; Arbiter sperrt, solange sie nicht in *Kohärenz* ist (Etappe 1, Anliegen 945 F1 A).
Am Bildschirm: „Aufstellen der Einheit beenden“ klicken.

- AUF-10.1 **Wenn** ein *Spieler* „Aufstellen der Einheit beenden“ klickt, **dann** wählt er *Aufstellen der Einheit beenden*.
- AUF-10.2 **Gegeben** die *Einheit in Aufstellung* hat ein nicht *gesetztes* *Modell*, **wenn** jemand *Aufstellen der Einheit beenden* wählt, **dann** *Sperre* ‚Modelle fehlen‘ (Etappe 1).
- AUF-10.3 **Gegeben** die *Einheit in Aufstellung* ist nicht in *Kohärenz* ([QUE-4](../../querschnitt/kohaerenz.md)), **wenn** jemand *Aufstellen der Einheit beenden* wählt, **dann** *Sperre* ‚keine Kohärenz‘ (`core_rules.txt:434`).
- AUF-10.4 **Wenn** AUF-10.2 und AUF-10.3 zugleich sperren, **dann** nennt Arbiter den *Grund* beider.
