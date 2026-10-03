# Plan · Zyklus 2

Etappe: [1 · Aufstellen](../domaene/etappen/01-aufstellen.md)

## Items
1. [Ausgangslage von Only War](../domaene/items/ausgangslage-only-war.md): AUF-2.1 bis AUF-2.5
2. [Sperren beim Setzen](../domaene/items/sperren-beim-setzen.md): AUF-3.1 bis AUF-3.3, nach Item 1

## Empfehlung
Freigeben mit beiden Items. Reihenfolge nach Abhängigkeit und Nutzen: Die Sperren beim Setzen
sind der Kern von Etappe 1 und das erste Stück Geometrie (Bases, Zonen, Abstände), auf dem
Bewegen, Schießen und Charge aufbauen; prüfen lassen sie sich erst mit Bases und Zonen der
Ausgangslage. Reicht der Zyklus nur für eins, kommt Item 1 allein. Beide ohne Oberfläche:
Nach Zyklus 2 ist noch nichts klickbar.

Der Zyklus ist größer als die zwei Items aussehen ([102](anliegen/102-plan2KostenUndGrenzen.md)):
- Item 1 liest die Daten der Ausgangslage über `katalog/`, ohne Datenbank; der Regelumsetzer
  baut im selben Zyklus den Importvertrag (Architektur A1).
- Item 2 ändert die grünen AUF-1-Tests: Setzen mit Stelle, Modelle mit Base.
- Item 2 ist technisches Neuland: Vor dem Testautor legt der Architekt nach einem
  Wegwerf-Versuch fest, wie eine Stelle angegeben wird und womit gerechnet wird, damit die
  Grenzfälle aus 100 F2 ohne Toleranz gelten; dazu die Messungen (M1) um *überdecken*.

AUF-3.4 (Nahkampfreichweite) ist nicht dabei: Mit den 9″-Bändern liegt jede solche Stelle auch
außerhalb der eigenen Zone, prüfbar ist sie erst mit dem Kriterium zu mehreren Gründen, das der
Anforderungsautor nach deiner Antwort in [100](anliegen/100-auf2auf3BegriffeUndGrenzfaelle.md)
schreibt, dazu dein Begriff Nahkampfreichweite. Steht beides vor der Freigabe, nehme ich das
Item `nahkampfreichweite-beim-setzen` als drittes auf; sonst führt es Zyklus 3 an. Den Begriff
habe ich in Etappe 1 übernommen.

Grenzen der Items, damit Testautor und Implementierer nichts erfinden:
- Gesetzt wird in Tests nur aus der Ausgangslage; die Ablage als Ort neben der Karte, Umsetzen
  und Zurücklegen kommen später (Etappe 1, Anliegen 16 F1, F2, git).
- Mit Sperre bleibt der Zustand unverändert (Architektur D2): Das Modell ist nicht gesetzt.
  Stehenbleiben mit Grund, „zurück“, „gemeinsam übergehen“ und Protokoll kommen später (16 F4).
- Akzeptanztests beenden eine Einheit erst, wenn alle ihre Modelle gesetzt sind und die Einheit
  in Kohärenz steht; die Sperren beim Beenden kommen später (16 F3).
- Nur runde Bases ohne FLY; andere Formen bringt Etappe 6.

## Danach, nach Abhängigkeit
Nahkampfreichweite beim Setzen (siehe oben) · Ablage, Umsetzen, Zurücklegen und die erste
Oberfläche: Karte mit Spielfeld und Zonen, Ziehen mit Maus und Touch, dafür UX und Mockup ·
Zurück, gemeinsam übergehen und Protokoll (16 F4) · Beenden mit fehlenden Modellen und
Kohärenz (16 F3). Mit diesen vier ist Etappe 1 erreichbar.

## Offene Anliegen
An dich:
- [83](anliegen/83-sprungErproben.md): Sprung zwischen Kriterium und Test erproben.

Zwischen Rollen:
- [102](anliegen/102-plan2KostenUndGrenzen.md): Kritik des Architekten an Plan 2, angenommen,
  seine Nachprüfung.
- [100](anliegen/100-auf2auf3BegriffeUndGrenzfaelle.md): deine Antworten stehen, der
  Anforderungsautor arbeitet sie ein (Glossar, AUF-3.4, Kriterium zu F3); Plan 2 hängt nicht
  daran.
- [97](anliegen/97-kritikAmZweckDerAufstellung.md): deine Kritik am Zweck der Aufstellung,
  angenommen, deine Nachprüfung.
- Anliegen 92, Anliegen 96 an den
  Regelumsetzer, angenommen, Nachprüfung durch den Reviewer.
