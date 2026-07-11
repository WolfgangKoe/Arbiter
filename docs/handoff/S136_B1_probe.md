STATUS: ANSWERED

# S136 — B1 Scroll-Sprung: H1 (Fokus-Autoscroll) vs. Drittursache (Layout-Shift)

Bezug: B1 (Scroll-Sprung beim Ändern eines Command-Protocol-Slots im Setup),
`docs/goals/backlog.md` §2. Vorprobe: `docs/handoff/S135_B1_probe.md`
(H2 — Sechsfach-Key-Rewrite — **widerlegt**, Ergebnis Ja/Ja).

Diese Probe braucht **keinen Code-Patch** — reine Browser-DevTools-Beobachtung
reicht aus, um H1 (Fokus-Autoscroll) von der Drittursache (Layout-Shift durch
`st.columns`/variable Label-Länge) zu unterscheiden. Kein `git apply` nötig,
kein Koordinator-Schritt zwischendurch.

## Stand nach S135

H2 (Sechsfach-Key-Rewrite verursacht DOM-Remount) ist widerlegt: der Sprung
tritt mit und ohne den Rewrite-Patch identisch auf. Verbleibende Kandidaten:

- **H1 — Fokus-Autoscroll:** Der Browser holt beim Rerun automatisch das
  zuletzt fokussierte Widget (die geänderte Selectbox) in den sichtbaren
  Bereich, unabhängig davon, ob sich sonst etwas am Layout ändert.
