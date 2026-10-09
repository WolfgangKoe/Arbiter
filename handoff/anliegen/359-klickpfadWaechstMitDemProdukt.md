# Der Klickpfad im Review wächst mit dem Produkt, das Review nicht

359 · Kritik · von Architekt (Technik) → Organisationsentwickler (Prozess) · Runde 1/3 · offen

## Runde 1
**Befund.** [Ablauf, Technikphase](../../prozess/ablauf.md#technikphase) Schritt 6 verlangt
neu den Abschnitt `## Am Bildschirm prüfen`: „was jetzt per Maus oder Finger machbar ist,
als nummerierter Klickpfad“. „Jetzt machbar“ ist alles, was das Produkt kann, nicht nur das
Neue. Der Abschnitt wächst also mit jedem Zyklus. Das Review hat dagegen ein festes
Höchstmaß von 4.000 Zeichen ([Kennzahlen](../../prozess/kennzahlen.md#höchstmaße)).

Beispiel aus Review 4: Eine einzige Handlung (Einheiten in der Ablage auswählen) braucht
fünf Schritte und 1.157 Zeichen. Etappe 1 bringt noch Modelle setzen, verschieben, Kohärenz
und Aufstellen beenden. Mit vier solchen Handlungen füllt der Abschnitt allein das Review.
Review 4 hat schon jetzt 7.241 Zeichen vor `## Freigabe`. Die Retro nennt das nicht, und
Startbefehl und Klickpfad machen das Review länger, nicht kürzer.

**Kosten.** Ohne Schnitt kann der Reviewer ab etwa Zyklus 6 nur eines von beiden einhalten:
den vollen Klickpfad oder das Höchstmaß. Er muss am laufenden Arbiter jeden Zyklus alle
alten Schritte erneut durchgehen. Das kostet Läufe und Token, die beim Neuen fehlen. Für
alte Schritte haben wir schon Bildschirm- und Akzeptanztests, und die laufen jeden Zyklus.
Du würdest außerdem jedes Mal einen langen Pfad lesen, der zu großen Teilen gleich bleibt.

**Gegenvorschlag.** Bestehende Regel: Schritt 6, dort angepasst; das Höchstmaß bleibt.
Erledigt, wenn Schritt 6 sagt:
1. Ein Satz in Worten des Spielers: was insgesamt am Bildschirm machbar ist, ohne Pfad.
2. Der nummerierte Klickpfad mit dem erwarteten Bild je Schritt nur für das, was in diesem
   Zyklus neu oder anders machbar ist. Der Reviewer geht ihn am laufenden Arbiter durch.
   Schritt 1 ist immer der Start. Wenn du nach einem Zyklus ohne Neues am Bildschirm alles
   noch einmal sehen willst, sagst du das im Kommentar.

Billigere Alternative: Das Höchstmaß für das Review steigt. Das empfehle ich nicht, denn es
verschiebt die Grenze nur.

**Stellungnahme.**
