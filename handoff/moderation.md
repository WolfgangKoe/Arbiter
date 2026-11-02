# Moderation

Stand: Domänenphase 10, Plan 10 wartet auf Kritik und Freigabe ([Plan](plan.md)). 38 Anliegen
offen, 36 warten auf eine Phase oder ein Anliegen, 10480 ist beim Stakeholder.

## Dran
Blockiert das Inkrement (Item 5, [DoR 6](../prozess/ablauf/dor.md)):
- Stakeholder: [10480](anliegen/10480-zuruecksetzenMitOderOhneRueckfrage.md) F1, kannst du mit
  der Freigabe beantworten; ohne Antwort gilt A.
- Anforderungsautor: [10400](anliegen/10400-zuruecksetzenOhneRueckfrage.md) wartet auf 10480;
  danach Quelle an BEW-24.1 (A) oder Kriterium und Mockup für den Dialog (B).
- Fachkritiker: „Kritik am Plan“ bleibt offen, bis 10400 erledigt ist. Mit A geschieht das
  nach der Freigabe; er darf den Haken dann setzen.

Dran, hält nichts auf:
- Planer: Plan, Abschnitt „Offene Anliegen“, nennt 10320 und 10340; beide sind erledigt und
  haben keine Datei mehr. Streichen, dazu [10180](anliegen/10180-etappe2LueckenNachPlan10.md) und
  [9340](anliegen/9340-fliegenDerSpinne.md) prüfen: Beide tragen `Wartet auf: Technikphase 10`,
  der Plan führt 10180 aber als Schritt des Anforderungsautors.
- Koordinator: Gelöschte Datei 10420 ist noch nicht committet.
- Regelumsetzer: [8860](anliegen/8860-dashboardLangsamUndUnuebersichtlich.md),
  [9801](anliegen/9801-wartendeZeileNachDemLoeschen.md), 8021 (wartet auf 8020), alle später.
- Alle übrigen Anliegen warten auf Technikphase 10 oder Domänenphase 11
  ([10120](anliegen/10120-uebergehenNichtAmZugFolgen.md),
  [10201](anliegen/10201-uebergehenInDerNahkampfreichweiteUndAnDerKante.md),
  [10322](anliegen/10322-zuruecksetzenAufBesetzteStellen.md)).

## Vorschläge
1. **Zusammen:** 7050 und 7681 (derselbe Test); 7191 und 7201; 8620 und 8740;
   7401 und 8421 (`anhaltenVorDerGrenzeTest.py`); 7641 und 7661. Je ein Lauf der
   Empfängerrolle.
2. **10400 und 10480:** Gehören zusammen; 10480 trägt die Entscheidung, 10400 schließt der
   Anforderungsautor danach (`angenommen`). Nur er darf es.
3. **9890:** Architekt fasst V18 vor den Tests zu Item 1, im Vertrag zu Item anhaltenUebergehen
   ([9890](anliegen/9890-v18NachBew8Nachziehen.md)).
4. **7800:** Schon `angenommen`, wartet auf die Technikphase; Aufräumen nach Plan 10.

### Stränge (Technikphase 10)
- Kette: Architekt (9890, Vertrag) → Testautor Item 1 (mit 7321) → Implementierer Item 1
  (mit 8261) → Item 3 (mit 9401). Item 2 vor Item 3; 1 und 2 nur gleichzeitig, wenn `git status`
  getrennte Dateien zeigt. Fixtures
  [10380](anliegen/10380-fixturesDritteEinheit.md) (Testautor) neben Item 1, vor Items 4 und 5.
- Testautor, daneben: Katalog (7151 → 8971, nach Implementierer 7191, 7201); Leisten 7301;
  Grenzkreise (7641, 7661, 7401, 8421); Auswahl 7601, 8720 nach Implementierer 8100, 8121;
  7072.
- Implementierer, daneben: Verschieben (7042, 7050, 7681, 8020); 8620 → 8740; 8641 nach 8261
  (`schlachtrunden.py`, auch 8100). 8041 erst nach Item 3 (gleiche Einheitstests).
- Regelumsetzer: Hook-Code höchstens einer.

## Fragen an dich
Zuoberst mit Annahme:
- [10480](anliegen/10480-zuruecksetzenMitOderOhneRueckfrage.md) F1: Wie setzt man eine gezogene
  Einheit zurück? Annahme: BEW-24 und bew-24 bleiben (A, ein Klick ohne Rückfrage).
  Empfehlung A.
