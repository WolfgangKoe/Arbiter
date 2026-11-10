# P6 abgehakt, obwohl das Dashboard noch nicht schneller lädt

Form: Fragen
Von: Organisationsentwickler
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Im Fortschritt der [Retro](../retro.md) ist „Regelumsetzer: P6“ abgehakt. P6
ist aber erst gemessen, nicht behoben ([8860](8860-dashboardLangsamUndUnuebersichtlich.md)).
Der Haken kommt vom Commit c246746 „P6: Messung, warum das Dashboard langsam lädt“: Das
Skript ([fortschritt.py](../../prozess/pruefungen/standregeln/fortschritt.py), `hatItemCommit`
in [phasenfolge.py](../../prozess/pruefungen/standregeln/phasenfolge.py)) zählt jeden Betreff,
der mit `P<k>:` beginnt, als fertiges Item. Die Regel dafür gibt es schon
([Prozessphase 5](../../prozess/ablauf/prozessphase.md)): Ein Zwischenstand heißt
`P<k> Zwischenstand: …`. Dieselbe Verwechslung noch zweimal:
- P4: Commit 4855394 „P4: …“ lieferte nur meinen Teil (Text); der Teil des Regelumsetzers
  läuft gerade. Die Zeile „Regelumsetzer: P4“ fehlt, weil das Skript je Item nur die erste
  Rolle der Klammer liest („Organisationsentwickler, dann Regelumsetzer“); von Hand
  nachgetragen löscht es sie beim nächsten Lauf wieder.
- P1: umgekehrt. Der Betreff „DoR 7 und P1: …“ beginnt nicht mit `P1:`; der Stand nennt P1
  darum als offen, obwohl es fertig ist.

Folge: Endet P5, gilt die Prozessphase nur deshalb noch nicht als beendet, weil P1 offen
scheint. Wird P1 nachgetragen, beginnt die Domänenphase 11, obwohl P4 und P6 fehlen.

**Kosten.** F1 A: ein Befehl des Koordinators, Sekunden, kein Token; die Commits sind noch
nicht gepusht. F2 B: ein kleiner Teil im Commit-Befehl, den der Regelumsetzer für P4 ohnehin
baut.

**Gegenvorschlag.** Die drei Betreffe richtigstellen, dann stimmt der Fortschritt; künftig
verhindert das der Commit-Befehl.

**Stellungnahme.**

Annahme: Bis zur Antwort ändert niemand die Betreffe; P1 bleibt so lange scheinbar offen und
hält die Phase offen.

**F1 · Wie stimmt der Haken bis zum Abschluss-Commit von P6?**
A: Der Koordinator schreibt die Betreffe um: 760a2c6 zu „P1: DoR 7, …“, 4855394 zu „P4
Zwischenstand: …“, c246746 zu „P6 Zwischenstand: …“. Danach ändere ich in der Retro die
Klammer von P4 zu „(Regelumsetzer, nach dem Organisationsentwickler)“ und setze P6 zurück;
das Skript schreibt dann `- [ ] Regelumsetzer: P4` und `- [ ] Regelumsetzer: P6`, der Commit
`P4:` oder `P6:` hakt sie ab. (Prozessphase 5, [Commits](../../prozess/ablauf/commits.md))
B: Alles bleibt; der Koordinator achtet darauf, dass die Phase nicht vor P4 und P6 endet. (neu)
Empfehlung: A, nur so zeigen Fortschritt und Stand, was wirklich fertig ist.
Antwort: .

Probe von A an einem Klon in `/tmp`: Befehl `bash /tmp/oe16360/probe.sh <Projektordner>`;
er schreibt nur die Betreffe neu (`git commit-tree`, `git update-ref` mit altem Stand), Inhalt
und Arbeitsbaum bleiben gleich, uncommittete Änderungen auch. Danach: P1 fertig, P4, P5, P6
offen, ein `P6: …` hakt P6 ab. Rückweg: `git update-ref refs/heads/dev 8f6ace2`, solange
nichts darauf committet ist. Ein Commit danach geht, erprobt ohne Commit-Hook.

**F2 · Wie wird das künftig verhindert?**
A: Nur die bestehende Regel, der Koordinator hält sie ein. (Prozessphase 5)
B: Die Rolle hakt ihr Item am Ende ab ([Befehl](../../prozess/ablauf/fortschritt.md)); der
Commit-Befehl aus P4 lehnt `P<k>:` ab, solange die Zeile offen ist, und einen Betreff, der
`P<k>:` nicht vorne nennt. (Fortschritt, Commits)
Empfehlung: B, die Regel bestand schon und wurde in einem Zyklus dreimal verfehlt; ohne Probe.
Antwort: .
Kommentar: Lassen wir es so. Das Dashboard lädt jetzt in der Tat deutlich schneller.
