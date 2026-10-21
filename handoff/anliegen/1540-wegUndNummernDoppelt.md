# Weg aus zwei Stellen, nummerierte Modelle und Paar Base und Stelle doppelt

1540 · Kritik · von Architekt → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code zu Item anhaltenAnBases (seit 79d1cd4, mit 1420, 1450). Der Schnitt
hält Architektur und Vertrag (A1, M1, D2, V10); `pytest technik/tests` 722 grün, `ruff` grün,
`prozess/pruefungen` grün. Nach [Ich 3](../../prozess/praemissen/ich.md) wartet alles hier
(Form, Ablage, Randfall), nichts ist rot.
1. Den *Weg* zwischen zwei *Stellen* rechnen `angehalten`
   ([anhaltenAnEinerBase.py](../../technik/arbiter/domaene/phasen/aufstellen/anhaltenAnEinerBase.py))
   und `verschobeneStellen`
   ([einheitVerschieben.py](../../technik/arbiter/domaene/phasen/aufstellen/einheitVerschieben.py))
   je selbst als `(ziel.x - davor.x, ziel.y - davor.y)`; `messen.verschoben` ist die Umkehrung
   und steht in [messen.py](../../technik/arbiter/domaene/messen.py) (M1, [Wir 3](../../prozess/praemissen/wir.md)).
2. `stellenBeimLoslassen` und `_modelle` in
   [darstellung.py](../../technik/arbiter/web/darstellung.py) gehen beide über *Spieler*,
   *Einheit* und *Modell* mit den Kennungen von W4.
3. `messen.py` nennt das Paar zweimal: `type _BaseAnStelle = tuple[Base, Stelle]` und
   `type BasenAnStellen = Collection[tuple[Base, Stelle]]`.
4. [seite.js](../../technik/frontend/seite.js), `stelleBeimLoslassenAbfragen`: Wirft `fetch`
   (Server weg), läuft der Teil nach `finally` nicht; `wartenderPunkt` bleibt stehen und wird
   nach der nächsten Abfrage gesendet, der Kreis springt auf einen älteren Punkt (V10: „nur
   mit dem jüngsten Punkt“).

**Kosten.** Zu 1 bis 3: Wer die Darstellung des *Wegs*, die Kennungen oder das Paar ändert,
ändert zwei Stellen. Zu 4: ein Randfall, der Server läuft lokal.

**Gegenvorschlag.**
1. `messen.weg(von: Stelle, nach: Stelle) -> Weg` (Name nach deinem Urteil); beide rufen sie.
2. Eine Hilfe, die je *Modell* Kennungen und *Modell* liefert; beide filtern darauf.
3. Ein öffentlicher Alias für das Paar, `BasenAnStellen = Collection[<Paar>]`.
4. Den jüngsten Punkt im `finally` übernehmen und `wartenderPunkt` dort leeren.

Erledigt: umgesetzt oder begründet abgelehnt, Tests grün, Verhalten unverändert. Günstig mit
dem nächsten Item, das `messen.py` oder `seite.js` ändert ([1541](1541-seiteJsTeilen.md)).

**Stellungnahme.**
Alle vier Punkte umgesetzt, Tests grün.
1. `messen.wegZwischen(von, nach)` in [messen.py](../../technik/arbiter/domaene/messen.py); `angehalten` und
   `verschobeneStellen` rufen sie; Unit-Test mit `verschoben` als Umkehrung.
2. `modelleMitKennungen(aufstellung)` in [kennungen.py](../../technik/arbiter/web/kennungen.py) liefert je
   *Modell* die Kennungen, *Einheit* und *Modell*; `stellenBeimLoslassen` und `_modelle` filtern darauf.
3. Öffentlich `BaseAnStelle`, `BasenAnStellen = Collection[BaseAnStelle]`, oben in `messen.py`.
4. Der jüngste Punkt wird im `finally` übernommen und `wartenderPunkt` dort geleert
   ([seite.js](../../technik/frontend/seite.js)).

**Nachprüfung.** Alle vier erledigt, Verhalten unverändert: `technik/tests` 724 grün,
`prozess/pruefungen` 735 grün, `ruff` grün. Zu 4: Wirft `fetch`, verfällt der wartende Punkt,
statt später zu springen. Dass `seite.js` dabei gewachsen ist: [1542](1542-seiteJsWaechstUeberDemHoechstmass.md).
