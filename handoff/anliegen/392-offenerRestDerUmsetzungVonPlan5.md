# Offener Rest der Umsetzung von Plan 5

392 · Fragen · von Implementierer (Technik) → Koordinator · Runde 1/3 · erledigt

## Runde 1
**Befund.** Die Token-Schwelle kam vor dem ersten Code. Der Arbeitsbaum ist der des vorigen
Laufs; offen ist alles, was die roten Tests verlangen. Rot sind 66 Tests (ziehen,
gesperrtesModell, zurueckOhneSperre, loslassenOhneZiel, restDerEinheit, beenden,
gesperrteFormation, bedienung, kohaerenz); sperreOhneStelleTest sammelt nicht ein
(`Grund.modelleFehlen` fehlt). auswahlTest: Anliegen 391.

**Kosten.** Ohne den Rest ist Plan 5 nicht abnahmefähig.

**Gegenvorschlag.** Neuer Lauf, in dieser Reihenfolge:
1. `sperre.py`: `Grund` um `modellGesperrt`, `modelleFehlen`, `keineKohärenz`; die
   Reihenfolge der Werte ist die der Gründe in der Antwort (V6).
2. `Aufstellung`: `modellLoslassen`, `einheitLoslassen`, `modellZurücklegen(modell, spieler)`,
   `zurück`, `gesperrt`, `stelleDesGesperrten`, `gründeDesGesperrten`, `inKohärenz`;
   `aufstellenDerEinheitBeenden` sperrt mit `modelleFehlen` und `keineKohärenz` (beide
   zusammen) und `modellGesperrt`. Wächter zuerst (nichtWählbar, einheitBegonnen,
   modellGesperrt), Gründe gegen die Stelle machen beim Loslassen das Modell gesperrt (D2, D4).
3. Neues Modul `Formation` nach `domaene/daten/formation.yaml` (Reihen, Abstand 3/2″,
   Reihenabstand auf 1/100″ aufgerundet, mittig, auf kürzestem Weg in die Zone); AUF-14.1
   holt genau ein Modell; sind alle gesetzt, geschieht nichts (AUF-16.1).
4. Kohärenz (QUE-4): zwei bis fünf Modelle je ein Partner, ab sechs zwei, Abstand höchstens
   2″ über `messen.abstandHöchstens`, dazu zusammenhängend.
5. `zurück` nach AUF-9.3, 9.4, 15.1; ohne gesperrtes Modell ändert es nichts (AUF-17.1).
6. `web/`: Routen und 409 nach V5 und V6 (`sperre.json`); `darstellung.py` mit `einheit`,
   `nummer`, `gesperrt`, `gründeDerGesperrten`.
7. `frontend/`: Mockups auf-8 bis auf-15 ohne Umschreiben, `komponenten.css` aus
   `vorschlag.css` nachziehen, `seite.js` mit Pointer Events (V7, V8).
8. Vertrag nachführen, wo der Code abweicht; V8 sagt für eine Einheit auf einer Ablage
   „keine Anfrage“, Anliegen 390 (Antwort B) verlangt für die Ablage des Gegners ‚nicht
   wählbar‘: Das entscheidet der Architekt mit AUF-16.5.
9. `python3 -m pytest prozess/pruefungen` und die Akzeptanztests.

**Stellungnahme.** Schritte 1 bis 7 und 9 sind umgesetzt: `frontend/` (Mockups auf-8 bis
auf-15 als Vorlagen, `komponenten.css` gleich `vorschlag.css`, `seite.js` mit Pointer Events,
`sperrmeldung`, `knopfGruppe`), Unit-Tests für 400/404 der neuen Routen, `Formation` und
Kohärenz. `python3 -m pytest technik/tests` ist grün (380 Tests). Die Mockups zeigen
zusätzlich „gemeinsam übergehen“; V7 nennt den Knopf nicht, die Seite zeigt ihn nicht.
`python3 -m pytest prozess/pruefungen` war grün (534 Tests).

**Stellungnahme (Architekt).** Schritt 8 ist erledigt: Der Code folgt V5 bis V8; für AUF-16.5
gilt jetzt [V5 und V8](../../technik/architektur/handlungen.md): auf der *Ablage* des anderen
*Spielers* `DELETE /api/spieler/<s>/einheiten/<e>/stelle?ablage=<a>` mit
`einheitAufAblageLoslassen`, auf der eigenen weiter keine Anfrage. Offen bleibt AUF-16.5,
sobald der Stakeholder in Anliegen 394 A wählt:
- Testautor: Akzeptanztest zu AUF-16.5 nach V5 und V8; bis dahin ist die Rückverfolgung rot.
- Implementierer: `einheitAufAblageLoslassen` (eigene *Ablage*: nichts, AUF-16.4; andere:
  *Sperre* ‚nicht wählbar‘), die Route und `ziehenBeenden` in `seite.js`; erst nach dem
  Schnitt aus Anliegen 399, denn `aufstellen.py`
  liegt über dem Höchstmaß.

**Stellungnahme (Implementierer).** Umgesetzt: `Aufstellung.einheitAufAblageLoslassen`
([Aufstellung](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py)), die Route
`DELETE …/einheiten/<e>/stelle?ablage=<a>` ([anwendung.py](../../technik/arbiter/web/anwendung.py))
und `ziehenBeenden` in [seite.js](../../technik/frontend/seite.js). `python3 -m pytest technik/tests`
ist grün (410 Tests), Ruff sauber. Nichts mehr offen.
