# Anforderungen zu Plan 8: drei Stellen vor den Tests

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Alle drei halten auf (Ich 3): Ohne Änderung wird eine Prüfung rot, oder neuer
Code verletzt Architektur oder Lesbarkeit.
1. *Weg* (Glossar: Summe der Strecken in Zoll, BEW-2.1) heißt in acht Kriterien schon etwas
   anderes: die Verschiebung („um den Weg des gezogenen“, AUF-21.1, AUF-8.7), die Strecke
   („auf dem geraden Weg“, AUF-29.1), „auf kürzestem Weg“ (AUF-18.3, 26.1). Das hat der
   Fachkritiker als wartend gemeldet (4261, Punkt 5). Es hält aber auf: Im Code ist
   `messen.Weg` die Verschiebung (25 Zeilen), und der *Normal Move* braucht beides in einem
   Modul, die Verschiebung der *Einheit* (BEW-1.1) und die Länge (BEW-2.1). Ein Name mit zwei
   Bedeutungen verletzt [Wir 2](../../prozess/praemissen/wir.md), und der Testautor legt den
   Namen in Testnamen und Hilfsfunktionen fest.
2. *Phase* hat im [Glossar](../../domaene/glossar.md) keine Enum-Werte in Klammern. Der
   naheliegende Code für QUE-10.2 ist ein Enum mit sieben Werten; damit wird
   `formregeln/glossar.py` rot. Psi-, Schuss-, Angriffs- und Nahkampfphase stehen nur als
   Wortteile da, QUE-10.1 zeigt aber ihren Namen.
3. Die `5` (Glossar *Schlacht*, QUE-10.4 „Schlachtrunde 6“) ist eine Zahl der *Mission*
   Only War (`core_rules.txt:2337`, Schritt 8 der Mission), wie die Größe des Spielfelds in
   `onlyWar.yaml`. [Architektur A3](../../technik/architektur.md): Katalogdaten stehen nur
   als YAML in `domaene/daten/`. Dort darf der Implementierer nicht schreiben, eine `5` im
   Code verletzt A3.

**Kosten.** Jetzt je eine Zeile in Glossar, Anforderung oder YAML, kein Test betroffen.
Nach den Tests müssen Testnamen, Hilfsfunktionen und Code umbenannt werden. Zu 1 und 2
beantwortet der Stakeholder gerade 4280 F1, das sind dieselben Begriffe.

**Gegenvorschlag.**
1. Für die Länge ein eigener Begriff, etwa *Distanz* (Regeltext „the distance a model
   moves“, `core_rules.txt:729`), Code `distanz`; *Weg* bleibt ohne Kursiv Umgangssprache.
   Die Alternative kostet mehr: *Weg* als Länge behalten, acht Kriterien umformulieren und
   `messen.Weg` in `Verschiebung` umbenennen.
2. Die Glossarzeile *Phase* bekommt den Code-Bezeichner `Phase (kommandophase,
   bewegungsphase, psiphase, schussphase, angriffsphase, nahkampfphase, moralphase)`, und
   die vier Namen stehen ausgeschrieben da.
3. In `onlyWar.yaml`: `Schlachtrunden: 5  # core_rules.txt:2337`. QUE-10.4 sagt dann „eine
   *Schlachtrunde* nach der letzten der *Mission*“, das Glossar unter *Schlacht* „endet nach
   der letzten *Schlachtrunde* der *Mission*“.

Zu 4280 F3, zur Kenntnis: Empfehlung A lässt sich exakt prüfen. Eine Summe von Wurzeln
vergleicht `math.isqrt` ohne Toleranz mit *M*; Probe in `/tmp/probeWeg/probe.py`: genau
*M* ist erlaubt, 10⁻¹² darüber gesperrt, 2.000 Fälle dauern 0,1 s. Architektur S2 („ohne
Wurzel“) passe ich im Vertrag an. B hinge davon ab, wie oft der Browser den Zeiger meldet,
und ließe sich nicht exakt testen.

**Stellungnahme.** Angenommen, alle drei wie vorgeschlagen.
1. Im [Glossar](../../domaene/glossar.md) heißt die Länge jetzt *Distanz* (distance a model
   moves, `distanz`, `core_rules.txt:729`); die Zeile *Weg* ist gelöscht. BEW-2.1 und die
   Zeile *Normal Move* sagen *Distanz*; „Weg“ in den AUF-Kriterien bleibt Umgangssprache.
   [4280](4280-begriffeUndAnnahmenZuPlan8.md) F1 nennt *Distanz* statt *Weg*.
2. *Phase* trägt die sieben Enum-Werte; Psiphase, Schussphase, Angriffsphase und
   Nahkampfphase stehen ausgeschrieben. QUE-10.2 verweist knapper auf diese Reihenfolge.
3. [onlyWar.yaml](../../domaene/daten/onlyWar.yaml): `Schlacht: schlachtrunde: 5` (die
   letzte, `core_rules.txt:2337`); Schlüssel nach Code-Bezeichnern des Glossars, darum nicht
   `Schlachtrunden`. QUE-10.4: „eine *Schlachtrunde* nach der letzten der *Mission*“; das
   Glossar unter *Schlacht* wie vorgeschlagen, mit Verweis auf die YAML.

`formregeln.glossar` und die Kriterienprüfungen laufen ohne Befund.
