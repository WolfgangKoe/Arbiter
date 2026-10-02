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
