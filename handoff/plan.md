# Plan · Zyklus 2

Etappe: [1 · Aufstellen](../domaene/etappen/01-aufstellen.md)

## Items
1. [Ausgangslage von Only War](../domaene/items/ausgangslage-only-war.md): OBJ-1.1, AUF-2.5 bis
   AUF-2.7, nur Daten
2. [Sperren beim Setzen](../domaene/items/sperren-beim-setzen.md): QUE-1.1, QUE-1.2, AUF-2.4,
   AUF-3.2, AUF-3.5, AUF-3.6, AUF-3.7, ohne Nahkampfreichweite, nach Item 1
3. [Nahkampfreichweite beim Setzen](../domaene/items/nahkampfreichweite-beim-setzen.md):
   AUF-3.4 mit seinem Teil von AUF-3.5 und AUF-3.7, nach Item 2

## Empfehlung
Freigeben mit allen drei Items. Reihenfolge nach Abhängigkeit und Nutzen: Die Sperren beim
Setzen sind der Kern von Etappe 1 und das erste Stück Geometrie (Zonen, Bases, Abstände), auf
dem Bewegen, Schießen und Charge aufbauen; sie brauchen die Modelle mit Base aus Item 1. Die
Nahkampfreichweite ist die letzte Sperre beim Setzen; mit den 9″-Bändern sperrt sie nie
allein, sie braucht die mehreren Gründe (AUF-3.5) aus Item 2. Reicht der Zyklus nicht, fällt
zuerst Item 3, dann Item 2. Alle ohne Oberfläche: Nach Zyklus 2 ist noch nichts klickbar.

Der Zyklus ist größer als die Items aussehen (Architekt, Anliegen 102, git):
- Item 1 liest die Daten der Ausgangslage über `katalog/`, ohne Datenbank; der Regelumsetzer
  baut im selben Zyklus den Importvertrag (Architektur A1).
- Item 2 ändert die grünen Tests zu AUF-1: Setzen mit Stelle, Modelle mit Base, eine Sperre mit
  mehreren Gründen.
- Item 2 ist technisches Neuland: Vor dem Testautor legt der Architekt nach einem
  Wegwerf-Versuch fest, wie eine Stelle angegeben wird und womit gerechnet wird, damit die
  Grenzfälle aus 100 F2 ohne Toleranz gelten; dazu die Messungen (M1) um *überdecken*. Die
  ganze Geometrie, auch das Zonenband (AUF-2.4), liegt deshalb in Item 2; Item 1 ist allein
  machbar.

Grenzen der Items, damit Testautor und Implementierer nichts erfinden:
- Gesetzt wird in Tests nur aus der Ausgangslage oder von der vorigen Stelle (AUF-3.7); die
  Ablage als Ort neben der Karte und Zurücklegen kommen später (Etappe 1, Anliegen 16 F1, F2,
  git).
- Mit Sperre bleibt der Zustand unverändert (Architektur D2): Das Modell bleibt ungesetzt
  oder an seiner vorigen Stelle. Stehenbleiben mit Grund, „zurück“, „gemeinsam übergehen“ und
  Protokoll kommen später (16 F4).
- Akzeptanztests beenden eine Einheit erst, wenn alle ihre Modelle gesetzt sind und die Einheit
  in Kohärenz steht; die Sperren beim Beenden kommen später (16 F3).
- Nur runde Bases ohne FLY; andere Formen bringt Etappe 6.

## Danach, nach Abhängigkeit
Ablage, Zurücklegen und die erste Oberfläche: Karte mit Spielfeld und Zonen, Ziehen mit Maus
und Touch, dafür UX und Mockup · Zurück, gemeinsam übergehen und Protokoll (16 F4) · Beenden
mit fehlenden Modellen und Kohärenz (16 F3). Mit diesen drei ist Etappe 1 erreichbar.

## Offene Anliegen
An dich:
- [83](anliegen/83-sprungErproben.md): Sprung zwischen Kriterium und Test erproben, Runde 3.

Zwischen Rollen:
- Anliegen 108,
  Anliegen 109,
  Anliegen 110,
  Anliegen 112: angenommen und eingearbeitet, Nachprüfung
  durch Anforderungsautor und Architekt.
