# Hindernis: Kritik an den Tests zu Item anhaltenAufDemWeg

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Diese Tests sind grün, bevor der Code besteht: testAuf29_1DerDienstHältAufDerStreckeAbDerZuvorGezeigtenStelleAn, testAuf29_1DieSeiteSchicktJederAbfrageDieZuvorGezeigteStelleDesGezogenenModells, testAuf29_2DerDienstZeigtDasModellUmDenFreienTeilDesWegesVerschoben[beideTeileFreiWaagrecht], testAuf29_2DerDienstZeigtDasModellUmDenFreienTeilDesWegesVerschoben[nurSenkrechtFrei], testAuf29_2DerDienstZeigtDasModellUmDenFreienTeilDesWegesVerschoben[nurWaagrechtFrei], testAuf29_3IstDieGanzeEinheitEbeneZeigtDerDienstAlleAmEigenenModellVorbeiVerschoben, testAuf28_2DieSeiteSendetBeimLoslassenDieEingabenDerLetztenAbfrage. Mache sie rot oder nenne die Stelle, die das Kriterium schon erfüllt. Das hält den Schritt „Kritik an den Tests zu Item anhaltenAufDemWeg“ von Architekt im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Nachgeprüft vom Architekten.** Alle sieben sind rot gegen den Produktcode aus 4d8ca81
(Kopie in `/tmp`, Tests aus dem Arbeitsbaum), und zwar an ihren Prüfzeilen: AUF-29.1
`assert False` und leere zuvor gezeigte Stellen, AUF-29.2 und AUF-29.3 falsche gezeigte
*Stellen*, AUF-28.2 „Die letzte Abfrage nennt keine zuvor gezeigte Stelle“. Grün macht sie
erst 096dfed („anhaltenAufDemWeg Teil 1: Aufstellen hält auf dem Weg an“). Das Abhaken prüft
gegen `HEAD`, weil „Implementierer: Tests zu Item anhaltenAufDemWeg grün“ noch offen ist
(Ursache: Anliegen 12600). Die Tests prüfen ihr Kriterium.

**Gegenvorschlag.** Testautor nennt als Stelle, die das Kriterium erfüllt, Commit 096dfed
und setzt `angenommen`; am Test ändert sich nichts.

**Stellungnahme.** Angenommen; an den Tests ändert sich nichts. Die Stelle, die die sieben
Aussagen erfüllt, ist Commit 096dfed „anhaltenAufDemWeg Teil 1: Aufstellen hält auf dem Weg
an“ (`technik/arbiter/domaene/phasen/aufstellen/anhaltenAufDemWeg.py`, mit Seite und Web).
Gegen 4d8ca81 selbst nachgeprüft wie in Anliegen 12521: alle sieben rot an ihren Prüfzeilen.
Ursache ist das Abhaken gegen HEAD (Anliegen 12600).
