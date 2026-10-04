# Freigabefeld, Kommentare und Freigabe des Reviews im Stand

167 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder gibt Plan, Review und Retro künftig in der Datei frei und
kommentiert überall darin; das Review bekommt `## Nächstes Vorgehen` und eine eigene
Freigabe vor der Retro. Regeln: [Ablauf, Freigabe und
Kommentare](../../prozess/ablauf.md#freigabe-und-kommentare), Technikphase 6 und 7,
Auslöser der Prozessphase, [Kennzahlen](../../prozess/kennzahlen.md) (Höchstmaße). Alle nur
Text; Rückfragen an den Stakeholder in Anliegen 169.

**Kosten.** Ohne Mechanismus meldet der Stand nach Review 3 gleich die Prozessphase und
überspringt die neue Freigabe. Ein Kommentar ohne Stellungnahme sieht niemand; die
Nachkorrektur hängt davon ab, dass der Koordinator die Datei liest.

**Gegenvorschlag.** Je Lauf ein Teil, in dieser Reihenfolge; 1 vor Review 3, 2 vor der
Freigabe von Plan 3.
1. Freigabe des Reviews (`phasenfolge.lage`): Liegt Review n vor und fehlt Retro n, meldet
   der Stand ohne `Freigabe Review <n>` „Review n wartet auf Kritik und Freigabe“. Zyklus 2
   bleibt, wie er ist, weil Retro 2 vorliegt. Zu prüfen: `codekritik.py` und
   `beantwortetDurchFreigabe` rechnen ab `letzteFreigabe`; die neue Freigabe darf keinen
   Code-Commit ohne Kritik aus dem Fenster schieben.
2. Kommentare: Eine Zeile `Kommentar:` in `handoff/plan.md`, `review.md` oder `retro.md` mit
   anderem Text als `.` und ohne Zeile `Stellungnahme:` als nächste nicht leere Zeile: Dran
   ist der Autor (Planer, Reviewer, Organisationsentwickler), in der Zeile „Dran“ des Stands
   neben den Anliegen. Steht `Freigabe: ja` und fehlt der Commit `Freigabe <Plan|Review|Retro>
   <n>`, nennt der Stand als nächsten Schritt „Koordinator: Freigabe … committen“.
3. Format: Plan, Review und Retro ohne ihren Freigabe-Commit enden mit `## Freigabe`, darin
   genau eine Zeile `Freigabe: offen` oder `Freigabe: ja`; das Review hat davor
   `## Nächstes Vorgehen` mit den Punkten Produktziel, Etappenziel, Zyklusziel. Dateien mit
   Freigabe-Commit bleiben ungeprüft (Plan 2, Review 2).
4. Höchstmaß: Plan, Review, Retro je 4.000 in `hoechstmassTest.py`; jede Zeile `Kommentar:`
   zählt als `Kommentar: .`, mit derselben Zählfunktion wie `Antwort:` in
   Anliegen 162.

Scheiter-Tests: (1) Review 3 ohne Retro 3 und ohne Freigabe: wartet; mit `Freigabe Review 3`:
Prozessphase. (2) Kommentar ohne Stellungnahme: Autor dran; mit Stellungnahme oder
`Kommentar: .`: nicht dran; `Freigabe: ja` ohne Commit: Koordinator. (3) Review ohne
Zyklusziel rot. (4) Retro mit 3.990 Zeichen eigenem Text und 500 Zeichen Kommentar grün,
mit 4.010 Zeichen eigenem Text rot.

`prozess/regeln.md` nennt je Teil den Mechanismus; „nur Text“ im Ablauf ersetze ich.

Erledigt, wenn die vier Teile gebaut sind, die Scheiter-Tests so ausgehen,
`python3 -m pytest prozess/pruefungen` grün ist und der Reviewer den Code geprüft hat
([Kritik am Code](../../prozess/ablauf.md#kritik-am-code)).

**Stellungnahme.** Teil 1 umgesetzt (`phasenfolge.lage`, `standTest.py`, `regeln.md`).

**Stellungnahme (Teil 2).** Umgesetzt: `freigabeKommentare.py`, `stand.py`, `standTest.py`.

**Stellungnahme (Teil 3).** Umgesetzt: `freigabeFormat.py`, `freigabeFormatTest.py`, `regeln.md`. Mit 209.

**Stellungnahme (Teil 4).** Umgesetzt: `hoechstmassTest.py`, `kennzahlen.md`, `regeln.md`. Alle Teile gebaut; offen: Kritik am Code.

**Kritik am Code (Reviewer, e772442 bis 5bb18bb).** Alle vier Teile sind geprüft, die Scheiter-Tests und `pytest prozess/pruefungen` grün. Eigene Befunde: [208](208-freigabeReviewBeantwortetFragen.md), [210](210-freigabefeldNurImAbschnittLesen.md). Noch hier: Die Zeile in `regeln.md` nennt 3.990 Zeichen, der Test zählt 3.980; mit `Kommentar: .` wären 3.990 rot. Korrigieren, dann `angenommen`.

**Nachprüfung.** In Ordnung; „nur Text“ im Ablauf ersetzt, Rest trägt 168.
