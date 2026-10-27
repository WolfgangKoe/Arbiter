# Links in Regeln und Prüfcode zeigen auf alte Dateien der Architektur

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Item [architekturUmordnen](../../domaene/items/architekturUmordnen.md) hat die
Architektur nach Anliegen 2570 (F1, F2 C) umgeordnet: je Ordner von `technik/` eine Datei,
der Vertrag je Phase in `technik/architektur/vertrag/`. Danach zeigen vier Stellen ins Leere:
- [Formregeln](../../prozess/regeln/formregeln.md), Zeile SonarLint: `technik/architektur/vertrag.md`
  (V4) heißt jetzt `technik/architektur/vertrag/querschnitt.md`.
- [Frontendregeln](../../prozess/regeln/frontendregeln.md): `technik/architektur/oberflaeche.md`
  (O1) heißt jetzt `technik/architektur/frontend.md`.
- [Kriterienregeln](../../prozess/regeln/kriterienregeln.md), Zeile Spiegel:
  `technik/architektur.md#grundschnitt-der-domäne` steht jetzt in
  `technik/architektur/domaene.md#grundschnitt-der-domäne`; T1 und T2 stehen in
  `technik/architektur/tests.md`.
- `eslint.config.mjs`, `meldung`: „Architektur, Web, O1“; O1 steht in Frontend.

Verweise auf `technik/architektur.md` mit Kennung (A1, T1, S1 …) gelten weiter: Die
Übersicht nennt je Datei ihre Kennungen.

**Kosten.** Wer dem Link folgt, findet die Regel nicht oder nur über die Übersicht. Wartet
auf die nächste Phase seiner Perspektive ([Ich 3](../../prozess/praemissen/ich.md)): keine
Prüfung rot, kein Schritt des Happy Path betroffen.

**Gegenvorschlag.** Die vier Stellen auf die neuen Pfade setzen, sonst nichts.

**Stellungnahme.**
