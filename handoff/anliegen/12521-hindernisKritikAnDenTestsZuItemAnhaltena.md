# Hindernis: Kritik an den Tests zu Item anhaltenAufDemWeg

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Diese Tests sind grün, bevor der Code besteht: testAuf29_1DerDienstHältAufDerStreckeAbDerZuvorGezeigtenStelleAn, testAuf29_1DieSeiteSchicktJederAbfrageDieZuvorGezeigteStelleDesGezogenenModells, testAuf29_2DerDienstZeigtDasModellUmDenFreienTeilDesWegesVerschoben[beideTeileFreiWaagrecht], testAuf29_2DerDienstZeigtDasModellUmDenFreienTeilDesWegesVerschoben[nurSenkrechtFrei], testAuf29_2DerDienstZeigtDasModellUmDenFreienTeilDesWegesVerschoben[nurWaagrechtFrei], testAuf29_3IstDieGanzeEinheitEbeneZeigtDerDienstAlleAmEigenenModellVorbeiVerschoben, testAuf28_2DieSeiteSendetBeimLoslassenDieEingabenDerLetztenAbfrage. Mache sie rot oder nenne die Stelle, die das Kriterium schon erfüllt. Das hält den Schritt „Kritik an den Tests zu Item anhaltenAufDemWeg“ von Fachkritiker im Fortschritt auf.

Nachgeprüft vom Fachkritiker: Mit dem Produktcode aus 4d8ca81 (Kopie in /tmp, Tests aus dem Arbeitsbaum) sind alle sieben rot, jeweils an ihrer Zusicherung, nicht an einem Fehler im Aufbau. Grün macht sie der Commit 096dfed „anhaltenAufDemWeg Teil 1: Aufstellen hält auf dem Weg an“ des Implementierers. Abhaken prüft gegen HEAD, solange „Implementierer: Tests zu Item anhaltenAufDemWeg grün“ fehlt, und hält so den Code von Teil 1 für den Stand vor der Umsetzung (Anliegen 12600). Die Tests prüfen ihr Kriterium; zu ändern ist an ihnen nichts.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter. Kosten der Antwort: eine Stellungnahme, keine Änderung an Tests.

**Gegenvorschlag.** Testautor nennt als Stelle, die das Kriterium erfüllt, Commit 096dfed und setzt `angenommen`; der Fachkritiker prüft nach und setzt `erledigt`.

**Stellungnahme.** Angenommen; an den Tests ändert sich nichts. Die Stelle, die die sieben
Aussagen erfüllt, ist Commit 096dfed „anhaltenAufDemWeg Teil 1: Aufstellen hält auf dem Weg
an“ (`technik/arbiter/domaene/phasen/aufstellen/anhaltenAufDemWeg.py`, mit Seite und Web).
Selbst nachgeprüft: Mit dem Produktcode aus 4d8ca81 (Kopie in `/tmp`, Tests aus dem
Arbeitsbaum) sind alle sieben rot, je an ihrer Prüfzeile (AUF-29.1 `aufDerStrecke` und leere
zuvor gezeigte Stellen, AUF-29.2 und AUF-29.3 falsche gezeigte *Stellen*, AUF-28.2 die zuvor
gezeigte Stelle der letzten Abfrage). Ursache ist das Abhaken gegen HEAD (Anliegen 12600).
