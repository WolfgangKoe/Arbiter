# AUF-29.2: ein Teil der Länge null hält das Modell vor der Base fest

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet, ein Randfall des
Anhaltens.
1. [AUF-29.2](../../domaene/anforderungen/phasen/aufstellen/anhaltenAufDemWeg.md): Rückt der
   Zeiger nur senkrecht auf eine fremde *Base* zu, ist der waagrechte Teil null. Er
   *überdeckt* keine, also zeigt die *Karte* das *Modell* nach 29.2 „um diesen Teil verschoben“
   und damit unverändert. 29.1 greift dann nicht: Das *Modell* bleibt um ein ganzes Weiterrücken
   vor der *Base* stehen. ArbiterMap überspringt einen Teil ohne Fortschritt und rückt bis an die
   *Base* heran (`ArbiterMap/…/model_drag.js:897`, `advanceUntilBlocked`). Mit der Maus fehlt
   dann kaum etwas. Mit dem Finger oder einem schnellen Zeiger bleibt eine sichtbare Lücke.
2. AUF-29.1 nennt „die *Stelle*, an der AUF-24.3 oder 26.5 sie danach zeigen“. Beide sagen
   aber „außer AUF-29 hält es an“. Das liest sich im Kreis. Gemeint ist die *Stelle* nach
   AUF-8.2 und 26.1 bzw. 21.1 und 21.2.

**Kosten.** Ein Test nach dem Wortlaut legt die Abweichung von ArbiterMap fest, ohne dass der
Stakeholder sie entschieden hat (DoR 6).

**Gegenvorschlag.** Als neues Kriterium: „nur der waagrechte oder nur der senkrechte Teil, der
nicht null ist“. In 29.1 die Kriterien nennen, nach denen *gesetzt* würde, statt 24.3 und 26.5.

**Stellungnahme.** Angenommen, beide Punkte, in
[Anhalten auf dem Weg](../../domaene/anforderungen/phasen/aufstellen/anhaltenAufDemWeg.md).
Noch kein Test prüft AUF-29, darum in den bestehenden Kennungen statt als neues Kriterium.
1. AUF-29.2 gilt nur für einen Teil, der nicht null ist und für sich keine fremde *Base*
   *überdeckt*; sonst hält AUF-29.1 an, rückt also bis an die *Base* heran. Das folgt
   ArbiterMap (`model_drag.js:897`), eine Abweichung entsteht nicht.
2. AUF-29.1 nennt jetzt die *Stelle*, an die AUF-8.2 und 26.1 oder 21.1 und 21.2 die *Base*
   *setzen* würden; der Weg läuft zwischen ihr und der zuvor gezeigten *Stelle*, und alle
   gezogenen *Modelle* rücken gemeinsam.

Um unter 1.200 Zeichen zu bleiben, nennt der Zweck nur noch die Anliegen 1820 und 2090.
