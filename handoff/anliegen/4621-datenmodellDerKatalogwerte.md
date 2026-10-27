# Datenmodell der Katalogwerte prüfen

Form: Fragen
Von: Anforderungsautor
An: Architekt
Runde: 1/3
Status: offen
Wartet auf: Technikphase

## Runde 1
**Befund.** Der Stakeholder will über die Daten aus Arbiter-old im nächsten Zyklus
entscheiden, damit sie sauber aufgesetzt werden: „Der Architekt soll prüfen, wie wir das
Datenmodell aufbauen können. Vielleicht ist dieses aus Arbiter-old brauchbar und muss vor
allem mit Begriffen aus dem Glossar bestückt werden.“ (Anliegen 4280, F7).

Was die Domäne an jedem Datenmodell verlangt ([Domäne](../../domaene/CLAUDE.md)):
- Schlüssel sind Code-Bezeichner des [Glossars](../../domaene/glossar.md), etwa
  `bewegungsweite` statt `move` (`Arbiter-old/data/wh40k_9e/necrons/units.yaml:28`).
- Jeder Wert trägt seine Fundstelle; in Arbiter-old steht die Quelle nur im Kopf der Datei
  (`necrons/units.yaml:2`).
- Nur Werte, die die 9. Edition kennt: `oc` (`necrons/units.yaml:37`) fehlt im Profil
  (`core_rules.txt:561` bis `:581`).

Heute stehen Katalogwerte nur als YAML in `domaene/daten/` ([Architektur, A3](../../technik/architektur.md));
Etappe 2 nutzt davon `durchmesser` und `bewegungsweite` von vier *Einheiten*
(`domaene/daten/ausgangslage.yaml`).

**Kosten.** Ohne Prüfung entscheidet der Stakeholder im nächsten Zyklus ohne die Folgen für
Code, Arbeit und Tokenkosten (Absicht 4), oder ich trage Werte in ein Modell ein, das danach
umgebaut wird.

**Gegenvorschlag.** Prüfe das Datenmodell aus `Arbiter-old/data/wh40k_9e/` gegen Architektur
und die Anforderungen oben, und lege dem Stakeholder vor der Domänenphase 9 eine Frage mit
Empfehlung und Folgen vor; nenne ihre Nummer in deiner Stellungnahme.

**F1 · Wie bauen wir das Datenmodell der Katalogwerte auf?** A: Gliederung aus Arbiter-old
(je Fraktion `units.yaml`, `weapons.yaml` usw.), Schlüssel aus dem Glossar, Fundstelle je
Wert, als YAML (Arbiter-old, Architektur A3). B: Eine Datenbank (Anliegen 4280).
Empfehlung: A. Aus Sicht der Domäne genügt YAML für Orks gegen Necrons, und die Gliederung
liegt schon vor; ob sie technisch trägt, prüfst du.
Antwort: .

**Stellungnahme.**
