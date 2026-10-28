# Voller Mutationslauf: früher starten, Fortschritt zeigen

Form: Fragen
Von: Organisationsentwickler
An: Stakeholder
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Dein Wortlaut: „Der Mutationstest muss früher starten. Mir scheint es so, dass er
mal unterbrochen wurde.“ Er lief laut `ps` seit 19:32 ohne Pause, schreibt aber erst am Ende:
`/tmp/mutationVoll8.log` bleibt bis dahin leer. Letzte Änderung am Produkt: 17:58. Regel, nur
Text: [Prozessphase](../../prozess/ablauf/prozessphase.md) 1, [DoD](../../prozess/ablauf/dod.md).

**Kosten.** Am Bildschirm: nichts. Du wartest kürzer. Wir: parallele Tests langsamer; ändert
sich `technik/` danach, startet der Lauf neu. Token: keine.

**Gegenvorschlag.** Start nach der DoD über das Inkrement
([Technikphase](../../prozess/ablauf/technikphase.md) Schritt 4), je fertigem Modul eine Zeile.

**Stellungnahme.**

**F1 · Wann startet der volle Lauf?**
A: Nach der DoD über das Inkrement; ändert sich `technik/` danach, startet der Koordinator ihn
neu (neu, Grund: [Absicht 2](../../prozess/praemissen/absicht.md), parallel arbeiten). Zyklus
8: 17:58 statt 19:32. Nachteil: parallele Tests langsamer, Neustart bei späten Änderungen.
B: Mit `Freigabe Review <n>` (Prozessphase 1): 8 Minuten früher, nichts parallel.
Empfehlung: A, Stunden Vorsprung.
Antwort: A

**F2 · Soll der Lauf unterwegs zeigen, wie weit er ist?**
A: Ja, je fertigem Modul eine Zeile: Modul, Mutanten, Überlebende (neu, Grund:
[Absicht 5](../../prozess/praemissen/absicht.md), verstehen). Arbeit: Regelumsetzer, einige
Zeilen in `mutationsregeln/mutation.py` mit Scheiter-Test. Nachteil: mehr Prüfcode. Rückweg:
Zeile streichen. Nicht an einer Kopie erprobt.
B: Nein, das Protokoll füllt sich erst am Ende (`mutation.py`).
Empfehlung: A. Ein leeres Protokoll hat dich getäuscht.
Antwort: A

**F3 · Ab wann gilt die Änderung?**
A: Jetzt, nach `Freigabe Retro 8` (Prozessphase, Auslöser): Auftrag in Retro 8, wirkt ab
Technikphase 9.
B: Über den [Backlog](../../prozess/backlog.md) (Prozessphase 1), wirkt ab Technikphase 10.
Empfehlung: A.
Antwort: A
Kommentar: Du sagst, dass Parallelisieren langsamer macht. Aber wie stark wird das System belastet? Wir hatten auch mal gesagt, dass wir die Mutationstest gezielt einsetzen. Und zwar primär dort, wo wir Code ändern. Eine Art Fortschritt und Zwischenspeicherung der Erkenntnisse wäre gut. Dann kann man vielleicht auch mal unterbrechen oder die Prüfung geschickt aufteilen. Dann weiß man, Wo es gut aussieht und findet Probleme ggf. schneller. Was meinst du?

**Klärung.** Belastung, um 22:31 am laufenden Lauf gemessen: ein Testlauf zur Zeit, mit
Browser etwa 0,6 von 8 Kernen, 0,5 von 31 GB; andere Tests verlieren wenig.
Gezielt gibt es: Ohne `--voll` prüft `mutation.py` nur die seit `Freigabe Plan` geänderten
Zeilen der Domänenmodule (Schwelle der DoD). Der volle Lauf prüft dazu `web/` und Zeilen, deren
Tests sich geändert haben können.
Zwischenspeichern: Der Merkzettel `.git/arbiter/mutation.json` gilt je Stand von `technik/`,
wird aber erst am Ende geschrieben; ein Abbruch verliert alles. Aufteilen geht
(`mutation.py <modul>:<von>-<bis>`), der volle Lauf übernimmt das beim gleichen Stand.
Regelumsetzer: nach jedem Modul merken, neben der Zeile aus F2; etwa drei Zeilen und ein
Scheiter-Test im selben Lauf. Dann setzt ein unterbrochener Lauf fort. Einen Stand je Modul
empfehle ich nicht: Ein Mutant hängt auch an Tests und anderen Modulen.

**F4 · Merkt sich der Lauf seine Ergebnisse je fertigem Modul?**
A: Ja, mit F2 (Anliegen 6960, dein Kommentar). Rückweg: streichen. Nicht an einer Kopie erprobt.
B: Nein, wie bisher am Ende (`mutation.py`).
Empfehlung: A, unterbrechen kostet dann nichts.
Antwort: .
