STATUS: NEEDS-DECISION

# S132 — GO-Karte Praxisbefunde (Stakeholder-Review)

Untersuchung, read-only. Bezug: `docs/spec/design_system.md` §6, `src/uiLayout/go_card.py`,
`src/uiLayout/_common.py::render_go_card`.

## Befund 1 — CP dreimal, Use-Button an falscher Stelle

**Diagnose (bestätigt):** `go_card.py::go_card_html()` baut in `action_html` (Z. 113–117) eine
reine `<span>`-Attrappe `Use (N CP)` oben rechts in der Karten-HTML — kein `onclick`, keine
Funktion. `_common.py::render_go_card()` (Z. 721–779) rendert danach den **echten** `st.button`
separat UNTER der Karte (nach dem Expander), mit demselben Label. Ergebnis: CP-Kosten erscheinen
3× (Header „· N CP", Attrappe „Use (N CP)", echter Button „Use (N CP)"), zwei visuelle
Action-Slots statt einem. §6.1 verlangt „Header-Zeile: Name · CP-Kosten · genau **ein**
Aktions-Slot rechts" — ein Slot in derselben Zeile wie der Header, nicht ein toter Zwilling plus
ein echter Button in einer neuen Zeile darunter. Root Cause: HTML kann keinen klickbaren
Streamlit-Widget enthalten, der Attrappen-Slot wurde als Platzhalter für das Layout gebaut, aber
nie durch echtes Spaltenlayout ersetzt.

**Fix-Optionen:**
- **Option A — `st.columns` statt Attrappe (empfohlen).** Karte bleibt `st.container(border=True)`
  (wie `unitCard.py:170`, bereits etabliertes Muster) mit `st.columns([5,2])`: linke Spalte
  Header-HTML (Name · CP, ohne Action-Span), rechte Spalte der echte `st.button` — beide in
  derselben Zeile. Chips + Akkordeon darunter wie bisher. Aufwand: **S** (go_card_html verliert
  `action_html`, render_go_card bekommt Spalten-Wrapper). Risiko: `st.container(border=True)`
  nutzt eine feste Theme-Randfarbe (Emotion-Klasse laut CLAUDE.md) — pro Zustand Gold/gedimmt
  einzufärben geht NICHT zuverlässig per CSS-Selektor (kein Zustands-Attribut am Container-Node).
  Deshalb Rand weiter über die bestehende HTML-`<div>` lösen, nur den Button in eine Spalte daneben
  setzen — kein echter `st.container(border=True)`-Wechsel, nur `st.columns` innerhalb des
  HTML-Flows.
- **Option B — Attrappe entfernen, echten Button direkt danach ohne Zeilenumbruch.** Minimal-Fix:
  `action_html` aus `go_card_html` streichen (kein Duplikat mehr), Button bleibt wo er ist (unter
  der Karte). Behebt die 3×CP-Dopplung, aber NICHT die Slot-Position lt. §6.1 (Use weiterhin unter
  statt in der Header-Zeile). Aufwand: **XS**. Nur als Zwischenschritt sinnvoll, keine echte
  Design-Treue.

Empfehlung: Option A (Design-Treue vs. Aufwand S vertretbar).

## Befund 2 — Command Re-Roll Advance/Charge: kein Dauerangebot, kein Undo

**Diagnose (bestätigt):** `render_inline_command_reroll()` (`_common.py:633`) wird in
`movementPhase.py:140` nur innerhalb `if current == "advanced":` aufgerufen — sichtbar erst NACH
der Advance-Statuswahl, nicht vorher/immer. In `chargephase.py:114` erscheint es nach
Ziel-Auswahl, vor Successful/Failed. Nach Klick: `spend_stratagem()` + `on_reroll()` +
`st.rerun()` — kein „used"-Zustand, kein `undo_stratagem`-Aufruf. Die Schleife filtert zusätzlich
hart auf `vis == "clickable": continue` sonst — d.h. nach Verbrauch verschwindet das Angebot
vollständig (nicht einmal gedimmt), obwohl `stratagem_undo_visible`/`undo_stratagem` im Modul
existieren und von `render_go_card` bereits genutzt werden. Kein Undo-Pfad vorhanden.

**Skizze Soll (GO-Karten-Kompaktform):** `render_go_card(..., compact=True)` an derselben
Call-Site, State-Mapping wie in `gameProtocoll.py::_go_state_and_reason`: „ruhend" solange kein
Roll-Kontext (z. B. vor Advance-Klick, falls das gewünscht ist — KLÄRUNGSBEDARF s.u.), „bereit"
sobald Trigger-Fenster offen + CP reichen, „verwendet" mit `↺ Undo (+1 CP)` nach Klick,
„gesperrt" bei 0 CP. Erfordert: (1) State-Ableitung analog `_go_state_and_reason` in beide
Phase-Module ziehen oder gemeinsame Helper-Funktion, (2) `on_undo` Callback der Advance/Charge
NICHT zurücksetzt (nur CP + Stratagem-Buchung, da kein Wert-Feld existiert — §6.3
Gegenbeispiel-Absatz bestätigt: Advance/Charge hat keine Werterfassung). Aufwand: **S–M**
(zwei Call-Sites, State-Helper, kein neues Datenmodell).

## Befund 3 — Reaktive Stratagem-Box noch alter Stil

**Ort:** `render_reactive_stratagem_box()` in `_common.py:523`, aufgerufen von
`chargephase.py:164`, `fightPhase.py:458`, `movementPhase.py:386`. Bestätigt: NICHT auf
`render_go_card` umgestellt (eigenes Use/Pass-Dialog-Layout, kein `go_card_html`). Migration ist
bereits als **Paket 3 (S133)** in `docs/goals/backlog.md` §2 vorgesehen — kein neuer Fix hier
nötig, nur Bestätigung.

## Befund 4 — „BEAST SNAGGA" fehlt bei „Get Stuck In, Ladz!"

**Diagnose:** Datenlücke in YAML, kein Render-Bug. `data/wh40k_9e/orks/stratagems.yaml:154` hat
`conditions: [BOYZ]` — nur ein Keyword, obwohl `rule_text` (Z. 158) explizit „a BOYZ or BEAST
SNAGGA BOYZ unit" nennt. `gameProtocoll.py:272` übergibt `keywords=strat.conditions` komplett an
`render_go_card`/`go_card_html` — **alle** Einträge der Liste werden als Chips gerendert (kein
„nur erstes Element"-Bug, s. `go_card.py:126` `for kw in keywords`). Fix: `conditions:
[BOYZ, BEAST SNAGGA]` ergänzen (Doku-Quelle: `docs/work/wahapedia_orks/` bestätigt „Get Stuck
In!" als Waaagh-Stage-2-Fähigkeit, nicht dasselbe wie das Stratagem — der Stratagem-Wortlaut
selbst steht nur im YAML-`rule_text`, keine widersprüchliche Quelle gefunden). Aufwand: **XS**
(1-Zeilen-YAML-Fix + Regressionstest auf `conditions`-Länge).

## Befund 5 — „Alt. Fire"-Chip unerklärt in der Attackensequenz

**Fund:** `src/uiLayout/dice_html.py:70` — `special_die_html("Alt. Fire")` wird gerendert, wenn
`weapon_special.get("alternating_fire")` truthy ist (HIT-Block, neben Extra-Hits/−1-to-Hit-Badges,
nicht neben DENSE-COVER — das ist eine separate Checkbox im SAVE-Kontext, ggf. optische Nähe im
Screenshot). Bedeutung: 9E-Sonderregel „Alternating Fire" (bestimmte Waffen/Einheiten würfeln
Hit-Rolls einzeln statt gepoolt — Wortlaut in `core_rules.txt`/Fraktions-Regelwerk zu verifizieren,
hier nicht gegengelesen). Der Chip ist **kein** S132-Zuwachs — `special_die_html` und der
`weapon_special`-Dict-Zugriff sind Bestandscode aus der Attackensequenz, unverändert in diesem
Sprint. Ursache des Stakeholder-Befundes: dem Badge fehlt Kontext/Tooltip — anders als „Extra
Hits" (das einen Erklärungstext im Label trägt: „unmod. 6 = +2 Hits") hat „Alt. Fire" keinen
Zusatztext. Fix: `special_die_html("Alt. Fire", "<Kurzerklärung>")` analog Extra-Hits ergänzen,
sobald Wortlaut aus Regelwerk verifiziert. Aufwand: **XS**, aber Regelrecherche zuerst nötig.

## Entscheidungsbedarf Stakeholder

1. **Befund 2 — Soll-Verhalten:** Soll der Command-Re-Roll für Advance/Charge wirklich „immer"
   sichtbar sein (auch VOR der Advance/Charge-Entscheidung, als Vorschau ohne Trigger-Kontext)
   oder nur „bleibt stehen mit Undo, nachdem die zugehörige Aktion erfolgt ist" (aktuelles
   Trigger-Fenster, nur Undo ergänzt)? Das ändert Scope/Aufwand von Befund 2 spürbar.
2. **Befund 1 — Options-Wahl:** Option A (echte Spalten-Lösung, empfohlen) vs. Option B
   (Zwischenschritt, nur Dopplung weg) — oder direkt Paket 3/4-Rahmen abwarten und Befund 1 dort
   mit erledigen?
