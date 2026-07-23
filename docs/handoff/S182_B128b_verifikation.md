STATUS: AWAITING-VERIFICATION

# S182 B-128(b) Verifikation: DAMAGE-Block vereinheitlicht

Änderung: `_render_damage_block` (`src/uiLayout/_common.py`) wurde gemäß dem in S181
freigegebenen Mockup vereinheitlicht (D1–D3 umgesetzt, Spec `docs/spec/design_system.md`
§1.4.1): Sub-Header „Enter damage taken" vor den Zahlenfeldern in beiden Pfaden, Label
„Total damage dealt" → „Damage dealt" (Pfad Gruppen-Wunden), Obergrenze `max_value` für
„Models lost" ergänzt (Pfad Einzel-/Multi-Modell).

---

## Testfall (i) — group_wounds-Pfad (Silent King)

### Voraussetzung
Roster `data/rosters/necrons_1500pts_silent_king.yaml` laden (Necron-Seite). Enthält
Szarekh, the Silent King (`the_silent_king`, W16 + Triarchal Menhirs W7,
`has_per_group_wounds` — zwei Modell-Gruppen mit unterschiedlichen Wounds-Werten).

### Klickpfad
1. Kampfphase (eigene oder gegnerische, Hauptsache eine Attacke gegen den Silent King).
2. Silent King als Ziel wählen, einen Angriff bis zum DAMAGE-Block durchführen (mind. ein
   fehlgeschlagener Save).
3. DAMAGE-Block der Ziel-Einheit betrachten.

### Erwartung
- Sub-Header **„Enter damage taken"** erscheint als gedämpfter Absatz-Titel (Caption, nicht
  fett) zwischen Subgruppen-Selector/Header und den Zahlenfeldern.
- Eingabefeld heißt **„Damage dealt (0–N)"** — **nicht mehr** „Total damage dealt".
- Caption „Per-group HP: …" (Szarekh-Wert · Triarchal-Menhirs-Wert) bleibt unverändert
  sichtbar über dem Feld.
- Feld liegt in der halbbreiten Spalte (`dmg_col`) wie der restliche DAMAGE-Block.

### Checkpunkte (vor Abschluss prüfen)
- [ ] **1 — Regelkonform:** Feld erfasst weiterhin die Gesamt-HP-Zahl für die Gruppe (kein
  Verhaltenswechsel ggü. vorher — nur Label/Sub-Header sind neu); Verteilung auf Szarekh vs.
  Triarchal Menhirs folgt weiterhin `apply_damage`/`get_locked_group()` (`unitMutations.py`).
- [ ] **2 — Komponente + Anker `design_system.md` §1.4.1:** Reihenfolge Header → Dmg/HP-Zeile
  → Subgruppen-Selector → „Enter damage taken" → Zahlenfeld → Mortal Wounds → Apply
  entspricht exakt dem Schema in §1.4.1.
- [ ] **3 — Wortlaut-Familie englisch/konsistent:** „Damage dealt" liegt sprachlich näher an
  „Models lost"/„Wounds on front model" (Testfall ii) als das alte „Total damage dealt";
  durchgehend Englisch, keine deutschen Reste.

---

## Testfall (ii) — Multi-Modell-Pfad (Lokhust Heavy Destroyers)

### Voraussetzung
Dasselbe Roster (`data/rosters/necrons_1500pts_silent_king.yaml`), Einheit **Lokhust Heavy
Destroyers** (`lokhust_heavy_destroyers`, mehrwundiges Mehrmodell-Team, kein
`group_wounds`).

### Klickpfad
1. Kampfphase, Angriff gegen die Lokhust Heavy Destroyers bis zum DAMAGE-Block durchführen.
2. Im Feld **„Models lost"** versuchen, einen Wert **größer** als die aktuelle Modellzahl der
   Einheit einzutragen (z. B. Modellzahl + 5).
3. DAMAGE-Block insgesamt betrachten.

### Erwartung
- Derselbe Sub-Header **„Enter damage taken"** erscheint (identischer Wortlaut/Stil wie in
  Testfall i).
- Feld **„Models lost (0–models_max)"** — die Obergrenze greift: es lässt sich **nicht** mehr
  eintragen, als die Einheit an Modellen hat (D3-Fix, vorher fehlte `max_value`).
- Zusätzlich Feld **„Wounds on front model (0–N-1)"** unverändert vorhanden.
- Kein Sub-Group-Selector (Einheit hat keine `model_groups`-Gruppenwunden).

### Checkpunkte (vor Abschluss prüfen)
- [ ] **1 — Regelkonform:** Obergrenze `max_value=def_unit.models_max` verhindert
  Falscheingaben > tatsächliche Modellzahl (9E-Regel „Schaden wird pro Modell zugeteilt,
  Überschuss verfällt", `core_rules.txt` Z. 1682–1706) — Eingabe-UI kann jetzt keinen
  regelwidrigen Zustand mehr erzeugen.
- [ ] **2 — Komponente + Anker `design_system.md` §1.4.1:** Reihenfolge Header → Dmg/HP-Zeile
  → (kein Selector, da kein `group_wounds`) → „Enter damage taken" → Models-lost-Feld →
  Wounds-on-front-Feld → Mortal Wounds → Apply entspricht dem Schema.
- [ ] **3 — Wortlaut-Familie englisch/konsistent:** „Models lost"/„Wounds on front model"
  bleiben wie vorher, jetzt aber unter demselben Sub-Header-Wortlaut wie Pfad (i) — eine
  Vokabel-Familie über beide Pfade, durchgehend Englisch.
