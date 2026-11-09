# Moderation

Stand: vor Freigabe Retro 10 ([Retro](retro.md)), nachkorrigiert, beide Kritiker haben
abgehakt. 60 Anliegen offen. Die Technikphase 10 ist bis auf Item 6 durch
([Plan](plan.md): offen nur 14482). Nichts blockiert das Inkrement mehr.

## Dran
- Stakeholder: [15820](anliegen/15820-absichtPunktParallel.md) F1 (wo der neue Absichtspunkt
  steht). [14360](anliegen/14360-parallelArbeitenIstDieRegel.md) F1 ist mit B beantwortet und
  wartet auf 15820.
- Koordinator: [11100](anliegen/11100-teilCommitScheitertBeiLaufenderRolle.md) (in P4),
  [13580](anliegen/13580-planFliegenRest.md) (Plan für den Rest von fliegen).
- Testautor: 14482 (Plan-Item, zuerst), dann
  [15462](anliegen/15462-mutationZyklus10Ueberlebende.md); daneben laufen 15720 und 15680.
  Nachprüfung fällig: Architekt 15720, Reviewer 15462.
- Regelumsetzer, Prozessphase nach der Retro: P2, P3, P5, P6 mit 12520, 15301, 11500, 12900,
  13102, 13420, 15361, 9801, 13150 (ohne Wartet-Zeile, dran), dazu
  [8860](anliegen/8860-dashboardLangsamUndUnuebersichtlich.md) Runde 2.
- Organisationsentwickler: P1, P4 mit 14500, 15301, 15361, 12520, 12900, 11500. 14360 und
  15820 erst nach deiner Antwort: Er verweist in P4 auf den Punkt und schließt.
- Anforderungsautor, Domänenphase 11: 10120, 10201, 10322, 14320, 15100, 15300, 15461.
  Fachkritiker: 15220; Planer: 13842; UX: 15261.
- Implementierer und Testautor, Technikphase 11: übrige Kritiken, nichts hält auf.

## Vorschläge
1. **Doppel, der Implementierer setzt den späteren auf `angenommen` mit Verweis, der Absender
   prüft nach:** 13540 = 13520 Punkt 2; 13661 Punkt 1 = 13640 Punkt 3.
2. **Vermutlich dasselbe Thema, in Technikphase 11 gemeinsam vorlegen:**
   [14240](anliegen/14240-fliegenDoppelteTypenUndImportUeberFliegen.md) und
   [14261](anliegen/14261-fliegenUmgebungUndWeiteGehoerenZuFliegen.md). Nur nach Titeln,
   im Text nicht geprüft: 11860 und 11880; 12904 und 12962; 12681 und 12702; 13400 und 15320;
   15280 und 15281; 10120 und 15461; 10201 und 14320. Der Empfänger prüft und setzt bei einem
   Doppel `angenommen` mit Verweis.
3. **Ein Lauf des Anforderungsautors:** 15220 und 15300 (Link, Überschrift nach Umbenennen);
   13842 (Höchstmaß der Testdateien, kein Item) legt nur Entscheidungen ab.
4. **Prozess-Items:** 12520, 15301 zu P2; 11500, 12900, 13102, 13420 zu P3; 14360, 11100,
   14500, 15820 zu P4; 15361, 9801, 13150 zu P5. Der Empfänger setzt `angenommen`, wenn sein
   Item steht; der Absender schließt.
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
1. [15820](anliegen/15820-absichtPunktParallel.md) F1, mit `Annahme:` (P4 verweist auf
   Absicht 7). Wo steht der neue Punkt: A als Punkt 7 am Ende, B als Punkt 3. Empfehlung A:
   keine Nummer ändert sich. Du änderst danach
   [absicht.md](../prozess/praemissen/absicht.md) selbst und setzt im Anliegen `angenommen`.
   Sonst ist nichts offen.
