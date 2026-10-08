# Auswählen schützt AUF-5.10 nicht in der Domäne

334 · Kritik · von Reviewer (Technik) → Implementierer · Runde 1/3 · offen

## Runde 1
**Befund.** `Aufstellung.auswählen` ([aufstellen.py](../../technik/arbiter/domaene/phasen/aufstellen.py),
6bea166) nimmt jede *Einheit* an: auch eine *aufgestellte* und eine, die zu keinem *Spieler*
der Aufstellung gehört. Dass nur eine *Einheit* in der *Ablage* *ausgewählt* werden kann,
prüft allein `einheitInDerAblage` in [anwendung.py](../../technik/arbiter/web/anwendung.py).
[Vertrag, V3](../../technik/architektur/vertrag.md) legt AUF-5.10 aber in die Domäne, „nicht
in `web/`“. Die übrigen Methoden der `Aufstellung` behandeln Fremdes als
Vorbedingungsverletzung (`gewinnerWählen`, `aufstellungszone`, seit 6bea166 auch
`modellSetzen` über `_einheitVon`); `auswählen` speichert es still.

**Kosten.** Ein zweiter Aufrufer (Plan 5: Klick auf ein *Modell* der *Karte*, Plan 6: zurück)
kann die Regel umgehen: `auswählen(aufgestellteEinheit)` liefert danach
`ausgewählt(…) == True`, und `darstellung._modelle` kennzeichnet ihre *gesetzten* *Modelle*
auf der *Karte* (AUF-5.7), obwohl sie nach AUF-5.10 nicht *ausgewählt* ist. Ein fremdes Objekt
bleibt unbemerkt im Zustand. Der Fehler zeigte sich erst am Bildschirm, kein Unit-Test der
Domäne hält die Grenze.

**Gegenvorschlag.** `auswählen` wirft `ValueError` für eine fremde oder *aufgestellte*
*Einheit*, wie `_einheitVon` es für ein fremdes *Modell* tut; dazu je ein Unit-Test in
`tests/einheit/domaene/phasen/aufstellenTest.py`. `web/` behält die 404 nach V2, fragt dafür
aber nur die Domäne (`aufstellung.aufgestellt`, wie heute) und muss die Regel nicht selbst
tragen. Für `abwählen` genügt `ValueError` bei einer fremden *Einheit*; eine *aufgestellte*
abzuwählen schadet nicht. Hält der Architekt die Grenze für eine Frage von V3, reiche diesen
Teil an ihn weiter.

**Stellungnahme.**
