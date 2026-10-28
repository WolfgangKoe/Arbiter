# Verhalten im Frontend ohne Test fängt keine Prüfung

Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 1/3
Status: offen
Wartet auf: Prozessphase 9

## Runde 1
**Befund.** Wartet ([Ich 3](../../prozess/praemissen/ich.md): keine Prüfung rot, kein Schritt
des Happy Path fehlt). Zu Befund 2 der [Retro 8](../retro.md): 6101 lag in `bedienung.js`
(Greifen am Rand, AUF-8.7). Bestehende Regeln ([Ich 4](../../prozess/praemissen/ich.md)):
[DoD](../../prozess/ablauf/dod.md) 1 misst die Abdeckung nur für `technik/arbiter`, die
Mutationsschwelle nur die Domänenmodule, der volle Lauf auch `web/`; `technik/frontend/`
misst keine. Dort fängt nur die Kritik am Code ein Verhalten ohne Test.

**Kosten.** Heute keine; 6101 fand die Kritik am Code. Wächst das Frontend (Etappe 2: Phasen,
Bewegung), hängt jeder solche Fund an meinem Lesen.

**Gegenvorschlag.** Eine Zeile im [Backlog](../../prozess/backlog.md): „Abdeckung auch für
`technik/frontend/` in DoD 1. Auslöser: wieder Verhalten im Frontend ohne Test.“ Technisches
Neuland, nicht erprobt: Wie die Bildschirmtests (Playwright, Python) die Abdeckung von
JavaScript messen, klärt vor dem Bau ein Wegwerf-Versuch in `/tmp`.

**Stellungnahme.**
