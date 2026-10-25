# Soll bei einer aufhaltenden Kritik ein Hindernis unter der Zeile im Fortschritt stehen?

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wenn ein Kritiker einen Befund hat, der seinen Schritt aufhält, steht der Befund schon als Anliegen. Der Befehl für Hindernisse legte bisher ein zweites an. Fachkritiker und Architekt ließen ihn deshalb weg, weil er eine Nummer außerhalb ihres Bereichs vergab. Mit Retro 7, P5 nimmt der Befehl die Nummer aus dem Bereich des Auftrags oder nennt ein vorhandenes Anliegen, ohne ein zweites anzulegen.

**F1 · Soll unter der Zeile der Kritik im Fortschritt das Hindernis mit Link auf das Anliegen stehen, wenn sie aufhält?**
A: Ja, mit der Nummer des vorhandenen Anliegens; der Fortschritt zeigt, was aufhält. B: Nein, der Fortschritt bleibt ohne Hindernis, die Kritik steht nur im Anliegen.
Empfehlung: A.
Antwort: A

**Stellungnahme.**
Kommentar: Ich finde es wichtig, dass eine aufhaltende Kritik im Fortschritt notiert wird. Mir würde ein Link auf das Anliegen reichen mit Nummer und einem (für mich als Menschen) verständlichen Satz, worum es geht. (z.B. Testautor -> Anforderungsautor: Das Akzeptanzkriterium lässt sich nicht als Test umseten.)

**Nachprüfung (Regelumsetzer).** Gebaut war: Unter der Zeile steht `Hindernis: <Text> (Anliegen <nr>)`, das Dashboard macht „Anliegen <nr>“ zum Link. Es fehlte, dass die Zeile sagt, wer wen aufhält; das hing am Text, den die Rolle frei schrieb. Nachgebessert: `standregeln/hindernis.py` setzt `<Rolle> → <Beseitiger>: ` vor den Satz, auch bei einem vorhandenen Anliegen. Endgültiges Format: `  Hindernis: Testautor → Anforderungsautor: <Satz> (Anliegen <nr>)`, danach bei Annahme `; beseitigt: Commit „<Betreff>“`. Der Satz bleibt Sache der Rolle: ein ganzer Satz in Worten des Spielers. Test: `standregeln/hindernisTest.py` (`testEinHindernisLegtAnliegenUndZeileAn`, `testEinVorhandenesAnliegenWirdGenanntStattEinNeuesAnzulegen`), `rollenregeln/dashboardFortschrittTest.py` (Link) grün. Die Formatzeile in [Fortschritt](../../prozess/ablauf/fortschritt.md) zieht der Organisationsentwickler nach.
