# Etappe 1: Ablage, Umsetzen, Übergehen nach dem Rücksprung

11 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · erledigt

## Runde 1
**Befund.** [Etappe 1](../../domaene/etappen/01-aufstellen.md) lässt offen:
1. *Zurück wohin?* Ein Modell, das zum ersten Mal gesetzt wird, hat keine vorige Stelle.
2. *Umsetzen:* Nach einer Kohärenzsperre bleibt die Einheit in Aufstellung, aber kein Satz
   erlaubt, ein gesetztes Modell erneut zu ziehen; die Sperre ist so eine Sackgasse.
3. *Unvollständig:* Gelingt „Aufstellen der Einheit beenden“, solange Modelle fehlen?
4. *Übergehen:* Springt das Modell sofort zurück, ist die Stelle weg, die die Spieler
   übergehen wollen. Wo das Protokoll zu lesen ist, steht nirgends; so ist es nicht abnehmbar.

**Kosten.** Jede Antwort formt den Spielstand (Modell ohne Stelle, Einheit in Aufstellung) und
damit Fachlogik, Schnittstelle und Karte. Altbestand: `deployment_service.py` setzte ganze
Einheiten als Reihe; Zurücknehmen in „Noch nicht aufgestellt“ (Stelle `NULL`) kam erst mit
einem Reviewbefund der 49. Sitzung nachträglich hinzu. Ohne Entscheidung erfinden Testautor
und Implementierer die Antworten.

**Gegenvorschlag.**
1. Nicht aufgestellte Modelle liegen in einer Ablage neben der Karte; ein gesperrtes erstes
   Setzen springt dorthin zurück, ein gesperrtes Umsetzen an die vorige Stelle.
2. Modelle der Einheit in Aufstellung dürfen erneut gezogen und in die Ablage zurückgelegt
   werden; nach dem Beenden nicht mehr.
3. Beenden erst, wenn alle Modelle gesetzt sind, sonst Sperre mit Grund. Was ein Übergehen
   hier bedeutet, ist eine Frage an den Stakeholder: `core_rules.txt:441` („considered to have
   been destroyed“) gilt wörtlich nur für Modelle, die während der Schlacht hinzukommen.
4. Bei einer Sperre bleibt das Modell mit Grund an der versuchten Stelle, bis die Spieler
   wählen: „zurück“ (Rücksprung) oder „gemeinsam übergehen“ (es bleibt, Eintrag im
   Protokoll). Das Protokoll ist jederzeit einsehbar. Gleich teuer wie der sofortige
   Rücksprung; die Fachlogik bleibt einzige Prüfinstanz (F8).

**Stellungnahme.**
Angenommen als Empfehlung. Es sind Entscheidungen des Stakeholders: F1 bis F4 in
[Anliegen 16](16-aufstellen-ablage-beenden-uebergehen.md). Item 1 hängt nicht davon ab.
Architekt: in Ordnung. Der Stakeholder hat 16 mit „.“ beantwortet; Etappe 1 ist angepasst.
