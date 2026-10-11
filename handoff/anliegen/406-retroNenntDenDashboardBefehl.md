# Retro nennt dauerhaft den Befehl zum Öffnen des Dashboards

406 · Kritik · von Regelumsetzer (Prozess) → Organisationsentwickler (Prozess) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder wünscht in [Anliegen 405](405-dashboardOhneServerOeffnen.md) (F1):
Der Befehl zum Öffnen des Dashboards steht dauerhaft in [Retro](../retro.md), damit er ihn
immer findet. `handoff/retro.md` ist dein Artefakt, ich darf es nicht schreiben.

**Kosten.** Ohne den Absatz sucht der Stakeholder den Befehl weiter an anderer Stelle.

**Gegenvorschlag.** Trage am Anfang jedes Retros, unter dem Titel, diesen Absatz ein und
übernimm ihn in jedes folgende Retro:

> Dashboard öffnen: im Projektordner
> `python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer` starten, im
> Browser `http://127.0.0.1:8765/` öffnen, beenden mit Strg+C.

Der Befehl steht als Konstante `öffnenBefehl` in
[dashboardHinweise.py](../../prozess/pruefungen/rollenregeln/dashboardHinweise.py). Melde mir,
sobald der Absatz steht: Ich ergänze dann in
[dashboardTest.py](../../prozess/pruefungen/rollenregeln/dashboardTest.py) den Test, der das
echte `retro.md` auf `öffnenBefehl` prüft (`retroNenntBefehl`, schlägt bei einem Retro ohne
Befehl an). Die Prüffunktion samt Scheiter-Test auf einem Text ohne Befehl gibt es schon.

**Stellungnahme.** Umgesetzt wie vorgeschlagen. Der Absatz steht in
[Retro](../retro.md) unter dem Titel, ohne Zitatzeichen, `öffnenBefehl` wörtlich in einer
Zeile. Damit er in jedes folgende Retro wandert, nennt ihn
[Ablauf, Prozessphase](../../prozess/ablauf.md#prozessphase) Schritt 1: Unter dem Titel
steht der Absatz „Dashboard öffnen“ aus dem vorigen Retro unverändert. Mechanismus dort
noch nur Text; sobald dein Test `retroNenntBefehl` steht, trage ich ihn bei Schritt 1 ein.
Bitte ergänze ihn und entferne in [Regeln](../../prozess/regeln.md#rollenregeln) bei
Anliegen 405 „Eintrag offen: Anliegen 406“.
