# Prüfskripte: `pfade.py` nicht vollständig, `lage` dreimal je Test

142 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Gegenstand: ed4d7e4 (Kritik am Code). `python3 -m pytest prozess/pruefungen` grün, `ruff`
sauber. `hookProtokoll.py`, `phasenfolge.py` und die Umstellung der Hooks verhalten sich wie
vorher. Keine Aufrufer der verschobenen Funktionen gebrochen, keine `ablehnen`/`sperren`
mehr. Der neue Test in `konfigurationTest.py` greift, weil `ruffAufrufen` die
`pyproject.toml` mit `--config` übergibt.

**Befund.**
1. `pfade.py` sagt von sich „Ordner des Repos, die mehrere Prüfungen kennen“, nennt aber nur
   drei. Mehrfach als Literal stehen weiter:
   - `domaene/etappen`: `benennung.py:37`, `phasenfolge.py:32`, `hoechstmassTest.py:32`
   - `domaene/items`: `benennung.py:37`, `plan.py:23`, `plan.py:37`
2. `standTest.py:163`, `testFreigabeDerRetroBeginntDenNächstenZyklus`: Der Test ruft
   `lage(repo.wurzel)` dreimal, je mit allen git-Aufrufen der Phasenfolge.
   `testSolangeEinItemOffenIstNenntDerStandDieAbnahmeAuchMitReview` (Zeile 119) zeigt die
   Form schon: einmal `aktuelle = lage(repo.wurzel)`.

**Kosten.** Zu 1: Wer `pfade.py` liest, hält es für vollständig. Ein Umzug von
`domaene/items` ändert dann `pfade.py` und übersieht zwei Literale. Das ist derselbe Fall wie
114, Punkt 5, nur an zwei weiteren Ordnern. Zu 2: Der Test dauert länger als nötig, und er
liest sich schlechter als der Test daneben.

**Gegenvorschlag.**
1. `etappenOrdner = "domaene/etappen"` und `itemsOrdner = "domaene/items"` in `pfade.py`
   aufnehmen und an den sechs Fundstellen nutzen; `nummerierteOrdner` in `benennung.py` baut
   sich daraus.
2. `aktuelle = lage(repo.wurzel)`, dann
   `assert (aktuelle.zyklus, aktuelle.phase) == (2, "Domänenphase")` und
   `assert aktuelle.schritt.startswith("Planer: Plan 2")`.

Erledigt, wenn kein Literal aus 1 außerhalb von `pfade.py` steht (Tests dürfen Dateien
anlegen, wie `standTest.py` es tut), 2 umgesetzt ist und `python3 -m pytest prozess/pruefungen`
grün ist.
