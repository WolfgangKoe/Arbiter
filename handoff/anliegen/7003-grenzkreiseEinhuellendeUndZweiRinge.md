# Grenzkreise: Einhüllende der Einheit, zwei Kreise beim Vorrücken, weitere Grenzen

Form: Kritik
Von: Ux
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Stakeholder kommentiert [Anliegen 6410](6410-grenzkreiseNahkampfUndBewegung.md) und
will ein anderes Verhalten als [BEW-11](../../domaene/anforderungen/phasen/bewegung/grenzkreise.md).
Ein Mockup ohne Kriterium darf ich nicht zeichnen. Es fehlt:
1. Wählt der *Spieler* ein *Modell* aus, zeigt die *Karte* dessen *Grenzkreis*. Beim *Vorrücken*
   zwei Kreise: einen bis zur *Bewegungsweite*, einen weiteren für die Zusatzbewegung des
   *Vorrückwurfs*. BEW-11.2 sagt bisher nur einen größeren Kreis (Anliegen 6998 F1 A).
2. Ist eine ganze *Einheit* *ausgewählt*, zeigt die *Karte* nicht die Kreise der einzelnen
   *Modelle*, sondern ihre Einhüllende. Das gilt für alle Grenzen aus 1 und für die
   *Nahkampfreichweite* (BEW-11.3).
3. Dieselbe Darstellung für weitere Grenzen (Angriffsreichweite, Aura, „innerhalb von x Zoll der
   *Aufstellungszone* des Gegners“); nur, wenn eine Regel sie braucht.
4. Andere *Base*-Formen: die Form wird ausgedehnt; zu gegebener Zeit.
Farbe, Linienart und -dicke sind Parameter der Darstellung, keine Fachlichkeit; die Komponente
klärt der Architekt in Anliegen 7004.

**Kosten.** Ohne neue Fassung bleibt bew-11 beim Kreis je *Modell*; die Einhüllende zeichne ich
erst mit Kriterium.

**Gegenvorschlag.** BEW-11 für Punkt 1 und 2 neu fassen (neue Kennungen, alte bleiben); Punkt 3
und 4 erst mit einem Kriterium, das sie braucht.

**Stellungnahme.** Punkt 1 und 2 standen schon seit den Antworten in Anliegen 6998 Runde 2,
jetzt für die *Einhüllende* beim *Vorrücken* genauer:
- Ein *Modell* als *Ebene*: sein *Grenzkreis*
  ([BEW-11.1](../../domaene/anforderungen/phasen/bewegung/grenzkreise.md)); die ganze *Einheit*
  als *Ebene*: die *Einhüllende* (BEW-11.5); *Nahkampfreichweite* je *Einheit* des anderen
  *Spielers* als *Einhüllende* (BEW-11.3, 6998 F3 A).
- *Vorrücken*: vor dem *Vorrückwurf* sechs weitere *Grenzkreise* oder *Einhüllende*, je
  *Grenzkreis* um 1″ bis 6″ größer
  ([BEW-13.1](../../domaene/anforderungen/phasen/bewegung/grenzkreiseBeimVorruecken.md)),
  danach nur der des Wurfs (BEW-13.2), zusammen also zwei: *Bewegungsweite* und *Bewegungsweite*
  plus Wurf, wie der Stakeholder es will.
Punkt 3 und 4 wie vorgeschlagen: erst mit einem Kriterium, das sie braucht; in Etappe 2 braucht
keines Angriffsreichweite, Aura oder Abstand zur *Aufstellungszone*, und alle *Bases* sind rund.
bew-11 kannst du danach neu zeichnen; bew-13 zeigt die sechs und die zwei.
