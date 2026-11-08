# Vertrag: Aufstellen · Ziehen

Abschnitt der *Aufstellung*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt/).

Nach V10 (AUF-24.3, 26.5, 28.2, 29): `stellenBeimLoslassen(modell, stelle, weiter=None)` →
`Gezeigt` nennt in `stellen` (*Modell* → *Stelle*) jedes *Modell*, das
`modellLoslassen(modell, stelle, weiter=None)` → `None` *setzen* würde (das gezogene oder jedes
*gesetzte* der *Einheit*, [V3](auswahl.md)), ohne zu *setzen*, Wächter wie dort;
`modellLoslassen` *setzt* genau diese (AUF-28.2). `Schlacht` hat beide gleich, ohne weiteren
Parameter (übergangen wird nach [V18](../schlacht/uebergehen.md)). Unveränderlich, in
`phasen/aufstellen/anhaltenAufDemWeg.py`: `Weiterrücken(zuvor: Stelle | None,
angehaltenAufDemWeg: bool)` trägt die übrigen Eingaben von V10, `zuvor` `None` heißt die
*Stelle* vor dem Ziehen; in `querschnitt/setzen.py`: `Gezeigt(stellen: Mapping[Modell,
Stelle], angehaltenAufDemWeg: bool)`. `weiter=None` gilt wie `Weiterrücken(None, False)`;
`web/` übergibt `None`, wenn die Anfrage keine der Eingaben nennt. Warum `Gezeigt` keine
Zuordnung ist: Es trägt zwei Aussagen, ein Untertyp von `Mapping` mit Zusatzfeld hielte den
Vertrag von `Mapping` nicht (Es, L). Warum dort: Module spiegeln die Anforderungen
([Domäne](../../domaene.md#grundschnitt-der-domäne)); `Gezeigt` nennt, was beide Phasen
*setzen* würden (QUE-1), das Gleiten ist AUF-29, BEW-17 verweist darauf.

**Gleiten** (AUF-29, in `phasen/aufstellen/anhaltenAufDemWeg.py`, auch für BEW-17): Alle
*Modelle* der *Ebene* gehen um denselben Weg; zuvor gezeigt ist jedes um den des gezogenen
von seiner *Stelle* vor dem Ziehen nach `zuvor` verschoben. Ziel ist die *Stelle* nach
AUF-8.2, 21.1, 21.2 und 26.1 (Bewegung: [Ziehen](../bewegung/ziehen.md)). Hindernis ist jede
nach AUF-29.3 fremde *Base*, die zuvor keine der *Ebene* *überdeckt*. *Überdeckt* am Ziel
keine eines, zeigt sie das Ziel. Sonst rückt sie ab zuvor um den waagrechten, dann den
senkrechten Teil des Wegs zum Ziel, wenn er nicht null ist und an seinem Ende keine eines
*überdeckt* (29.2); sonst so weit auf der geraden Strecke zum Ziel, wie keine eines
*überdeckt* (29.1, Raster [S3](../../domaene.md#stelle-und-rechnen)). Geprüft wird nur das
Ende, nicht der Weg dorthin (Zweck AUF-29). `angehaltenAufDemWeg` ist wahr, wenn es die
Eingabe war oder 29.1 oder 29.2 griff. Warum zuvor aus der Seite: Die Seite schickt sie als
double, `web/` rundet nach S2 bis 10⁻¹¹″ daneben; im Versuch zu 10321 *überdeckt* ein Halt
10⁻⁹″ vor der Berührung danach nie, enger liegt einer nach S3 etwa einmal in 10⁹, dann zählt
diese *Base* einen Schritt lang nicht. Beispiel
[stelleBeimLoslassen.json](../stelleBeimLoslassen.json): Stand von V1, `x=35&y=28` für
*Modell* 1, AUF-21.2 rückt den Block hinein.

*Neben der Karte* loslassen (V10, Seite): AUF-28.1 mit dem Punkt der letzten 200; ein
*Modell* einer *aufgestellten* *Einheit* bekommt in V10 nur 409, also keine Anfrage und
keine `sperrmeldung` (AUF-16.8). Ist das gezogene *Modell* nicht *gesetzt* (eine zweite Seite
zeigt es noch, AUF-16.7), geben vor jedem Wächter `stellenBeimLoslassen` `Gezeigt({}, False)`
(V10 200 mit leerem `modelle[]`) und `modellLoslassen` nichts zurück, ohne `Sperre`, Stand unverändert.
Warum vor den Wächtern: Kein *Grund* nach AUF-16.7, auch wenn inzwischen eine andere
*Einheit in Aufstellung* ist. Beispiele: [losgelassen.json](../losgelassen.json), V5 200:
Stand von `stelleBeimLoslassen.json`, dann `PUT …/modelle/1/stelle` mit `{"x": 35, "y": 28}`,
also neben der *Karte* nach dieser 200 losgelassen.
[keineStelleBeimLoslassen.json](../keineStelleBeimLoslassen.json), V10 200: Stand von
`zurueckgelegt.json`, dann dieselbe Abfrage wie `stelleBeimLoslassen.json`; V5 danach an
jedem Punkt 200 gleich `zurueckgelegt.json`. Eine 409 in V10 liefert die Seite wie
[sperre.json](../sperre.json), ihr Inhalt zählt dort nicht (V10).

Prüft wie im Querschnitt: AUF-29.1 mit einem Weiterrücken ab der *gesetzten* *Stelle*, an
der *Stelle* nach dem Loslassen (28.2): auf der Strecke zur *Stelle*, wie `web/` sie liest
(S2, exakt kollinear), keine *Base* *überdeckt*, zur ersten angestoßenen `abstandHöchstens`
1/100″; den Raster prüfen nur Unit-Tests. AUF-29.1 und 29.2 mit zwei Abfragen, die zweite
mit `zuvorX`, `zuvorY` aus der ersten; 28.2: V5 mit den Eingaben der zweiten *setzt* deren
`modelle[]` exakt. Am Bildschirm mit `page.route`: Die zweite Abfrage trägt `x`, `y` des
gezogenen aus der ersten 200, der Körper von V5 die Eingaben der letzten Abfrage. AUF-24.3, 26.5 und 28.1 am Bildschirm nach V10.
AUF-28.1 mit `page.route`: Der Körper von V5 gleicht dem Punkt der letzten 200, auch wenn
danach eine 409 kam; die Kreise stehen wie `losgelassen.json`. Am Dienst: die Antworten
gleich den Beispielen. Am echten Server: über die *Spielfeldkante* auf eine *Armeeliste* und daneben
loslassen, die *Stellen* gleich den zuletzt gelesenen `cx`, `cy` (B3). AUF-16.8: keine
Anfrage nach V5, Kreise wie vor dem Ziehen, keine `sperrmeldung`. AUF-16.7: mit einer Seite
von vor `PUT /api/zurücklegen`, auf und neben der *Karte* losgelassen, danach kein *Modell*
der *Einheit* auf der *Karte* (die Seite zeichnet die Antwort, V6) und keine `sperrmeldung`.
