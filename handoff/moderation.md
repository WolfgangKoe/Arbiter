# Moderation

Stand e079472, nach Retro 10. 58 Anliegen offen, 47 warten auf Domänenphase 11 (15) oder
Technikphase 11 (32). Nichts blockiert ein Inkrement: [Plan](plan.md) 10 ist umgesetzt, Plan 11
gibt es noch nicht.

## Dran
- Prozessphase jetzt: Organisationsentwickler 14500, 15361; Regelumsetzer 16240, 16380, 8860;
  Nachprüfung: Organisationsentwickler 16440, 9801; Regelumsetzer 16340, 16400; Testautor 13150;
  Stakeholder 15960.
- Domänenphase 11, Anforderungsautor: 16150, 16101, 10322, 15461, 10201, 14320, 10120, 15100,
  15300, 16080, 16241. Fachkritiker: 15220. Planer: 16171, 13842. UX: 15261.
- Technikphase 11, Implementierer: 10720, 10861, 11860, 11880, 12681, 12702, 12904, 12962,
  12963, 13400, 13520, 13540, 13640, 13661, 13761, 14240, 14261, 14740, 15020, 15280, 15320.
  Testautor: 11000, 11381, 12021, 12041, 13051, 13301, 13320, 14482, 15260, 15281, 15721.

## Vorschläge
Obsolet scheinen, je Empfänger, der es beurteilt (`angenommen` mit Verweis, der Absender schließt):
1. **Anforderungsautor:** [16101](anliegen/16101-angebotNachDerSperreBeimUebergehen.md): Der
   Stakeholder hat in 16100 entschieden, dass eine *Base* nie überdeckt; [16150](anliegen/16150-basesNieUeberdeckt.md)
   streicht BEW-18.6, und 16101 sagt selbst, dann erübrige es sich. Absender Planer.
2. **Anforderungsautor, erst nach [15461](anliegen/15461-uebergehenDannFolgtDemZeiger.md):** Fasst
   er BEW-8.4 neu (die *Modelle* folgen dem Zeiger), ist neu zu beurteilen, ob 10201 Punkt 1,
   14320 und 10120 Punkt 1 noch gelten; sie handeln vom Weiterziehen nach dem Übergehen.
3. **Implementierer:** [12963](anliegen/12963-startIstNurEinZweiterNameFuerEbene.md): `start`
   steht in `phasen/bewegung/` nicht mehr im Code. Absender Reviewer.
4. **Implementierer, Doppel:** 13540 = 13520 Punkt 2; 12904 = 11860 Punkt 1 und mit 12681
   Punkt 2 gemeinsam; 14261 Punkt 2 = 12702 Punkt 2.
5. **Implementierer, teils erledigt, Rest bleibt:** 12681 Punkt 2 (`Gezogen` statt sechs
   Parameter), 12702 Punkt 4 (`stellenNachV16` fort), 12904 und 12962 (Angebot nimmt
   `hältAnDerGrenze` aus `gezeigt`, kein `noqa` mehr). Zum Rest: 11860, 11880, 12681 Punkt 3,
   11000, 11381, 15721 Punkt 2 betreffen den Code und die Tests von BEW-8 und BEW-25, die 15461
   neu fasst; nach der Domänenphase prüfen, ob sie ersetzt werden.
6. **Testautor:** 13320 Punkt 1 teils erledigt (Geometrie liegt zum Teil in `ruecken.py`).
7. Alle übrigen Anliegen stimmen mit dem Stand überein (Stichproben im Code, nicht jede Zeile).
8. **Zusammen:** 16150 mit 10322 (Zurücksetzen auf besetzte Stelle); 15100 mit 15220; 15300
   mit 15280, 15281, 15260 (ein Umbenennen der Tests nach dem Glossar); 16080 mit 16241
   (Ordner und Wörter des Ziehens).

### Stränge
- Anforderungsautor, eine Kette je Datei, daneben nichts in denselben Dateien: (a) 16150, 16101,
  10322, 16241; (b) 15461, dann 10201, 14320, 10120; (c) 15100, 15220, 15300; (d) 16080.
  16171 schreibt rund 86 Kriterien um, auch BEW-8; ich empfehle: nach (b), sonst steht BEW-8
  zweimal an (Planer entscheidet).
- UX 15261 und Planer 13842: daneben, eigene Dateien.
- Implementierer: eine Kette im Code der Bewegung (11860 bis 12962, 13400 bis 15320); 10720,
  13520, 13540 (Katalog) und 14740 (CSS) daneben.
- Testautor: eine Kette je Testdatei (14482, 12021 bis 13320, 15260, 15281, 15721).

## Fragen an dich
Offen im Anliegen: [16380](anliegen/16380-arbeitsbaumUnterClaudeWorktrees.md) F1. Der
Regelumsetzer hat deine Rückfrage geklärt; wähle A oder B. Weitere Fragen stellt der
Anforderungsautor in der Domänenphase 11 (15461, 16080, 10322).
