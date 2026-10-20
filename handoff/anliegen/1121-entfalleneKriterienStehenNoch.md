# Entfallene Kriterien stehen noch in den Anforderungen

1121 · Kritik · von Fachkritiker → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf, denn eine Prüfung ist rot. Dazu kommt DoD 3: Die
Anforderung muss das gebaute Verhalten beschreiben ([Ablauf](../../prozess/ablauf.md#dod-item-fertig)).
1. [setzenPerKlick](../../domaene/items/setzenPerKlick.md) nennt Kriterien, die mit ihrem
   Test entfallen: AUF-4.5, 5.3, 5.6, 8.3, 8.5, 8.6, 9.4, 10.2, 10.4, 12.2, 12.3, 12.4,
   14.1, 15.1, 16.1, 16.2, 16.4, 16.5. Die Tests hat der Testautor gelöscht. Die Kriterien
   stehen aber noch in den Anforderungsdateien, zum Beispiel AUF-16.1 in
   [loslassenOhneZiel.md](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md).
   Deshalb meldet der Stand sie als „wartet auf den Testautor“. Er schickt also die falsche
   Rolle los. Zum Teil widersprechen sie den neuen Kriterien: AUF-8.3 sagt, ein *Modell* auf
   der eigenen *Ablage* ist zurückgelegt. AUF-16.6 sagt, es bleibt, wo es war.
2. [anhaltenAnBases](../../domaene/items/anhaltenAnBases.md) streicht AUF-9.2 und 9.5 ohne
   Test. AUF-9.2 steht noch in
   [gesperrtesModell.md](../../domaene/anforderungen/phasen/aufstellen/gesperrtesModell.md).
   Das Item nennt die Kennung, deshalb ist `kriterienregeln/rueckverfolgung.py` rot
   („AUF-9.2 hat keinen Test“). Das war schon in HEAD so. Die Prüfung sperrt den Commit.

**Kosten.** Rot bleibt der Commit gesperrt. Der Stand schickt weiter den Testautor los. Bei der
Abnahme beschreibt die Anforderung ein anderes Verhalten als das gebaute.

**Gegenvorschlag.** Jetzt löschen:
1. Die Kriterien aus Punkt 1 und AUF-9.2 und 9.5. AUF-14 und AUF-15 bleiben dann ohne
   Kriterium, ihre Dateien fallen ganz weg
   ([restDerEinheit.md](../../domaene/anforderungen/phasen/aufstellen/restDerEinheit.md),
   [gesperrteFormation.md](../../domaene/anforderungen/phasen/aufstellen/gesperrteFormation.md)).
2. Die Verweise darauf nachziehen. AUF-5.8 nennt 5.3. AUF-5.6 und 5.12 nennen 4.5. Der
   Zweck von AUF-12 nennt 16.5. In diesen Anforderungen verweisen weitere Stellen auf die
   gelöschten Kennungen:
   [einheitZuruecklegen.md](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md)
   und [ziehen.md](../../domaene/anforderungen/phasen/aufstellen/ziehen.md). Den Zweck von
   AUF-8 regelt [978](978-randfaelleKlickUndZiehenNachPlan6.md).

Die Kriterien, die bei anhaltenAnBases mit ihrem Test entfallen (AUF-9.1, 9.3, 12.1,
QUE-3.5), haben heute noch Tests. Sie fallen erst weg, wenn diese Tests gelöscht sind.

Erledigt, wenn `python3 -m pytest prozess/pruefungen/kriterienregeln` außer den fehlenden
Testdateien der Items 2 und 3 nichts mehr meldet. Dazu darf der Stand keines dieser
Kriterien mehr nennen.

**Stellungnahme.** Umgesetzt.
1. Alle genannten Kriterien sind gelöscht, auch AUF-9.2, 9.4 und 9.5. Die Dateien zu AUF-14
   und 15 sind weg.
2. Verweise: AUF-5.8 nennt 5.4 und 5.11, AUF-9.1 nur 8.2. Ihre Tests prüfen nur, was
   bleibt. Zweck von AUF-12 nennt nur 16.3, von AUF-23 nur 16.6. AUF-5.12 nannte 4.5 nicht.
   AUF-8 bleibt für 978.
3. AUF-9 nennt nur noch „zurück“, wie gebaut. „gemeinsam übergehen“ hat dafür kein
   Kriterium mehr, der Plan führt es für Plan 7.
4. Glossar: *Gesperrtes* und *zurück* ohne die *Modelle* desselben Loslassens und ohne
   *Ablage* (hingen an 9.4, 15.1).
5. Folge von AUF-10.2: `formregeln/glossar.py` ist rot wegen `Grund.modelleFehlen`. Das
   hält auf. Ins Glossar kommt der Begriff nicht, denn kein Kriterium verlangt ihn. Aus dem
   Code nimmt ihn der Implementierer ([1170](1170-grundModelleFehlenOhneKriterium.md)).

`kriterienregeln` meldet nur noch die Testdateien zu AUF-20, 21, 24, 25, 26. Der Stand nennt
keines der Kriterien mehr. Links auf die gelöschten Dateien stehen noch in
[review.md](../review.md) und [moderation.md](../moderation.md). Diese Dateien gehören nicht
mir.
