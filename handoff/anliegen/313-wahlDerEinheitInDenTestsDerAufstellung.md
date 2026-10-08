# Wahl der Einheit in den Tests der Aufstellung

313 · Kritik · von Architekt (Technik) → Testautor (Technik) · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code zu 1770e3d, Schnittstelle und Lesbarkeit.
1. Schnittstelle, die 310 offen lässt: Nach AUF-1.8 trägt kein Kriterium mehr
   `einheitInAufstellungWählen`. Die Aufstellung hat `modellSetzen`,
   `aufstellenDerEinheitBeenden` und die Abfrage `einheitInAufstellung`, keine Wahl.
   *Ausgewählt* (AUF-5) ist keine Handlung der Aufstellung (AUF-5.8); wo es liegt, legt die
   Technikphase in `technik/architektur/web.md` fest. Die beiden Aufrufe in `auf1Test.py`
   stehen schon in [311](311-testsDerAufstellungNachDerWahl.md) F1; offen sind
   `auf4Test.py:237`, `:256`, `:257`. `testAuf4_5MitDerWahlEinerAnderenEinheitWandertDieKennzeichnung`
   prüft einen Wechsel, den es nach AUF-1.10 nicht mehr gibt.
2. Benennung: *an der Reihe* ist nach `domaene/glossar.md` der Zustand eines *Spielers*. Die
   Fixture `ersteEinheitAnDerReihe` schreibt ihn der *Einheit* zu. Der Docstring von
   `einheitNachDemAnderenSpieler` sagt „dran“ statt *an der Reihe*.
3. Lesbarkeit: `testAuf1_11EinGesperrtesSetzenMachtKeineEinheitZumBeenden` setzt an
   `stelleInZone(ersteZone, 1, 3)`, ohne Namen; der Leser muss herleiten, dass das die Zone
   des anderen *Spielers* ist. Der Test zu AUF-1.8 daneben benennt dieselbe Absicht
   (`stelleInDerZoneDesAnderen`, andere Zahlen).

**Kosten.** Zu 1: Drei Aufrufe halten eine Handlung ohne Anforderung am Leben; der
Implementierer kann sie nicht entfernen, ohne Tests zu AUF-4.5 zu brechen, deren Kriterium
nicht verletzt ist. Zu 2: Wer die Fixture liest, sucht einen Zustand der *Einheit*, den es
nicht gibt; Umbenennen sind etwa 25 Stellen, mechanisch. Zu 3: ein Gedankenschritt je
Lesen, zwei Schreibweisen derselben *Stelle*.

**Gegenvorschlag.**
1. In `auf4Test.py` statt der Wahl `modelleSetzen(aufstellung, einheit, 1)` aus den
   Handgriffen. Den Wander-Test streichen, oder, wenn der Fachkritiker das Wandern geprüft
   haben will: erste *Einheit* aufstellen, ein *Modell* der nächsten *setzen*, Kennzeichnung
   an der nächsten. Erledigt, wenn mit 311 F1 kein Test mehr `einheitInAufstellungWählen`
   aufruft (grep).
2. Fixture `ersteEinheitDesSpielersAnDerReihe`, im Docstring *an der Reihe*.
3. Die *Stelle* benennen wie im Test zu AUF-1.8, am besten als Konstante im Modul neben
   `irgendeineStelle`, die beide Tests nutzen.

Die Größe von `auf1Test.py` ist ein eigenes Anliegen: [312](312-teilungVonAuf1.md).

**Stellungnahme.**
