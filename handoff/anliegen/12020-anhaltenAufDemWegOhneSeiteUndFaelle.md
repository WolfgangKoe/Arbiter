# Anhalten auf dem Weg: Seite ungetestet, zwei Fälle fehlen

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Kritik: ein Test prüft sein Kriterium nicht), Tests zu Item
[anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md), Stand des Arbeitsbaums.

1. **Am Bildschirm fehlt jeder Test.** [AUF-29](../../domaene/anforderungen/phasen/aufstellen/anhaltenAufDemWeg.md)
   und [BEW-17](../../domaene/anforderungen/phasen/bewegung/anhaltenVorFremdenBases.md)
   gelten ab der *zuvor gezeigten Stelle*, [AUF-28.2](../../domaene/anforderungen/phasen/aufstellen/loslassenWoDieKarteZeigt.md)
   und BEW-17.2 *setzen*, wo die *Karte* zuletzt zeigte. Der Vertrag verlangt dafür
   ([Aufstellen · Ziehen](../../technik/architektur/vertrag/aufstellen/ziehen.md), „Prüft“):
   „Am Bildschirm mit `page.route`: Die zweite Abfrage trägt `x`, `y` des gezogenen aus der
   ersten 200, der Körper von V5 die Eingaben der letzten Abfrage“. Kein Test prüft das; die
   Seite schickt heute nur `x` und `y` ([anfragen.js](../../technik/frontend/anfragen.js),
   `stellenBeimLoslassen`). Alle Tests des Items laufen am Dienst und an der Domäne.
   Kosten: Grün mit unveränderter Seite gleitet die *Karte* in jedem Schritt ab der *Stelle*
   vor dem Ziehen; an einer fremden *Base* entlang gleitet nichts (AUF-29.2, BEW-17.1), BEW-17.4
   greift nie. Der Stakeholder sieht beim Ziehen an einer *Base* vorbei nicht, was die
   Anforderung verspricht („Am Bildschirm: an fremden *Bases* vorbeiziehen“).
2. **BEW-17.1 ohne den Fall 6.2 beim Teil nach 29.2.** Das Kriterium nimmt einen Teil nach
   AUF-29.2 nur, „auf dem BEW-3.1, 6.1 und 6.2 keines anhalten“.
   `testBew17_1HältArbiterAufDemFreienTeilAnZeigtDerDienstDasModellAufDerStrecke` prüft 3.1
   und 6.1 (`senkrechterTeilÜberDieBewegungsweite`, `…ÜberDieSpielfeldkante`), 6.2 nicht.
   Kosten: Ein Gleiten in die *Nahkampfreichweite* eines *Modells* des anderen *Spielers*
   bliebe grün; das wäre eine Bewegung, die die Regel verbietet (`core_rules.txt:745`).
3. **BEW-17.1 ohne *Modell* derselben *Einheit*.** Fremd nach AUF-29.3 ist bei einem
   einzelnen *Modell* als *Ebene* auch jedes *Modell* derselben *Einheit*. In der
   *Bewegungsphase* hält jeder Test nur vor einer anderen *Einheit* an; der Fall steht nur in
   der *Aufstellung* (`testAuf29_3AlleinGezogenHältDerDienstVorDemModellDerselbenEinheitAn`).
   Kosten: Wer die Boyz einzeln bewegt (Happy Path der Partie Orks gegen Necrons), bekäme beim
   Anstoßen an einen eigenen Boy statt des Gleitens die *Sperre* ‚Base überdeckt‘, und kein
   Test würde rot.

**Gegenvorschlag.**
1. Ein Test mit `page.route` nach dem Vertrag: einen Boy in der *Aufstellung* zweimal
   weiterrücken lassen; die zweite Abfrage trägt `zuvorX`, `zuvorY` gleich `x`, `y` des Boys
   aus der ersten 200 (und `angehaltenAufDemWeg`, wenn die erste es meldete), der Körper von V5
   die Eingaben der letzten Abfrage. Da die Seite keine *Phase* unterscheidet
   ([Bewegung · Ziehen](../../technik/architektur/vertrag/bewegung/ziehen.md)), reicht einer
   für AUF-29 und BEW-17.
2. Ein dritter Parameter `senkrechterTeilInDieNahkampfreichweite`, gebaut wie
   `testBew17_3HältDieNahkampfreichweiteFrüherAnZeigtDerDienstDasModellVorIhr` (Warboss vorher
   übergehen, ein Necron gleitet).
3. Ein Test wie `testBew17_1DerDienstHältDasModellAufDerStreckeVorDerFremdenBaseAn` mit
   einem Boy, der ohne `auswählen` auf einen anderen Boy derselben *Einheit* gezogen wird:
   200, auf der Strecke, `angehaltenVor` dem anderen Boy.

**Stellungnahme.** Angenommen, rot bis Seite und Domäne folgen. 1: `page.route` reicht
durch; je Kriterium ein Test: `testAuf29_1DieSeite…`, `testAuf28_2DieSeite…`,
`testBew17_4DieSeite…`, `testBew17_2DieSeite…`. 2: eigener Test
`testBew17_1HältDieNahkampfreichweiteAufDemFreienTeilAn…`, da andere *Modelle*. 3:
`testBew17_1AlleinGezogen…`, zwei Abfragen, da die Boyz sich berühren.
