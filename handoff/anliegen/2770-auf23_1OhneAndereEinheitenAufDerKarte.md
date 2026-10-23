# AUF-23.1: Kein Test legt zurück, während andere Einheiten auf der Karte stehen

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund (hält auf).** [AUF-23.1](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md)
verlangt, dass keines *ihrer* *Modelle* mehr *gesetzt* ist, also nur die der *Einheit in
Aufstellung*; der Zweck sagt „nimmt die ganze *Einheit in Aufstellung* von der *Karte*“, das
Glossar unter *zurücklegen* ebenso. Alle Tests zu AUF-23.1 in
[einheitZuruecklegenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/einheitZuruecklegenTest.py)
beginnen aber auf einer sonst leeren *Karte*: Die Boyz sind die erste *Einheit*, im Beispiel
des Vertrags stehen nur die Necron Warriors. So bestehen alle Tests auch dann, wenn
„Einheit zurücklegen“ die ganze *Karte* leert. Der Dienst-Test prüft sogar
`spielstand["modelle"] == []` und der Bildschirmtest heißt `…LeertDieKarte…` und erwartet null
*Modelle* auf der *Karte*; beide verlangen damit mehr als das Kriterium, und das Falsche
fiele nicht auf.

Auf dem Happy Path von Etappe 1 legt ein *Spieler* fast immer zurück, während *aufgestellte*
*Einheiten* beider *Spieler* schon stehen: jede *Einheit* nach der ersten.

**Kosten.** Ohne den Fall kann der Implementierer die *Karte* leeren und alle Tests sind grün;
am Bildschirm verschwänden dann beim Zurücklegen auch die schon *aufgestellten* *Einheiten*.
Nachbessern: je Ebene (Domäne, Dienst, Seite) ein Fall mehr, kein neuer Helfer.

**Gegenvorschlag.**
1. Einen Fall, in dem schon *Einheiten* *aufgestellt* sind, etwa über
   `aufstellungMitModellenBeiderSpieler` (Boyz und Necron Warriors *aufgestellt*, Spieler 1
   wieder *an der Reihe*), dann setzt Spieler 1 den Warboss (`modelleSetzen`). Nach
   *zurücklegen*: der Warboss nicht *gesetzt*, jedes *Modell* der Boyz und Necron Warriors an
   seiner *Stelle* wie davor (`stellenAllerModelle`), Spieler 1 *an der Reihe*.
2. Im Dienst dasselbe: `modelle` nennt danach genau die *Modelle* der beiden *aufgestellten*
   *Einheiten*.
3. Den Bildschirmtest umbenennen, etwa `…NimmtDieEinheitInAufstellungVonDerKarte…`, und mit
   dem Fall aus 1 prüfen, dass die *Karte* die *Modelle* der *aufgestellten* *Einheiten*
   weiter zeigt.

**Stellungnahme.** Angenommen und umgesetzt, ohne neuen Helfer außer `gesetzteStellen` in der
Testdatei. Je Ebene ein Fall mit `aufstellungMitModellenBeiderSpieler`, Warboss gesetzt, dann
zurücklegen: Domäne (`stellenAllerModelle` wie davor, Spieler 1 an der Reihe), Dienst (`modelle`
wie davor), Seite (Zahl der Kreise gleich der Zahl der aufgestellten Modelle). Der
Bildschirmtest heißt jetzt `…NimmtDieEinheitInAufstellungVonDerKarte…`.
