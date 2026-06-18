# 0001 — Explizite Freigabe für Probe-Session beibehalten

**Datum:** 2026-06-18
**Status:** angenommen

## Kontext

Das Operating Model kennt vier Entscheidungsmodi; für gebundene Umsetzungs-Entscheidungen wäre **Konsent** (kein Einspruch genügt, klarer Default) der reibungsärmere Standard. Die CLAUDE.md-Kultur fordert aber seit Projektbeginn ein **explizites "Ja"** — d. h. "ja", "mach es", "ok", "Freigabe" oder direkter Befehl. Rückfragen oder Ergänzungen des Stakeholders gelten ausdrücklich nicht als Freigabe.

Diese Strenge hat eine **empirische Wurzel**, kein Dogma: Der Agent ist in der Vergangenheit "losgesprungen" und hat dabei das Ziel verfehlt oder übersprungen. Das explizite "Ja" ist die Lehre aus dieser Erfahrung.

Die Frage: Soll dieses strengere Muster beibehalten oder auf Konsent gelockert werden?

## Entscheidung

Das **strengere explizite "Ja"** bleibt vorerst in Kraft — als **bewusste Probe-Entscheidung für genau eine Session**. Es geht nicht um Endgültigkeit, sondern darum, gemeinsam zu lernen und das Operating Model im agilen Sinne iterativ weiterzuentwickeln: erst Erfahrung sammeln, dann in der Retrospektive datenbasiert entscheiden, ob die Zügel gelockert werden können. In der aktuellen Phase überwiegt der Wert der Klarheit (kein Ziel-Verfehlen) den der Geschwindigkeit.

## Konsequenzen

- **Einfacher:** Stakeholder hat volle Kontrolle; keine impliziten Freigaben durch Rückfragen oder Ergänzungen.
- **Schwieriger:** Mehr Round-Trips bei kleineren, offensichtlichen Entscheidungen.
- **Folgefrage:** Welche Klassen von Entscheidungen könnten sicher auf Konsent wechseln (z. B. Datei-Format-Wahl im Executor)? Für die Retrospektive vormerken.

## Review-Termin

Nächste Retrospektive (Session-Ende-Event) — Frage: Hat das explizite "Ja" in dieser Session Mehrwert gebracht oder war es Overhead?
