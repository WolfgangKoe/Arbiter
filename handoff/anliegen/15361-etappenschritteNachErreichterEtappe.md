# Nach einer erreichten Etappe fehlen Ausformulieren und Freigabe der nächsten

Form: Kritik
Von: Fachkritiker
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Die Regel behindert die Fachlichkeit. Der [Fortschritt](../../prozess/ablauf/fortschritt.md)
legt die Zeilen „Planer: Etappe · Architekt: Kritik an der Etappe · Stakeholder: Freigabe
Etappe“ nur „ohne Etappe“ an. `aktuelleEtappe` in
[phasenfolge.py](../../prozess/pruefungen/standregeln/phasenfolge.py) nimmt aber die erste
Datei unter `domaene/etappen/`, egal ob sie ausformuliert ist. Erreicht ist jetzt Etappe 2
(Review 10). Löscht der Planer sie, gilt sofort
[Etappe 3](../../domaene/etappen/03-angriffUndFallBack.md) als aktuell. Die ist nur ein
Entwurf aus der Neuordnung (684791f): ohne `Zweck:`, ohne `Erreicht, wenn:`
([Domäne](../../domaene/CLAUDE.md), Zeile 6), ohne „Freigabe Etappe 3“. Domänenphase 1 bis 3
liefen dann nie. Der Anforderungsautor schriebe die Happy Paths zu Plan 11 gegen ein Ziel,
das der Stakeholder nicht freigegeben hat. Für Review 10 steht der Befund in
Anliegen 15360, Punkt 5. Hier geht es um den
Mechanismus.

Wartend, weil das Review nicht davon abhängt. Die Prozessphase 10 liegt vor der
Domänenphase 11, das reicht.

**Kosten.** Ein Kriterium im Skript und ein Satz im Fortschritt. Ohne die Änderung beginnt
jede neue Etappe ohne Ausformulierung und Freigabe, nicht nur Etappe 3.

**Gegenvorschlag.** Bestehende Regel anpassen ([Ich 4](../../prozess/praemissen/ich.md)):
„Domäne 1 bis 3, nur ohne Etappe“ wird zu „…, solange die aktuelle Etappe kein
`Erreicht, wenn:` hat oder kein Commit `Freigabe Etappe <n>` sie freigibt“. Dazu im
Fortschritt nach dem Review eine Zeile „Planer: Etappe <n> erreicht, Datei gelöscht“, wenn
das Review die Etappe für erreicht erklärt (Vorbild 3300).

**Stellungnahme.** Umgesetzt als P5 der [Retro 10](../retro.md), Commit „P5: Etappenzeilen
im Fortschritt …“: Die drei Zeilen stehen in der Domänenphase, solange die aktuelle Etappe
kein `Erreicht, wenn:` hat oder kein Commit `Freigabe Etappe <n>` sie freigibt
([Fortschritt](../../prozess/ablauf/fortschritt.md), erste Zeile der Tabelle;
[Standregeln](../../prozess/regeln/standregeln.md), Mechanismus `etappenzeilen`). Die Zeile
„Planer: Etappe <n> erreicht, Datei gelöscht“ entfällt: Die Regel besteht schon (Ich 4), das
Review nennt die erreichten Etappen ([Technikphase](../../prozess/ablauf/technikphase.md) 6),
Erreichtes wird gelöscht ([Domäne](../../domaene/CLAUDE.md)); bleibt das aus, nennt der Stand
die alte Etappe (Anliegen 16400).
