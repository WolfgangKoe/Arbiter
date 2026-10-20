# Tests entfallener Kriterien widersprechen dem Anhalten an Bases

1350 · Kritik · von Fachkritiker → Testautor · Runde 1/3 · offen

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf. Ist Item 3 gebaut, sind diese Prüfungen rot, und
der Implementierer kann nicht beide Seiten grün machen. Die neuen Tests zu AUF-24.1 und 26.2
bis 26.4 treffen ihre Kriterien. Sie sind rot, weil Code fehlt, nicht wegen Testfehlern
(selbst ausgeführt: 152 rot, 6 grün).
Doch das [Item](../../domaene/items/anhaltenAnBases.md) streicht AUF-9.1, 9.3, 12.1 und
QUE-3.5 samt Test. [Plan 6](../plan.md#items) streicht mit Item 3 auch den Bildschirmtest zu
AUF-17.1 (1210). Diese Tests stehen alle noch und verlangen das Gegenteil von AUF-26.1 und 26.2:
1. [gesperrtesModellTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/gesperrtesModellTest.py),
   alle acht Tests zu AUF-9.1 und 9.3. Ein Beispiel:
   `testAuf9_1EinModellAufEinerBaseIstNachDemLoslassenGesperrtMitDemGrund` erwartet ein
   *gesperrtes* *Modell* auf der *Base*. AUF-26.2 hält es davor an.
   `testAuf9_1EinModellAußerhalbDerZone…` erwartet *gesperrt*, AUF-26.1 rückt es hinein.
2. Die fünf Tests `testAuf12_1…` in `sperreOhneStelleTest.py` und die zwei `testQue3_5…` in
   `bedienungTest.py`. Sie erzeugen ein *gesperrtes* *Modell* durch Ziehen auf eine *Base*.
   Nach AUF-26.2 entsteht so keines mehr.
3. [zurueckOhneSperreTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/zurueckOhneSperreTest.py):
   Der Bildschirmtest
   `testAuf17_1EinKlickAufZurückAufEinerVorherGeöffnetenSeite…` braucht den Knopf „zurück“
   neben einem *gesperrten* *Modell*. Die beiden Tests zu 17.1, die bleiben, laufen auch mit
   dem Fall `zumZweitenMalZurück` (`nachZurückBeiGesperrtemModell`). Er braucht ebenfalls
   ein *gesperrtes* *Modell*.

**Kosten.** Mit dem Anhalten werden rund 17 Tests rot. Item 3 wird nicht grün, der Commit
bleibt gesperrt. Lässt der Implementierer stattdessen das Sperren stehen, baut er etwas
anderes als AUF-26.

**Gegenvorschlag.** Lösche die Tests aus 1 und 2, den Bildschirmtest aus 3 und den Fall
`zumZweitenMalZurück`. Die übrigen Fälle zu 17.1 bleiben (1210). Danach löscht der
Anforderungsautor die Kriterien ([1351](1351-kriterienZumGesperrtenModellNachAnhalten.md)).
Hinweis: Drei weitere Tests prüfen *nicht gesperrt* über `gesperrt(…)`, nämlich
`ziehenTest.py:45`, `:62` und `sperreOhneStelleTest.py:245`. Nach V10 entfällt `gesperrt`.
Fachlich stimmen diese Aussagen weiter. Ob der Aufruf bleiben kann, beurteilt der Architekt.
Erledigt, wenn `grep -rn "def testAuf9_\|def testAuf12_1\|def testQue3_5"
technik/tests/akzeptanz` nichts mehr findet. Außerdem darf kein Akzeptanztest mehr ein
*Modell* durch Loslassen auf eine *Base* *sperren*.

**Stellungnahme.**
