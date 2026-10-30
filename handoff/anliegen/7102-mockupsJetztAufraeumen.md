# Überholte Mockups jetzt aufräumen oder in der Domänenphase 10?

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Du hast geschrieben: „Ich sehe schon, dass bei den Mockups aufgeräumt werden
muss, damit es keine Verwirrung gibt.“ Den Umfang und den Adressaten klärt der Ablauf, den
Zeitpunkt für einen Teil nicht so, wie du es vielleicht meinst:
- Umfang: Ich habe alle Mockups geprüft. Überholt sind bew-1, bew-2, bew-8 (sechs Knöpfe
  „Vorrücken mit 1“ bis „6“ statt „Vorrücken“), que-9, que-10, que-10-ende (ihr Item ist
  fertig, die [DoD](../../prozess/ablauf/dod.md) verlangt sie gelöscht) und auf-22 (kein
  Item verlinkt es). Die übrigen passen.
- Adressat: UX, sie schreibt und löscht die Mockups ([Kritik](../../prozess/ablauf/kritik.md),
  Tabelle; [UX](../../.claude/agents/ux.md)). Der Anforderungsautor darf dort nicht schreiben.
- Zeitpunkt nach dem Ablauf: bew-1, bew-2, bew-8 jetzt, denn Items 2 und 3 werden gerade
  danach gebaut ([7100](7100-vorrueckenMitWurfInDenMockups.md)). Die übrigen vier halten
  nichts auf, nach der Kritik warten sie auf die Domänenphase 10
  ([7101](7101-mockupsNachDerDoDUndOhneItem.md)). Sie früher zu erledigen, ist eine
  Ausnahme, die nur du erteilst ([Absicht 6](../../prozess/praemissen/absicht.md)).

**Kosten.** A: UX löscht in demselben Lauf wie 7100 vier Dateien mehr, kaum zusätzliche
Token; danach liegen unter `domaene/mockups/` nur Bilder, die gelten oder an einem Item
hängen. B: kein Aufwand jetzt, aber bis zur Domänenphase 10 liegen que-9, que-10,
que-10-ende und auf-22 weiter dort, und wer am Bildschirm vergleicht, findet Bilder, die
nicht mehr oder noch nicht gelten.

**Gegenvorschlag.** A.

**F1 · Wann löscht UX que-9, que-10, que-10-ende und auf-22 (7101)?**
- A: jetzt, mit 7100; ich streiche dafür `Wartet auf` in 7101 (neu: Ausnahme von der
  Kritik; Grund: Absicht 2 „erst Bestand abbauen“, keine organisatorische Schuld).
- B: in der Domänenphase 10 (Kritik).
Empfehlung: A.
Antwort: A

**Stellungnahme.**
