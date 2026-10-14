# Markierter Text sperrt das Ziehen einer Einheit

680 · Kritik · von Fachkritiker → Implementierer · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder kann keine *Einheit* aufstellen: „Necron Warriors“ (Spieler 2,
*an der Reihe*) geht nicht aus der *Ablage* auf die rote Zone. Eingegrenzt:
- Startweg, Stand: Sein Arbiter läuft mit `.venv/bin/arbiter` aus der Wurzel; die
  ausgelieferten `seite.js`, `komponenten.css`, `index.html` gleichen dem Repo, und sein Brave
  hat genau diese `seite.js` geladen (Cache, 19:55:58). Am Server ist kein *Modell* *gesetzt*.
- Server: Dieselben Anfragen von Hand (Warboss auswählen, dann Necron Warriors loslassen):
  200, zehn Kreise.
- Browser: Sein Brave 1.97 (Flatpak, Chromium 155) mit eigenem Profil, mit und ohne Fenster,
  und Playwright-Chromium 148 der Bildschirmtests: Auf frischer Seite gelingt der Zug mit der
  Maus jedes Mal, auch nach einem Klick auf „Warboss“. So ist auch der Lauf aus
  [660](660-klickpfadZeigtNichtAllesNeue.md) erklärbar.
- Gerät: Funkmaus und Touchpad, kein Touchscreen.

Nachgestellt, in seinem Brave mit Fenster: Wer 4 px unter „Necron Warriors“ ansetzt (Lücke
zwischen den Karten) und zur Karte zieht, trifft keine `.einheitenKarte`; der Browser markiert
stattdessen Text: „Aufstellen der Einheit beenden / Spieler 2 / Necron Warriors / 10“. Nichts
zeichnet neu, die Markierung bleibt. Der nächste, richtige Zug auf der Karte „Necron Warriors“
greift den markierten Text: Der Browser beginnt sein eigenes Ziehen (`dragstart`, dann
`pointercancel`), `ziehenAbbrechen` legt die Karte zurück, keine Anfrage, keine Meldung, null
Kreise. Das wiederholt sich bei jedem Versuch, bis ein Klick auf eine Karte neu zeichnet.
Ursache in [seite.js](../../technik/frontend/seite.js): Ablage und Karten lassen Text
markieren, und `ziehenBeginnen` verhindert weder Markieren noch das Ziehen des Browsers.
[V8](../../technik/architektur/handlungen.md) sagt dazu nichts.

Nicht gesehen habe ich seine Handgriffe. Die zweite Erklärung ist ein Tippen aufs Touchpad
statt Halten und Ziehen: Das ist ein Klick und markiert nur (AUF-5.3), wie bei „Warboss“; sie
geht an UX ([681](681-zeigenWasDerSpielerTunKann.md)). Prüfstein für ihn: Folgt dem Zeiger ein
blasses Textbild statt der Karte, ist es dieser Fehler.

**Kosten.** Das Ziehen ist der einzige Weg zu *setzen* (AUF-8.5, [Ziel](../../domaene/ziel.md):
Abstände zieht man auf der *Karte*). Einmal knapp daneben, und es geht scheinbar gar nicht
mehr, ohne *Grund*; der Stakeholder blieb vor dem ersten Schritt stehen und kann Review 5 nicht
prüfen. Am Touchpad und in der Hektik einer Partie trifft man die 8 px Lücke leicht.

**Gegenvorschlag.** Ablage und Karten sind keine Lesetexte: Markieren dort abschalten
(`user-select: none` an `.armeeKarte`) und in `ziehenBeginnen` das Standardverhalten des
Browsers verhindern, sobald eine `.einheitenKarte` oder ein `.modell` gegriffen ist; welches von
beiden reicht, entscheidest du. Absichern mit einem Test, der genau diese Folge zieht (erst aus
der Lücke, dann auf der Karte), mit rohen Mausereignissen, denn Playwrights Ziehen auf frischer
Seite sieht den Fehler nicht. Falls V8 das festhalten soll: Anliegen an den Architekten.
Erledigt, wenn die Folge in Brave am laufenden Arbiter zehn Kreise setzt.

**Stellungnahme.**
