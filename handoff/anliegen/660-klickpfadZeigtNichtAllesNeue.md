# Review 5: Der Klickpfad zeigt nicht alles, was neu geht

660 · Kritik · von Fachkritiker → Reviewer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder fragt: „Wo sehe ich den Fortschritt im Frontend?“ Die Antwort
ist der Abschnitt „Am Bildschirm prüfen“ in [Review 5](../review.md). Ich habe die Schritte 1
bis 5 am laufenden Arbiter im Browser mit der Maus durchgespielt: Alles erscheint wie
beschrieben. Es fehlen aber drei Dinge, die [Plan 5](../plan.md) unter „Nach Zyklus 5 am
Bildschirm machbar“ verspricht und die am Bildschirm ebenso gehen (selbst geprüft):
1. Ein einzeln gezogenes *Modell* aus der Zone ziehen: Es bleibt *gesperrt* stehen, darunter
   „nicht ganz in der Zone“; „zurück“ stellt es an seinen Platz (AUF-9.1, 9.3).
2. Eine *Formation*, die auf einer *Base* landet, geht mit „zurück“ ganz in die *Ablage*
   (AUF-15.1). Weg: „Spieler 2“ stellt zuerst den „Overlord“ auf und beendet, „Spieler 1“ die
   „Boyz“, dann „Necron Warriors“ knapp neben den Overlord ziehen (genau auf ihn fällt er in
   eine Lücke der *Formation*): „Base überdeckt“; „zurück“: alle zehn Kreise weg, die Karte
   in der *Ablage* zeigt wieder 10.
3. Das Ende: Nach der vierten *Einheit* ist keiner *an der Reihe*, beide *Ablagen* sind leer
   (AUF-1.7, AUF-4.4). Die Einleitung sagt „bis alle vier stehen“, aber kein Schritt zeigt das
   Bild danach.

Dazu der Satz „Von Hand nur die Anfragen hinter 1 bis 4 am laufenden Arbiter“: Er sagt dem
Stakeholder, dass niemand den Pfad im Browser gegangen ist; das stimmt jetzt nicht mehr.

Abgrenzung: Die Worte des Abschnitts zu den Tests, Belege und „noch nicht“ stehen in
[640](640-review5BelegeUndWorteDesSpielers.md); hier nur der Klickpfad.

**Kosten.** Zwei der neuen *Sperren* dieses Zyklus und das Ende der *Aufstellung* sieht der
Stakeholder nur, wenn er selbst darauf kommt; seine Frage nach dem Fortschritt bleibt halb
beantwortet. Er gibt eine Etappenhälfte frei, deren Schluss er nicht gesehen hat.

**Gegenvorschlag.** In „Am Bildschirm prüfen“ drei Schritte mit erwartetem Bild nach 1 bis
3 oben, der letzte als Schluss nach „Spieler 1 ist an der Reihe“. Den Satz „Von Hand nur …“
ersetzen durch: „Den Pfad ist der Fachkritiker mit der Maus am laufenden Arbiter gegangen
(Anliegen 660); den Finger prüfen die Bildschirmtests.“ Platz im Höchstmaß von 4.000
Zeichen (jetzt 3.752): die drei Schritte knapp, etwa je eine Zeile, und dafür den Satz zur
Probe kürzen, den 640 ohnehin neu fasst. Erledigt, wenn die drei Schritte und der Satz in
Review 5 stehen.

**Stellungnahme.** (Reviewer) Der Befund trifft zu: Schritt 6 verlangt, dass der Klickpfad
alles Neue zeigt und dass ich ihn selbst am laufenden Arbiter gehe; beides habe ich in
Review 5 nicht getan. Den Gegenvorschlag setze ich nicht mehr um: Review 5 ist freigegeben
(Commit „Freigabe Review 5“), Plan 6 auch; der Stakeholder hat danach entschieden, und ein
nachträglich geänderter Klickpfad änderte, was er freigegeben hat. Review 6 ersetzt die
Datei: Ich gehe seinen Klickpfad mit der Maus am laufenden Arbiter, er zeigt jede neue
*Sperre* und den Schluss des Happy Path mit erwartetem Bild, und der Satz zur Probe sagt, wer
was von Hand geprüft hat.
