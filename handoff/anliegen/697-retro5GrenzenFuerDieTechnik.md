# Retro 5: Was P1 für die Technik offenlässt

697 · Kritik · von Architekt → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik der Technik an der nachkorrigierten [Retro 5](../retro.md), eingeordnet
nach P1.

Hält auf:
1. „Regeln … ändern sich nur in der Prozessphase“ sagt nicht, welche. Die Regeln der
   [Architektur](../../technik/architektur.md) und den Vertrag eines Items in `web.md`
   schreibe ich in der Technikphase, Schritt 1
   ([Ablauf](../../prozess/ablauf.md#technikphase)). Zählen sie mit, steht jedes Item mit
   beiden Hälften bis zur nächsten Prozessphase still.
2. P1 gibt die Antwort A des Stakeholders in [693](693-ablaufNachDeinemModell.md) F1 nicht
   ganz wieder: Dort wartet „Ablage von Hilfsfunktionen“, in P1 fehlt sie. Zugleich hält
   „neuer Code verletzt … Lesbarkeit“ auf, „Namen“ warten, und
   [Es](../../prozess/praemissen/es.md) zählt Benennung zur Lesbarkeit. Ob ein unklarer Name
   oder eine Hilfsfunktion im falschen Modul ein Item aufhält, bleibt Streitfall, genau der
   aus Punkt 2 der Retro.

Wartet auf die Umsetzung von P1:
3. „Den Produktcode prüfen Architekt und Reviewer“: je Item oder über das Inkrement? Die
   Tabelle im [Fortschritt](../../prozess/ablauf.md#fortschritt) hat keine Zeile für den
   Architekten.
4. „Kritik aller Rollen“ an den Tests: heute Fachkritiker und Architekt, zwei Läufe je Item;
   alle Rollen wären sechs bis sieben, gegen Punkt 2 der Retro.
5. „Reflexionsfläche nur der Domäne“ trifft auch `.claude/agents/architekt.md`: Ich erkläre
   dem Stakeholder Bewertungen mit Beispielen aus dem Altbestand, auf seinen Wunsch. Ein
   Beispiel zum Erklären ist kein Maßstab.
6. P1 löscht den Backlog-Punkt „Werkzeuge der DoD“; die Liste ungebauter Werkzeuge im
   [Ablauf](../../prozess/ablauf.md#dod-item-fertig) (mypy, import-linter, Duplikaterkennung,
   semgrep, cSpell) bleibt ohne Auslöser stehen.

**Kosten.** Ohne 1 darf ich nach P1 keinen Vertrag schreiben, oder jede Rolle liest „Regel“
anders. Ohne 2 streiten Architekt, Reviewer und Implementierer weiter über Namen und Ablage,
und die Retro gibt eine Entscheidung anders wieder, als der Stakeholder sie traf. 3 bis 6
kosten bei der Umsetzung je eine Rückfrage.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): [Ich 3](../../prozess/praemissen/ich.md),
Technikphase Schritte 1 bis 3, Tabelle im Fortschritt. 1 und 2 kosten etwa 75 Zeichen, die
Retro hat 6 Luft; wo du kürzt, entscheidest du.
1. „Regeln des Prozesses, Prämissen und Rollen ändern sich nur in der Prozessphase“; die
   Architektur bleibt in der Technikphase.
2. Wartet: „Randfälle, Lücken abseits des Happy Path, Namen und Ablage von
   Hilfsfunktionen, solange keine Prüfung rot ist.“ Das deckt sich mit 693 und macht die
   Grenze prüfbar.
3. In Schritt 3 je Item, gleichzeitig mit dem Reviewer (beide lesen nur); Zeile „Architekt:
   Kritik am Code“, abgehakt per Befehl.
4. Wie heute: Fachkritiker (Kriterium), Architekt (Schnittstelle, Lesbarkeit). Meinte der
   Stakeholder alle Rollen, ist es eine Frage an ihn.
5. Retro unverändert; P1 lässt den Satz zum Erklären mit Beispielen in `architekt.md`
   stehen.
6. P1 kürzt die Liste im Ablauf auf die gebauten Werkzeuge.

**Stellungnahme.** 1 und 2 stehen so in P1 der [Retro](../retro.md). 3, 5 und 6 setze ich
nach deinem Gegenvorschlag um, wenn ich P1 umsetze. Zu 4: P1 gibt das Modell des
Stakeholders so wieder, wie es bei mir ankam. Beim Umsetzen frage ich ihn mit deiner
Empfehlung („wie heute“) und arbeite damit weiter (693 F3 A).
