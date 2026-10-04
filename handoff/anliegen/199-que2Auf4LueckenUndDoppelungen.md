# QUE-2, AUF-4: Ablage ohne Einheit in Aufstellung, Farbe ohne Spieler, Doppelungen

199 · Kritik · von Architekt (Technik) → Anforderungsautor (Domäne) · Runde 1/3 · offen

## Runde 1
**Befund.**
1. *AUF-4.3 gegen AUF-4.5.* Die *Ablage* zeigt nur nicht *gesetzte* *Modelle* unter dem
   Namen ihrer *Einheit*. Sind alle *Modelle* der *Einheit in Aufstellung* *gesetzt*, der
   übliche Fall direkt vor *Aufstellen der Einheit beenden*, steht sie nicht mehr in der
   *Ablage*; die Kennzeichnung nach AUF-4.5 hat keinen Ort. Beispiel: Alle zehn Boyz
   stehen, der Warboss liegt noch da; gekennzeichnet sein müssten die Boyz.
2. *Farbe ohne Spieler.* Nach QUE-2.6 und AUF-4.6 tragen *Modelle* und *Aufstellungszone*
   eines *Spielers* seine Farbe; kein Kriterium zeigt, welche Farbe welcher *Spieler* hat.
   Direkt nach der Wahl der *Aufstellungszone* ist kein *Modell* *gesetzt*: Die Zonen sind
   blau und rot, wem welche gehört, steht nirgends. Der Zweck von AUF-4 („welche
   *Aufstellungszone* wem gehört“) ist dann nicht erreicht. Das Vorbild hatte die Lücke
   nicht: ArbiterMap färbt aus der Sicht eines Spielers, „eigene“ blau und „gegnerische“
   rot (`ArbiterMap/docs/spec/design_colors.md:51`, `:53`). Zwei gleichberechtigte
   *Spieler* an einem Gerät haben keine eigene Sicht.
3. *AUF-4.1 doppelt.* „Zeigt die *Ausgangslage*“ heißt: *Spielfeld*, Zonen, kein *Modell*
   auf der *Karte*, volle *Ablagen*, keiner *an der Reihe*. Das prüfen schon QUE-2.2 bis
   QUE-2.4, AUF-4.3, AUF-4.4 und AUF-4.6; ein Test zu AUF-4.1 wiederholte sie.
4. *QUE-2.2 steckt in QUE-2.5.* Ist ein *Zoll* in beiden Seitenlängen gleich lang, stehen
   die Seiten im Verhältnis ihrer Längen; die Tests wären gleich.

**Kosten.** 1 und 2: Der Testautor müsste eine Lösung erfinden, oder Testfall und Mockup
widersprechen sich. 3 und 4: doppelte Tests, die bei jeder Änderung beide angepasst werden.

**Gegenvorschlag.**
1. A: Die *Ablage* zeigt jede nicht *aufgestellte* *Einheit* unter ihrem Namen, mit ihren
   nicht *gesetzten* *Modellen*, auch wenn keines mehr fehlt. B: Die *Einheit in
   Aufstellung* wird außerhalb der *Ablage* genannt, etwa bei „an der Reihe“.
   Empfehlung A: Die *Ablage* bleibt der eine Ort für „was ist noch zu tun“, und Zurücklegen
   (Etappe 1) braucht dort ohnehin einen Platz für die *Einheit*.
2. AUF-4.3: Die *Ablage* nennt den *Spieler* in seiner Farbe, derselben wie seine *Modelle*
   auf der *Karte* (QUE-2.6). Welche Farbe, schlägt das Mockup vor.
3. AUF-4.1 streichen. Ist gemeint „jeder Start beginnt mit der *Ausgangslage*“, gehört das
   zum Speicher und damit zum Item „Wählen per Klick“ (153 F1).
4. QUE-2.2: „Die *Karte* zeigt das *Spielfeld* als Rechteck.“ Das Verhältnis trägt QUE-2.5.

Prüfbar sind alle Kriterien auch ohne Handlung über HTTP: [198](198-plan3SichtbarGeprueftUndAbhaengigkeiten.md),
Befund 1; an den Kriterien ändert das nichts.

**Stellungnahme (Anforderungsautor).**
