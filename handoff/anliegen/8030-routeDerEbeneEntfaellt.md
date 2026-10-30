# Route der Ebene entfällt

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält nicht auf. Nach Anliegen 4921 geht jeder Klick auf ein *Modell* über V14
`modellAnklicken`, auch der auf ein *Modell* der *ausgewählten* *Einheit* (AUF-25.1, 25.2);
V9 `…/modelle/<m>/ebene` gibt es im Vertrag nicht mehr
([Aufstellen · Auswahl](../../technik/architektur/vertrag/aufstellen/auswahl.md),
[Bewegung · Auswahl](../../technik/architektur/vertrag/bewegung/auswahl.md),
[Querschnitt](../../technik/architektur/vertrag/querschnitt.md): Routen nur nach V1, V2, V5,
V10, V12 bis V14). Der Code hat sie noch:
1. [anwendung.py](../../technik/arbiter/web/anwendung.py): `modellAlsEbene`,
   `einheitAlsEbene`, `gesetztesModellDerAusgewählten`, `pfadDerEbene`; die Regel „nur ein
   *gesetztes* *Modell* der *ausgewählten* *Einheit*“ steht damit in `web/`.
2. [aufstellen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py):
   `ebeneWählen`, `ebeneAbwählen` an der Tür `Aufstellung` (V3 nennt dort jetzt
   `modellAnklicken`).
3. [anfragen.js](../../technik/frontend/anfragen.js): `ebeneSenden` mit `PUT`/`DELETE`.

**Kosten.** Bleibt es, gibt es zwei Wege zur *Ebene*, einen davon mit der Fallunterscheidung
in der Seite und der Regel in `web/`; die Unit-Tests in
[anwendungTest.py](../../technik/tests/einheit/web/anwendungTest.py) halten toten Code am Leben.

**Gegenvorschlag.** Mit den Tests zu AUF-25 grün: Route, `ebeneSenden` und die beiden
Methoden an `Aufstellung` entfernen, ebenso die Unit-Tests zu `pfadDerEbene`.
`Auswahl.ebeneWählen` und `ebeneAbwählen` dürfen bleiben, wenn
`Aufstellung.modellAnklicken` sie ruft.

**Stellungnahme.** Angenommen. Entfernt: Route und Hilfsfunktionen in `web/anwendung.py`, `ebeneWählen` und `ebeneAbwählen` an `Aufstellung`, `ebeneSenden` im Frontend, die Unit-Tests zu `pfadDerEbene`. `modellAnklicken` an `Aufstellung` und `Schlacht` ruft jetzt `Auswahl.modellAnklicken`, das zwischen auswählen und *Ebene* wechselt.
