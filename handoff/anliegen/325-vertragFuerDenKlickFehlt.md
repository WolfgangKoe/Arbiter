# Vertrag für den Klick fehlt in web.md

325 · Kritik · von Testautor (Technik) → Architekt · Runde 1/3 · offen

## Runde 1
**Befund.** [Plan 4](../plan.md) kündigt vor dem Testautor einen Vertrag für den Klick in
[web.md](../../technik/architektur/web.md) an; dort stehen keine Pfade und kein JSON-Beispiel für
Auswählen ([Ablauf, Technikphase 1](../../prozess/ablauf.md#technikphase)).

**Kosten.** Ohne Vertrag gibt es keinen Backend-Test mit dem Flask-Testclient und keinen
Bildschirmtest mit geliefertem Beispiel. AUF-5 und QUE-3 sind nur als Bildschirmtests gegen den
echten Server geschrieben (Klasse `ausgewählt` der Komponentenseite).

**Gegenvorschlag.** Pfad, Methode und je Antwort ein JSON-Beispiel für Auswählen und Abwählen
in web.md festlegen, oder festhalten, dass der Bildschirmtest genügt.

Erledigt, wenn web.md den Vertrag nennt oder den Verzicht begründet.

**Stellungnahme.**
