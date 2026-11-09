# Prüfskript: Bezüge in Kriterien nur in Klammern

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Der Stakeholder verlangt Kriterien, die ein Mensch ohne Nachlesen anderer versteht;
Bezüge auf andere Kriterien nur in Klammern zur Orientierung (Kommentar in
[16100](16100-sperreNachDemUebergehenBisEtappe7.md)). Die Regel steht als
[DoR 7](../../prozess/ablauf/dor.md), Mechanismus bis zum Prüfskript nur Text. Er hat
entschieden: ein Prüfskript, das beim Schreiben mitläuft, von dir als nächstes Item vor P2
gebaut, mit Probe am Bestand. Bestehende Regeln (Ich 4): DoR 1 und 2 und das Format in
[Domäne](../../domaene/CLAUDE.md) prüfen nichts davon; `kriterienregeln/kriterium.py` liest die
Kriterienzeilen schon und lässt sich wohl mitnutzen.

**Kosten.** Ein Prüfskript mit Scheiter-Test und Hook-Eintrag, ein Lauf. Ohne es hängt DoR 7
am Urteil des Fachkritikers, und der Bestand bleibt ohne Zahl.

**Gegenvorschlag.** Das Skript prüft je Kriterienzeile (`- <Kürzel>-<n>.<m> …`) unter
`domaene/anforderungen/`, nach Entfernen aller Klammern samt Inhalt, auch geschachtelter:
1. Kein Bezug bleibt stehen: keine Kennung `<Kürzel>-<n>` oder `<Kürzel>-<n>.<m>` und keine
   Kurzform `<n>.<m>` (`18.1`). Maße mit `″` (`1/100″`, `2″`) und Fundstellen in Backticks
   zählen nicht.
2. Jeder Teil nach **Gegeben**, **wenn** und **dann** behält mindestens ein Wort, sonst stand
   ein Bezug in Klammern statt eines Satzes (`**Gegeben** (18.1), **wenn** …`).

Rot: `**Gegeben** 18.1, **wenn** BEW-8.4 *setzt*` (BEW-18.7), `**Gegeben** eine *Sperre* nach
QUE-1.2` (QUE-1.4). Grün: `**Gegeben** die *Sperre* ‚Base überdeckt‘ (QUE-1.2), **dann** …`.
Ob der Satz ohne Nachlesen verständlich ist, bleibt Urteil des Fachkritikers.

Beim Schreiben: ein Hook nach Write und Edit auf `domaene/anforderungen/` meldet der
schreibenden Rolle die roten Kriterien dieser Datei, wie schon `anliegenregeln/anliegenLaenge.py`
(Bordmittel: Hook `PostToolUse` mit Matcher `Write|Edit`). Den Bestand schreibt erst Domänenphase 11 um (Anliegen 16171); bis
dahin hält das Skript keinen Commit an, der kein Kriterium neu schreibt. Wie, entscheidest du.

Probe am Bestand: rote Kriterien und Dateien, je Etappe, in deiner Stellungnahme. Meine grobe
Probe nach 1. (`/tmp/oe16170/probe.py`): 86 von 176 Kriterien in 44 Dateien.
Danach Zeile in [Regeln](../../prozess/regeln/); ich ersetze in DoR 7 „nur Text“.

**Stellungnahme.**