- **Drittursache — Layout-Shift + Chrome Scroll-Anchoring:** Eine der sechs
  Selectboxes ändert beim Rerun ihre Höhe (Textumbruch durch unterschiedlich
  lange Ability-Namen), und zwar **oberhalb** des sichtbaren Bereichs. Chrome
  korrigiert die Scroll-Position automatisch, um den fokussierten Ausschnitt
  visuell stabil zu halten (CSS-Feature „Scroll Anchoring") — diese Korrektur
  ist der wahrgenommene „Sprung".

## Code-Befunde

**Mechanik des Slot-Tauschs** — `src/uiLayout/gameActionsArea.py:130-140`
(`_swap_round_choice_slot`): bei jeder Slot-Änderung wird die Bijektion neu
berechnet und **alle sechs** Widget-Werte in `session_state` geschrieben
(Zeile 138-140). Das reine Neuschreiben wurde in S135 als Sprung-Ursache
widerlegt — aber es bedeutet auch: der **Tausch-Partner** (die Selectbox, die
den alten Wert des geänderten Slots übernimmt) kann eine ganz andere,
unterschiedlich lange Beschriftung bekommen.

**Render-Reihenfolge** — `src/uiLayout/gameActionsArea.py:210-212`:
```
_slot_selectbox("extra", "Always active (6th)")   # Zeile 210 — ZUERST
for round_num in range(1, 6):
    _slot_selectbox(round_num, f"Round {round_num}")  # Zeile 211-212
```
Der 6. Slot („extra") steht **über** allen Runden-Dropdowns. Ändert der
Nutzer z. B. Runde 3 und der verdrängte Wert landet im 6. Slot oder in einer
früheren Runde (1/2) — beides oberhalb des Klicks — ändert sich dort die
angezeigte Beschriftung, **ohne dass der Nutzer dort hinschaut**.

**Variable Label-Länge** — `format_func=lambda pid: by_id[pid].name_de`
(`src/uiLayout/gameActionsArea.py:204`), gespeist aus
`src/gameObjects/loader.py:499` (`name_de=a.get("name_de", a["name_en"])` —
Necron-Fraktion hat aktuell **kein** `name_de` in den YAML, fällt also auf
`name_en` zurück). Necron-Protokollnamen (`data/wh40k_9e/necrons/
faction_abilities.yaml:54,76,94,125,143,162`) schwanken zwischen 27 und 33
Zeichen („Protocol of the Hungry Void" vs. „Protocol of the Conquering
Tyrant"). Die Dropdowns sitzen in einer schmalen Spalte:
`st.columns(2)` bei `src/uiLayout/gameActionsArea.py:304` (Setup-Blöcke
nebeneinander, S135 B6) **innerhalb** der bereits schmalen Center-Spalte
(`st.columns([2.5, 5, 2.5], ...)`, `src/uiLayout/gameHeader.py:304`) — bei
dieser Breite ist ein Textumbruch (1 vs. 2 Zeilen) bei den längeren
Necron-Namen plausibel, bei den kürzeren Custodes-Ka'tah-Namen
(`data/wh40k_9e/adeptus_custodes/faction_abilities.yaml:8,27,44,64,83,106`,
13-16 Zeichen) eher nicht.

**Frontend-Check (nicht schlüssig):** Statisch geprüft (CLAUDE.md-Vorgabe „JS
zuerst"), ob die Selectbox-Komponente selbst einen `scrollIntoView`/`.focus()`-
Aufruf enthält: `.venv/.../static/static/js/Selectbox.IrFeiYNi.js` enthält
keinen der beiden Strings. Das schließt H1 nicht aus (Fokus-Restore kann auch
auf einer allgemeineren Ebene im React-Framework passieren), liefert aber
keinen Beleg dafür — die Frage lässt sich nur live im Browser klären, nicht
aus dem Quellcode.

**`render_scroll_to_top`** (`src/uiLayout/gameHeader.py:218-241`, ausgelöst
über `st.session_state.pop("_scroll_to_top", False)` in `src/app.py:36-37`)
wurde geprüft und **ausgeschlossen**: das iframe-Skript feuert nur beim
Phasenwechsel (Flag wird explizit gesetzt), nicht beim Ändern eines
Protocol-Slots innerhalb der Setup-Phase.

## Probe — Schritt für Schritt (im Browser, DevTools, kein Patch)

**Vorbereitung (einmalig):**
1. App öffnen, DevTools öffnen (F12 oder Rechtsklick → „Untersuchen"),
   Tab **Console** wählen.
2. Folgenden Code in die Console einfügen, Enter drücken (misst nur, ändert
   nichts an der App):
   ```js
   window.__clsLog = [];
   new PerformanceObserver((list) => {
     for (const e of list.getEntries()) {
       window.__clsLog.push({wert: e.value, element: e.sources?.[0]?.node?.outerHTML?.slice(0,120)});
     }
   }).observe({type: 'layout-shift', buffered: false});
   ```

**Stufe 1 — Beobachtung (Fokus + Layout-Shift-Messung):**
3. In der Setup-Phase einen der sechs Command-Protocol-Slot-Dropdowns ändern
   (**nicht** das „Read directive"-Dropdown darunter).
4. Direkt danach in die Console eingeben: `document.activeElement` → Enter.
   Notieren: Zeigt die Ausgabe ein Element, das zum gerade geänderten
   Dropdown gehört (z. B. ein `<input>` oder `<div>` mit erkennbarem Text/
   Klassennamen des Dropdowns), oder etwas anderes (z. B. `<body>`)?
5. Danach eingeben: `window.__clsLog` → Enter.
   Notieren: Ist die Liste leer `[]`, oder enthält sie einen oder mehrere
   Einträge?
   Siehe Bildschirmfoto vom 2026-07-10 21-55-11

**Stufe 2 — Scroll-Anchoring testweise deaktivieren:**
6. Folgenden Code in die Console einfügen (deaktiviert eine Chrome-Funktion
   namens „Scroll Anchoring", die den Browser bei Layout-Änderungen
   automatisch nachscrollen lässt; rein clientseitig im aktuellen Tab, kein
   Python-Code betroffen, verschwindet beim nächsten Neuladen):
   ```js
   var s = document.createElement('style');
   s.textContent = '* { overflow-anchor: none !important; }';
   document.head.appendChild(s);
   ```
7. Wiederholen: einen Command-Protocol-Slot-Dropdown ändern (gerne einen
   anderen als in Stufe 1).
8. **Springt der Screen noch? Ja/Nein** notieren.
9. Seite neu laden (F5) — entfernt beide Console-Snippets wieder, kein
   Aufräumschritt nötig.

## Interpretation

**Haupttest (Schritt 8):**

| Springt mit deaktiviertem Scroll-Anchoring noch? | Bedeutung |
|---|---|
| **Nein** | Drittursache bestätigt: Layout-Shift + Chrome-Scroll-Anchoring ist die Ursache. Fix-Richtung: Höhe der sechs Dropdowns stabilisieren (z. B. feste Mindesthöhe/kein Umbruch) oder `overflow-anchor: none` dauerhaft per CSS setzen. |
| **Ja** | H1 (Fokus-Autoscroll) wahrscheinlich, unabhängig vom Layout — der Browser holt das fokussierte Widget aktiv in den sichtbaren Bereich. Fix-Richtung schwieriger (Browser-/Framework-Default-Verhalten bei Widget-Refokussierung nach Rerun). |

**Zusatzbeleg aus Stufe 1 (Schritt 4+5), zur Absicherung:**

- `activeElement` = das geänderte Dropdown **und** `__clsLog` leer →
  stützt „Ja" oben (reiner Fokus, kein gemessener Layout-Shift).
- `__clsLog` **nicht** leer → stützt „Nein" oben (es hat tatsächlich ein
  Layout-Shift-Ereignis stattgefunden, unabhängig vom Fokus).
- Beide Signale können auch gemeinsam auftreten (Fokus UND Layout-Shift) —
  dann ist Schritt 8 der Tie-Breaker: nur wenn das Deaktivieren des
  Anchorings den Sprung tatsächlich stoppt, ist Layout-Shift die
  hinreichende Ursache; sonst bleibt Fokus die treibende Kraft.

## Automatisierter Befund (Playwright, S136)

Durchführung: Playwright 1.60 / Chromium headless, Viewport 1920×1080,
Skript + Screenshots + Roh-JSON im Session-Scratchpad (`b1_probe.py`,
`b1_probe_results.json`, `stage{1,2}_iter{1-3}_{before,after}.png`).
Observer-Snippet wortgleich aus dieser Datei übernommen. Zwei Anpassungen
gegenüber der manuellen Anleitung:

- **Scroll-Messgröße:** Die App scrollt nicht das Dokument, sondern den
  inneren Container `[data-testid="stMain"]` — `window.scrollY` bleibt
  konstant 0. Gemessen wurde daher `stMain.scrollTop` (die für den Nutzer
  sichtbare Scroll-Position); `window.scrollY` wurde mitprotokolliert (immer 0).
- **Reproduzierbarkeit:** Jeder Durchlauf startet mit frischem Seiten-Load +
  „Start Game" (Streamlit-Session reset), Scroll-Position `stMain.scrollTop
  = 1250` (6. Slot + Round 1 oberhalb des Viewports, Round 2/3 sichtbar),
  dann Round 3 per Klick auf den Wert des 6. Slots getauscht (Labelwechsel
  oberhalb des sichtbaren Bereichs, Necron-Namen 27–33 Zeichen). Klicks per
  Koordinaten (`mouse.click`), damit Playwright selbst nie scrollt.

**Die drei Antworten:**

1. **Schritt 4 — `document.activeElement`:** `<body>` — der Fokus liegt nach
   dem Rerun NICHT auf dem geänderten Dropdown (3/3 Durchläufe). Damit fehlt
   H1 (Fokus-Autoscroll) die Grundlage: es gibt kein fokussiertes Widget, das
   der Browser in den sichtbaren Bereich holen könnte.
2. **Schritt 5 — `window.__clsLog`:** In Stufe 1 (Anchoring aktiv) praktisch
   leer (nur ein Eintrag mit Wert ~7e-07 ≈ 0). In Stufe 2 (Anchoring aus)
   dagegen echte Layout-Shift-Einträge mit Werten **0.22–0.92** auf
   `<div data-testid="stLayoutWrapper">` — der Layout-Shift findet also
   tatsächlich statt; bei aktivem Anchoring wird er von Chrome kompensiert
   (und darum nicht als Shift gescored), die Kompensation ist der Sprung.
3. **Schritt 8 — Springt mit deaktiviertem Scroll-Anchoring noch?** **Nein**
   (3/3 Durchläufe, Delta exakt 0).

**Gemessene scrollTop-Deltas (`stMain`, Start je 1250):**

| Durchlauf | Stufe 1 (Baseline) | Stufe 2 (`overflow-anchor: none`) |
| --- | --- | --- |
| 1 | **+2348** (→ 3598 = Seitenende) | 0 |
| 2 | **+2348** (→ 3598 = Seitenende) | 0 |
| 3 | **+2348** (→ 3598 = Seitenende) | 0 |

Der Sprung landet jedes Mal exakt bei `scrollHeight − clientHeight` — die
Anchoring-Korrektur zieht den Viewport bis ans Seitenende. Nebenbefund: Der
Sprung tritt nur beim **ersten** Slot-Wechsel nach frischem Laden auf;
weitere Wechsel in derselben Session springen nicht (dort bleibt der Fokus
auf dem `<input>` des Dropdowns und Delta = 0).

**Schlussfolgerung (gemäß Interpretationstabelle):** Drittursache
**bestätigt** — Layout-Shift (`stLayoutWrapper`, Shift-Werte bis 0.92 beim
Rerun) + Chrome Scroll-Anchoring ist die Ursache. H1 (Fokus-Autoscroll) ist
**widerlegt** (activeElement = `<body>`; Sprung verschwindet durch reines
CSS ohne jede Fokus-Änderung).

**Empfohlene Fix-Richtung:** `overflow-anchor: none` dauerhaft per CSS auf
dem Scroll-Container setzen (`[data-testid="stMain"]`, in `CSS_THEME`,
`src/uiLayout/gameHeader.py`) — die Probe zeigt, dass genau das den Sprung
vollständig eliminiert (3/3, Delta 0), rein clientseitig, ohne Python-Logik.
Optional als zweiter Schritt: Höhe der sechs Slot-Dropdowns stabilisieren
(kein Umbruch bei langen Necron-Namen), um den zugrundeliegenden
Layout-Shift selbst zu reduzieren.

**Fix umgesetzt (S136, Stakeholder-Freigabe):**
`section[data-testid="stMain"] { overflow-anchor: none; }` in `CSS_THEME`
(`src/uiLayout/gameHeader.py`, direkt unter den stMain-Hintergrund-Regeln).
Verifikation nach App-Neustart mit demselben Playwright-Ablauf, diesmal
**ohne** Console-Injektion: computed `overflow-anchor` auf stMain = `none`,
scrollTop-Delta beim ersten Slot-Wechsel nach frischem Laden = **0 / 0 / 0**
(3 Durchläufe, Screenshots `verify_iter{1-3}_{before,after}.png` im
Session-Scratchpad). Keine Tests referenzieren `CSS_THEME`/gameHeader
(grep über `tests/` leer). Der optionale zweite Schritt (Dropdown-Höhen)
bleibt offen, ist für B1 aber nicht mehr nötig.

## Entscheidung erbeten

1. Ergebnis Schritt 4 (activeElement), 2. Ergebnis Schritt 5 (`__clsLog`
   leer/nicht leer), 3. Ergebnis Schritt 8 (Ja/Nein) — danach Fix-Auftrag
   gemäß Interpretationstabelle planen (eigener Executor-Auftrag, S137).

   Ich finde das auf diese Weise sehr schwer zu testen. Kannst du das nicht in dem Browser hier in VS Code prüfen?

   > **Antwort (S136):** Erledigt — die Probe wurde automatisiert per
   > Playwright/Chromium durchgeführt (beide Stufen, je 3 Durchläufe, mit
   > Screenshots als Beleg). Keine manuelle DevTools-Arbeit mehr nötig.
   > Ergebnis + Fix-Empfehlung stehen oben unter
   > „Automatisierter Befund (Playwright, S136)".
