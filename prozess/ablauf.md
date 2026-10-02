# Ablauf

## Domänenphase
1. Planer: Etappen aus dem Ziel. Auslöser: Stand „Keine Etappe“.
2. Architekt: Kritik an den Etappen, als Anliegen an den Planer.
3. Stakeholder: Freigabe der Etappen im Chat, nur wenn Schritt 1 sie neu abgeleitet hat.
4. Anforderungsautor: Anforderungen zur aktuellen Etappe, Begriffe ins Glossar.
5. Planer: Items und `handoff/plan.md`.
6. Kritik am Ergebnis: Architekt (Technik) an Anforderungen und Items, Organisationsentwickler
   (Prozess) an Format, Größe und Schnitt. Der Besitzer nimmt im Anliegen Stellung.
7. Freigabe: Der Stakeholder schreibt „.“ in den Chat, der Koordinator committet
   `Freigabe Plan <n>`. Danach meldet der Stand die Technikphase.

Gleichzeitig laufen nur Rollen, die ausschließlich Anliegen schreiben (Schritt 6), sonst
meldet die Schreibgrenze fremde Änderungen als Verstoß.

Mechanismus: Schritt 1 und 7 Stand-Hook (`prozess/pruefungen/stand.py`); Reihenfolge 2–6
und Gleichzeitigkeit nur Text, der Koordinator beauftragt danach.

## Technikphase
Auslöser: Stand „Technikphase“ nach `Freigabe Plan <n>`. Fehlen Rollen, schlägt der
Organisationsentwickler sie vor.
1. Testautor: Akzeptanztests je Kriterium der Items, rot.
2. Kritik: Fachkritiker (trifft der Test das Kriterium?), Architekt (Schnittstelle).
3. Implementierer: macht die Tests grün; Refactoring nur aus einem Befund.
4. Reviewer: DoD, `/code-review`, Wiederverwendung, Vereinfachung, Effizienz, Flughöhe.
5. Fachkritiker: fachliche Abnahme gegen Kriterien und Etappe.
6. Reviewer: `handoff/review.md`, erste Zeile `# Review · Zyklus <n>`. Danach meldet der
   Stand die Prozessphase; eine Freigabe ist nicht nötig.

## Prozessphase
Auslöser: Review n liegt vor.
1. Organisationsentwickler: `handoff/retro.md` (`# Retro · Zyklus <n>`) aus Anliegen an den
   Prozess, Kennzahlen und Auslösezählern; Prozess-Items nur aus einem Befund.
2. Regelumsetzer: Mechanismen zu den Prozess-Items, je mit Scheiter-Test.
3. Kritik: Domäne und Technik an Regeländerungen, als Anliegen.
4. Freigabe: Der Stakeholder schreibt „.“, der Koordinator committet `Freigabe Retro <n>`.
   Danach meldet der Stand die Domänenphase mit Plan n+1.

Nach jeder Freigabe empfiehlt der Koordinator einen neuen Chat; den Stand bringt der Hook mit.

Mechanismus der Übergänge: Stand-Hook (`prozess/pruefungen/stand.py`).
