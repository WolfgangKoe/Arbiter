# P1 und die Freigabe von Etappe 2 bekommen nie ihren Haken

Form: Fragen
Von: Organisationsentwickler
An: Stakeholder
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Zwei Schritte bleiben offen, obwohl die Arbeit getan ist; beide halten den
Zyklus auf.
1. P1: Der Stand nennt „Organisationsentwickler: Prozess-Item P1 aus Retro 10“ als nächsten
   Schritt, obwohl P1 umgesetzt ist (Commit 760a2c6 „DoR 7 und P1: …“). Gezählt wird nur ein
   Betreff, der mit `P1:` beginnt ([Prozessphase 5](../../prozess/ablauf/prozessphase.md)).
   Den Betreff umzuschreiben hast du in 16360 abgelehnt. So endet die Prozessphase 10 nie.
2. Etappe 2: Seit P5 stehen in der Domänenphase „Planer: Etappe 2 · Architekt: Kritik an
   der Etappe 2 · Stakeholder: Freigabe Etappe 2“, solange kein Commit `Freigabe Etappe 2`
   besteht ([Fortschritt](../../prozess/ablauf/fortschritt.md), erste Zeile der Tabelle).
   Den gab es nie: Du hast Etappe 2 mit „.“ zu Plan 8 freigegeben (Anliegen 3300). Die Zeile
   bliebe in der Domänenphase 11 offen, bis du Etappe 2 ein zweites Mal freigibst.

Probe an einem Klon (`bash /tmp/oe16520/probe.sh /tmp/oe16520/repo "<Betreff>"`, leere
Commits): Nach „P1: …“ nennt der Stand Domänenphase 11, „Anforderungsautor, dann Planer:
Plan 11“. Nach „Freigabe Etappe 2“ sind Planer und Stakeholder abgehakt; „Architekt: Kritik
an der Etappe 2“ bleibt offen, weil die Freigabe in diese Phase fällt. Seine Kritik dazu
liegt vor (Anliegen 10200, 10201, Commit 102c588).
Bestehende Regeln (Ich 4): Ein Commit ohne Pfad geht schon, „leer für eine Freigabe“
([Commits](../../prozess/ablauf/commits.md)); der Betreff `P<k>:` aus Prozessphase 5.

**Kosten.** Je A: ein Befehl des Koordinators, Sekunden, kein Token; bei F2 hakt der
Architekt in seinem ersten Lauf der Domänenphase 11 eine Zeile ab. F1 B und F2 B: je ein Lauf
des Regelumsetzers mit Code und Test für einen einmaligen Fall. F2 C: ein Lauf des
Architekten und deine zweite Freigabe derselben Etappe.

**Gegenvorschlag.** Zwei leere Commits des Koordinators halten fest, was schon geschah;
keine Datei ändert sich. „P1: …“ kommt als letzter Commit der Prozessphase 10, wenn alle
ihre Läufe committet sind, denn danach sperrt die Schreibgrenze Änderungen an Regeln. Rückweg
vor dem Push: `git update-ref refs/heads/dev <Commit davor>`.

**Stellungnahme.**

**F1 · Wie gilt P1 als fertig?**
A: Der Koordinator committet leer „P1: DoR 7, Kriterien ohne Nachlesen verständlich (Inhalt in 760a2c6)“, als letzten Commit der Prozessphase 10 (Prozessphase 5, Commits)
B: Der Regelumsetzer lässt auch „DoR 7 und P1:“ als Commit des Items gelten, mit Test (neu)
Empfehlung: A, erprobt und ohne Code; B ändert eine Prüfung für einen einmaligen Fall.
Antwort: .

**F2 · Wie gilt Etappe 2 als freigegeben?**
A: Der Koordinator committet leer „Freigabe Etappe 2“ mit Verweis auf Freigabe Plan 8 und Anliegen 3300; der Architekt hakt „Kritik an der Etappe 2“ ab, seine Kritik liegt vor (Domänenphase 3, Commits)
B: Der Regelumsetzer zeigt die drei Zeilen nur nach einer erreichten Etappe, wenn seit der vorigen Retro eine Etappendatei gelöscht wurde; Etappe 2 bekommt keine (Retro 10 P5)
C: In der Domänenphase 11 kritisiert der Architekt Etappe 2 neu, du gibst sie noch einmal frei (Domänenphase 2 und 3)
Empfehlung: A, erprobt, hält deine Entscheidung zu Plan 8 fest; ab Etappe 3 greift P5 wie gedacht, B und C kosten einen Lauf.
Antwort: .
