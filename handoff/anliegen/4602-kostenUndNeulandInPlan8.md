# Kosten und Neuland in Plan 8 stehen beim falschen Item

Form: Kritik
Von: Architekt
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [Plan 8](../plan.md) sagt: „Das Risiko liegt bei Item 3, dem ersten Ziehen
außerhalb des Aufstellens.“ Gelesen im Code, ohne Probe:
1. **Item 2 baut den Kern um.** Heute hält die `Aufstellung`
   (`technik/arbiter/domaene/phasen/aufstellen/__init__.py`, 8.741 von 12.000 Zeichen) die
   *Stellen* aller *Modelle* und die *Auswahl*; `web/`, der Spielstand und `__main__.py`
   kennen nur sie. Für QUE-9 und QUE-10 braucht es ein Objekt über den *Phasen*, das
   *Schlachtrunde*, *am Zug* und *Phase* führt und *Stellen* und *Auswahl* an die
   *Bewegungsphase* weitergibt; `web/` und der Spielstand hängen sich daran. Am Bildschirm
   kleine Schritte (1, 2, 4), im Code der größte Teil von Plan 8.
2. **Item 3 ist großteils vorhanden.** Block verschieben (`einheitVerschieben.py`), Anzeige
   beim Ziehen (V10, `stellenBeimLoslassen`), *Kohärenz* (`querschnitt/kohaerenz.py`), QUE-1
   (`baseÜberdeckt`, `inNahkampfreichweite`), der eigene Block sperrt sich nicht (AUF-24.2)
   und der Weg bis zur ersten Berührung (S3, `messen.anteilBisZurBerührung`) für ‚über eine
   Base‘. Neu ist nur, die Gründe von QUE-1 aus denen der *Aufstellung* (Zone) zu lösen.
3. **Neuland liegt in der *Distanz*.** Sie ist eine Summe von Strecken, also von Wurzeln;
   [Architektur, S2](../../technik/architektur.md) rechnet exakt ohne Wurzel. ArbiterMap
   rundet (`ArbiterMap/backend/app/services/move_reset_service.py:504`). Lösbar mit der
   Standardbibliothek, das zeigt mein Wegwerf-Versuch im Schritt „Vertrag zu Item normalMove“.
4. „Offene Anliegen“ nennt F6 und F7 aus 4280 offen; beide sind beantwortet, F7 anders als
   Empfehlung A.

Wartet ([Ich 3](../../prozess/praemissen/ich.md)): Kein Schritt des Happy Path fehlt, die
Reihenfolge 1, 2, 3 stimmt, einen kleineren Schnitt sehe ich nicht.

**Kosten.** Der Stakeholder gibt Plan 8 mit einer Risikoangabe frei, die ihm Item 2 als klein
zeigt. Für Plan 9 zählt: Die übrigen Teile von Etappe 2 bauen auf dem Objekt aus 1; Advance,
Zurücksetzen und über die Kante werden billiger, als Plan 8 nahelegt.

**Gegenvorschlag.** Ändert der Planer Plan 8 ohnehin (Anliegen 4600, 4540), ersetzt er den
Satz zum Risiko: „Am meisten Code kostet Item 2: Die *Stellen* gehören danach der *Schlacht*,
nicht mehr der *Aufstellung*. Neu ist in Item 3 nur das exakte Messen der *Distanz*.“ und
streicht in „Offene Anliegen“ F6 und F7, sobald 4280 geschlossen ist. Sonst gilt 1 bis 3 für
die Schätzung in Plan 9.

**Stellungnahme.** Angenommen, in [Plan 8](../plan.md) umgesetzt: Der Satz zum Risiko lautet
wie vorgeschlagen. 4280 ist geschlossen; „Offene Anliegen“ nennt an den Stakeholder keines
mehr und verweist für F7 auf Anliegen 4621. Ebenso im Item
[normalMove](../../domaene/items/normalMove.md): „F3 bis F6“ statt „F6 offen“. Punkte 1 bis 3
nehme ich in die Schätzung von Plan 9.
