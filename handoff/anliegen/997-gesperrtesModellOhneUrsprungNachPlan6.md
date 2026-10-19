# Nach Plan 6 entsteht kein gesperrtes Modell mehr, seine Kriterien bleiben

997 · Kritik · von Architekt → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf. Mit Item 2 werden Tests rot, und zwei Kriterien
von Item 1 lassen sich nicht über ein Kriterium herstellen.
1. Ein *gesperrtes* *Modell* entsteht nur nach [AUF-9.1](../../domaene/anforderungen/phasen/aufstellen/gesperrtesModell.md).
   Item 1 streicht 9.1 mit Test, obwohl AUF-8.2 bis Item 2 weiter dorthin führt: Ein *Modell*
   auf eine fremde *Base* gezogen ist im Code *gesperrt* (`Aufstellung._loslassen`), nur ohne
   Kriterium.
2. Mit Item 2 klemmt AUF-26.2 dasselbe Ziehen. Die Tests zu AUF-9.3, 9.4, 12.1, 15.1 und 17.1
   bauen ihr *gesperrtes* *Modell* aber genau so: `einGesperrtesModell` in
   `technik/tests/akzeptanz/handgriffe.py` lässt ein *Modell* auf einem anderen los. Diese
   Tests werden mit Item 2 rot, ohne dass ein Item sie nennt.
3. [AUF-19.4](../../domaene/anforderungen/phasen/aufstellen/gesperrterKlick.md) und
   [AUF-12.5](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md) (Item 1)
   nennen 12.1, also ein *gesperrtes* *Modell*, das nach Plan 6 kein Kriterium erzeugt. Der
   Testautor müsste es über Verhalten ohne Kriterium herstellen.

Du hast in [984](984-klemmenStattSperreUndOhneAbzeichen.md) geschrieben: „ein *gesperrtes*
*Modell* entsteht nicht mehr“. Die Kriterien, die eines voraussetzen, sind geblieben.

**Kosten.** Ohne Entscheidung baut der Testautor in Item 2 die Hilfsfunktionen auf einen Weg
ohne Kriterium um, oder der Implementierer findet rote Tests, die kein Item nennt. Am
Bildschirm bliebe „zurück“ für einen Fall, den der Stakeholder nicht will.

**Gegenvorschlag.** Ich 4: wie in 984 („entfällt mit Test“).
- A · Empfehlung: AUF-9.1 entfällt erst mit Item 2, nicht schon mit Item 1. Mit Item 2
  entfallen AUF-9.2 bis 9.5, 12.1, 15.1 und 17.1 samt Tests. Aus 12.5 und 19.4 fällt „12.1“
  heraus. Mit ihnen gehen `gesperrtesModell.py`, „zurück“ (V5, V7) und die Felder `gesperrt`
  im Spielstand (V1). Das ist billig, weil es nur Code löscht. Du sagst dazu in einem Satz, was
  bis Plan 7 bei einem Klick geschieht, dessen *Formation* eine fremde *Base* *überdecken*
  würde (992, 987 F1 C). Meine Empfehlung: wie 19.4, also kein *Modell* kommt dazu, und
  Arbiter nennt den *Grund*. Das kann `modellSetzen` heute schon (D2), ein Klick, „der gerade
  nicht geht“ (Plan 6).
- B · Alles bleibt bis Plan 7. Dann baut der Testautor in Item 2 `einGesperrtesModell` auf den
  Klick neben eine stehende *Einheit* um. Dann gilt 9.1 auch für AUF-18.2. Das kostet mehr,
  und „zurück“ bleibt am Bildschirm.

Erledigt, wenn die Kriterien zu A oder B stehen und deine Stellungnahme die Kennungen nennt;
der Planer zieht die Items nach.

**Stellungnahme.** A, berichtigt:
- Nach Item 1 entsteht ein *gesperrtes* *Modell* nur über AUF-8.2: ein *gesetztes* auf ein
  anderes *gesetztes* gezogen, ab Item 2 mit der *Ebene* *Modell* (AUF-20.4). Die
  Hilfsfunktionen setzen heute über die *Ablage* (14.1, 8.5 entfallen); der Testautor baut sie
  in Item 1 darauf um, auch für 9.3, 12.1, 17.1, QUE-3.5.
- Mit Item 1 entfallen zudem AUF-9.4 und die Fälle zu 9.1 über die *Ablage*; 15.1 wie geplant.
- Mit dem Item, das AUF-26.2 bringt: AUF-9.1, 9.3, 12.1, QUE-3.5 entfallen mit Test, 9.2, 9.5
  ohne.
- „zurück“ bleibt für ‚keine Kohärenz‘ (AUF-10.3, 13.2), also auch 17.1; seine Fälle mit
  *gesperrtem* *Modell* baut der Testautor mit 26.2 auf 10.3 um.
- AUF-12.5 und 19.4 nennen 12.1 nicht mehr.
- Klick, dessen *Formation* eine *Base* *überdecken* würde, bis Plan 7: Randfall ohne Test;
  9.1 nennt den Klick nicht, QUE-1.2 gilt, also wie du empfiehlst. Plan 7: AUF-18.7, 992 C.
