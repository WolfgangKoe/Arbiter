STATUS: NEEDS-DECISION — Design-Vorschlag B-128(b), wartet auf Stakeholder-Abnahme

**Lebensdauer:** temporär — löschen nach Stakeholder-Entscheid, Inhalt (Entscheid + finale
Bauform) wandert nach `docs/spec/design_system.md` §1.4.

# B-128(b) — Vereinheitlichung DAMAGE-Block (`_render_damage_block`)

## 1. Ist-Zustand (`src/uiLayout/_common.py:2689-2870`)

Alle drei Pfade teilen sich bereits Kopf und Fuß: `**DAMAGE**`-Header, die farbige
Dmg/HP-Info-Zeile, die Halbbreite-Spalte (`dmg_col`), den Apply-Button
(`⚔ Apply {total} Damage → {target}`) und danach denselben Post-Apply-Zustand
(`success`-Zeile + optionale Wiped-Group-Warnungen + Reroll-GO-Karte + Reset). Die
Divergenz sitzt **ausschließlich im mittleren Eingabe-Absatz** — dort aber mit
unterschiedlichen Labels, unterschiedlicher Feldzahl und unterschiedlichem Wortlaut je
Einheitstyp:

| | (i) Gruppen-Wunden (Z. 2762-2806) | (ii) Einzel-/Multi-Modell (Z. 2807-2843) | (iii) Post-Apply (Z. 2712-2743) |
|---|---|---|---|
| Auslöser | `def_state["group_wounds"]` gesetzt (z. B. Nobz, Silent King) | kein `group_wounds` | `tab_state["applied"] == True`, jeder Typ |
| Subgruppen-Selector | ja, wenn >2 aktive Gruppen (§1.4) | entfällt | entfällt |
| Caption | „Per-group HP: Boss Nob 3 · Nobz 15" | keine | — |
| Haupt-Eingabefeld | **„Total damage dealt (0–N)"** — 1 Zahl | **„Models lost"** (nur falls >1 Modell) + **„Wounds on front model (0–N-1)"** (nur falls `wounds>1`) — bis zu 2 Zahlen | — |
| Mortal Wounds | „Mortal Wounds" (falls `has_mortal_wounds`) | „Mortal Wounds" (falls `has_mortal_wounds`) | — |
| Ergebnis | `success`-Zeile + Wiped-Group-Warnungen + Reroll-GO + Reset | identisch | identisch |

Konkrete Divergenzen, die der Stakeholder als „uneinheitlich" gerügt hat (T3-V S168):
- **Wortlaut:** „Total damage dealt" (Substantiv+Partizip) vs. „Models lost" + „Wounds on
  front model" (zwei andere Substantiv-Phrasen) — kein gemeinsames Vokabular für „wie viel
  Schaden kam durch".
- **Range-Hinweis inkonsistent:** Pfad (i) zeigt „(0–N)" für Total Damage, aber nicht für
  Mortal Wounds. Pfad (ii) zeigt „(0–N-1)" für Wounds-on-front, aber **keine** Obergrenze
  für „Models lost" (`max_value` fehlt dort im Code).
  Kein Sonderfall — Anlass des Divergenz-Sonderfalls, s. §4.
- **Feldzahl:** 1 Zahl (i) vs. bis zu 2 Zahlen (ii) — der Nutzer sieht bei jedem Einheitswechsel
  ein anders aussehendes Formular, ohne erkennbares gemeinsames Muster.
