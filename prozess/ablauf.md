# Ablauf

## Domänenphase
Der Stand nennt den nächsten Schritt; die Folge steht in `prozess/pruefungen/stand.py`.
1. Planer: Etappen aus dem Ziel; nur die aktuelle ausformuliert. Auslöser: keine Etappe.
2. Architekt: Kritik an der aktuellen Etappe und der Reihenfolge, als Anliegen.
3. Freigabe: „.“ → Koordinator committet `Freigabe Etappe <n>`.
4. Anforderungsautor: die erste Anforderung zur Etappe, Begriffe ins Glossar. Eine genügt.
5. Planer: `handoff/plan.md` (`# Plan · Zyklus <n>`) mit den Items, die bereit sind:
   eins genügt, höchstens drei. Weitere Anforderungen kommen in späteren Zyklen.
6. Kritik: Architekt an Anforderungen und Items; Format und Größe prüfen die Tests.
7. Freigabe: „.“ → Koordinator committet `Freigabe Plan <n>`. Danach Technikphase.

Kritik blockiert nicht: Offene Anliegen stehen in der Freigabevorlage. Budget je Phase in
Rollenläufen (Domäne 8, Technik 10, Prozess 5, `rollenzaehler.py`); darüber entscheidet der
Stakeholder: freigeben, kürzen oder verlängern. Gleichzeitig laufen nur Rollen, die
ausschließlich Anliegen schreiben.

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
