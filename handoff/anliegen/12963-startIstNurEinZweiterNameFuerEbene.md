# start ist in der Bewegung nur ein zweiter Name für ebene

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Am Stand fd5b7e7, `Bewegungsphase._gezeigt`
(`technik/arbiter/domaene/phasen/bewegung/__init__.py`): Seit 12961 steht dort
`start = ebene`. Die Bedingung, die `start` von `ebene` unterschied, ist weg; `start` ist
nur noch ein zweiter Name für dieselbe *Stelle* vor dem Ziehen.

**Kosten.** Wer die Funktion liest, sucht, worin `start` sich von `ebene` unterscheidet,
und findet nichts. Neben `ebene` und `zuvor` steht so ein dritter Name für einen
Ausgangspunkt. Eingeordnet als wartend: Keine Prüfung ist rot, das Verhalten stimmt mit dem
[Vertrag](../../technik/architektur/vertrag/bewegung/ziehen.md) (Probe
`/tmp/rev12700probe/probe.py`, Mutation in `/tmp/rev12961mut`).

**Gegenvorschlag.** Streiche `start` und nimm in den drei Zeilen danach `ebene`.

**Stellungnahme.** Überholt: `start` steht nicht mehr in
`technik/arbiter/domaene/phasen/bewegung/`; die Bewegung benennt die Ausgangs-*Stelle* nicht
mehr doppelt. Nichts bleibt offen.
