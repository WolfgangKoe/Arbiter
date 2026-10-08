# Vertrag für den Klick fehlt in web.md

325 · Kritik · von Testautor (Technik) → Architekt · Runde 1/3 · angenommen

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

**Stellungnahme.** Umgesetzt mit der ersten Variante: [Vertrag](../../technik/architektur/vertrag.md),
verlinkt aus [Web](../../technik/architektur/web.md) und der
[Übersicht](../../technik/architektur.md); in web.md selbst fehlte der Platz (6.000 Zeichen,
`prozess/kennzahlen.md`).
- V1: `GET /api/spielstand`, Beispiel als Datei
  [spielstand.json](../../technik/architektur/vertrag/spielstand.json), der Stand des Mockups
  auf-5. Eine Datei statt eines Blocks in Markdown: Tests lesen sie (`route.fulfill(path=…)`,
  Vergleich im Flask-Testclient), keine zweite Abschrift.
- V2: `PUT` und `DELETE` auf `/api/spieler/<nummer>/einheiten/<nummer>/ausgewählt`, beide
  200 mit dem Spielstand, 404 ohne *Einheit* in der *Ablage*. Idempotent statt Umschalten;
  damit bleibt QUE-3.1 auch dann grün, wenn beide Server dieselbe Auswahl teilen (zu Punkt 2
  in [326](326-klickDesSpielersAnDerReiheUndGeteilterStand.md)).
- V3: Die Auswahl hält `Aufstellung` (`auswählen`, `abwählen`, `ausgewählt`), AUF-5.10 inklusive;
  D3 nennt das Auswählen jetzt neben den Handlungen.
- Prüft: Backend `tests/einheit/web/anwendungTest.py`, Frontend mit Beispiel
  `tests/einheit/frontend/seiteTest.py`, die bestehenden Bildschirmtests bleiben die
  Akzeptanztests.

Wegwerf-Versuch: Die Route mit „ausgewählt“ trifft Flask im Testclient und aus `fetch` in
Chromium (PUT und DELETE 200, unbekannte Kennung 404). Der Beispielstand ist von der
Ausgangslage nach AUF-6 aus erreichbar: drei Necron Warriors gesetzt, zwei `PUT`.
