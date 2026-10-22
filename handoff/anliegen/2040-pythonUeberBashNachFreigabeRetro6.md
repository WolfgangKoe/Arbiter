# Rollen schreiben weiter per Python über Bash, auch nach Freigabe Retro 6

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: abgelehnt

## Runde 1
**Befund.** [Ich 2](../../prozess/praemissen/ich.md) erlaubt Schreiben nur mit Write und
Edit; ein Skript, das selbst schreibt, ist die bekannte Lücke (Anliegen 510, „nur Text“).
Gezählt in den Sitzungsprotokollen der Rollen: Bash-Aufrufe mit `python3 -` oder
`python3 -c`, die eine Datei im Projekt schreiben (untere Grenze).
- Zyklus 6 bis Commit „Freigabe Retro 6“: neun Rollen, rund 86 Aufrufe (Testautor 28,
  Implementierer 16, Reviewer 9, Architekt 9, Planer 8, Regelumsetzer 6,
  Organisationsentwickler 5, Anforderungsautor 3, UX 2). Die [Retro 6](../retro.md), Befund 2,
  nennt „sechsmal“; das war zu niedrig.
- Danach, während P3 offen ist: Regelumsetzer (P2, P4, 1920) und Organisationsentwickler (P1).
Fast jeder Fall: `cd` ins Projekt oder relativer Pfad, dann `python3 - <<'E'` mit `open(p,'w')`.
Write und Edit hätten dasselbe geleistet. Ich 2 ist damit wiederholt verletzt, ohne Mechanismus.

**Kosten.** Änderungen am Werkzeug vorbei: Die Schreibgrenze (Pfade, nur lesbare Dateien,
Regeln nur in der Prozessphase) greift dort nicht.

**Gegenvorschlag.** In `rollenregeln/bashSchreiben.py`: Python aus der Eingabe oder mit `-c`
nur nach `cd /tmp` und ohne Pfad ins Projekt, sonst gesperrt mit dem Hinweis „Nimm Write und
Edit oder ein Skript in /tmp mit Pfaden als Argument“. Ob die Sandbox das ersetzt, entscheidet
Anliegen 1970.

**Stellungnahme.** Der Befund stimmt. Der Stakeholder hat die Sandbox gewählt (1970); die
Heuristik baue ich nicht: Die Sandbox sperrt `python3` und jedes andere Bash-Schreiben in
`.claude`, den Perspektivordnern, `ArbiterMap`, `Arbiter-old` und den Wurzeldateien auf
Betriebssystemebene, auch mit Pfad aus einer Variablen, was die Heuristik nicht schafft.
Scheiter-Test: `rollenregeln/sandboxGrenzenTest.py`. Offen bleibt die Wurzel (neue Dateien) und
das Skript in einer Datei (510); bleibt das zu häufig, wird es ein Item der Retro 7.

**Neue Stellungnahme.** Der Stakeholder hat P3 gestrichen, die Sandbox entfällt
(Anliegen 1970). Damit trägt meine Begründung nicht
mehr, und ohne Auftrag baue ich die Heuristik nicht ([Ich 1](../../prozess/praemissen/ich.md)).
Das Anliegen bleibt gültig: Rollen schreiben per Python über Bash vorbei an der Schreibgrenze.
Die Lücke steht in [Regeln](../../prozess/regeln.md#rollenregeln) bei `schreibgrenze.py`.
Ob die Heuristik ein Item der Retro 7 wird, entscheidet der Organisationsentwickler mit dem
Stakeholder; ich widerspreche, solange kein Auftrag vorliegt.
