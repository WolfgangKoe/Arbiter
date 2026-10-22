# Moderation

Stand vor „Freigabe Plan 7“. Nichts hält die Freigabe auf; alle Kritiken am Plan sind
beantwortet oder warten auf die Technikphase.

## Dran
- Stakeholder: nichts. Keine offene Frage, keine Nachprüfung.
- Organisationsentwickler (Prozessphase, blockiert Plan 7 nicht): [2040](anliegen/2040-pythonUeberBashNachFreigabeRetro6.md)
  und [2140](anliegen/2140-sandboxOeffnetAlleUnixSockets.md), beide abgelehnt, er entscheidet
  über eine neue Runde oder `erledigt`; [2360](anliegen/2360-es8MechanismusNachziehenUndHakenP5.md)
  (Es 8 ändert er erst in der Prozessphase).
- Wartend nach Phase:
  - Technik, hält Item 1 auf: [2450](anliegen/2450-auf8_4SchonMitItem1.md) und
    [2440](anliegen/2440-auf8_4FolgenFuer12und16_8.md) (Anforderungsautor, Schritt des
    Testautors), danach [2410](anliegen/2410-auf8_4MitAufraeumenStattUmbenennen.md) (Planer
    setzt `angenommen`); [1651](anliegen/1651-auswahlUndAufstellungImplizit.md) und
    [1761](anliegen/1761-loslassenOhneAntwortBleibtInDerVorschau.md) (Implementierer, `seite.js`
    und Auswahl liegen in Item 1).
  - Technik, hält nicht auf: [1750](anliegen/1750-testLegtFestWasAuf27AndersRegelt.md),
    [1752](anliegen/1752-stellePrueftFractionSelbst.md) (Implementierer);
    [2130](anliegen/2130-goldenerRahmenInKomponentenCss.md),
    [2240](anliegen/2240-leistenInKomponentenseiteEintragen.md) (Implementierer);
    [2215](anliegen/2215-leistenOhneEigenenNamen.md),
    [2251](anliegen/2251-handlungenNachAuf28.md) (Architekt).
  - Prozess: [2201](anliegen/2201-aenderungenDesStakeholdersVorherErproben.md)
    (Organisationsentwickler), [2460](anliegen/2460-hindernisAbhakenUndCommitBeiLaeufen.md)
    (Regelumsetzer, Item der Retro 7).

## Vorschläge
- Anforderungsautor, ein Lauf: 2450 und 2440 sind dieselbe Änderung (AUF-8.4 löschen, AUF-12
  und AUF-16.8 neu); danach setzt der Planer `angenommen` in 2410 und 2450.
- Architekt, ein Lauf: 2251 und die AUF-8.4-Zeile in `handlungen.md` aus 2410 berühren
  dieselbe Datei; 2215 mit 2240 verwandt (Leisten), aber 2240 gehört dem Implementierer.
- Implementierer: 2130 und 2240 zusammen (`komponenten.css`); 1651 und 1761 im Lauf von
  Item 1; 1750 und 1752 getrennt davon.
- Organisationsentwickler, Prozess: 2140 ist gegenstandslos (Sandbox entfällt, 1970) und kann
  er `erledigt` setzen. 2040 bleibt: Der Anforderungsautor hat bei 2440 und 2450 Stellungnahmen
  erneut per Python-Skript über Bash geschrieben (Hinweis des Koordinators, nicht von mir
  geprüft); das ist ein weiterer Beleg gegen [Ich 2](../prozess/praemissen/ich.md) für die
  Retro 7. 2201 gehört mit dem zweiten Fall (Sandbox) in dieselbe Retro.
- 2360, Teil 2: Das Entfernen der `# Regel:`-Kommentare unter `technik/` fehlt in
  [Plan 7](plan.md); ohne sie ist die DoD ab Technikphase 7 rot. Der Planer kann es als Teil von
  Item 1 aufnehmen, oder der Stakeholder schiebt es (siehe Fragen: keine, nur Hinweis).
- Stränge Technikphase 7: Kette Architekt (Vertrag) → Testautor → Kritiker → Implementierer
  je Item. Gleichzeitig zur Kette dürfen nur die nicht blockierenden Anliegen
  (Implementierer 2130/2240 nach Item 1, Architekt 2215/2251 vorher). Prozessphase:
  Organisationsentwickler und Regelumsetzer getrennt, nur ein Lauf mit Hook-Code.

## Fragen an dich
Keine offenen Fragen, keine `Annahme:`. Die Annahme im Plan („Etappen 1 und 2 gelten, wie sie
stehen“) beantwortet dein „.“ zur Freigabe.
