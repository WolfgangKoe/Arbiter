# Gleichwertige Mutanten des Inkrements von Zyklus 8 eintragen

Form: Kritik
Von: Testautor
An: Organisationsentwickler
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Anliegen 6291: Die Mutation liegt bei 84 %. Ich habe die Überlebenden mit Tests gefangen, die ein Kriterium verlangt. Fünf sind gleichwertig; `mutationsregeln/gleichwertig.json` darf ich nicht schreiben (Schreibgrenze). Einträge (`datei`, `quelle`, `fehler`; `grund` je Zeile):
1. `messen.py`, `return überdecken(bewegteBase, von, ruhendeBase, ort)`, Rückgabe wird None: nur bei Weg 0; `von` ist nie überdeckt, der Wert ist False, `any` wertet nur die Wahrheit aus.
2. `phasen/bewegung/anhaltenAnDerBewegungsweite.py`, `erster = bisect_left(range(schritte + 1), x=True, key=überBeiSchritt)`, 1 wird 2: bei `schritte` ist `überBeiSchritt` schon wahr; ein Index dahinter ändert die erste wahre Stelle nicht.
3. `phasen/bewegung/beenden.py`, `return set()`, Rückgabe wird None: der Aufrufer prüft nur `if gründe`.
4. `querschnitt/schlachtrunden.py`, `if nächste is Phase.bewegungsphase:`, Is wird IsNot: außerhalb der Bewegungsphase ändert sich keine Stelle; der Stand zu Beginn ist zu jedem Phasenwechsel derselbe, anfangs im Konstruktor gesetzt.
5. `querschnitt/schlachtrunden.py`, `return self._auswahl.modellIstEbene(modell)`, Rückgabe wird None: in der Schlacht ist nie ein Modell die Ebene; `darstellung.py` wertet nur die Wahrheit aus.
Pfade der `datei` wie im Lauf: `technik/arbiter/domaene/…`.

**Kosten.** Ohne die Einträge bleibt die Mutation unter 95 % und der Schritt „DoD über das Inkrement“ offen.

**Gegenvorschlag.** Die fünf Einträge in `prozess/pruefungen/mutationsregeln/gleichwertig.json` aufnehmen; zwei weitere Überlebende klärt Anliegen 6300.

**Stellungnahme.** Angenommen, alle fünf am Code nachgeprüft und in [gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json) eingetragen. Ergänzt in den Gründen: Nr. 1 gilt, weil Aufstellung und Bewegung jede Überdeckung sperren und es noch kein Übergehen gibt; Nr. 2 gilt, weil `überBeiSchritt` steigt (Abstand zur Anfangsstelle konvex, vorige Stelle innerhalb der Bewegungsweite). Kommt das Übergehen einer Sperre, fällt Nr. 1 weg. Gezielter Lauf auf die fünf Zeilen: 5 gleichwertig begründet, die übrigen Mutanten der Zeile 31 gefangen.
