# Mockups ohne „in Aufstellung“, ohne Sperrbild für Base und Nahkampfreichweite

988 · Kritik · von Ux → Planer · Runde 2/3 · erledigt

## Runde 1
**Anweisung des Stakeholders.** In der *Ablage* braucht es keinen Hinweis „in Aufstellung“.
„Base überdeckt“ und „in Nahkampfreichweite“ sind Randfälle ohne Sinn; ArbiterMap klemmt
ein *Modell*, das auf eine *Base* gezogen wird (`ArbiterMap/backend/app/domain/deployment.py:17`,
`ArbiterMap/frontend/static/js/model_drag.js:14`).

**Stellungnahme.** Umgesetzt, kein Widerspruch.
1. Das Abzeichen „in Aufstellung“ ist aus allen Bildern entfernt. Die *Einheit* zeigt wie die
   anderen ihre Zahl der *Modelle*; ausgewählt ist sie am goldenen Rahmen.
2. `auf-19` ist gelöscht: Es zeigte nur „Base überdeckt“ mit „zurück“. Ein geklemmtes *Modell*
   sieht aus wie ein gesetztes, das zeigt schon [auf-18](../../domaene/mockups/auf-18.html).
3. [que-7](../../domaene/mockups/que-7.html) (Plan 7) zeigt nur noch „nicht ganz in der Zone“.

**Dateien je Item.**
- Item 1 [Setzen per Klick](../../domaene/items/setzenPerKlick.md):
  [auf-18-ausgewaehlt](../../domaene/mockups/auf-18-ausgewaehlt.html),
  [auf-18](../../domaene/mockups/auf-18.html). Der Link auf `auf-19` in der Zeile Mockup
  gehört gestrichen.
- Item 2 [Einheit und Modell verschieben](../../domaene/items/einheitVerschieben.md):
  [auf-20](../../domaene/mockups/auf-20.html), [auf-21](../../domaene/mockups/auf-21.html).
- Item 3 [Gewinner und Zone](../../domaene/items/gewinnerUndZone.md): unverändert
  [auf-11-rolloff](../../domaene/mockups/auf-11-rolloff.html),
  [auf-11-gewinner](../../domaene/mockups/auf-11-gewinner.html),
  [auf-11-zone](../../domaene/mockups/auf-11-zone.html).

**Offen für Planer und Anforderungsautor.**
1. Item 1 nennt AUF-19.1, 19.2, 19.4 im Umfang und [Plan 6](../plan.md) den *Grund* für
   *Base* und *Nahkampfreichweite*; beides folgt der Anweisung nicht mehr. Die Kriterien
   (AUF-19.1 mit QUE-1.2, 1.3) sind ihre Sache.
2. Die Klassen `inAufstellung` und `einheitenKartenAbzeichen` in `vorschlag.css` sind jetzt
   unbenutzt; der Architekt entscheidet beim Einbau der Komponentenseite.

## Runde 2
**Befund.** Kommentar des Stakeholders: „Roll-off gewonnen“ ist nicht erforderlich, Spieler 2
hat bis auf Weiteres gewonnen und ist „an der Reihe“; viele Mockups sehen gleich aus.

**Stellungnahme.** Umgesetzt. Gestrichen sind
[auf-11-rolloff](../../domaene/mockups/auf-11-rolloff.html) (nur der Knopf unterschied es von
auf-11-gewinner), `auf-23` (Byte für Byte gleich auf-18-ausgewaehlt) und `auf-20` (gleiche
Lage wie auf-18, nur der Block weiter oben). [auf-11-gewinner](../../domaene/mockups/auf-11-gewinner.html)
zeigt Spieler 2 „an der Reihe“, die Zonen noch ohne Spieler. Offen für den Planer: Die
Zeilen Mockup in `domaene/items/gewinnerUndZone.md` (auf-11-rolloff) und
`domaene/items/einheitVerschieben.md` (auf-20) verlinken Gestrichenes. Der Plan nennt kein
Mockup beim Namen.

**Stellungnahme (Planer).** Angenommen, umgesetzt. [Einheit und Modell verschieben](../../domaene/items/einheitVerschieben.md)
nennt nur noch [auf-21](../../domaene/mockups/auf-21.html),
[Gewinner und Zone](../../domaene/items/gewinnerUndZone.md) auf-11-gewinner und auf-11-zone.
Der Stakeholder hat in Anliegen 990 F1 A gewählt: Arbiter startet wie gebaut mit verteilten
Zonen, Spieler 2 *an der Reihe*. Item 3 ist deshalb nicht in [Plan 6](../plan.md); seine zwei
Mockups zeigen die Wahl am Bildschirm, die später kommt, und gehören zu keinem Schritt von
Plan 6. Die Stellungnahme im Plan verweist für die gleichen Mockups auf dich.
