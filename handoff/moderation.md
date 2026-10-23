# Moderation

Stand vor „Freigabe Plan 7“. Keine Frage hält die Freigabe auf. Item 1 hängt an den
Kommentar-Anliegen 2540 und 2541; sie warten auf die Technikphase, die mit der Freigabe beginnt.

## Dran
- Stakeholder: nichts außer der Freigabe. Keine offene Frage in den Anliegen.
- Organisationsentwickler (Prozessphase, blockiert Plan 7 nicht):
  [2040](anliegen/2040-pythonUeberBashNachFreigabeRetro6.md) und
  [2140](anliegen/2140-sandboxOeffnetAlleUnixSockets.md), beide abgelehnt, er entscheidet über
  neue Runde oder `erledigt`; [2360](anliegen/2360-es8MechanismusNachziehenUndHakenP5.md) (Es 8).
- Wartend, hält Item 1 auf (Kommentare zuerst, Plan 7):
  - Anliegen 2540 (Implementierer löscht, Architekt
    trägt die sechs Sätze gleichzeitig in die Architektur ein) und
    Anliegen 2541 (Testautor, drei Sätze in
    `web.md`).
  - Anliegen 2450 und
    Anliegen 2440 (Anforderungsautor), danach
    Anliegen 2410 (Planer setzt `angenommen`).
  - [1651](anliegen/1651-auswahlUndAufstellungImplizit.md) und
    [1761](anliegen/1761-loslassenOhneAntwortBleibtInDerVorschau.md) (Implementierer, in Item 1).
- Wartend, hält nicht auf: Implementierer
  [1750](anliegen/1750-testLegtFestWasAuf27AndersRegelt.md),
  [1752](anliegen/1752-stellePrueftFractionSelbst.md),
  [2130](anliegen/2130-goldenerRahmenInKomponentenCss.md),
  [2240](anliegen/2240-leistenInKomponentenseiteEintragen.md); Architekt
  [2215](anliegen/2215-leistenOhneEigenenNamen.md),
  [2251](anliegen/2251-handlungenNachAuf28.md).
- Prozessphase: [2201](anliegen/2201-aenderungenDesStakeholdersVorherErproben.md)
  (Organisationsentwickler), [2460](anliegen/2460-hindernisAbhakenUndCommitBeiLaeufen.md)
  (Regelumsetzer).

## Vorschläge
- Anforderungsautor, ein Lauf: 2450 und 2440 sind dieselbe Änderung (AUF-8.4 löschen, AUF-12
  und AUF-16.8 neu); danach Planer: `angenommen` in 2410 und 2450.
- Zusammen: 2540 und 2541 sind dasselbe Thema (Kommentar löschen, Satz in die Architektur);
  der Architekt trägt beide Seiten in einem Lauf ein, ein Commit nach dem Aufräumen.
  Zusammenlegen dürfen nur die Absender; die Empfänger (Implementierer, Testautor) bleiben getrennt.
- Architekt, ein Lauf: 2251, die AUF-8.4-Zeile aus 2410 und die Einträge zu 2540/2541 berühren
  `handlungen.md`, `web.md`; 2215 gehört zu den Leisten wie 2240.
- Implementierer: 2130 und 2240 zusammen (`komponenten.css`); 1651 und 1761 im Lauf von Item 1;
  1750 und 1752 getrennt davon.
- Organisationsentwickler: 2140 ist gegenstandslos (Sandbox entfällt, 1970); der Absender
  schließt. 2040 bleibt als weiterer Beleg gegen [Ich 2](../prozess/praemissen/ich.md) für Retro 7;
  2201 gehört mit dem zweiten Fall in dieselbe Retro.
- 2360 Teil 2: Das Entfernen der `# Regel:`-Kommentare deckt Item 1 in [Plan 7](plan.md) ab,
  zusammen mit 2540 und 2541; Es 8 ändert der Organisationsentwickler erst in der Prozessphase.
- Stränge Technikphase 7: Implementierer und Testautor löschen gleichzeitig (getrennte Dateien),
  der Architekt trägt gleichzeitig ein; danach je Item die Kette Architekt (Vertrag), Testautor,
  Kritiker, Implementierer. Parallel zur Kette nur 2215 und 2251 (Architekt) vorher. Prozess:
  Organisationsentwickler und Regelumsetzer getrennt, nur ein Lauf mit Hook-Code.

## Fragen an dich
Keine offenen Fragen (`F<n>`) in den Anliegen.

Annahme im Plan, nicht in einem Anliegen: Der Planer nimmt die 40 Kommentare `Warum:` zu den
38 `Regel:` hinzu, weil [Es 8](../prozess/praemissen/es.md) sie ebenso verbietet. Sollen sie
bleiben, braucht Es 8 eine Ausnahme; sag es mit deiner Freigabe.
