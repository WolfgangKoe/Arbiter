# Zustand der Aufstellung in die Aufstellung, Spielobjekte unveränderlich

55 · Kritik · von Architekt (Technik) → Implementierer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Regel D3 in [`technik/architektur.md`](../../technik/architektur.md), aus
[Anliegen 49](49-zustandDerAufstellungInSpielobjekten.md): Zustand ändern nur Handlungen.
Heute in [`spielobjekte.py`](../../technik/arbiter/domaene/spielobjekte.py):
`Modell.gesetzt`, `Einheit.aufgestellt`, `Einheit.begonnen`,
`Armee.hatEinheitenZumAufstellen`, alle nur von der Aufstellung gebraucht und frei
schreibbar; in [`aufstellen.py`](../../technik/arbiter/domaene/phasen/aufstellen.py) sind
`gewinner`, `anDerReihe`, `einheitInAufstellung`, `beendet` öffentliche Felder.

**Kosten.** `modell.gesetzt = True` von außen umgeht jede *Sperre* und später das
Protokoll; mit `web/` gibt es Code, der das tun könnte. Jede Phase legte ihre Flags in
`spielobjekte.py` ab.

**Gegenvorschlag.**
1. `Modell`, `Einheit`, `Armee`, `Spieler`: `@dataclass(frozen=True, eq=False)`, Sammlungen
   als Tupel. Identität bleibt (D1), ein Objekt ohne `eq` ist über seine Identität hashbar.
2. `Aufstellung` hält `_gesetzt` (Menge der Modelle) und `_aufgestellt` (Menge der
   Einheiten); Abfragen `gesetzt(modell)` und `aufgestellt(einheit)`. `begonnen` und
   „hat Einheiten zum Aufstellen“ werden private Methoden der `Aufstellung`.
3. `gewinner`, `anDerReihe`, `einheitInAufstellung` als Properties ohne Setter über
   `_`-Feldern; `beendet` berechnet, wie in
   [Anliegen 47](47-aufstellungRandfaelle.md), Befund 3.
4. Reihenfolge: erst der Testautor
   ([Anliegen 54](54-zustandUeberDieAufstellungLesen.md)), dann du; am besten im selben Lauf
   wie 47.

**Stellungnahme.** Angenommen, alle Punkte. Spielobjekte sind `frozen` mit Tupeln; die `Aufstellung` hält `_gesetzt` und `_aufgestellt` und bietet `gesetzt(modell)` und `aufgestellt(einheit)`. `gewinner`, `anDerReihe`, `einheitInAufstellung` sind Properties ohne Setter, `beendet` ist berechnet. Alle Tests und Prüfungen grün.
