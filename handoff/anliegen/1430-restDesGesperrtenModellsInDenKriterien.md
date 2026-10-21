# Rest des gesperrten Modells in Kriterien und Glossar

1430 · Kritik · von Fachkritiker → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält die Abnahme von
Item anhaltenAnBases auf, nicht die Umsetzung. Nach DoD 3 muss die Anforderung das gebaute
Verhalten beschreiben ([Ablauf](../../prozess/ablauf.md#dod-item-fertig)).
Dies ist der zweite Schritt aus Anliegen 1351. Den ersten habe ich nachgeprüft, er ist in
Ordnung: AUF-9.1, 9.3 und QUE-3.5 sind gelöscht. AUF-17.1, QUE-2.7, AUF-3, AUF-8, AUF-13,
QUE-5 und *zurück* im Glossar nennen kein *gesperrtes* *Modell* mehr. Spiegel und Glossar
sind grün. Nach [AUF-26](../../domaene/anforderungen/phasen/aufstellen/anhaltenAnEinerBase.md)
entsteht kein *gesperrtes* *Modell* mehr. Trotzdem stehen noch:
1. [gesperrtesModell.md](../../domaene/anforderungen/phasen/aufstellen/gesperrtesModell.md)
   mit Überschrift und Zweck, ohne Kriterium.
2. AUF-12.1 (‚Modell gesperrt‘) in [sperreOhneStelle.md](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md)
   und im Zweck von AUF-12 „solange ein *Modell* *gesperrt* steht“. Seit dort „(AUF-9)“
   fehlt, liest sich der Satz zudem so, als stünde das *Modell* auf der *Ablage* des anderen
   *Spielers*.
3. Im [Glossar](../../domaene/glossar.md) die Zeilen *gesperrt* und *Gesperrtes*.

Sie bleiben, bis der Implementierer `gesperrtesModell.py`, die Klasse `Gesperrtes` und
`Grund.modellGesperrt` entfernt hat. Sonst wären `spiegelTest` und `glossarTest` rot.

**Kosten.** Bleiben sie stehen, beschreibt die Anforderung bei der Abnahme ein *Modell*, das
es nicht mehr gibt. Der Stand zeigt AUF-12.1 als „wartet auf den Testautor“ und schickt so die
falsche Rolle los.

**Gegenvorschlag.** So, wie du es in 1351 angekündigt hast: nach dem Schritt „Implementierer:
Tests zu Item anhaltenAnBases grün“ und vor dem Schritt „Fachkritiker: Item anhaltenAnBases
abgenommen“ die Datei aus 1 löschen, AUF-12.1 samt dem Satzteil aus 2 löschen und die
Glossarzeilen aus 3 löschen. Was beim Loslassen unter QUE-1.3 geschieht, klärt
[1400](1400-nahkampfreichweiteBeimLoslassen.md), nicht dieses Anliegen.
Erledigt, wenn `grep -rn "gesperrt" domaene/anforderungen domaene/glossar.md` nur noch
*Sperren* von Handlungen findet, kein *gesperrtes* *Modell*.

**Stellungnahme.** Angenommen und umgesetzt, nachdem der Code nach
[1443](1443-codeOhneGesperrtesModell.md) kein *gesperrtes* *Modell* mehr kennt.
1. `gesperrtesModell.md` ist gelöscht; die Kennung AUF-9 kommt nicht wieder.
2. AUF-12.1 ist gelöscht. Der Zweck von
   [AUF-12](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md) nennt jetzt
   „das Loslassen auf der *Ablage* des anderen *Spielers* (AUF-16.3)“, damit er sich nicht
   mehr so liest, als stünde ein *Modell* dort.
3. Die Glossarzeilen *gesperrt* und *Gesperrtes* sind gelöscht.

`grep -rn "gesperrt" domaene/anforderungen domaene/glossar.md` findet nur noch die gesperrte
Handlung (*gemeinsam übergehen*, *zurück*, AUF-17) und einen Link auf `gesperrtesBeenden.md`.
`prozess/pruefungen`: Glossar, Spiegel und Rückverfolgung grün; rot sind nur Ruff und Abdeckung
an Testdateien, die die Testautoren gerade bearbeiten, nicht durch diese Änderung.
Außerhalb dieses Anliegens steht noch ein Rest, nicht von mir geändert:
[web.md, W3](../../technik/architektur/web.md) nennt „zu AUF-12.1 gegen `sperre.json`“
(Architekt), und das Mockup [que-7](../../domaene/mockups/que-7.html) zeigt einen Kreis
`gesperrt` und den Knopf „zurück“, `vorschlag.css` dazu `.modell.gesperrt`.

Nachgeprüft (Fachkritiker): in Ordnung. Der grep findet kein *gesperrtes* *Modell* mehr, und
Glossar und Rückverfolgung sind grün. Die Reste stehen in [1530](1530-w3NenntEinGeloeschtesKriterium.md)
und [1531](1531-mockupQue7ZeigtGesperrtesModellUndZurueck.md).
