# V18 nach BEW-8.3 bis 8.5 nachziehen

Form: Kritik
Von: Architekt
An: Architekt
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Wartet (Kritik: In der Domänenphase ziehe ich nur Namen nach, Anliegen 370; hier
ändert sich eine Regel des Vertrags). Nach 9881 ist
[V18](../../technik/architektur/vertrag/schlacht/uebergehen.md) veraltet:
1. Er nennt BEW-8.1 und 8.2, die es nicht mehr gibt, und kennt Übergehen nur nach einer 409
   mit `übergehbar`. [BEW-8.3](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md)
   bietet es nach einem Loslassen mit 200 an, angehalten, ohne *Grund*.
2. „ohne *Sperre* wie ohne `übergehen`, ohne Eintrag (QUE-5.1: „bei einer *Sperre*“)“
   widerspricht BEW-8.5: Übergehen nach Anhalten trägt ein, ohne *Sperre*. QUE-5.1 bleibt
   bei der *Sperre* und ist in Etappe 2 nicht mehr erreichbar (9940).
3. BEW-8.4 (nach 9941 B): ein Weiterrücken ab der angehaltenen *Stelle* zum Punkt des
   Loslassens, ohne BEW-3.1 und 6.2, mit BEW-17; die *Gründe* sind die, die dabei angehalten
   hätten, nicht die einer 409.
4. Schickt die Seite dazu wieder `modellLoslassen` mit `übergehen`, ändert ein Loslassen das
   *Protokoll*; QUE-5.6 sagt nein. Der Name der Handlung muss zur Domäne passen.

**Kosten.** Ein Abschnitt V18 und ein Beispiel neu, vor den Tests zu Item anhaltenUebergehen
(Technikphase 1). Bleibt er, baut der Testautor auf einen Vertrag, der BEW-8.4 und 8.5 nicht
erfüllt. 8261 (1, 2) hängt an derselben Stelle von `modellLoslassen`.

**Gegenvorschlag.** In Technikphase 10, Schritt 1: V18 auf BEW-8.3 bis 8.5 fassen, eine eigene
Handlung *gemeinsam übergehen* der *Bewegungsphase* ohne Körper außer dem Punkt des
Loslassens; die Domäne rechnet ab der angehaltenen *Stelle* (nichts zusätzlich gespeichert,
[P2](../../technik/architektur/speicher.md)) und bildet die *Gründe*. Der Weg über
`Sperre(übergehbar=True)` bleibt für QUE-5.1 bis AUF-31. Antwort von 9941 vorher einarbeiten.

**Stellungnahme.**
