# Technikphase

Auslöser: `Freigabe Plan <n>`. Fehlen Rollen, schlägt der
Organisationsentwickler sie vor. Die Regeln der Architektur ändern sich nur in dieser
Phase; davor zieht der Architekt nur Namen und Pfade nach (Anliegen 370). Mechanismus: nur Text.
1. Testautor: Akzeptanztests je Kriterium der Items, rot. Hat ein Item beide Hälften
   (Handlung über HTTP, ihre Anzeige), legt vorher der Architekt den Vertrag fest: Pfade
   und je Antwort ein JSON-Beispiel in `technik/architektur/web.md`. Daraus testet der
   Testautor das Backend mit dem Flask-Testclient, das Frontend mit einem Bildschirmtest,
   dem Playwright das Beispiel statt des Servers liefert; derselbe Bildschirmtest gegen den
   echten Server ist der Akzeptanztest des Items (Anliegen 241). Mechanismus: nur Text.
2. Kritik an den Tests ([Kritik](kritik.md)). Ein Test, dessen Befund aufhält, geht nicht in
   die Umsetzung, bis das Anliegen geklärt ist; widerspricht der Testautor, wird es an den Anforderungsautor zum Kriterium gehoben. Der
   Rest läuft weiter. Mechanismus: nur Text.
3. Implementierer: macht die Tests grün. Refactoring nur aus einem Befund, als Anliegen an
   ihn von dem, der den Befund hat; der Gegenvorschlag nennt die Erledigt-Bedingung, dazu gilt
   „Verhalten unverändert“ (Akzeptanztests grün). Nach jedem Lauf prüfen Architekt
   (Architektur) und Reviewer (Lesbarkeit) gleichzeitig ([Kritik am Code](kritik.md#kritik-am-code)).
   Bei einer Oberfläche übernimmt er Markup und CSS des Mockups ohne Umschreiben und ersetzt nur Beispielinhalte durch Daten (Anliegen 151). Er meldet erst
   fertig, wenn alle Tests in `technik/tests` grün sind, auch die Bildschirmtests, und
   SonarLint grün ist ([DoD](dod.md) 1, 2; Retro 6, Befund 4). Mechanismus: nur Text.
   Hat das Item Vertrag und Tests beider Hälften, laufen Implementierer (Backend) und
   Frontend-Implementierer gleichzeitig ([Gleichzeitige Läufe](gleichzeitigeLaeufe.md)).
   Mechanismus: nur Text.
4. Reviewer: [DoD](dod.md) über das Inkrement, `/code-review`, Wiederverwendung, Vereinfachung,
   Effizienz, Flughöhe.
5. Fachkritiker: fachliche Abnahme gegen Kriterien und Etappe. Danach löscht der Planer
   die abgenommenen Items mit `rm` ([Ich 2](../praemissen/ich.md)). Mechanismus: nur Text.
6. Reviewer: `handoff/review.md`, erste Zeile `# Review · Zyklus <n>`, darunter der
   Startbefehl der App mit Link auf [Web, W5](../../technik/architektur/web.md#aufbau) (auf
   Wunsch des Stakeholders auch hier, Anliegen 353). Danach der Abschnitt
   `## Am Bildschirm prüfen`: ein Satz, was insgesamt per Maus oder Finger machbar ist;
   dann als nummerierter Klickpfad mit dem erwarteten Bild je Schritt nur, was in diesem
   Zyklus neu oder anders machbar ist, Schritt 1 ist der Start. Der Reviewer geht ihn am
   laufenden Arbiter durch; was nur ein Test zeigt, steht dabei (Anliegen 355, 359). Vor
   dem Abschnitt `## Freigabe` der Abschnitt `## Nächstes Vorgehen` mit drei Punkten, je
   mit Beleg:
   - Produktziel: welche Etappen erreicht sind, was dem Ziel am meisten fehlt.
   - Etappenziel: was zur aktuellen Etappe fehlt, nach der Abnahme des Fachkritikers und dem
     Abschnitt „Danach“ des Plans; in wie vielen Zyklen sie erreichbar ist.
   - Zyklusziel: Empfehlung für Plan n+1. Zuerst, was danach am Bildschirm machbar ist und
     was noch nicht, in Worten des Spielers mit den Begriffen des Glossars (Anliegen 358);
     dann die technischen Voraussetzungen und Schulden, die vorher weg müssen.
   Der Reviewer fasst zusammen und empfiehlt; der Stakeholder entscheidet mit Freigabe und
   Kommentaren, der Planer schneidet die Items. Davor der Abschnitt `## Rundgang Prüfcode`:
   Einmal je Zyklus geht der Reviewer mit dem Stakeholder durch den Prüfcode, der seit dem
   letzten Review entstanden ist (`prozess/pruefungen/`, Hooks in `.claude/settings.json`,
   Prüfkonfiguration): die Dateien und die wesentlichen Probleme, je mit Fundstelle. Der
   Stakeholder kommentiert; was er beauftragt, wird in der Nachkorrektur ein Anliegen an den
   Regelumsetzer. Mechanismus: nur Text.
7. Kritik am Review ([Kritik](kritik.md)), dann Freigabe ([Freigabe und Kommentare](freigabe.md))
   → Koordinator committet `Freigabe Review <n>`. Danach [Prozessphase](prozessphase.md).
   Mechanismus: nur Text.

Ausnahmen vom Test vor dem Code: Oberfläche (Mockup zuerst, Bildschirmtest danach),
technisches Neuland (Wegwerf-Versuch, dann Test).
