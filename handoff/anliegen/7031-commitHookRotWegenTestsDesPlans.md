# Commit-Hook rot: 17 Kriterien der Items von Plan 9 ohne Test

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 2/3
Status: angenommen
Wartet auf: 7030

## Runde 1
**Befund.** Der Hook „stand“ in `.pre-commit-config.yaml` (`pytest prozess/pruefungen -m
"stand and not abdeckung"`) ist rot. Allein
`prozess/pruefungen/kriterienregeln/rueckverfolgungTest.py` scheitert: 16 Kriterien haben
keinen Test, zuerst MIV-1.5 (`technik/tests/akzeptanz/missionsvorbereitung/ausgangslageTest.py`).
Es sind die Kriterien der Items von [Plan 9](../plan.md). Nach der [Technikphase](../../prozess/ablauf/technikphase.md)
schreibt der Testautor die Tests erst nach dem Vertrag je Item; bis dahin scheitert jeder
Commit, auch die Freigabe von Plan 9 in [review.md](../review.md) (vorgemerkt) und alle Läufe
(6102, 6241, 6290, Vertrag des Architekten). Nach den [Commits](../../prozess/ablauf/commits.md)
committet der Koordinator nur ohne laufende Rolle und prüft nicht vorher; ein roter Hook
lässt alles stehen. Ursache: Die Regel „Kriterium zu Test“ misst den Stand, den die Phase
erst herstellt.

Probe: Kopie des Repos in `/tmp/probe7031`; mit `--deselect` auf diesen einen Test läuft der
Hook-Befehl durch (die zwei übrigen Rote dort sind Kopierfolgen: kein `.git`-Hook, kein
`node_modules`). Gedacht ist C, es ist nicht erprobt. Rückweg jeder Option: `git revert` des
einen Commits, der `.pre-commit-config.yaml` oder `rueckverfolgung.py` ändert.

**Kosten.**
A, nichts ändern: keine Änderung, keine Regel gelockert. Keine Commits, bis alle 16 Tests
stehen; Freigabe und Arbeit der Rollen bleiben ungesichert, ein Fehlgriff eines Laufs
überschreibt Uncommittetes. Tokenkosten hoch.
B, den Test aus dem Hook nehmen (Marker `abdeckung`): sofort grün, kleine Änderung. Die
Rückverfolgung misst dann nur noch beim Implementierer und Reviewer; Löcher im Bestand
fallen später auf.
C, Kriterien der Items des laufenden Plans im Hook ausnehmen: `rueckverfolgung.py` liest die
Items aus dem Plan (wie `lesen/plan.py`), im Hook fehlen nur deren Tests nicht; für alles
andere bleibt der Schutz, im DoD-Lauf gilt alles. Mehr Code und ein Scheiter-Test, Folge:
Anliegen 7030 (Itemliste des Plans) muss vorher stehen.
D, `--no-verify`: verstößt gegen „Regeln gelten für alle“ ([Absicht 6](../../prozess/praemissen/absicht.md)).

**Gegenvorschlag.** C. Sie lässt den Hook als Wächter des Bestands, und die Lücke ist genau
die Phase, in der sie entsteht. Ich setze sie um, sobald 7030 erledigt ist und du antwortest;
bis dahin hilft nur B als Übergang, wenn du Commits jetzt brauchst.

**Stellungnahme.**

**F1 · Wie geht der Hook mit den fehlenden Tests der Items von Plan 9 um?**
- A: nichts ändern (Ich 2)
- B: Test aus dem Hook nehmen, nur beim Implementierer und Reviewer (neu)
- C: nur die Kriterien der Items des Plans ausnehmen, nach 7030 (neu, empfohlen)
Antwort: .
Kommentar: Ich verstehe dieses Anliegen nicht. Denke bitte an absicht.md. Ich habe wenig Ahnung von technischen Details und welche Auswirkungen dies haben mag. Bitte erläutern und die Konsequenzen meiner Entscheidungen transparent machen.

