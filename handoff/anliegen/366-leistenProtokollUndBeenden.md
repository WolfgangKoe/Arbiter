# Seitenleisten, Protokoll und gesperrtes Beenden

366 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 1/3 · offen
Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Deine Antworten aus 362 stehen in den
[Anforderungen](../../domaene/anforderungen/phasen/aufstellen/):
[AUF-11](../../domaene/anforderungen/phasen/aufstellen/gewinnerUndZone.md) (Gewinner und
Zone am Bildschirm), [AUF-12](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md)
(‚Modell gesperrt‘, Zurückspringen), [AUF-13](../../domaene/anforderungen/phasen/aufstellen/gesperrtesBeenden.md)
(„zurück“ beim Beenden), QUE-5.1 und QUE-5.4 im
[Übergehen](../../domaene/anforderungen/querschnitt/uebergehen.md),
QUE-4.4 in der [Kohärenz](../../domaene/anforderungen/querschnitt/kohaerenz.md). AUF-6 bleibt,
bis AUF-11 gebaut wird. Auch ‚Modell gesperrt‘ lässt ein gezogenes *Modell* zurückspringen
und bietet kein Übergehen an (AUF-12.3): Der Weg heraus ist „zurück“ oder „gemeinsam
übergehen“ am *gesperrten* *Modell*.
Offen bleiben zwei Stellen: Deine drei einfahrbaren Seitenleisten (an den Architekten in
[364](364-frontendMitDreiEinfahrbarenLeisten.md)) berühren „stets sichtbar neben der *Karte*“
aus 362 F4 A, und bei AUF-13 ist ungeregelt, was eine andere Handlung tut, solange „zurück“
und „gemeinsam übergehen“ angeboten sind.

**Kosten.** Bis zur Antwort fehlen die Kriterien zu den Leisten und zum Ort des *Protokolls*;
den Fall bei AUF-13 kann kein Test prüfen.

**Gegenvorschlag.** Je Frage die Empfehlung.

**F1 · Was in den drei Leisten steht.** A: Links die *Ablage* von „Spieler 1“, rechts die
von „Spieler 2“, unten das *Protokoll*; jede fährt per Griff ein und aus und ist beim Start
ausgefahren. Das *Protokoll* ist damit stets einsehbar (Etappe 1), sichtbar aber nur
ausgefahren. B: Wie A, aber das *Protokoll* steht stets sichtbar außerhalb der Leisten
(362 F4 A), und du nennst, was die untere Leiste trägt. Empfehlung A nach ArbiterMap:
Spielerleisten links und rechts, unten `BattleLog` (`ArbiterMap/docs/spec/design_system.md:55`,
`:56`). Dort starten sie eingefahren (`:85`); hier beginnt die *Aufstellung* in den *Ablagen*.

Antwort: .

**F2 · Andere Handlung beim gesperrten Beenden.** „zurück“ und „gemeinsam übergehen“ sind
angeboten (AUF-13.1), und jemand *setzt* ein *Modell* oder wählt erneut *Aufstellen der
Einheit beenden*. A: Das gilt als *zurück* (AUF-13.2), dann geschieht die Handlung. B: Wie
bei einem *gesperrten* *Modell* (AUF-12.1) sperrt Arbiter sie mit ‚Beenden gesperrt‘, bis
„zurück“ oder „gemeinsam übergehen“. Empfehlung A: Auf der *Karte* steht nichts *gesperrt*,
also bleibt nichts hängen.

Antwort: .

**Stellungnahme.**
