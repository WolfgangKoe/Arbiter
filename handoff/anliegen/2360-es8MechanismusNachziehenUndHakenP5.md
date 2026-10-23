# Es 8 nennt den Mechanismus der Kommentare noch nicht, Haken P5 fehlt

Form: Auftrag
Von: Regelumsetzer
An: Organisationsentwickler
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** P5 (Retro 6, Anliegen 1660, 1860) ist gebaut und grün: [Regeln, Formregeln](../../prozess/regeln.md#formregeln),
`formregeln/kommentare.py`, `formregeln/technikphase.py`, `frontendregeln/eslintKommentare.mjs`.
Zwei Dinge liegen nicht in meinen Schreibpfaden:
1. [Es 8](../../prozess/praemissen/es.md) sagt am Ende „Mechanismus: nur Text, bis Retro 6, P5
   `formregeln/kommentare.py` umbaut“. Neu: „Mechanismus: `formregeln/kommentare.py`,
   `frontendregeln/eslintKommentare.mjs`; unter `technik/` rot ab Technikphase 7.“
2. Der Haken „Regelumsetzer: P5“ in [Retro](../retro.md) steht offen; `standregeln/abhaken.py` findet
   die Zeile nicht, weil die laufende Phase die Domänenphase ist (Plan 7 wartet auf Freigabe).

**Kosten.** Es 8 verweist auf einen Umbau, der schon geschehen ist; das Anliegen 1660 bleibt offen.

**Gegenvorschlag.** Organisationsentwickler ändert Es 8 in der Prozessphase; der Koordinator
hakt P5 in der Retro. Technikphase 7: Implementierer und Testautor entfernen die Kommentare
unter `technik/` (32 `# Regel:`, 7 `// Regel:`, Tests eingeschlossen), sonst ist die DoD rot.

**Stellungnahme.**
Teil 1 wartet auf die Prozessphase: Prämissen ändern sich nur dort und erst nach
`Freigabe Retro <n>` ([Ablauf, Prozessphase](../../prozess/ablauf.md#prozessphase)); jetzt
läuft Technikphase 7. Die Retro 7 beschreibt die Änderung; nach ihrer Freigabe endet Es 8 mit
„Mechanismus: `formregeln/kommentare.py`, `frontendregeln/eslintKommentare.mjs`“. Den Zusatz
„rot ab Technikphase 7“ lasse ich weg: Technikphase 7 läuft, er wäre Historie ([Wir 4](../../prozess/praemissen/wir.md));
die Schwelle steht in den [Regeln](../../prozess/regeln.md#formregeln). Dann setze ich `angenommen`.
Teil 2 ist erledigt: Der Haken „Regelumsetzer: P5“ in der [Retro](../retro.md) ist gesetzt.
Die Kommentare unter `technik/` sind entfernt (kein `# Regel:` und `// Regel:` mehr).
Teil 1 umgesetzt mit Retro 7, P1: [Es 8](../../prozess/praemissen/es.md) endet mit
„Mechanismus: `formregeln/kommentare.py`, `frontendregeln/eslintKommentare.mjs`.“
