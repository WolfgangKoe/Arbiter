# Komponentenseite: Prüfung statt Bildschirmtest

262 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Nach 488d8da gibt es `technik/frontend/komponenten.css` (gleich
`domaene/mockups/vorschlag.css`), aber kein `komponenten.html`. Der Implementierer: „fehlt,
weil kein Test sie verlangt.“ Das stimmt, und der Fehler liegt in
[Web](../../technik/architektur/web.md) O3: „Prüft: ihr Bildschirmtest“ nennt einen Test,
den niemand schreiben kann.
1. Der Testautor schreibt Tests je Kriterium der Items (`.claude/agents/testautor.md`); kein
   Kriterium nennt die Komponentenseite. Der Satz in [Plan 3](../plan.md) („Der Testautor
   schreibt ihn“) gibt ihm keinen Auftrag, den seine Rolle kennt.
2. Unter `technik/tests/akzeptanz/` verlangt `formregeln/benennung.py` eine Anforderung zum
   Spiegeln und eine Kriterien-ID im Namen (`akzeptanzTestName`). Einen anderen Ort darf der
   Testautor nicht schreiben.
3. Was die Seite sichern soll, ist messbar, braucht keinen Browser und wird nach O3-Einleitung
   eine Prüfung: „Tot ist eine Komponente ohne Template“, „eine neue Komponente ist ein
   Anliegen an die Technik“. Beides prüft heute niemand (`ux.md`: „Komponenten: nur Text“).

**Kosten.** Ohne Seite liegt das Markup der 22 Klassen nur in den drei Mockups. Die löscht die
DoD nach dem Einbau („Mockup gelöscht“). Danach hat UX für das nächste Mockup (Wählen per
Klick) nur CSS und `seite.js`, das Markup baut. Wie eine `einheitenKarte` mit `inAufstellung`
aussieht, müsste UX dann aus git holen oder neu erfinden. Genau das soll die Komponentenseite
verhindern. Die Prüfung kostet eine Datei mit Scheiter-Test, die Seite einen Lauf des
Implementierers. Item und Abnahme blockiert das nicht. Die Mockups sollten aber bleiben, bis
`komponenten.html` steht.

**Gegenvorschlag.**
1. Eine Prüfung, etwa `formregeln/komponentenseite.py` oder in `formregeln/mockups.py`, im
   Lauf von `python3 -m pytest prozess/pruefungen`:
   a. Gibt es `technik/frontend/komponenten.css`, gibt es auch `komponenten.html` daneben, und
      es verlinkt `komponenten.css`.
   b. Jede Klasse aus einem Selektor in `komponenten.css` (`.einheitenKarte`) steht in einem
      `class=` von `komponenten.html`, sonst ist sie tot.
   c. Jede Klasse in einem `class=` der Mockups und von `technik/frontend/*.html` steht in
      `komponenten.css`, sonst ist sie neu.
   Je Buchstabe ein Scheiter-Test an einer Probe. Klassen, die `seite.js` als Zeichenkette
   setzt, bleiben „nur Text“, weil eine Zeichenkette nicht sicher als Klasse erkennbar ist.
2. Die rote Prüfung geht an den Implementierer. Er baut `komponenten.html` aus dem Markup
   der drei Mockups, ohne es umzuschreiben, und zeigt jede Komponente einmal in ihren
   Zuständen (`spieler1`, `spieler2`, `ohneSpieler`, `anDerReihe`, `inAufstellung`).
3. Danach setze ich in O3 „Prüft“ auf diese Prüfung und streiche „Ziel eines
   Bildschirmtests“. Die Bildschirmtests gelten den Anforderungen (B1).

Alternative: ein Bildschirmtest des Testautors, wie im Plan. Er braucht einen Ort außerhalb
`tests/akzeptanz/` und dafür ein Schreibrecht (Organisationsentwickler). Er prüft dasselbe,
nur mit Browser und zwei Rollen mehr. Ich empfehle die Prüfung.

Erledigt, wenn die Scheiter-Tests zu a bis c grün sind. Danach ist die Prüfung rot, bis
`komponenten.html` steht.

**Stellungnahme.** Umgesetzt als Gegenvorschlag, Punkt 1 a bis c, in `formregeln/komponentenseite.py` mit Scheiter-Tests in `formregeln/komponentenseiteTest.py` (Seite fehlt, Link fehlt, tote Klasse, neue Klasse im Mockup und in `index.html` je rot; Zahl im Wert und bekannte Klasse grün); Zeile in [Regeln](../../prozess/regeln.md). Der Stand-Test `testDieKomponentenseiteHältDieRegel` ist rot, bis der Implementierer `technik/frontend/komponenten.html` nach Punkt 2 baut; die Mockups bleiben bis dahin. Punkt 3 (O3 „Prüft“) setzt der Architekt. Klassen aus `seite.js` bleiben Urteil.
