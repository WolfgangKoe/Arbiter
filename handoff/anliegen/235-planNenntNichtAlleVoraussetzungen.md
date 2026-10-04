# Plan 3 nennt nicht alle Voraussetzungen vor dem Testautor

235 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · offen

## Runde 1
Geprüft: [Plan 3](../plan.md), beide Items, die drei Mockups. Prüfbar sind QUE-2.1 bis
QUE-2.6 und AUF-4.2 bis AUF-4.7; die Domäne liefert schon alles, was AUF-4 anzeigt
(`anDerReihe`, `einheitInAufstellung`, `aufstellungszone(spieler)`, `gesetzt`, `stelle`).
Zustände außer der Ausgangslage erreichen nur die Tests: Sie stellen sie mit Handlungen der
Domäne her und geben sie `web/` mit; diese Naht lege ich in `web.md` fest.

**Befund 1.** „Vor dem Testautor“ nennt nur meine Schritte (153, Wegwerf-Versuch,
Komponentenseite). Es fehlen zwei, die andere Rollen tun müssen:
- Flask und Playwright in `pyproject.toml`, Regelumsetzer
  ([234](234-flaskUndPlaywrightFehlen.md)).
- Schreibrecht auf `technik/frontend/` für den Implementierer, Organisationsentwickler
  ([233](233-frontendOhneAutor.md)).
Dazu fehlt, wer die Komponentenseite baut: Nach `architektur.md` (Oberfläche) ist sie Ziel
eines Bildschirmtests, also schreibt der Testautor den Test und der Implementierer die Seite,
nicht ich.

**Befund 2.** „Nach DoR ist nichts offen“ stimmt nicht: [223](223-mockupsBenennungUndZonenfarbe.md)
F1 ist offen, UX benennt die Mockups erst danach um (DoR 4 und 5; die Moderation führt es als
blockierend). Unter „Offene Anliegen“ fehlt 223 F1, obwohl die Freigabe es beantwortet.

**Kosten.** Der Stakeholder schätzt den Zyklus nach dieser Liste („füllen allein einen
Zyklus“); zwei Schritte anderer Rollen stehen nicht darin und laufen in keiner Reihenfolge.
Bleibt 223 unerwähnt, gibt er Mockups frei, deren Namen sich danach noch ändern.

**Gegenvorschlag.** Unter „Vor dem Testautor“: 234 (Regelumsetzer) und 233
(Organisationsentwickler) vor meinem Wegwerf-Versuch; die Komponentenseite als erster
Bildschirmtest des Testautors, gebaut vom Implementierer. 223 F1 in „Offene Anliegen“ mit
Empfehlung A, „Nach DoR ist nichts offen“ erst nach der Umbenennung.

**Stellungnahme.**
