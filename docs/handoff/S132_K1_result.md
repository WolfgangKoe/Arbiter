STATUS: NEEDS-DECISION

# S132 K1 — Blocker: Freigabe-Gate-Marker fehlt

Auftrag K1 (GO-Karten-Anatomie designtreu machen, Befund 1 / Fix-Option A) konnte
**nicht umgesetzt werden**: Der erste `Edit`-Aufruf auf `src/uiLayout/go_card.py`
wurde vom PreToolUse-Hook `tools/freigabe_gate.py` mit folgender Meldung blockiert:

```
🔒 Freigabe-Gate aktiv: kein freigegebener Plan. Zeige dem Stakeholder Plan +
betroffene Dateien und warte auf Freigabe. Freigabe erfolgt physisch mit
`touch .claude/.freigabe` (re-armt automatisch bei Session-Start). NICHT
selbst den Marker setzen.
```

Geprüft: `.claude/.freigabe` existiert im Repo nicht (`ls` bestätigt
„Datei oder Verzeichnis nicht gefunden"). Der Hook ist ein harter,
werkzeug-erzwungener Gate — unabhängig davon, dass der Auftrag im Prompt
„Freigabe des Stakeholders liegt vor" behauptet, verlangt der Hook den
**physischen** Marker (`touch .claude/.freigabe`), gesetzt vom Stakeholder
selbst bzw. vom Koordinator nach eingeholter Zustimmung — laut Hook-Doku
ausdrücklich NICHT vom Subagenten.

**Kein Code wurde geändert.** Der geplante Fix (Option A, unverändert gültig)
lautet:

1. `src/uiLayout/go_card.py::go_card_html()`: `action_html`-Span (Z. 113–117)
   ersatzlos streichen, `action_html` nicht mehr in `f"<div>{header_html}{action_html}</div>"`
   einsetzen (nur noch `header_html`), die dadurch verwaiste Variable `action_color`
   ebenfalls entfernen.
2. `src/uiLayout/_common.py::render_go_card()`: `st.columns([5, 2])` einführen —
   linke Spalte `st.markdown(go_card_html(...), unsafe_allow_html=True)` (volle
   Karten-HTML inkl. Zustandsrahmen, Chips bleiben wie bisher Teil derselben
   HTML-Box), rechte Spalte der echte `st.button(...)` (aktuelle Button-Logik
   unverändert, nur in die rechte Spalte verschoben statt darunter). Akkordeon
   (`st.expander`) bleibt wie bisher unterhalb der Spalten-Zeile, volle Breite.
   Zustandsrahmen bleibt über die bestehende HTML-`<div>`-Lösung, kein Wechsel
   auf `st.container(border=True)`.
3. `tests/uiLayout/test_go_card.py`: Assertions, die die entfernte
   `action_html`-Attrappe erwarten, entfernen/anpassen (Sichtprüfung des
   aktuellen Tests zeigt: keine Assertion prüft `float:right`/Attrappen-spezifische
   Marker direkt — die Action-Text-Assertions wie `"Use (1 CP)" in html` bleiben
   gültig, da der Text weiterhin im Header via `action_slot_text()` mitgeprüft
   wird; ggf. Docstring-Kommentar am Modulkopf nachziehen, falls er die
   Attrappe erwähnt).

**Nächster Schritt:** Stakeholder/Koordinator setzt `touch .claude/.freigabe`
nach (erneuter) Freigabe, dann kann derselbe oder ein neuer Executor-Lauf K1
unverändert nach obigem Plan umsetzen. Kein Vollsuite-/mypy-Lauf durchgeführt,
da keine Codeänderung vorliegt, die geprüft werden müsste.