## Runde 2
**Befund.** In Worten des Spielers statt der Technik. Vor jedem Commit läuft eine
Wächterprüfung. Eine ihrer Regeln lautet: Zu jeder freigegebenen Anforderung muss ein Test
existieren. Seit der Freigabe von Plan 9 fehlen diese Tests noch, weil der Testautor sie erst
in der laufenden Technikphase schreibt. Aktuell sind es 17, zuerst
`technik/tests/akzeptanz/phasen/aufstellen/aufgestellteEinheitAuswaehlenTest.py`. Darum
scheitert jeder Commit. Die Folge für dich: 71 Dateien liegen nur auf der Festplatte,
darunter deine Freigabe von Plan 9, die Anliegen und die Arbeit der Rollen; git hat keine
Kopie davon.

**Kosten.** Am Bildschirm siehst du in keiner Option einen Unterschied; es geht um die
Sicherheit und die Qualität der Arbeit.
- A, nichts ändern. Für dich: nichts zu tun. Für die Rollen: Der Testautor schreibt die 17
  Tests ohnehin; danach geht der Commit durch, vorher keiner. Risiko: Ein Fehlgriff einer
  Rolle überschreibt Ungesichertes, ohne Rückweg. Qualität: voller Schutz, aber ohne
  Sicherung.
- B, diese eine Regel im Wächter abschalten. Für dich: Commits gehen sofort durch, nichts zu
  tun. Für die Rollen: eine kleine Änderung des Regelumsetzers. Qualität: Ein fehlender Test
  fällt nicht mehr beim Commit auf, sondern später, wenn Implementierer oder Reviewer die
  Gesamtprüfung laufen lassen. Rückweg: ein Commit zurück, dann gilt die Regel wieder.
- C, die Regel nur für die Anforderungen des laufenden Plans lockern, für alles Ältere
  bleibt sie. Für dich: nichts zu tun, aber es greift erst nach Anliegen 7030, das auf die
  Prozessphase wartet; für Plan 9 hilft C also nicht. Für die Rollen: mehr Code samt Test.
  Qualität: bester Schutz, die Lücke entsteht in keinem späteren Plan wieder.
- `--no-verify` (Prüfung umgehen) biete ich nicht an: Regeln gelten für alle (Absicht 6).

**Gegenvorschlag.** Zwei Fragen statt einer: F1 sichert jetzt, F2 entscheidet, ob die Lücke
bei jedem künftigen Plan wiederkehren darf. Empfehlung: B jetzt, C danach. B beendet den
Zustand ohne Sicherung, den ich für das größere Risiko halte; C macht B überflüssig, und ich
nehme B dann zurück.

**Stellungnahme.**

**F1 · Soll der Wächter die fehlenden Tests der Items von Plan 9 jetzt übergehen, damit
Commits wieder gelingen?**
- A: nein, warten, bis der Testautor alle 17 geschrieben hat (Ich 2)
- B: ja, die Regel bis dahin abschalten (neu, empfohlen)
Antwort: C

**F2 · Soll ich die Regel dauerhaft so ändern, dass sie die Anforderungen des laufenden
Plans nicht prüft (Änderung C)?**
- Ja: ändern, nach 7030, B wird dann zurückgenommen (neu, empfohlen)
- Nein: Regel bleibt wie sie ist, die Lücke kehrt bei jedem Plan wieder (Ich 2)
Antwort: Ja

**Klärung.** Nachprüfung: Noch nicht erledigt. Der Hook ist rot, 6 Tests fehlen noch (zuerst
`technik/tests/akzeptanz/phasen/bewegung/grenzkreiseTest.py`, der Testautor schreibt ihn
gerade). Dein „C“ bei F1 gab es dort nicht; ich lese es mit F2 „Ja“ als Wunsch nach C. C
braucht 7030, das auf die Prozessphase 9 wartet; bis dahin ändere ich keinen Hook-Code, die
Commits bleiben bis dahin gesperrt. Dann setze ich C um und prüfe erneut.
