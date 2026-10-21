# Auswahl sieht fremden Zustand, Ebene und Spielerpaar ohne Namen

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: 1655

## Runde 1
**Befund.** Ich habe [auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py) und
die Module daneben gegen [kritik-entwickler.md](../kritik-entwickler.md), Abschnitt 1 („Domänenmodell
teilweise zu implizit“, „sprechende Namen“), und [Es](../../prozess/praemissen/es.md) gelesen;
Anlass ist die Einschätzung des Stakeholders (Anliegen 1652). Namen,
Verzweigung und Größe sind gut. Was implizit bleibt:
1. `Auswahl` bekommt die Menge `_aufgestellt` der `Aufstellung` als `Collection[Einheit]`
   ([`__init__.py`](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py):41–42,
   auswahl.py:9–11). Sie liest dieselbe Menge, die `aufstellenDerEinheitBeenden` füllt. Wer
   auswahl.py liest, sieht nicht, dass sie sich ändert; `Collection` sagt das Gegenteil.
   `Auswahl` hält dafür auch beide *Spieler*, nur für eine Prüfung.
2. Die *Ebene* entscheidet über AUF-21.1 und AUF-20.4 in einem Vergleich:
   `if self.ebene(einheit) is not einheit` (`__init__.py`:126) deckt „Ebene ist ein *Modell*“
   und „nicht *ausgewählt*“ (`None`) zugleich ab, ebenso `ebene(einheit) is modell`
   ([darstellung.py](../../technik/arbiter/web/darstellung.py):78). Die Frage des Fachs („bewegt
   das Ziehen die ganze *Einheit*?“) hat keinen Namen.
3. `spieler` heißt das Paar beider *Spieler* (auswahl.py:9, `__init__.py`:35,
   [reihenfolge.py](../../technik/arbiter/domaene/phasen/aufstellen/reihenfolge.py) in jeder
   Funktion) und in denselben Modulen ein einzelner (`aufstellungszone(spieler)`). Ob einer
   oder beide gemeint sind, sagt nur der Typ.
4. `_aufgerundeteWurzel` ([setzenPerKlick.py](../../technik/arbiter/domaene/phasen/aufstellen/setzenPerKlick.py)):
   `-(-quadrat.numerator // quadrat.denominator)` ist Aufrunden als Kunstgriff.
5. `Aufstellung` reicht sieben Aufrufe an `Auswahl` durch, an zwei Stellen (Zeilen 76–83 und
   199–209); öffentliche Handlungen und private Helfer wechseln sich ab.

Nach [Ich 3](../../prozess/praemissen/ich.md) wartet alles: Keine Prüfung ist rot, keine Regel aus
Es ist verletzt. 1, 3 bis 5 sind älter als dieses Item, 2 ist neu, aber Form und Name.

**Kosten.** 1 ist teuer: Wer `_aufgestellt` ersetzt (etwa durch ein Tupel nach D3), bricht die
Auswahl, ohne es zu sehen. 2 bis 5: Der Leser muss rechnen statt lesen; Punkt 2 wächst mit
jeder Anforderung zur *Ebene*.

**Gegenvorschlag.**
1. Die `Aufstellung` prüft vor `auswählen` selbst, ob die *Einheit* aufgestellt ist und zur
   Partie gehört; ihr gehört der Zustand. `Auswahl` kennt dann nur *Einheit* und *Ebene*.
2. Benannte Fragen in `Auswahl`, etwa `ganzeEinheitIstEbene(einheit) -> bool` (AUF-21.1) und
   `modellIstEbene(modell) -> bool` (AUF-25.4); die Aufrufer fragen sie statt `is`.
3. `beideSpieler` für das Paar, `spieler` nur für einen.
4. `isqrt(ceil(quadrat))` mit `math.ceil`, das `Fraction` genau aufrundet.
5. Reihenfolge: Abfragen, Handlungen, Auswahl, dann private Helfer. Ob die Aufrufe durch
   `aufstellung.auswahl` entfallen, nach deinem Urteil (Vertrag V3).

Erledigt: 1 bis 5 umgesetzt oder begründet abgelehnt, Tests grün.

**Stellungnahme.**
