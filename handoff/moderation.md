# Moderation

Stand: vor Freigabe Retro 10 ([Retro](retro.md)). 56 Anliegen offen. Die Technikphase 10 ist
bis auf Item 6 durch ([Plan](plan.md): offen nur 14482). Nichts blockiert das Inkrement mehr.

## Dran
- Stakeholder: [14360](anliegen/14360-parallelArbeitenIstDieRegel.md) F1 (Rückfrage).
- Koordinator: [11100](anliegen/11100-teilCommitScheitertBeiLaufenderRolle.md) (in P4),
  [13580](anliegen/13580-planFliegenRest.md) (Plan für den Rest von fliegen).
- Testautor: 14482 (Plan-Item, zuerst), dann
  [15462](anliegen/15462-mutationZyklus10Ueberlebende.md) (ohne Wartet-Zeile).
- Regelumsetzer, Prozessphase nach der Retro: P2, P3, P5, P6 mit 12520, 15301, 11500, 12900,
  13102, 13420, 15361, 9801, 13150 (ohne Wartet-Zeile, dran), dazu
  [8860](anliegen/8860-dashboardLangsamUndUnuebersichtlich.md) Runde 2.
- Organisationsentwickler: P1, P4 mit 14500, 14360.
- Anforderungsautor, Domänenphase 11: 10120, 10201, 10322, 14320, 15100, 15300, 15461.
  Fachkritiker: 15220; Planer: 13842; UX: 15261.
- Implementierer und Testautor, Technikphase 11: übrige Kritiken, nichts hält auf.

## Vorschläge
1. **Doppel, der Implementierer setzt den späteren auf `angenommen` mit Verweis, der Absender
   prüft nach:** 13540 = 13520 Punkt 2; 13661 Punkt 1 = 13640 Punkt 3.
2. **Vermutlich dasselbe Thema, in Technikphase 11 gemeinsam vorlegen:**
   [14240](anliegen/14240-fliegenDoppelteTypenUndImportUeberFliegen.md) und
   [14261](anliegen/14261-fliegenUmgebungUndWeiteGehoerenZuFliegen.md). Nur nach Titeln,
   im Text nicht geprüft: 11860 und 11880 (Übergehen doppelt gerechnet); 12904 und 12962
   (Angebot); 12681 und 12702 (Gleiten); 13400 und 15320 (doppelt geprüft); 15280 und
   15281 (alte Ebene in Tests und ids); 10120 und 15461 (Modelle folgen dem Zeiger);
   10201 und 14320 (Weiterziehen aus der Nahkampfreichweite). Der Empfänger prüft und
   setzt bei einem `angenommen` mit Verweis.
3. **Ein Lauf des Anforderungsautors:** 15220 und 15300 (Link, Überschrift nach Umbenennen);
   13842 (Höchstmaß der Testdateien, kein Item) legt nur Entscheidungen ab.
4. **Prozess-Items:** 12520, 15301 zu P2; 11500, 12900, 13102, 13420 zu P3; 14360, 11100,
   14500 zu P4; 15361, 9801, 13150 zu P5. Der Empfänger setzt `angenommen`, wenn sein Item
   steht; der Absender schließt.
5. **Schließen:** nichts, keines ist `angenommen`.

### Stränge
- Regelumsetzer: P3, P2, P4, P5, P6 als Kette (Hook-Code höchstens einer).
- Organisationsentwickler: P1 und P4 schreiben nur Text und laufen daneben.
- Testautor: 14482, dann 15462 (Testdateien); die Hilfen-Anliegen (12041, 13051, 13320,
  15260) je Testdatei in einem Lauf.
- Implementierer: Fliegen (13520 bis 15320) als eine Kette; Übergehen (11860, 11880) daneben
  nur bei getrennten Dateien nach `git status`.
- Anforderungsautor, Fachkritiker, Planer, UX schreiben nur Anliegen und Anforderungen: daneben.

## Fragen an dich
1. [14360](anliegen/14360-parallelArbeitenIstDieRegel.md) F1, mit `Annahme:` (bis zur
   Prozessphase ändert sich keine Regel). Empfehlung B; Retro 10 verweist darauf.
