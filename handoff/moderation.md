# Moderation

Stand: Technikphase 10, Plan 10 freigegeben ([Plan](plan.md)). 24 Anliegen offen, 14 sind seit
dem letzten Stand gelöscht (nicht committet). Beim Stakeholder liegt nichts.

## Dran
Blockiert das Inkrement (Items 1 und 2 in [Plan](plan.md), Vertrag beider steht):
- Fachkritiker: Kritik an den Tests zu Item anhaltenUebergehen, mit
  Anliegen 7641 (angenommen, nachprüfen).
- Architekt: Kritik an denselben Tests, mit
  Anliegen 7661; dazu
  Anliegen 8740 nachprüfen und
  Anliegen 10560 beantworten (V18).
- Testautor: Tests zu Item loslassenNebenDerKarte, mit
  Anliegen 7601,
  Anliegen 8720.
- Implementierer: Tests zu Item anhaltenUebergehen grün, sobald die Kritik durch ist
  (mit Anliegen 8261).

Dran, hält nichts auf:
- Implementierer: Anliegen 10880 samt
  Anliegen 10900; Anliegen 10561.
- Planer: Anliegen 10380 und
  Anliegen 10860 sind angenommen; die Absender
  prüfen nach (Testautor-Lauf bzw. Reviewer).
- Anforderungsautor: Anliegen 10540,
  Anliegen 10180,
  Anliegen 9340 (Daten vor Item 4 und 5),
  Anliegen 7800 (angenommen).
- Regelumsetzer: Anliegen 8021 (wartet auf 8020, das
  gelöscht ist: Wartet-Zeile prüfen), [8860](anliegen/8860-dashboardLangsamUndUnuebersichtlich.md),
  [9801](anliegen/9801-wartendeZeileNachDemLoeschen.md) in der Prozessphase.
- Übrige warten auf Technikphase 11 oder Domänenphase 11
  ([10120](anliegen/10120-uebergehenNichtAmZugFolgen.md),
  [10201](anliegen/10201-uebergehenInDerNahkampfreichweiteUndAnDerKante.md),
  [10322](anliegen/10322-zuruecksetzenAufBesetzteStellen.md),
  [10720](anliegen/10720-katalogMeldungOhneNameUndEintragDoppeltBelegt.md),
  [10861](anliegen/10861-gegnerHinUndZurueck.md)).

## Vorschläge
1. **10880 Punkt 2 und 10900 (doppelt):** Beide wollen die Meldung in `Aufstellung.auswählen`
   mit „Armeeliste“ statt „Einheitenkarte“. 10880 trägt sie mit Punkt 1 in einem Lauf;
   Implementierer setzt 10900 auf `angenommen` mit Verweis auf 10880 Punkt 2, Reviewer prüft
   nach und setzt `erledigt`. Dazu: 10900 wartet auf „Technikphase 11“, 10880 auf
   „Technikphase“ ohne Nummer; Architekt setzt 10880 auf 10 (Plan führt es dort), Reviewer
   10900 ebenso.
2. **Zusammen:** 8261 und 8641 (`schlachtrunden.py`); 7601 und 8720 (Auswahl in der Schlacht);
   7151 und 8971 (Katalog); 10560 und 10561 (dritte Einheit im Katalog).
3. **7800:** Schon `angenommen`, nur noch Umbenennung im Code; Aufräumen nach Plan 10.

### Stränge (Technikphase 10)
- Kette: Tests anhaltenUebergehen (Kritik Fachkritiker und Architekt) → Implementierer
  Item 1 (mit 8261) → Item 3 (mit 9401). Item 2 vor Item 3; 1 und 2 nur gleichzeitig, wenn
  `git status` getrennte Dateien zeigt.
- Testautor: Item 2 (7601, 8720, BEW-11.3); daneben 7151 → 8971, 9401 später; 10380 liegt
  vor Items 4 und 5.
- Implementierer, daneben: 10880 mit 10900 (`auswahl.py`, `aufstellen/__init__.py`, `schlachtrunden.py`;
  nicht neben 8261/8641 in derselben Datei), 10561; 8041 erst nach Item 3.
- Fachkritiker, Architekt, Anforderungsautor: schreiben nur Anliegen und Kritik, laufen daneben.
- Regelumsetzer: Hook-Code höchstens einer.

## Fragen an dich
Keine offene. [8860](anliegen/8860-dashboardLangsamUndUnuebersichtlich.md) F1 bis F3 sind
beantwortet; Runde 2 wartet auf die Prozessphase.