- **Caption nur in Pfad (i)** — Pfad (ii) hat keine Entsprechung (z. B. „HP verbleibend").

## 2. Regel-Check — ist die Divergenz (i) vs. (ii) regelnotwendig?

**Ja, teilweise.** `core_rules.txt` Z. 1682-1706 (Allocate Attack / Damage): Schaden wird
**pro Modell sequenziell** zugeteilt — ein Modell muss vollständig sterben, bevor das
nächste Schaden nimmt; überschüssiger Schaden an einem sterbenden Modell **verfällt**
(„any excess damage inflicted by that attack is lost"), außer bei Mortal Wounds, die
zwischen Modellen weiterlaufen (Z. 1756).

- Pfad (ii) „Models lost" + „Wounds on front model" ist eine **kompakte Kodierung genau
  dieser Regel** unter der Annahme *eines einzigen* Wounds-Werts für alle Modelle der
  Einheit — die App multipliziert `models_lost × wounds_per_model` intern
  (`combat.apply_damage_attacks`) und rekonstruiert daraus die Gesamt-HP-Zahl, exakt
  wie ein Spieler am Tisch mitzählt („3 Modelle tot, das vierte hat noch 2 von 3 Wunden").
- Pfad (i) „Total damage dealt" existiert, **weil Gruppen-Wunden-Einheiten diese Annahme
  verletzen**: unterschiedliche Untergruppen haben unterschiedliche Wounds-Werte
  (Silent King: Szarekh W16, Triarchal Menhirs W7 — `unit.has_per_group_wounds()`,
  `unitMutations.py:129-149`). Ein „Modelle verloren"-Zähler wäre hier mehrdeutig (welche
  Gruppe?), deshalb nimmt die App direkt die Gesamt-HP-Zahl entgegen und verteilt sie
  intern per Priorität/Sperr-Logik (`apply_damage`, `unitMutations.py:203ff`).

**Fazit:** Die *Existenz* zweier unterschiedlicher Eingabe-Formen (Gesamtzahl vs.
Modell-Zähler+Rest) ist durch die Datenstruktur (homogene vs. gemischte Wounds-Werte je
Gruppe) begründet — hier NICHT einebnen. Die *Form* dieser Eingabe (Wortlaut, Reihenfolge,
Range-Anzeige, Caption-Stil) ist dagegen **keine Regelfrage**, sondern reines UI und kann
vereinheitlicht werden, ohne die Regel-Korrektheit zu berühren.

## 3. Grundannahmen des Entwurfs

- Die zwei Eingabe-*Formen* (Gesamtzahl vs. Modell-Zähler+Rest) bleiben bestehen — s. §2.
  Vereinheitlicht wird das **Drumherum**: Block-Reihenfolge, Label-Vokabular, Range-Anzeige,
  Caption-Konvention.
- Header, Dmg/HP-Zeile, Apply-Button und Post-Apply-Zustand sind bereits identisch über
  alle drei Pfade — keine Änderung nötig, nur explizit im Schema mit aufgeführt, damit der
  Stakeholder den Gesamt-Block am Stück sieht.
- Der Subgruppen-Selector (§1.4) bleibt unverändert (S181/B-128(a) bereits bestätigt) —
  dieser Vorschlag ändert daran nichts.
- Keine neue Feld-Logik, keine neue Berechnung — reines Layout-/Wortlaut-Schema.

## 4. Soll-Schema (vereinheitlicht)

```
┌──────────────────────────────────────────────────────────────┐
│ DAMAGE                                                        │  identisch heute
│ D{dmg} per failed save · Target: {wounds} HP/model            │  identisch heute
│ ────────────────────────────────────────────────────────────│
│ [Subgruppen-Selector — nur group_wounds + >1 aktive Gruppe]   │  §1.4, unverändert
│ ────────────────────────────────────────────────────────────│
│ SCHADEN-EINGABE                                                │  ← NEU: gemeinsamer Absatz-Titel
│                                                                 │
│  Gruppen-Wunden:                                               │
│   Per-group HP: {Gruppe A} {N} · {Gruppe B} {N}                │  Caption, unverändert
│   [ Damage dealt (0–{gw_total}) ]                              │  ← umbenannt, s. Entscheidung D1
│                                                                 │
│  Einzel-/Multi-Modell:                                         │
│   [ Models lost (0–{models_max}) ]  ← NEU: Obergrenze ergänzt  │  nur falls >1 Modell
│   [ Wounds on front model (0–{wounds-1}) ]                     │  nur falls wounds>1
│                                                                 │
│  Beide (falls Waffe MW hat):                                   │
│   [ Mortal Wounds (0–∞) ]                                      │  unverändert, Label gleich
│                                                                 │
│ ────────────────────────────────────────────────────────────│
│ [⚔ Apply {total} Damage → {target}]                            │  identisch heute
└──────────────────────────────────────────────────────────────┘
                          │ Klick Apply
                          ▼
┌──────────────────────────────────────────────────────────────┐
│ ✓ {N} models · {MW} MW · {total} damage applied                │  identisch heute
│ [⚠ Subgruppe „{Name}" verloren — {Waffen} nicht mehr verfügbar]│  optional, unverändert
│ [reaktive GO-Karte: Command Re-Roll — §6.2]                     │  unverändert
│ [↺ Reset]                                                       │  unverändert
└──────────────────────────────────────────────────────────────┘
```

Kernidee: **eine** gemeinsame Baustein-Reihenfolge (Header → Dmg/HP-Zeile → Subgruppen-
Selector → **„SCHADEN-EINGABE"-Absatz** mit typabhängigem Inhalt → Mortal Wounds → Apply →
Post-Apply), statt wie heute zwei optisch unverbundene Formulare, die sich nur zufällig im
Kopf/Fuß gleichen.

## 5. Ist → Soll je Pfad (kurz)

| Pfad | Heute | Vorgeschlagen |
|---|---|---|
| (i) Gruppen-Wunden | „Total damage dealt (0–N)", kein Absatz-Titel | „Damage dealt (0–N)" unter „SCHADEN-EINGABE"-Titel, sonst gleich |
| (ii) Einzel-/Multi-Modell | „Models lost" ohne Obergrenze, „Wounds on front model (0–N-1)" | „Models lost (0–{models_max})" mit Obergrenze, „Wounds on front model (0–N-1)" unverändert, unter „SCHADEN-EINGABE"-Titel |
| (iii) Post-Apply | success-Zeile + Warnungen + GO-Karte + Reset | unverändert (bereits einheitlich) |

## 6. Offene Design-Entscheidungen für den Stakeholder

- **D1 — Label „Total damage dealt" → „Damage dealt":** Kürzung auf ein gemeinsames
  Kernwort („Damage dealt" statt „Total damage dealt"), damit es näher am Vokabular von
  „Models lost"/„Wounds on front model" liegt (alle drei nennen das Ereignis, nicht mehr
  „Total"/"Wounds" uneinheitlich). Alternative: Label unverändert lassen, weil „Total"
  bei Gruppen-Wunden inhaltlich zutreffender ist (es ist wirklich eine Summe über die
  ganze Gruppe, kein Einzelwert wie bei „Models lost").
- **D2 — Gemeinsamer Absatz-Titel „SCHADEN-EINGABE":** neuer, bisher nicht vorhandener
  UI-Text. Einzuführen ja/nein? Falls ja: exakter Wortlaut (Deutsch/Englisch — App-UI ist
  sonst durchgehend Englisch, s. `CLAUDE.md`/Memory „Wahapedia — Regelreferenz") und
  Formatierung (fett wie „**DAMAGE**" oder kleiner Sub-Header).
- **D3 — Obergrenze für „Models lost" ergänzen:** heute kein `max_value` gesetzt (Bug oder
  bewusst? — Nutzer kann aktuell mehr Modelle eintragen als die Einheit hat). Vorschlag:
  `max_value=def_unit.models_max` ergänzen, analog zu „Wounds on front model". Zustimmung?
- **D4 — Bleiben „Models lost" und „Total damage dealt" zwei Konzepte oder soll langfristig
  auf EIN Konzept (immer „Damage dealt", App leitet Modelle intern ab) umgestellt werden?**
  Das wäre ein größerer technischer Umbau (nicht nur Wortlaut) und laut §2 regelbedingt nur
  für homogene Einheiten überhaupt möglich — als *separate* Zukunftsfrage vermerkt, nicht
  Teil dieses T2-Vorschlags.

## 7. Folge-Schritte nach Abnahme

- Bei Zustimmung: `docs/spec/design_system.md` §1.4 wird um das vollständige DAMAGE-Block-
  Schema (nicht nur den Subgruppen-Selector) erweitert — Ergänzung, kein Ersatz der
  bestehenden Zustände A/B/C.
- Die Code-Umsetzung (`_common.py:_render_damage_block`) ist ein **separates
  Backlog-Item** (Folgesession) — dieser Auftrag liefert nur den Entwurf, keinen Code.

Entscheidung: Der Stakeholder nimmt den Vorschlag und die empfohlene Vorgehensweise an. Bei D4 bin ich mir nicht sicher, ob ich dich richtig verstanden habe. Models Lost und Total Damage Dealt bleiben ja erhalten. Ich sehe gerade nicht den Vor- oder Nachteil eines Umbaus. Was meinst du? Was wäre besser. Betrachte hier bitte nicht den Mehraufwand, sondern was aus Clean Code oder Architektur-Sicht die bessere Lösung wäre.