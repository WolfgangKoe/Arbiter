# Lesbarkeit von d20da0b: Indizes und doppelte Bedingung, Docstrings im Bestand

92 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
Gegenstand: d20da0b und der Bestand in `prozess/pruefungen/`, um den 86 ein Urteil bat.
Korrektheit: [91](91-kritikAmCodeZuD20da0b.md).

**Befund.**
1. [`rueckverfolgung.py`](../../prozess/pruefungen/rueckverfolgung.py), `zuordnungen` und
   `anforderungsVerstöße`: `anforderungen[1:]`, `nummer == 0` und `zugeordnet[1:]` greifen
   per Index auf Fachobjekte zu ([`wir.md`](../../prozess/praemissen/wir.md), Punkt 6).
   Die Frage, ob ein Plan eine spätere Anforderung umfasst, steht zweimal: in `zuordnungen`
   als `spätereUmfasst` und in `anforderungsVerstöße` als eigene Bedingung mit
   `len(zugeordnet) > 1` und `sammeldatei.is_file()`. Dazu steckt ein bedingter Ausdruck
   mit `or` mitten im Konstruktor der `Zuordnung`.
2. Ebenda: `# Regel: Die Sammeldatei gilt der ersten Anforderung, bis ein Plan eine spätere
   umfasst.` Der Kommentar gibt die Regel wieder, statt auf ihre Fundstelle zu zeigen
   (`wir.md`, Punkt 8: `# Regel: <Fundstelle>`).
3. Bestand, Urteil zu 86: Mehrzeilige Docstrings haben 13 Module, nämlich `anliegen.py`
   (`antwortVerstöße`, `wartetAuf`), `anliegennummer.py`, `bashPositivliste.py`,
   `belegung.py`, `benennung.py`, `einstellungen.py`, `kennzahlen.py`, `lesegrenze.py`,
   `rollenkontext.py`, `rollenzaehler.py`, `schlussantwort.py`, `schreibgrenze.py` und
   `statusrecht.py`. Einen Prozessverweis tragen `anliegennummer.py` („Anliegen 42“),
   `belegung.py` („Anliegen 22“) und `benennung.py` („Anliegen 28“). Freie Kommentare ohne
   `Regel:` oder `Warum:` stehen in `benennung.py:34` und `bashPositivliste.py:59`.

**Kosten.** Zu 1: Wer „teilen“ ändert, muss zwei Stellen gleich halten. Laufen sie
auseinander, meldet der Stand „wartet“, während der Prüflauf schon rot ist, oder umgekehrt.
Zu 2: Ändert sich die Regel in T1 ([93](93-t1SammeldateiNachD20da0b.md)), veraltet der
Kommentar unbemerkt. Zu 3: Hier gelten dieselben Kosten wie in 86. Punkt 8 gilt für jeden
Code, nicht nur für geänderte Zeilen. Wer das nächste Skript schreibt, nimmt sich den Bestand
als Vorbild.

**Gegenvorschlag.**
1. `erste, *spätere = anforderungen`. Eine Funktion `sammeldateiGilt(…)` beantwortet die
   Frage, und beide Stellen rufen sie. Oder „teilen“ wird aus den Zuordnungen abgeleitet:
   Die Sammeldatei liegt vor, aber keine `Zuordnung` zeigt auf sie. Die Wahl der Testdatei
   bekommt eine eigene Funktion.
2. `# Regel: Architektur T1`, sobald 93 geklärt ist.
3. Docstrings einzeilig, Prozessverweise und freie Kommentare streichen oder als `# Warum:`
   fassen. Vor dem Streichen prüfen, ob die Aussage in `regeln.md` oder `ablauf.md` steht.
   Fehlt sie dort, kommt sie als Anliegen an den Organisationsentwickler.

**Stellungnahme.** Umgesetzt: 1 `erste, *spätere`, `sammeldateiGilt` als einzige Stelle der Frage; 2 `# Regel: Architektur T1` (T1 ist nach 93 angepasst); 3 alle Docstrings einzeilig, Prozessverweise gestrichen, die zwei freien Kommentare als `# Warum:`. Gestrichene Aussagen stehen in `regeln.md`, `ablauf.md` oder sind Historie in git.
