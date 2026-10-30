# Voller Mutationslauf einmal je Etappe?

Form: Fragen
Von: Organisationsentwickler
An: Stakeholder
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Dein Vorschlag, über den Koordinator: Der volle Mutationslauf (`--voll`) läuft
nicht mehr in jedem Zyklus nach der DoD über das Inkrement ([DoD](../../prozess/ablauf/dod.md),
Zeilen 30 bis 36, Anliegen 6960 F1), sondern einmal zum Abschluss jeder Etappe, parallel und
möglichst früh gestartet. Die Schwelle der DoD hängt nicht daran: Sie misst der gezielte Lauf
über die geänderten Zeilen der Domänenmodule, weiter in jedem Zyklus. Nur der volle prüft
`web/` und Zeilen, deren Tests sich geändert haben.
Dauer: Zyklus 8 mit einem Kern gut drei Stunden (Start 19:32, Commit „Voller Mutationslauf 8
ausgewertet …“ um 22:58). Mit 8 Kernen gut anderthalb Stunden, alle Module samt `web/`,
21 Überlebende, einer in `web/` (dokumentiert vom Reviewer); die Zeilen der Ausgabe:
```
Start 22:19:11 Stand 1cafd47
628 Mutanten, 96 % gefangen, Schwelle 95 %, 23 gleichwertig begründet, nicht gezählt
Ende 23:56:57, Dauer 5866 s, exit 0
```
Probe aus Anliegen 8122 (Commit
„Mutationslauf parallel auf allen Kernen (Anliegen 8122)“): ein Modul, 1129 s mit 1 Kern,
667 s mit 8 Kernen. Last während der Messung: 5,7 von 8 Kernen (`uptime`, 22:30); mit einem
Kern waren es 0,6 (Anliegen 6960, Klärung).

**Kosten.** Am Bildschirm: nichts. Im Code: Lücken in `web/` und Tests, die schwächer
wurden, fallen erst am Ende der Etappe auf statt im nächsten Zyklus, gesammelt und weiter weg
vom Code, der sie hat; das Nachbessern kostet dann mehr. Für unsere Arbeit: Der Lauf belegt
jetzt fast alle Kerne; in den übrigen Zyklen laufen Tests und Bildschirmtests daneben
ungebremst, kein Neustart, wenn sich `technik/` spät ändert, weniger Lücken-Anliegen je
Retro. Zeit: gut anderthalb Stunden im Zyklus, der die Etappe abschließt, je Neustart noch
einmal so viel; sonst keine. Token: weniger, je Etappe einmal Lücken auswerten (diesmal 21)
statt je Zyklus; der Lauf selbst kostet keine. Probleme 5 bis 7 im [Rundgang](../review.md#rundgang-prüfcode) bleiben: 5
trifft vor allem den gezielten Lauf, der weiter jeden Zyklus läuft; 7 trifft jeden Neustart.
Folge für Zyklus 10: keine, er schließt Etappe 2 ab ([8880](8880-etappe2MitZyklus10Abschliessen.md)),
der volle Lauf käme dort ohnehin. Bestehende Regel, angepasst ([Ich 4](../../prozess/praemissen/ich.md)):
DoD Zeilen 30 bis 33 und die Zeile `--voll` in den [Mutationsregeln](../../prozess/regeln/mutationsregeln.md);
[Prozessphase](../../prozess/ablauf/prozessphase.md) 1 (Lücken an den Reviewer) bleibt.
Mechanismus: nur Text, der Koordinator startet ihn. Keine Änderung an Einstellungen, Hooks
oder Prüfungen, darum keine Probe. Rückweg: die alten Zeilen der DoD aus git.

**Gegenvorschlag.** A aus F1; die DoD ändere ich erst nach deiner Antwort, in der
Prozessphase 9 nach `Freigabe Retro 9`.

**Stellungnahme.**

**F1 · Wann läuft der volle Mutationslauf?**
A: Nur im Zyklus, dessen Plan die Etappe abschließen soll, gestartet nach der DoD über das
Inkrement; ändert sich `technik/` danach, startet der Koordinator ihn neu; erreicht der
Zyklus die Etappe nicht, läuft er im nächsten wieder (dein Vorschlag, Startpunkt aus Anliegen
6960 F1). Nachteil: Lücken fallen spät auf.
B: Wie A, aber schon ab der Abnahme des letzten Items der Etappe (Technikphase 5), vor dem
Aufräumen (8880, Klärung). Früher, doch das Aufräumen ändert `technik/`: Der Merkzettel gilt
nur beim gleichen Stand, der Lauf beginnt dann von vorn (Mutationsregeln).
C: Wie bisher in jedem Zyklus (DoD, Anliegen 6960). Lücken früh, Kerne in jeder Technikphase
belegt.
Empfehlung: A, die Messung bestätigt sie. Der gezielte Lauf hält die Schwelle in jedem Zyklus; B gewinnt nur Zeit, wenn
nach der Abnahme nichts mehr an `technik/` geschieht.
Antwort: A
