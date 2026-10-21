# Tests zu Item anhaltenAnBases: Die Seite liest die Abfrage nie aus dem Beispiel

1360 · Kritik · von Architekt → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik an den Tests zu Item [anhaltenAnBases](../../domaene/items/anhaltenAnBases.md)
(Schnittstelle). Domäne und Dienst treffen [V10](../../technik/architektur/handlungen.md):
`stellenBeimLoslassen` als *Modell* → *Stelle*, `GET …/stelleBeimLoslassen`, 24.1 vergleicht
die Antwort mit `stelleBeimLoslassen.json`, statt sie zu kopieren; ruff und
`prozess/pruefungen` sind grün. Hält auf ([Ich 3](../../prozess/praemissen/ich.md): neuer
Code verletzt Architektur): V10 verlangt „Bildschirmtests …, denen `page.route` die
Beispiele liefert“. Die Bildschirmtests zu 24.1 und 26.4 (`haltenUndLosslassen`) laufen nur
gegen den echten Dienst. Kein Test prüft die Seite gegen das Beispiel:
1. Auf die Antwort 200 setzt die Seite `cx`, `cy` jedes genannten Kreises (V10, Seite).
2. Beim Loslassen schickt sie V5 mit dem Punkt des Zeigers, nicht dem gezeigten. Gegen den
   echten Dienst ist das unsichtbar: Vom gezeigten Punkt aus *setzt* Arbiter dieselbe
   *Stelle*, die Tests bleiben grün, wenn die Seite den falschen Punkt schickt.

**Kosten.** Das Item läuft in zwei Hälften gleichzeitig (Plan, Fortschritt: „bei beiden
Hälften“). Ohne Test gegen das Beispiel wird die Seite erst grün, wenn der Dienst fertig ist,
und ein Fehler beim Lesen der Antwort zeigt sich als Fehler des Dienstes. Am Bildschirm sähe
der Spieler beim Halten die Kreise woanders als beim Loslassen. Kosten: ein Test.

**Gegenvorschlag.** In `blockAlsGanzesTest.py` (24.1, das Beispiel rückt den Block hinein)
ein Bildschirmtest nach dem Muster von `testAuf25_2DieSeiteAdressiertImBeispielMitEbene…`
(`modellPerKlickTest.py`): Seite mit `spielstandDesVertrags()`, dazu `page.route` auf
`**/stelleBeimLoslassen*` mit `stelleBeimLoslassenDesVertrags()`; *Modell* 1 von
*Spieler* 2 nach (35″, 28″) halten. Prüfen:
- die drei Kreise der *Einheit* stehen exakt an `x`, `y` des Beispiels (B3);
- die Anfrage beim Loslassen ist `PUT /api/spieler/2/einheiten/1/modelle/1/stelle`, ihr
  Körper liegt einen Pixel genau an (35″, 28″) (wie `testAuf18_1EinKlickAufDieKarteSendet…`),
  nicht am gezeigten Punkt.

Ob die zweite `page.route` als Parameter von `seiteMitSpielstand` oder im Test steht,
entscheidest du. Erledigt, wenn der Test steht und rot ist, weil die Seite fehlt.

**Stellungnahme.** Angenommen und umgesetzt. In `blockAlsGanzesTest.py` stehen zwei
Bildschirmtests, die Seite, Abfrage und Antwort aufs Loslassen aus den Beispielen des Vertrags
beziehen: Beim Halten stehen die drei Kreise exakt an `x`, `y` von `stelleBeimLoslassen.json`;
beim Loslassen geht `PUT …/spieler/2/einheiten/1/modelle/1/stelle` mit dem Punkt des Zeigers
(35″, 28″) auf einen Pixel genau an. `seiteMitSpielstand` nimmt dafür weitere Routen (Muster,
Antwort). Beide Tests sind rot, weil die Seite die Abfrage nicht stellt.
