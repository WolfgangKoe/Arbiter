# Umfang von anhaltenUebergehen nennt BEW-17 und verlangt dadurch dessen Tests

Form: Kritik
Von: Regelumsetzer
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Im [Fortschritt](../plan.md) bleibt „Testautor: Tests zu Item anhaltenUebergehen“
offen, obwohl zu BEW-8.3, BEW-8.4, BEW-8.5, BEW-25 und QUE-5.6 Tests bestehen. Grund: Die
Prüfung (`itemKriterienGetestet`, `nennt` in `kriterienregeln/rueckverfolgung.py`) liest jede
Nennung einer Kennung als Umfang und kennt kein „ohne“. Der
[Umfang](../../domaene/items/anhaltenUebergehen.md) sagt „BEW-8.4 (ohne BEW-17, 10200)“; damit
gilt BEW-17 als Umfang, und es fehlen die Tests zu BEW-17.1 bis 17.4
(`anhaltenVorFremdenBasesTest.py`), die zum Item
[anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md) gehören. Alle anderen Kriterien
des Items sind getestet. Kein Test fehlt, die Prüfung arbeitet wie vorgesehen.

Bestehende Regel ([Ich 4](../../prozess/praemissen/ich.md)): die Regel „Umfang = genannte
Kennungen“ der Rückverfolgung deckt es; ein Ausschluss darin ist nicht vorgesehen, und ihn
einzubauen wäre ein Sonderfall im Prüfskript.

**Kosten.** Planer, eine Zeile in der Itemdatei. Sonst bleibt der Schritt offen, bis
anhaltenAufDemWeg getestet ist.

**Gegenvorschlag.** Umfang ohne die Kennung BEW-17 formulieren, z. B. „BEW-8.4 außerhalb des
Anhaltens vor fremden Bases (10200)“.

**Stellungnahme.** Umgesetzt wie vorgeschlagen: Der [Umfang](../../domaene/items/anhaltenUebergehen.md)
sagt „BEW-8.4 außer vor fremden *Bases* (10200)“, ohne die Kennung BEW-17; ebenso Item 1 im
[Plan](../plan.md).
