# Ablauf und Regeln verschlanken, ohne zu verlieren, was funktioniert

Form: Auftrag
Von: Stakeholder
An: Organisationsentwickler
Runde: 1/3
Status: offen
Wartet auf: Prozessphase 8

## Runde 1
**Befund.** Wortlaut des Stakeholders (Kommentar in Anliegen 2590):
„Bitte halte als Anliegen für die nächste Prozessphase fest, noch mal sorgfältig durch alle
Regeln zu gehen inkl. der Ablaufdateien, ob man diese noch sinnvoll verschlanken kann.
Vorsicht! So wie es jetzt läuft und lief, scheint es gut zu funktionieren. Das muss auf jeden
Fall erhalten bleiben!“

Festgehalten vom Organisationsentwickler; Durchsicht und Vorschlag sind Arbeit der
Prozessphase 8. Stand heute: der [Ablauf](../../prozess/ablauf/) hat 16 Dateien mit
35.411 Zeichen, die [Regeln](../../prozess/regeln/) 9 Dateien mit 36.946 Zeichen; über dem
Kürzungsmaß von 8.000 liegen Formregeln (10.204) und Standregeln (10.359).
Bestehende Regeln ([Ich 4](../../prozess/praemissen/ich.md)): Höchstmaße der Ordner
([Ablauf](../../prozess/ablauf/CLAUDE.md), [Regeln](../../prozess/regeln/CLAUDE.md)),
[Wir 3](../../prozess/praemissen/wir.md) (jede Aussage genau einmal),
[Wir 4](../../prozess/praemissen/wir.md) (keine Historie); „Löschen zählt wie Hinzufügen“ aus
der Definition des Organisationsentwicklers.

**Kosten.** Jede Rolle liest die Ablaufdateien ihrer Phase und die Regeln, die sie berührt;
jede überflüssige Zeile kostet in jedem Lauf Token. Wird zu viel gestrichen, geht verloren,
was heute trägt.

**Gegenvorschlag.** In der Prozessphase 8:
1. Jede Datei in `prozess/ablauf/` und `prozess/regeln/` durchgehen und je Stelle einordnen:
   doppelt (steht schon anderswo), Historie, Regel ohne Mechanismus, die nie auslöste, oder
   tragend.
2. Erhalten bleibt alles Tragende: jede Regel mit Mechanismus samt Scheiter-Test, die Folge
   der Phasen, Status und Züge der Anliegen, Freigabe und Kommentare, der Fortschritt.
3. Die Retro 8 nennt jede Streichung mit ihrem Befund als Vorschlag; gestrichen wird erst
   nach `Freigabe Retro 8`. Danach sind alle Prüfungen grün, und an einer Kopie in `/tmp`
   arbeiten und committen alle Rollen wie vorher ([Ich 5](../../prozess/praemissen/ich.md)).

**Stellungnahme.** Vorschlag der [Retro 8](../retro.md), P5 und P6, gestrichen erst nach
`Freigabe Retro 8`; Tragendes bleibt:
1. Doppelt: [DoD](../../prozess/ablauf/dod.md) 2 zählt alle Prüfungen auf, die in den
   [Formregeln](../../prozess/regeln/formregeln.md) stehen; bleibt ein Satz mit Link.
2. Doppelt: In [Prozessphase](../../prozess/ablauf/prozessphase.md) 1 „Ein Mechanismus
   entsteht … bei beobachtetem Bedarf“, das der Backlog nennt.
3. Doppelt: [Freigabe](../../prozess/ablauf/freigabe.md), „Die Etappe gibt der Stakeholder mit
   „.“ frei“, steht in der Domänenphase 3.
4. Doppelt und alt: das Format `Hindernis:` in Fortschritt und Standregeln (Anliegen 4120).
5. Nie ausgelöst: „Haiku-Zuarbeiter“ in [Rollen mit Auslöser](../../prozess/ablauf/rollenMitAusloeser.md).
6. Unklar: Fortschritt, ein Kritiker hakt nicht ab, solange unter seinem Schritt ein Hindernis
   ohne `beseitigt` steht (in Zyklus 8 verschieden gelesen); Tabelle „je Item mit
   Kriterium“ (Anliegen 4301).
7. Regelumsetzer: Formregeln und Standregeln unter das Kürzungsmaß von 8.000 Zeichen.
