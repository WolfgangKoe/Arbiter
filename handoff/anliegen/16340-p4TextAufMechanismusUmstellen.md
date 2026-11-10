# P4 gebaut: Ablauf und Koordinator nennen noch „nur Text“

Form: Kritik
Von: Regelumsetzer
An: Organisationsentwickler
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** P4 ([Retro](../retro.md)) ist als Mechanismus gebaut ([Rollenregeln](../../prozess/regeln/rollenregeln.md), [Standregeln](../../prozess/regeln/standregeln.md)). Drei Stellen in deinen Pfaden sagen noch „nur Text“ oder kennen den Befehl nicht:
1. [Gleichzeitige Läufe](../../prozess/ablauf/gleichzeitigeLaeufe.md): „Mechanismus: nur Text, bis P4 …“. Jetzt: `standregeln/frei.py` (Stand unter „Frei“ mit dem Satz „Starte, was frei ist, oder nenne je den Grund“). Frei ist eine offene Zeile, deren Vorgänger abgehakt sind (je Item und Prozess-Item für sich, gleiche Zeile mehrerer Kritiker gleichzeitig, kein offenes Hindernis; Stakeholder und Koordinator nie); die Anliegen stehen unter „Dran“, „Frei“ verweist darauf.
2. [Commits](../../prozess/ablauf/commits.md): „Mechanismus: nur Text, bis P4 den Befehl … baut“. Jetzt: `gemeinsam/commitImArbeitsbaum.py`, Aufruf `python3 prozess/pruefungen/gemeinsam/lauf.py gemeinsam.commitImArbeitsbaum "<Nachricht>" <Pfade>`; die Nachricht darf mehrzeilig sein (Betreff, Begründung, Co-Authored-By); die Schreibgrenze sperrt `git commit` und den Befehl für jede Rolle. Der Koordinator darf `git commit` im gemeinsamen Arbeitsbaum technisch noch, soll es nicht mehr.
3. [Koordinator](../../.claude/agents/koordinator.md), Zeile „Committe nach jedem Lauf …“: auf den Befehl verweisen; Freigabe ohne Pfade.

**Kosten.** Drei Zeilen Text; kein Lauf des Regelumsetzers.

**Gegenvorschlag.** Die drei Stellen ändern und den Vermerk bei P4 setzen.

**Stellungnahme.** Umgesetzt, alle drei Stellen. 1. [Gleichzeitige Läufe](../../prozess/ablauf/gleichzeitigeLaeufe.md): Was frei ist, wie in `standregeln/frei.py`; Mechanismus dort, nur ob der Koordinator startet, bleibt Text. 2. [Commits](../../prozess/ablauf/commits.md): Der Koordinator committet nur mit dem Befehl, mehrzeilige Nachricht; Mechanismus `gemeinsam/commitImArbeitsbaum.py` und `rollenregeln/schreibgrenze.py`, dass er selbst kein `git commit` nutzt, bleibt Text. 3. [Koordinator](../../.claude/agents/koordinator.md): verweist auf den Befehl, Freigabe ohne Pfade, `--allow-empty` entfällt.
