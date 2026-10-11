# Ungültige Zahlen und fehlende Formationen enden in 500

396 · Kritik · von Reviewer (Technik) → Implementierer (Technik) · Runde 1/3 · angenommen

## Runde 1
**Befund.** Kritik am Code zu d5f6050, Korrektheit.
1. `_zahl` in [anwendung.py](../../technik/arbiter/web/anwendung.py) lässt `NaN`, `Infinity`
   und `-Infinity` durch: Flask liest JSON mit `json.loads`, das diese Literale annimmt, und
   `float` besteht die Typprüfung. `Fraction(str(wert))` wirft dann `ValueError`, die Antwort
   ist 500. [V5](../../technik/architektur/handlungen.md) verlangt für einen Körper ohne Zahl
   `x` und `y` die 400. Beispiel: `PUT /api/spieler/1/einheiten/1/stelle` mit
   `{"x": NaN, "y": 20}`.
2. Die Formationen prüft niemand beim Laden. `ausgangslageAus` in
   [katalog/ausgangslage.py](../../technik/arbiter/katalog/ausgangslage.py) prüft Durchmesser
   und Zonen, aber nicht, ob jede *Einheit* eine *Formation* hat und ob die Reihen zusammen so
   viele *Modelle* zählen wie die *Einheit*. Fehlt der Eintrag oder stimmt die Summe nicht,
   wirft erst `einheitLoslassen` beim Ziehen aus der *Ablage* `KeyError`
   (`formationen[einheit.name]`) oder `ValueError` (`zip(modelle, stellen, strict=True)`
   in `einheitLoslassen`), die Antwort ist 500. Der Standardwert `formation=None` und
   `formationen = MappingProxyType({})` in
   [Ausgangslage](../../technik/arbiter/domaene/missionsvorbereitung/ausgangslage.py) machen
   genau diesen Zustand zum Normalfall jeder Ausgangslage ohne drittes Argument.

**Kosten.** Beides zeigt sich erst am Bildschirm: ein Fehler des Servers statt einer
Ablehnung (1) oder statt eines Fehlers beim Start (2). Ändern kostet je wenige Zeilen und
einen Unit-Test.

**Gegenvorschlag.** Bestehende Regel: V5 (400) und die Prüfungen, die `ausgangslageAus`
schon für Zonen macht; eine neue braucht es nicht.
1. In `_zahl` zusätzlich `math.isfinite(wert)` verlangen, sonst 400. Unit-Test in
   [anwendungTest.py](../../technik/tests/einheit/web/anwendungTest.py) mit
   `data='{"x": NaN, "y": 2}'` und `content_type="application/json"`.
2. In `ausgangslageAus` je *Einheit* beider *Armeen* `ValueError`, wenn ihr Name in
   `formation.yaml` fehlt oder `sum(reihen)` nicht der Zahl ihrer *Modelle* gleicht;
   `formation` ohne Standardwert, `formationen` in `Ausgangslage` ohne Standardwert. Unit-Test
   in [ausgangslageTest.py](../../technik/tests/einheit/katalog/ausgangslageTest.py) für beide
   Fälle.
Erledigt, wenn beide Tests grün sind und `python3 -m pytest technik/tests` grün bleibt.

**Stellungnahme.** Angenommen und umgesetzt wie vorgeschlagen: `_zahl` verlangt `isfinite`
(Unit-Test mit `NaN`, `Infinity`, `-Infinity`); `ausgangslageAus` prüft Formation und
Modellzahl je Einheit (zwei Unit-Tests), `formation` und `formationen` ohne Standardwert.
