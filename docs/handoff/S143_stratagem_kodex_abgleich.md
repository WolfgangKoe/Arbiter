STATUS: ANSWERED

# S143 — Stratagem-Kodex-Abgleich (Vorarbeit für spätere Datenpflege)

Auftrag: Nur Abgleichliste erstellen, NICHTS in den YAML-Daten geändert.

## Methodik

1. **Lokale Quell-Tags:** `docs/work/wahapedia_*/stratagems.txt` trägt hinter jedem
   Stratagem-Namen ein leeres `[]` (z. B. `[1 CP]  SWIFT DISMEMBERMENT  []`,
   necrons/stratagems.txt:150). Über alle geprüften Zeilen (Necrons, Orks) ist
   das Klammerpaar **immer leer** — der Scraper hat nie ein Quell-Feld befüllt.
   `tools/wahapedia_scraper.py` enthält **kein** Source-/Quelle-Feld (kein Treffer
   auf „source"/„Source" im gesamten Skript) — die Quelle wurde beim Scrapen nicht
   erfasst, ist also nicht nachträglich aus der lokalen Datei rekonstruierbar.
2. Für Custodes existiert lokal **keine** `stratagems.txt` und **kein**
   `data/wh40k_9e/adeptus_custodes/stratagems.yaml` — es gibt noch keine
   gescrapte/gepflegte Custodes-Stratagem-Datenbasis. Der Abgleich für Custodes
   entfällt daher inhaltlich (siehe unten).
