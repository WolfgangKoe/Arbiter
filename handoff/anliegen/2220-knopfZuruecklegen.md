# Der Knopf zum Zurücklegen: Name, ein Modell angewählt, wann er da ist

Form: Fragen
Von: Anforderungsautor
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Zu deiner Antwort in Anliegen 2062 („einen Button neben ‚Aufstellen der Einheit
beenden‘ … Dann kann das meiste so bleiben, oder?“): Ja, das meiste bleibt, wie es ist. Du klickst eine *Einheit* in deiner *Ablage* an und klickst in deine
Zone. Neu sind nur zwei Dinge:
- Ein Knopf neben „Aufstellen der Einheit beenden“ nimmt die Boyz von der *Karte*, alle zurück
  in die *Ablage*. Sie bleiben angewählt, ein Klick in die Zone stellt sie neu auf.
- Ziehst du die Boyz über die Kante hinaus und lässt los, gleich wo, auch auf einer *Ablage*:
  Sie stehen am Rand, wo die *Karte* sie zuletzt zeigte. Bisher sprangen sie zurück, auf der
  *Ablage* des anderen kam „nicht wählbar“.

Für den Knopf fehlen drei Entscheidungen, dazu eine Rückfrage zur *Ablage*.

**Kosten.** Ohne Antwort kann UX den Knopf nicht zeichnen und der Testautor nicht prüfen,
was nach dem Klick zu sehen ist.

**Gegenvorschlag.** Je Frage eine Empfehlung.

**F1 · Wie heißt der Knopf?**
- A: „Einheit zurücklegen“.
- B: „Aufstellen der Einheit zurücknehmen“, gleich gebaut wie „Aufstellen der Einheit beenden“.

Empfehlung: A. Kurz, und das Wort *zurücklegen* steht schon im Glossar. Den Knopf „zurück“
siehst du nur, wenn Arbiter das Beenden sperrt (AUF-13).
Antwort: A

**F2 · Du hast nur einen Boy angeklickt, der goldene Rahmen ist nur um ihn. Du klickst den Knopf.**
- A: Alle Boyz gehen zurück in die *Ablage*, wie sonst auch.
- B: Arbiter meldet „nur ganze Einheit“; erst klickst du den Boy noch einmal, dann den Knopf.

Empfehlung: A. Der Knopf gilt der *Einheit*, nicht dem angeklickten Boy, und kein Regeltext
verbietet es.
Antwort: A

**F3 · Wann siehst du den Knopf?**
- A: Nur solange eine *Einheit* in Aufstellung ist, also mindestens eines ihrer *Modelle* auf
  der *Karte* steht und sie noch nicht beendet ist.
- B: Immer. Steht nichts zum Zurücklegen, meldet Arbiter „nicht in Aufstellung“, wie beim
  Beenden.

Empfehlung: A. Ohne Boyz auf der *Karte* gibt es nichts zurückzulegen, und eine Meldung für
etwas, das nicht regelwidrig ist, hast du bisher vermieden (Anliegen 380).
Antwort: A

**F4 · Bleibt die Ablage, wo du die Einheit anklickst?** Du schreibst in 2062, eine *Ablage*
brauche es nur für die Reserve.
- A: Ja. Die *Ablage* bleibt die Liste, in der du die *Einheit* anklickst, bevor du in die Zone
  klickst (Review 6, Schritt 2). Nur als Ziel zum Hineinziehen entfällt sie.
- B: Nein. Dann sag bitte, wo du die *Einheit* anklickst.

Empfehlung: A.
Antwort: .

Annahme: A bei allen vier steht so in
[AUF-23](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md) und
[AUF-28](../../domaene/anforderungen/phasen/aufstellen/loslassenWoDieKarteZeigt.md).

**Stellungnahme.**
Kommentar: Frage f4 verstehe ich mal wieder nicht. Sobald wir bei der AUfstellung etwas "in Reserve" stellen, braucht es dafür einen Bereich neben dem Spielfeld. Das ist keine "Ablage" sondern die "Reserve". Eine Ablage braucht es in deinem Verständnis nicht.
Stellungnahme: Danke, F1 bis F3 stehen so in AUF-23. Zu F4: Einen Ort, in den man *Modelle* zurückzieht, gibt es nicht mehr. Es bleibt nur die Spalte neben der *Karte*, in der du eine *Einheit* anklickst; sie bekommt einen eigenen Namen ([2221](2221-ablageHeisstArmeeliste.md)). Die Reserve kommt erst, wenn eine Etappe sie verlangt.
