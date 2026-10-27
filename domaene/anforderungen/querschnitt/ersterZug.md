### QUE-9 · Erster Zug

Etappe: 2
Zweck: Nach der *Aufstellung* wählen die *Spieler* am Bildschirm, wer den *ersten Zug* hat; den *Roll-off* würfeln sie am Tisch (`core_rules.txt:2329`, Anliegen 2361 F3 A, Vorbild `Arbiter-old/src/uiLayout/gameActionsArea.py:274`).
Am Bildschirm: „Erster Zug“ in einer *Armeeliste* klicken.

- QUE-9.1 **Gegeben** die *Aufstellung* ist beendet (AUF-1.7) und kein *Spieler* hat den *ersten Zug*, **dann** zeigt jede *Armeeliste* „Erster Zug“; sonst zeigt es keine.
- QUE-9.2 **Wenn** ein *Spieler* in einer *Armeeliste* „Erster Zug“ klickt, **dann** hat ihr *Spieler* den *ersten Zug*, die *Schlachtrunde* 1 beginnt, und er ist *am Zug* in der *Kommandophase* (`core_rules.txt:639`, `:2329`, `:2333`).
