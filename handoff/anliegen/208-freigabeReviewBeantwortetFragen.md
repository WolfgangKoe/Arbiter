# Die Freigabe des Reviews beantwortet keine Fragen mehr

208 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von e772442 (Anliegen 167, Teil 1). `lage` und der Scheiter-Test
sind richtig. Codekritik bleibt nach `Freigabe Review <n>` fällig, das prüft
`testFreigabeDesReviewsSchiebtKeinenCodeCommitOhneKritikAusDemFenster`.

Die Ausnahme sitzt aber in `gitAufruf.letzteFreigabe` (`gitAufruf.py:31-39`) und gilt damit für
alle drei Aufrufer, nicht nur für `codekritik.py`: Betroffen sind auch `anliegen.dran`
(`beantwortetDurchFreigabe`, `wartetAuf`) und `kennzahlen.offeneAnliegenJeRolle`. Anliegen 167
verlangte für `beantwortetDurchFreigabe` eine Prüfung; einen Test dazu gibt es nicht.
Gegenprobe mit den Helfern aus `anliegenTest.py`: Fragen an den Stakeholder, Commit
`Freigabe Retro 3` → dran ist der Planer; Commit `Freigabe Review 3` → dran bleibt der
Stakeholder.

Nach [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen) beantwortet die Freigabe jede Frage
in der Freigabevorlage, und das Review verlinkt die offenen Anliegen. Mit der Freigabe des
Reviews müsste der Absender also dran sein.

**Kosten.** Fragen, die der Stakeholder mit dem Review freigibt, stehen im Stand weiter bei
ihm, und zwar bis zur Freigabe der Retro. Die Absender arbeiten die Antworten erst eine Phase
später ein. Ein Stand, der falsch „Dran: Stakeholder“ meldet, hält den Koordinator an.

**Gegenvorschlag.** `letzteFreigabe` bleibt, wie es war. `codekritik.py` bekommt sein eigenes
Fenster, etwa `letzteFreigabe(wurzel, ohne=("Review",))` oder eine Funktion
`letzteFreigabeOhneReview`. Scheiter-Test in `anliegenTest.py`: Fragen an den Stakeholder,
dann `Freigabe Review 3`, dran ist der Absender. Ist dir nicht klar, ob das Review Fragen
beantwortet, geht die Frage an den Organisationsentwickler (Ablauf); dann wartet dieses
Anliegen darauf.

Erledigt, wenn die Ausnahme nur für die Kritik am Code gilt, beide Scheiter-Tests grün sind,
`python3 -m pytest prozess/pruefungen` grün ist und der Reviewer den Commit geprüft hat.
