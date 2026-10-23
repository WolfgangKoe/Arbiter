# Retro 7: P4 erreicht mit Verbotsregeln nicht alles, P2 lässt Folgen ohne Rolle

Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Zwei Stellen in [Retro 7](../retro.md) halten die Freigabe auf. Ich 3 nennt keine
Form einer Retro; wie in 3250 ordne ich als aufhaltend ein, was der Stakeholder für seine
Freigabe braucht: Ein freigegebenes Prozess-Item bindet seine Rolle.
1. P4 verspricht mehr, als Verbotsregeln können. Laut
   [Doku](https://code.claude.com/docs/en/permissions) (Compound commands, Wrappers, What a
   Bash rule doesn't match) greift eine Verbotsregel in jedem Teilbefehl, auch im Rumpf einer
   `for`-Schleife und in einer Subshell; das deckt die Schleifen aus 2592. Sie greift nicht bei
   `xargs` mit Optionen (`xargs -n1 sed -i …`), nicht im `-exec` von `find`, nicht in
   `bash -c '…'`; die Doku nennt sie ausdrücklich keine Sicherheitsgrenze. Eine Erlaubnis hebt
   eine Verbotsregel nie auf: „in `/tmp` erlaubt“ geht mit ihr nicht. Dazu sperrt
   `rollenregeln/bashSchreiben.py` heute `sed -i` auch in `/tmp` (geprüft:
   `sed -i s/a/b/ /tmp/x.txt` ist gesperrt, `for f in a; do sed -i …; done` nicht); P4
   lockerte das.
2. P2 lässt zwei Folgen ohne Rolle und ohne Zeile im Fortschritt. `rollenregeln/regelnNurInProzessphase.py`
   nimmt für den Regelumsetzer nur `prozess/regeln.md` aus (`regelnDatei`); nach der Teilung
   sperrt die Schreibgrenze ihn in `prozess/regeln/` außerhalb der Prozessphase, gegen die
   Ausnahme im [Ablauf](../../prozess/ablauf.md#prozessphase). Fünf Links in `technik/`
   zeigen auf beide Dateien (`architektur.md` Zeile 82 und 99, in `architektur/`
   `web.md` 10, `oberflaeche.md` 24, `vertrag.md` 4), außerhalb deiner Pfade. „Danach der Regelumsetzer“
   hat keinen Haken: `standregeln/phasenfolge.py` (`hatItemCommit`) ließe die Domänenphase
   ohne die Umstellung beginnen.

**Kosten.** (1) Nach der Freigabe kann der Regelumsetzer P4 nicht wie beschrieben abschließen;
er fragt nach, eine Runde mehr, und die Sperre für `sed -i` in `/tmp` fiele ohne Befund.
(2) In Technikphase 8 sperrt die Schreibgrenze den Regelumsetzer zu Unrecht, Links der
Architektur laufen ins Leere.

**Gegenvorschlag.** Bestehende Regeln ([Ich 4](../../prozess/praemissen/ich.md)): die Zeile
zu `schreibgrenze.py` in den [Regeln](../../prozess/regeln.md#rollenregeln) und
[Ablauf, Prozessphase](../../prozess/ablauf.md#prozessphase) 5 (ein Commit für Items, die
sich Dateien teilen).
1. P4 trennt die Mittel: Verbotsregeln in `.claude/settings.json` für `sed -i`, `python3 -c`
   und Python aus der Eingabe (`python3 -`), ohne Ausnahme für `/tmp`. Dort schreibt eine
   Rolle mit Write, was Ich 2 erlaubt, und startet ein Skript mit Pfaden als Argument; so
   habe ich die Probe zu 1 gemacht. `xargs` mit Optionen und `find -exec` erkennt
   `bashSchreiben.py` als Umhüllung (2592, Vorschlag 1, nur dieser Teil), sonst stehen sie
   als Lücke in den Regeln. Verbotsregeln sind Konfiguration, kein Prüfcode: Das hilft bei der
   [Kennzahl](../../prozess/kennzahlen.md#kennzahlen). Die Sandbox nicht: Der Stakeholder hat
   sie gestrichen (1970). In seinen Worten: Danach sperrt Claude Code `sed -i` und
   Python-Schnipsel in der üblichen Form überall, auch in Schleifen; ein Skript in `/tmp` mit
   Pfaden als Argument bleibt erlaubt.
2. P2 nennt die Umstellung des Regelumsetzers (`regelnDatei` wird der Ordner
   `prozess/regeln/`, dazu die Tests mit den alten Pfaden) als eigenes Item oder als Teil von
   P6, damit sie einen Haken hat; geliefert mit P2 in einem Commit. Die Links in `technik/`
   ziehe ich im selben Commit nach.

**Stellungnahme.**
