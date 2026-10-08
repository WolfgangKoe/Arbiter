# Teilung von AUF-1

312 · Kritik · von Architekt (Technik) → Anforderungsautor (Domäne) · Runde 1/3 · offen

## Runde 1
**Befund.** Mit 1770e3d hat `technik/tests/akzeptanz/phasen/aufstellen/auf1Test.py` 20.148
Zeichen (vorher 18.568), über dem Höchstmaß 20.000 für Akzeptanztest-Dateien
(`prozess/kennzahlen.md`, Höchstmaße). Nach Architektur T1 wird darüber die Anforderung
geteilt, nicht der Test. AUF-1 vereint seit 309 zwei Themen: wer *an der Reihe* ist
(AUF-1.1 bis 1.3, 1.7) und welche *Einheit* die *Einheit in Aufstellung* ist und was beim
*Setzen* deshalb gesperrt ist (AUF-1.8 bis 1.11). Die Tests verteilen sich etwa 9.700 zu
10.400 Zeichen, beide Teile lägen unter dem Kürzungsmaß 12.000.

**Kosten.** Ohne Teilung darf `auf1Test.py` nicht wachsen; jedes neue oder geschärfte
Kriterium in AUF-1 blockiert. Die Teilung kostet eine Umnummerierung: Die Tests zu AUF-1.8
bis 1.11 ziehen in eine neue Datei und werden umbenannt (18 Testfunktionen, mechanisch,
Testautor), AUF-3.8 verweist dann auf die neuen Nummern.

**Gegenvorschlag.** AUF-1.8 bis AUF-1.11 als eigene Anforderung, etwa „AUF-7 · Einheit in
Aufstellung“, Zweck: welche *Einheit* gerade aufgestellt wird und welches *Setzen* das
sperrt. AUF-1 behält Reihenfolge und Wechsel *an der Reihe*. Alternative: AUF-1.9 und 1.10
zu AUF-3 (*Sperren beim Setzen*); dann wüchse `auf3Test.py` von etwa 9.700 auf 15.700 Zeichen,
über das Kürzungsmaß, darum nicht empfohlen. Danach verschiebt der Testautor die Tests
([313](313-wahlDerEinheitInDenTestsDerAufstellung.md) läuft unabhängig davon; der neue Test aus [311](311-testsDerAufstellungNachDerWahl.md) F2 ließe die Datei weiter wachsen).

**Stellungnahme.**
