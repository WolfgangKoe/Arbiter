# Finding: Silent-King Zielaufteilung Fernkampf (Select Targets)

## Frage

Darf ein einzelnes Modell mit ZWEI Fernkampfwaffen (konkret: Silent King / Szarekh mit
„Sceptre of Eternal Glory" und „Staff of Stars") seine Waffen auf VERSCHIEDENE
Feind-Einheiten aufteilen?

Die App zeigt aktuell nur EINE Feind-Einheit als Ziel — ist das regelkonform?

---

## Regel-Befund (mit Zitaten + Quellenangabe)

### 1. Waffen-Split erlaubt (Kernregel)

**Quelle:** `docs/work/wahapedia_core_rules/core_rules.txt`, Zeile 1402 — Abschnitt „Select Targets":

> „If a model has more than one ranged weapon, **it can shoot all of them at the same
> target, or it can split the weapons between different enemy units**. Similarly, if a
> unit has more than one model, they can shoot at the same or different targets.
> In either case, when you select a target unit you must declare which weapons will
> target that unit **before any attacks are resolved**."

→ Das Regelwerk erlaubt das Aufteilen von Waffen eines einzelnen Modells auf
verschiedene Feind-Einheiten **explizit**.

### 2. Alle Attacken EINER Waffe → dieselbe Ziel-Einheit (Pflicht)

**Quelle:** `docs/work/wahapedia_core_rules/core_rules.txt`, Zeile 1440:

> „**All of a ranged weapon's attacks must be made against the same target unit.**"

→ Innerhalb einer Waffe ist kein weiteres Aufteilen möglich; die Aufteilung geschieht
nur auf Waffen-Ebene, nicht auf Attacken-Ebene.

### 3. Illustrierendes Beispiel aus den Regeln

**Quelle:** `docs/work/wahapedia_core_rules/core_rules.txt`, Zeile 1416:

> „James splits their attacks as follows: **the lascannon targets an enemy vehicle unit,
> while the meltagun and all the boltguns target an enemy infantry unit.**"

Das Beispiel beschreibt eine Einheit mit mehreren Modellen, zeigt aber das Prinzip:
verschiedene Waffen → verschiedene Ziele. Für ein Einzelmodell gilt dieselbe Regel
(Zeile 1402 ist ausdrücklich „if a model has more than one ranged weapon").

### 4. Glossar-Bestätigung „Single target (model)"

**Quelle:** `docs/work/wahapedia_core_rules/rules_appendix.txt`, Zeile 808–809:

> „**Single target (model):** When a model attacks with one or more ranged weapons,
> if **all** of the attacks made with those ranged weapons have **the same target unit**,
> that model is said to be shooting at a single target."

→ Die Formulierung „if all" impliziert, dass es auch den Fall gibt, wo die Waffen
auf verschiedene Ziele gehen — sonst wäre die Einschränkung überflüssig.

### 5. Reihenfolge-Pflicht bei mehreren Zielen

**Quelle:** `docs/work/wahapedia_core_rules/core_rules.txt`, Zeile 1404:

> „If you have selected more than one target for your unit to shoot at, you must
> **resolve all the attacks against one target before moving on to the next target.**"

---

## Antwort (ja/nein, klar)

**JA — ein Einzelmodell mit zwei Fernkampfwaffen DARF seine Waffen auf verschiedene
Feind-Einheiten aufteilen.**

Die Regelpassage ist eindeutig: „If a model has more than one ranged weapon, it can
split the weapons between different enemy units." (core_rules.txt:1402)

Der Silent King mit Sceptre of Eternal Glory und Staff of Stars darf also je eine
Waffe auf je eine andere Feind-Einheit richten.

**Die aktuelle App-Einschränkung auf eine einzige Feind-Einheit ist regelwidrig.**

---

## UI-Implikation

Die aktuelle UI erlaubt nur EIN Ziel pro schießender Einheit/Modell. Das muss für
Modelle mit mehreren Fernkampfwaffen erweitert werden:

| Aktuell (falsch) | Soll (regelkonform) |
|---|---|
| Eine Feind-Einheit als Ziel für alle Waffen | Pro Waffe eine eigene Ziel-Einheit wählbar |
| Alle Attacken auf dieselbe Einheit | Waffe A → Einheit X, Waffe B → Einheit Y |

**Konkrete UI-Änderung:** „Ziel pro Waffe" statt „Ziel pro Modell/Einheit". Jede
Waffe eines Modells braucht eine eigene Ziel-Selektion. Deklaration aller Ziele muss
vor dem ersten Würfelwurf abgeschlossen sein.

---

## Sonderfälle / Einschränkungen

| Einschränkung | Regelstelle | Relevanz für Silent King |
|---|---|---|
| **Sichtbarkeit pro Waffe:** Mindestens ein Modell der Ziel-Einheit muss sichtbar und in Reichweite der jeweiligen Waffe sein | core_rules.txt:1403 | Beide Waffen haben 24" Reichweite (Assault 3 / Assault 9) — Sichtbarkeit muss pro Waffe geprüft werden |
| **Alle Attacken einer Waffe → gleiche Einheit** | core_rules.txt:1440 | Gilt absolut; kein Aufteilen innerhalb einer Waffe |
| **Deklaration vor Würfelwurf** | core_rules.txt:1402 | Alle Ziele müssen vor Auflösung der ersten Attacke feststehen |
| **Reihenfolge: ein Ziel vollständig abhandeln** | core_rules.txt:1404 | Erst alle Attacken auf Ziel A, dann alle auf Ziel B |
| **Blast-Waffen** | core_rules.txt:1624 | Weder Sceptre noch Staff ist eine Blast-Waffe → nicht relevant, aber als allgemeine Einschränkung merken |
| **Engagement Range** | core_rules.txt:1418 | Einheit nicht in Engagement Range (außer VEHICLE/MONSTER-Ausnahme) |
| **Preservative Auto-torpor (Silent King Sonderregel)** | wahapedia_necrons/units_all.txt:238 | Bei ≤ 8 Wunden verbleibend: Staff of Stars nicht mehr schießbar → UI muss Wundstand des Silent King abfragen und Staff ggf. sperren |

---

## Offene Punkte für Opus-Review

1. **App-Architektur:** Wo wird das Ziel aktuell gesetzt — pro Einheit, pro Modell oder
   pro Waffe? Welche State-Felder müssen von `target_unit: str` zu
   `target_unit_per_weapon: dict[str, str]` oder ähnlichem erweitert werden?

2. **Preservative Auto-torpor:** Die Sonderregel sperrt Staff of Stars bei ≤ 8
   Wunden. Ist dieser Wundstand im App-State verfügbar, und wird die Waffe schon
   deaktiviert?

3. **Allgemeinheit:** Wie viele andere Modelle/Einheiten im aktuellen Datenbestand
   haben mehr als eine Fernkampfwaffe? Wie groß ist der Refactoring-Scope?

4. **Blast + Split:** Gibt es im Datenbestand Modelle mit mehreren Waffen, von denen
   mindestens eine Blast ist? Dann greift die Engagement-Range-Einschränkung nur für
   die Blast-Waffe, nicht für alle — UI müsste das per Waffe prüfen.

5. **Reihenfolge in der UI:** Die Regel verlangt vollständige Auflösung einer Ziel-
   Einheit vor der nächsten. Ist das in der aktuellen Shooting-Phase-UI erzwungen oder
   frei wählbar?
