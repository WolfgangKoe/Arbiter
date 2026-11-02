# Moderation

Stand: Domänenphase 10, Plan 10 wartet auf Kritik und Freigabe ([Plan](plan.md)). 38 Anliegen
offen, 34 warten auf eine Phase.

## Dran
Blockiert das Inkrement (Items in Plan 10):
- Anforderungsautor, Item 2: Nachprüfung von
  [9760](anliegen/9760-loslassenNebenDerKarteUndFremdeModelle.md) (angenommen). F1 A gilt,
  dazu Regelrecherche zu Flugzeugen am Kartenrand; F2 B heißt neue *Sperre* ‚nicht am Zug‘.
  Danach [8480](anliegen/8480-ueberDieKanteHinausLoslassen.md), dann
  [6986](anliegen/6986-bewegungLueckenFuerSpaeter.md).
- Fachkritiker: „Kritik am Plan“ steht offen (siehe Vorschläge, Punkt 2).
- Stakeholder: [9941](anliegen/9941-wohinUebergehenSetzt.md) F1 (Item 1; ohne Antwort gilt
  B), die Fragen unten.
- Koordinator: 9880 ist gelöscht, noch nicht committet.

Hält nichts auf: Stakeholder [9860](anliegen/9860-roteProbeBeiTeilweiseGestagedemCommit.md);
Nachprüfung von 7380 und 9440 (Vorschläge). Regelumsetzer: 8860, 9801, 8021 (wartet auf
8020), alle später. Planer: Plan 11 (9340). Alle übrigen Anliegen warten auf Technikphase 10.

## Vorschläge
1. **Einvernehmlich:** Die Streichung in
   [uebergehen.md](../domaene/anforderungen/querschnitt/uebergehen.md) hält nicht auf. Titel
   und QUE-5.1 sagen „gemeinsam übergehen“, das Glossar definiert es als einvernehmlich, die
   Datei hat 1.187 Zeichen. Die Anforderung bleibt aber schwächer als `domaene/ziel.md`.
   Anforderungsautor: das Wort zurückholen und anderswo kürzen (13 Zeichen frei);
   Fachkritiker ordnet ein, ob das aufhält. Ändern darf es nur der Anforderungsautor.
2. **Fortschritt:** Er zeigt die Kritik nicht vollständig. Die Domänenzeilen stehen nicht im
   Plan, sondern im Fortschritt der [Review](review.md) ([Fortschritt](../prozess/ablauf/fortschritt.md)).
   Dort offen: „UX: Mockups“, „Fachkritiker: Kritik am Plan“. Erledigt: Anforderungen und
   Mockups (Fachkritiker), Kritik am Plan (Architekt). Der Plan wurde in f3ebfad neu gefasst,
   Haken der Kritik am Plan fallen dann zurück. Der Fachkritiker hat also nach der neuen
   Fassung nicht abgehakt (oder nur vor ihr). Koordinator: Fachkritiker erneut beauftragen.
   UX: Items 1 und 2 haben Oberfläche, kein Mockup verlinkt; Koordinator klärt, ob UX läuft
   oder die Zeile mangels neuer Komponente entfällt.
3. **9890:** Der Architekt soll V18 vor den Tests zu Item 1 fassen (Gegenvorschlag), im Plan
   steht die Zeile zuletzt. Architekt: mit „Vertrag zu Item anhaltenUebergehen“ erledigen.
4. **Schließen:** Stakeholder: 7380 erledigt (Fortschritt zeigt wartende Anliegen);
   9440 mit Freigabe Plan 10 (Plan setzt es um).
5. **AUF-27.2:** Deine Deutung von 9270 F2 hat kein offenes Anliegen (9270 ist gelöscht).
   Anforderungsautor: vor Etappe 7 eine Frage anlegen (Nummer aus 9980–9999).
6. **Zusammen:** 7050 und 7681 (derselbe Test); 7191 und 7201; 8620 und 8740;
   7401 und 8421 (`anhaltenVorDerGrenzeTest.py`); 7641 und 7661. Je ein Lauf der
   Empfängerrolle.

### Stränge (Technikphase 10)
- Kette: Architekt (9890, Vertrag) → Testautor Item 1 (mit 7321) → Implementierer Item 1
  (mit 8261) → Item 3 (mit 9401). Item 2 vor Item 3; 1 und 2 nur gleichzeitig, wenn `git status`
  getrennte Dateien zeigt.
- Testautor, daneben: Katalog (7151 → 8971, nach Implementierer 7191, 7201); Leisten 7301;
  Grenzkreise (7641, 7661, 7401, 8421); Auswahl 7601, 8720 nach Implementierer 8100, 8121;
  7072.
- Implementierer, daneben: Verschieben (7042, 7050, 7681, 8020); 8620 → 8740; 8641 nach 8261
  (`schlachtrunden.py`, auch 8100). 8041 erst nach Item 3 (gleiche Einheitstests).
- Regelumsetzer: Hook-Code höchstens einer.

## Fragen an dich
Zuoberst mit Annahme:
- [9941](anliegen/9941-wohinUebergehenSetzt.md) F1: Wo stehen die Boyz nach dem Übergehen?
  Annahme: BEW-8.4 steht nach B.
- [9860](anliegen/9860-roteProbeBeiTeilweiseGestagedemCommit.md) F1: Wie mit der nicht
  nachvollziehbaren roten Probe umgehen? Empfehlung A.
