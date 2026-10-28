# Ablauf und Regeln verschlanken, ohne zu verlieren, was funktioniert

Form: Auftrag
Von: Stakeholder
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

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

**Stellungnahme.** Punkte 1 bis 6 umgesetzt mit P5 der [Retro 8](../retro.md); Punkt 7 setzt
der Regelumsetzer mit P6 um, `erledigt` folgt dem Haken von P6 im Fortschritt der Retro. Der
[Ablauf](../../prozess/ablauf/) ist rund 1.000 Zeichen kürzer; Phasen, Status und Züge der
Anliegen, Freigabe und Fortschritt arbeiten wie vorher (an einer Kopie in `/tmp` geprüft:
Prüfungen mit Marke `stand` grün, der Start jeder Rolle nennt Stand und Befehle, ein Commit
geht durch).
1. Doppelt: [DoD 2](../../prozess/ablauf/dod.md) zählte die Prüfungen der Formregeln auf.
   Jetzt: die beiden Befehle, Links auf [Formregeln](../../prozess/regeln/formregeln.md) und
   [Kriterienregeln](../../prozess/regeln/kriterienregeln.md), das Urteil des Reviewers.
2. Doppelt: „Ein Mechanismus entsteht … bei beobachtetem Bedarf“ steht nur noch im
   [Backlog](../../prozess/backlog.md), nicht mehr in der Prozessphase 1; darauf verweist der
   [Regelumsetzer](../../.claude/agents/regelumsetzer.md).
3. Doppelt: Dass der Stakeholder die Etappe mit „.“ freigibt, steht nur noch in der
   [Domänenphase](../../prozess/ablauf/domaenenphase.md) 3, nicht mehr in der Freigabe.
4. Doppelt und alt: [Fortschritt](../../prozess/ablauf/fortschritt.md) nennt das Format
   `Hindernis: <Rolle> → <Beseitiger>: <Satz> (Anliegen <nr>)`; die Standregeln folgen mit
   P6 ([4120](4120-hindernisformatInAblaufUndRegeln.md)).
5. Nie ausgelöst: [Rollen mit Auslöser](../../prozess/ablauf/rollenMitAusloeser.md) ohne
   „Haiku-Zuarbeiter“.
6. Unklar: [Fortschritt](../../prozess/ablauf/fortschritt.md) sagt jetzt, ein Kritiker hakt erst
   ab, wenn unter seinem Schritt kein `Hindernis:` ohne `beseitigt` mehr steht; „je Item mit
   Kriterium“ steht in der Tabelle (Anliegen 6620).
7. Regelumsetzer: Formregeln und Standregeln unter das Kürzungsmaß von 8.000 Zeichen.
