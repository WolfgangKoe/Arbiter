# Kein Test zu QUE-7.1 rollt vor dem Klick

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf: Ein Test prüft sein Kriterium nicht. `ruhigeKarteTest.py` liest `davor` stets
ohne gerollte Spalte. Mit den neuen Maßen sind alle 88 Fälle grün, obwohl die *Karte* bei 1024×768
und 1100×800 nach dem Rollen 20 Pixel springt
([Messung](14480-ruhigeKarteSpringtNachDemRollen.md)). Grün hieße hier: Sprung übersehen.

**Kosten.** Ein Test, rund 15 Zeilen, etwa 5 Sekunden in den vier Fenstern.

**Gegenvorschlag.** Ein Test, der vor `davor` mit dem Mausrad über der Knopfzeile rollt und danach
den Knopf mit `seite.mouse` an seinem Platz klickt, denn `Locator.click` rollt selbst. Er legt den
Weg der Lösung nicht fest. Erprobt: `/tmp/arch1448/mess/rollenAnhang.py`, „gemeinsam übergehen“ mit
ausgewähltem *Warboss*. Ergebnis: Mit den Maßen aus `vorschlag.css` rot bei 1024 und 1100, grün bei
1280 und 1920; mit der Regel aus 14480 in allen vier grün. Erledigt, wenn ein solcher Test in
`ruhigeKarteTest.py` steht.

Ohne Befund geprüft:
- Die 6 Fälle in `ziehenTest.py` bei 1920×1080: Das Verhalten hängt nicht vom Fenster ab, die
  Annahme des Tests (Griffversatz und Zug über der Zugschwelle) ginge bei 1280×720 nicht auf
  (5,1 Pixel je *Zoll*). Der Test zur Zugschwelle selbst bleibt dort.
- `testBew8_4DieSeiteSetztNachDemKlickAufGemeinsamÜbergehenAmPunkt`: Ein Pixel genau entspricht B5,
  exakt prüfen die Tests zu BEW-8.4 ohne Bildschirm in derselben Datei, und ein Anhalten an der
  *Bewegungsweite* läge weit über einen Pixel daneben. Der Commit lockert keine weitere Prüfung; gelesen im Diff von 4fd5bd9.
- Die Abbildung aus `getScreenCTM()` samt Toleranz 1e-4 entspricht B3 und misst das Kriterium:
  Größe und Lage der *Karte*, auch nach dem Rollen. Rot am Commit: 58 von 88; grün mit den neuen
  Maßen: 88 von 88.
- Das `fenster` an `Bildschirm` und der zweite Browser mit Rollbalken sind klein und nur dort
  genutzt, wo sie gebraucht werden.
- `scrollbar-gutter` ändert nur etwas, wenn der Rollbalken kommt oder geht, also wenn die zweite
  Knopfzeile entsteht oder wegfällt; dass das nur wenige Fälle bemerken, ist kein Mangel. Die
  Gegenprobe (2 Tests in 2 Fenstern) habe ich nicht wiederholt.
- BEW-18.6 fehlt zu Recht, es gehört zu Etappe 7; dieser Commit berührt BEW-18.7 nicht.

**Stellungnahme.** Umgesetzt: `testQue7_1NachDemRollenBleibtDieKarteStehenWennGemeinsamÜbergehenNebenDenÜbrigenKnöpfenAufhört` in `ruhigeKarteTest.py`, in allen vier Fenstern. Er rollt nach der Vorbedingung (vier Knöpfe zu sehen) vor `davor` mit dem Mausrad und klickt den Knopf mit `seite.mouse` an seinem Platz.

Gelaufen:
- `komponenten.css` im Arbeitsbaum, nur die Maße: rot bei 1024 und 1100 an der Prüfung der Abbildung, grün bei 1280 und 1920; die übrige Datei grün (2 rot, 90 grün).
- Kopie in `/tmp` mit der Regel aus 14480: grün in allen vier Fenstern, nur dieser Test gelaufen.

Abweichungen von `rollenAnhang.py`, Absicht:
- Gerollt wird über der Mitte der `.knopfGruppe`, nicht 10 Pixel über dem Rand der Spalte.
- Der Test prüft nicht, dass etwas gerollt ist: Mit der Regel aus 14480 gibt es nichts mehr zu rollen, und der Weg der Lösung bleibt offen. Das Rollen wartet fest 200 Millisekunden wie die Probe, weil `mouse.wheel` das Ende nicht meldet und in Fenstern ohne Überstand kein Zustand zu erwarten ist.

Nicht abgedeckt, wie im Gegenvorschlag: die beiden anderen Auslöser aus 14480 (gesperrtes „Phase beenden“, freie *Stelle*) und 1220×800. Der gewählte Auslöser erfasst auch, dass bei 1100×800 die zweite Zeile wegfällt (14480, Weg B).
