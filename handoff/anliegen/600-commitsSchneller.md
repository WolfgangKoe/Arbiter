# Schneller und seltener committen, ohne eine Prüfung aufzugeben

600 · Fragen · von Organisationsentwickler → Stakeholder · Runde 2/3 · offen

## Runde 1
**Befund.** Ein Commit wartet 7 bis 8 Minuten: Alle Prüfungen laufen zweimal (Koordinator,
dann Commit-Hook), auch wenn er nur Texte ändert. Die Abdeckung braucht 1:40, drei
SonarLint-Proben 1:05, die übrigen 599 Prüfungen 54 Sekunden.

**Kosten.** Stunden je Zyklus; Commits im Hintergrund kosteten Arbeit (Anliegen 610).

**Gegenvorschlag.** Drei Fragen, aufgegangen in Runde 2.

**Stellungnahme.**
Kommentar: Ich habe in die aktuelle Session einen Screenshot gelegt, der die Thematik ggf. nochmal erweitert und vielleicht auch tiefer legt. Bitte im Transskript nachsehen

## Runde 2
**Befund.** Dein Bild „Arbiter – Kritik“, Zahlen aus Zyklus 5 (seit Commit „Freigabe Retro 4“):
1. Ablauf nicht transparent, ständig Anliegen: 78 neue in fünf Tagen. Antwort in
   [Anliegen 630](630-jedePhaseBringtDasProduktVoran.md), F1 und F3.
2. Zu viele Commits, volle Prüfung ohne Produktcode: 109 Commits, 8 davon ändern Produktcode
   (`technik/arbiter`, `technik/frontend`); 13 sind Kritik-Commits, 7 löschen erledigte
   Anliegen. Jeder wartet auf alle Prüfungen. Antwort hier, F1 bis F3.
3. Anliegen ohne Blockade, Fokus auf der Organisation: 24 der 78 gehen an den Regelumsetzer
   oder mich oder sind Prozessfragen an dich; 2.685 Zeilen Prüfcode neu gegen 1.035 Zeilen
   Produktcode ([Review 5](../review.md), Rundgang). Antwort in 630, F1 und F2.
4. Tests trivial grün? Nein: Der Reviewer baute 18 Fehler einzeln in eine Kopie des Codes
   ein, 17 machten Tests rot; die zwei Lücken schließen 621 und 622 (Review 5). Dass das
   jeden Zyklus geschieht: 630, F4.
5. Fortschritt im Frontend: Was am Bildschirm neu geht, zeigt der Abschnitt „Am Bildschirm
   prüfen“ des Reviews. Die Schritte der Phase stehen nur im [Plan](../plan.md), Abschnitt
   „Fortschritt“; das Dashboard zeigt sie noch nicht (Anliegen 490, Teil 3). Antwort in 630, F3.

**Kosten.** Wer wartet oder Anliegen abarbeitet, baut nicht am Produkt. Nach fünf Zyklen ist
keine der sieben Etappen erreicht.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): Commit-Regel des
[Koordinators](../../.claude/agents/koordinator.md), Commit-Hooks
([Regeln](../../prozess/regeln.md#formregeln)), [Kritik am
Code](../../prozess/ablauf.md#kritik-am-code). Jede Prüfung bleibt; den Bau beschreibt 601.

**F1 · Prüft nur noch der Commit-Hook?**
A: Ja. Der Koordinator prüft nicht vorher selbst; ist eine Prüfung rot, scheitert der Commit,
er meldet es. B: Nein, weiter doppelt.
Empfehlung: A. Halbiert das Warten; nach 610 lässt ein gescheiterter Commit alles stehen.
Antwort: .

**F2 · Prüft der Hook nur, was der Commit ändern kann?**
A: Ja. Ein Commit nur mit Texten prüft Form und Stand, unter einer Minute; die Abdeckung
läuft nur bei Produktcode, die Proben nur bei Prüfcode; der doppelte Hook „Benennung“
entfällt. B: Nein, immer alles.
Empfehlung: A. Was ein Commit nicht ändert, kann er nicht rot machen. Alles prüfen weiter der
Regelumsetzer, bevor er fertig meldet, und der Reviewer bei der DoD.
Antwort: .

**F3 · Weniger Commits?**
A: Ja. Ein Kritiklauf bekommt keinen eigenen Commit mehr, seine Anliegen gehen mit dem
nächsten; gelöschte erledigte Anliegen ebenso; Läufe nur mit Texten, die zusammen enden,
gehen in einen Commit. Jeder Lauf mit Produktcode bleibt ein Commit, die Kritik prüft ihn.
B: Nein.
Empfehlung: A. Zyklus 5 hätte mindestens 20 Commits weniger gehabt.
Antwort: .

Parallele Prüfungen (Runde 1, F3) stelle ich zurück: Nach F2 wartet ein Commit nur mit Texten
unter einer Minute.

**Stellungnahme.**