3. Quelle je Stratagem: WebFetch auf `https://wahapedia.ru/wh40k9ed/factions/<faction>/`
   (Faction-Übersichtsseite, gleiche Basis-URL wie der Scraper selbst verwendet,
   `BASE = "https://wahapedia.ru/wh40k9ed/factions"`). Direkte `/Stratagems`-Unterseiten
   (naheliegender Rateversuch) lieferten 404 — die Stratagems stehen auf der
   Faction-Hauptseite. WebFetch liefert eine Modell-Zusammenfassung der Seite, keine
   Rohdaten — bei Vollständigkeits-Zweifel (v. a. Orks „Core"-Liste) als **unsicher**
   markiert statt die Seite als erschöpfend zu behandeln.
4. Abgleich gegen `data/wh40k_9e/<fraktion>/stratagems.yaml`: Zeilen per `grep -n "name_en:"`.

**Wichtiger Befund vorab:** `necrons/stratagems.yaml` Zeilen 14–22 dokumentiert bereits
einen früheren Abgleich (S134) für Boarding-Actions-Ausschluss — das jetzige Kodex-Filter-
Vorhaben ist eine **weitere, strengere** Stufe obendrauf (Boarding Actions war schon raus,
jetzt geht es um Nicht-Codex-Supplements wie White Dwarf/Warzone).

---

## Necrons — 56 Einträge in YAML (Core 34/35 + Dynastic 6 + Cult of the Cryptek 8 + Annihilation Legion 8)

| Stratagem | Quelle (Wahapedia-Seite) | sicher? | In YAML (Zeile) | Empfehlung |
|---|---|---|---|---|
| Hand of the Phaeron … Revenge of the Doomstalker (34 Einträge, „Core Stratagems") | Codex: Necrons | sicher | necrons/stratagems.yaml:29–496 (Requisition/Fight/etc., einzeln aufgelistet in Datei) | **behalten** |
| Talent for Annihilation (Mephrit) | Codex: Necrons — Dynastic | sicher | :513 | behalten |
| Translocation Crypt (Nephrekh) | Codex: Necrons — Dynastic | sicher | :525 | behalten |
| Reclaim a Lost Empire (Nihilakh) | Codex: Necrons — Dynastic | sicher | :538 | behalten |
| Blood Rites (Novokh) | Codex: Necrons — Dynastic | sicher | :551 | behalten |
| Methodical Destruction (Sautekh) | Codex: Necrons — Dynastic | sicher | :565 | behalten |
| Empyric Damping (Szarekhan) | Codex: Necrons — Dynastic | sicher | :585 | behalten |
| Exalted Cryptek | White Dwarf 08/22 — „Cult of the Cryptek" | sicher (Wahapedia-Rubrik explizit als eigene Gruppe geführt) | :600 | **entfernen** |
| The Swarm Descends | White Dwarf 08/22 — Cult of the Cryptek | sicher | :614 | **entfernen** |
| Overkill Protocols | White Dwarf 08/22 — Cult of the Cryptek | sicher | :628 | **entfernen** |
| Aggression Overrides | White Dwarf 08/22 — Cult of the Cryptek | sicher | :643 | **entfernen** |
| Stalking Annihilator | White Dwarf 08/22 — Cult of the Cryptek | sicher | :658 | **entfernen** |
| Hyperdense Particle Beams | White Dwarf 08/22 — Cult of the Cryptek | sicher | :672 | **entfernen** |
| Enhanced Gloom Prism | White Dwarf 08/22 — Cult of the Cryptek | sicher | :687 | **entfernen** |
| Canoptek Overdrive | White Dwarf 08/22 — Cult of the Cryptek | sicher | :702 | **entfernen** |
| A Moment of Clarity | White Dwarf 10/22 — „Annihilation Legion" (Army-of-Renown-artiges Zusatzmaterial; referenziert ANNIHILATION-LEGION-Keyword, Anlass des Stakeholder-Hinweises) | sicher | :720 | **entfernen** |
| Canoptek Reinforcement | White Dwarf 10/22 — Annihilation Legion | sicher | :734 | **entfernen** |
| Swift Dismemberment | White Dwarf 10/22 — Annihilation Legion (Anlass-Stratagem #1) | sicher | :748 | **entfernen** |
| Weaponised Bodies | White Dwarf 10/22 — Annihilation Legion (Anlass-Stratagem #2) | sicher | :762 | **entfernen** |
| Efficient Disintegration | White Dwarf 10/22 — Annihilation Legion | sicher | :775 | **entfernen** |
| Hyperphase Impalement | White Dwarf 10/22 — Annihilation Legion | sicher | :792 | **entfernen** |
| Lurking Murderers | White Dwarf 10/22 — Annihilation Legion | sicher | :806 | **entfernen** |
| Murderous Demise | White Dwarf 10/22 — Annihilation Legion | sicher | :820 | **entfernen** |

**Necrons Zusammenfassung: 16 von 56 Einträgen zu entfernen (0 unsicher)** — exakt die
8 Cult-of-the-Cryptek- + 8 Annihilation-Legion-Stratagems. Deckt beide Anlassfälle
(„Swift Dismemberment", „Weaponised Bodies") sowie „A Moment of Clarity" ab (letzteres
bestätigt selbst als Annihilation-Legion-Quelle, nicht nur Indiz über das Keyword).

Hinweis: `stratagems.txt` (Rohquelle) enthält zusätzlich „Prismatic Dimensional Breach"
(Zeile 148 in stratagems.txt / Zeile 148 in stratagems.yaml) — von der WebFetch-Zusammenfassung
nicht namentlich genannt, aber im Zahlenbereich der 34 „Core"-Einträge; hier als **behalten**
eingestuft (Position/Struktur passt zu Core, keine Gegenanzeige gefunden), aber mit
niedrigerer Sicherheit als die übrigen 33 Core-Einträge — falls der Stakeholder Zweifel hat,
gezielt nachschlagen.

---

## Orks — 23 Einträge in YAML (8 Core + 7 Klan + 8 Specialist-Detachment)

| Gruppe | Quelle | sicher? | In YAML (Zeilen) | Empfehlung |
|---|---|---|---|---|
| Big Boss, Extra Gubbinz (Requisitions) | Codex: Orks | sicher | :24, :37 | behalten |
| Careen!, Breakin' Heads, Orks is Never Beaten, Get Stuck In Ladz!, Hit 'Em Harder, Gun Crazy Show Offs, Ramming Speed, Tough as Squig-Hide (8 Core) | Codex: Orks | sicher | :106–:211 | behalten |
| Showin' Off (Bad Moons), Ded Sneaky (Blood Axes), Wreckaz (Deathskulls), Drive By Dakka (Evil Sunz), Get Da Loot (Freebooterz), Unbridled Carnage (Goffs), Mystic Chanting (Snakebites) — je 1 pro Klan Kultur | Codex: Orks — Klan-Kultur-Stratagems | sicher | :234, :248, :261, :282, :294, :307, :321 | behalten |
| Blitz Brigade, Dread Waaagh!, Kult of Speed, Stompa Mob (Detachment-Setup) + je 2 zugehörige Regel-Stratagems (Opening Salvo/Krush 'Em/Hold On Boyz!; Kustom Ammo/Turbo-Boostas/…; Stomp Stomp Stomp/Stompa-Porta) | **Imperium Nihilus: Vigilus Defiant** (Kampagnenbuch, laut Wahapedia-Zusammenfassung) — NICHT Codex: Orks | **unsicher** | :52–:65, :78, :91, :336–:431 (Detachment-Setup + Folge-Stratagems) | Empfehlung abhängig von Scope-Frage 2 unten — wenn „nur Codex-Kernstratagems" strikt ausgelegt wird: **entfernen** (8 Einträge); wenn Specialist-Detachment-Regeln als inzwischen kodex-integriert gelten: behalten |

**Orks Zusammenfassung: 0 sicher zu entfernen / 8 unsicher** (die vier Specialist-Detachment-
Setup-Stratagems + ihre je 2 zugehörigen Regel-Stratagems — abhängig von der Scope-Frage,
ob Vigilus-Defiant-Specialist-Detachments als „Kodex-Inhalt" zählen). Die bereits in der
YAML-Kopfzeile ausgeschlossenen Boarding-Actions-/Speed-Mob-/Warzone-Octarius-Blood-Axes-
Stratagems sind schon draußen (S134-Altbefund) — kein neuer Handlungsbedarf dort.

---

## Adeptus Custodes — keine lokale Datenbasis

Es existiert weder `docs/work/wahapedia_adeptus_custodes/stratagems.txt` noch
`data/wh40k_9e/adeptus_custodes/stratagems.yaml` (nur `faction_abilities.yaml` und
zwei `placeholder.*.yaml`). Zur Vollständigkeit per WebFetch auf die Wahapedia-
Custodes-Seite geprüft: 33 Core-Stratagems (Requisition/Strategic Ploy/Battle
Tactic/Wargear/Epic Deed) plus 6 „Shield Host"-Stratagems (Emperor's Chosen,
Dread Host, Shadowkeepers, Aquilan Shield, Solar Watch, Emissaries Imperatus —
diese Shield Hosts sind reguläre Codex-Detachments, vermutlich Kern-Kodex-Inhalt,
**nicht** Kampagnen-Supplement) plus 6 „Boarding Actions"-Stratagems (analog zum
Necron-Fall vermutlich Spezialmodus-only).

**Custodes Zusammenfassung: 0 von 0 Einträgen zu entfernen** — es gibt (noch) keine
gepflegte YAML, an der etwas zu entfernen wäre. Falls/wenn Custodes-Stratagems künftig
gescrapt werden, sollte der Kodex-Filter direkt beim Erst-Scrape angewendet werden
(Shield Hosts vsl. behalten, Boarding Actions vsl. ausschließen wie bei Necrons).

---

## Offene Scope-Fragen an den Stakeholder

1. **Gilt der Kodex-Filter für alle drei Fraktionen oder nur Necrons?** (Anlass war
   ausschließlich der Necron-Fund; Orks hat einen eigenen Grenzfall — Vigilus-Defiant-
   Specialist-Detachments — der eine eigene Entscheidung braucht, unabhängig vom
   Necron-Fall.)
2. **Detachment-/Formation-Supplements wie Codex-eigene Nachfolge-Regeln (z. B.
   Pariah Nexus für Necrons) — behalten oder auch raus?** Betrifft aktuell keinen
   der 56 Necron- oder 23 Ork-Einträge direkt (kein Pariah-Nexus-Stratagem in der
   YAML gefunden), ist aber als Grundsatzfrage relevant für künftige Scrapes/Updates
   und für die Custodes-Shield-Hosts (s. o.) — sind Shield Hosts „Kern-Kodex" oder
   ein Nachfolge-Supplement? Wahapedia führt sie strukturell näher am Kodex als
   Boarding Actions, aber das ist eine Einordnung, keine belastbare Quellenangabe.

## Stakeholder-Entscheid (S143, 2026-07-12)

Necrons: die 16 belegten White-Dwarf-Supplement-Einträge werden entfernt (Datenpflege S144).
Orks: die 8 Vigilus-Kandidaten NICHT sofort entfernen — ihre Klärung ist bewusst als eigene
S144-Aufgabe eingeplant. Custodes: n/a (keine Stratagem-Daten vorhanden).
