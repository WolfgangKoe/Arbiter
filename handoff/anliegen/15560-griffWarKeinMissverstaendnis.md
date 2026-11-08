# Retro 10: Beim Griff hast du es nicht anders gemeint

Form: Kritik
Von: Fachkritiker
An: Organisationsentwickler
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Unter „Was nicht geklappt hat“ 1 steht für beide Items: „gebaut, wie Plan und Kriterium es sagen, du meintest es anders“. Für den *Griff* stimmt das nicht. Der Ablauf war so:
- In 851 fasste der Anforderungsautor [QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigesSpielfeld.md) auf meinen Befund hin so, dass es „für alles“ gilt, was neben dem *Spielfeld* zu sehen beginnt oder aufhört.
- In der Technikphase 10 kam die Ausnahme für den *Griff* dazu, aus einer Kritik des Architekten (13980, Commit 3c78499 „ruhigeKarte vorbereitet“). Der Grund: Nach [O4](../../technik/architektur/frontend.md) nimmt eine ausgefahrene *Leiste* dem *Spielfeld* Platz. Der Anforderungsautor nahm das an, ohne dich zu fragen („O4 bleibt“).
- In ArbiterMap liegen die *Leisten* über dem *Spielfeld*, es bleibt stehen (`ArbiterMap/frontend/templates/map.html:118`). Die Ausnahme weicht also von ArbiterMap ab, und zwar wegen einer Regel der Architektur. Genau diesen Fall soll nach [DoR 6](../../prozess/ablauf/dor.md) der Stakeholder als Frage entscheiden.

Die Ursache war also kein Missverständnis von dir. Die Bedienung wurde nach dem Fachkritiker in Domänenphase 5 geändert, und niemand hat dich gefragt. Auch ich habe es bei der Kritik an den Tests (Technikphase 2) übersehen.

P1 behebt diese Ursache nicht. P1 wirkt nur, wenn eine Geste einer gebauten gleicht oder ein Kriterium sagt, was beim Ziehen geschieht. Der *Griff* ist ein Klick, und die Ausnahme ist erst nach der Freigabe Plan entstanden; ein Mockup hätte sie vor der Freigabe nicht gezeigt. Außerdem verweist P1 auf 15460. Diese Datei ist gelöscht, die Einzelheiten fehlen also.

Einordnung: hält auf. Plan 11 baut genau diese beiden Stellen neu (15100, 15461). Wartet die Lücke auf Prozessphase 11, kann in Technikphase 11 wieder eine Kritik das Kriterium an eine Regel der Architektur anpassen, ohne dass du gefragt wirst, und Etappe 2 fehlt ein drittes Mal.

**Kosten.** Bleibt der Satz in der Retro stehen, liest du deinen Kommentar aus 15460 („fällt es mir doch immer etwas schwer, die Details aus den Texten richtig zu verstehen“) bestätigt, obwohl in diesem Fall der Ablauf an dir vorbeiging. Die Korrektur kostet einen Satz in der Retro und einen Satz im Ablauf. Danach braucht jede Änderung eines Kriteriums in der Technikphase einen kurzen Lauf des Fachkritikers; in Zyklus 10 waren das etwa die vier Kriterien aus Commit 3c78499.

**Gegenvorschlag.** Diese Regeln gibt es schon, sie lassen sich anpassen ([Ich 4](../../prozess/praemissen/ich.md)): DoR 6 erfasst den Fall bereits. Es fehlt nur der Weg zurück zum Fachkritiker, wenn sich ein Kriterium nach der Freigabe Plan ändert. Die Tabelle in [Kritik](../../prozess/ablauf/kritik.md) kennt Anforderungen nur in Domänenphase 5 und 7.
1. In der Retro „Was nicht geklappt hat“ 1 aufteilen. Beim Übergehen hast du es anders gemeint. Beim *Griff* hat eine Kritik in der Technikphase das Kriterium an O4 angepasst, gegen ArbiterMap und ohne Frage an dich.
2. P1 um einen Satz erweitern, etwa in [Technikphase](../../prozess/ablauf/technikphase.md), Schritt 2: „Ändert sich in der Technikphase ein Kriterium, prüft es der Fachkritiker nach DoR 6, bevor es getestet wird; weicht die Bedienung von ArbiterMap oder Arbiter-old ab, fragt der Anforderungsautor den Stakeholder.“ Mechanismus: nur Text.
3. Die Einzelheiten zu P1 in einem Anliegen, das noch besteht, statt in 15460.

Erledigt, wenn Retro und P1 beide Ursachen nennen.

**Stellungnahme.**
Angenommen, in der [Retro 10](../retro.md): „Was nicht geklappt hat“ 1 trennt beide Ursachen. P1 nimmt deinen Satz in DoR 6 auf statt in Technikphase Schritt 2: DoR 6 nennt schon, wo der Fachkritiker prüft (Ich 4), und Schritt 2 erfasst eine Änderung aus einer Kritik am Code nicht. P1 steht für sich, ohne 15460.
