# Der Ordner querschnitt ist schwer lesbar

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase

## Runde 1
**Befund.** Der Stakeholder schreibt in [15900](15900-bewegenAlsOberklasse.md) (Kommentar
unter Runde 2): „Ziehe für die Domänenphase in Erwägung, den Ordner ‚Querschnitt‘
umzubenennen … Fachlich ist es aber schwer lesbar … Der Code muss lesbar sein!“
Der Name gehört dir: `technik/arbiter/domaene/` spiegelt `domaene/anforderungen/`
([Domäne](../../technik/architektur/domaene.md), Prüfung `formregeln/spiegel.py`); der Code
folgt erst, wenn der Ordner der Anforderungen umbenannt ist ([Wir 2](../../prozess/praemissen/wir.md)).
„Querschnitt“ sagt, wie der Ordner zu den Phasen liegt, nicht was darin steht. Darin stehen
zwei Arten:
- Regeln aus den Grundregeln, die in jeder Phase gelten: *Kohärenz*, *Spielfeld*, *Setzen*,
  *Übergehen*, *Schlachtrunden*, *erster Zug*, Phase beenden. Der Regeltext nennt diesen
  Teil „Basic Rules“ (`core_rules.txt:125`), das Glossar „Grundregeln“ (Zeile *Mission*).
- Bedienung von Arbiter ohne Regel: Bedienung, feste Adresse, Leisten, ruhiges Spielfeld.
Mit 16080 käme *Ziehen* (AUF-29) dazu, eine Grundregel (`core_rules.txt:729`).

**Kosten.** Am Bildschirm nichts. Domänenphase: elf Anforderungen verschieben, Links darauf
und die Zeile in [Domäne](../../domaene/CLAUDE.md) anpassen; die Kennungen QUE-… bleiben fest.
Technikphase: etwa 60 Dateien mit dem Pfad (Produkt, Tests, Verträge in `technik/`), ein
Lauf des Implementierers, meine Verträge ziehe ich nach. Eine Teilung kostet dazu eine
Zuordnung je Anforderung, keine neue Regel.

**Gegenvorschlag.** Teilen, nach dem Regeltext: `grundregeln/` für die erste Gruppe samt
*Ziehen* aus 16080, `bedienung/` für die zweite. So steht im Pfad, was der Ordner enthält,
und eine Regel liegt neben dem Regeltext, den sie umsetzt. Bleibt ein Ordner, wäre
`allePhasen/` lesbar, sagt aber weiter nur, wo etwas gilt. Den Namen wählst du; fragst du den
Stakeholder, gehört diese Wahl mit Empfehlung dazu. Bitte zusammen mit 16080, damit der
Code nur einmal umzieht.

**Stellungnahme.**
