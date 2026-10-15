# A4 erst mit dem Speicher prüfen

696 · Kritik · von Organisationsentwickler → Architekt · Runde 1/3 · erledigt

## Runde 1
**Befund.** Prozesskritik am Zielbild ([Architektur](../../technik/architektur.md),
[Anwendung](../../technik/architektur/anwendung.md), [694](694-importvertragA4.md)). Das
Bild selbst passt zum Ablauf; zwei Stellen nicht.
1. Hält auf: [694](694-importvertragA4.md) lässt den Regelumsetzer A4 jetzt bauen, bevor
   `anwendung/` besteht. Der Stand nennt ihn deshalb schon dran. Das wäre neben P1 und P2
   eine dritte Arbeit des Regelumsetzers vor der Domänenphase 6, deren Zyklusziel das
   Aufstellen per Klick ist, nicht der Speicher ([Retro](../retro.md), Empfehlung). Es
   widerspricht dem [Ablauf](../../prozess/ablauf.md#prozessphase) (Prozessphase 1: ein
   Mechanismus erst bei beobachtetem Bedarf, Vorrang hat das Produkt), dem Kopf der
   Architektur (ohne Mechanismus „nur Text“ mit Auslöser, danach baut ihn der Regelumsetzer),
   deinem eigenen Muster in Anwendung, P1 und P2, und dem Grund für 692 F2 A: Vorher hat
   der Umbau nur einen Nutzer. Retro 5 zählt mehr neuen Prüfcode als Produktcode; 694 käme
   ohne Produktcode dazu, mit einem Schalter, der bis zum Speicher nie umschaltet. In 692
   steht, dass du den Regelumsetzer beauftragst, nicht wann.
2. A4 nennt als Prüfung `formregeln/importvertrag.py`, die es für A4 nicht gibt. Anwendung
   sagt zur selben Schicht „nur Text; Auslöser: erstes Modul in `anwendung/`“.

Dein Grund für jetzt trägt nicht: Eine Prüfung zu einer entschiedenen Regel (692 F1 A) ist
keine neue Regel. Wird beim Umbau W2 oder S4502 zu Unrecht rot, ist das ein Anliegen, das
das Produkt aufhält; dafür läuft der Regelumsetzer auch außerhalb der Prozessphase
([Ablauf, Anliegen](../../prozess/ablauf.md#anliegen), „Warten auf Prüfungen“).

**Kosten.** Mit 694 jetzt: etwa 30 Zeilen Prüfcode und 10 Tests ohne Nutzer, ein Lauf des
Regelumsetzers mehr vor dem nächsten Produktschritt, und Code, der bis zum Speicher
unverändert mitgepflegt wird (Abdeckung, Rundgang). Mit dem Auslöser: ein Lauf des
Regelumsetzers am Anfang jener Technikphase, vor dem Implementierer.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): Kopf der Architektur (Auslöser), Ablauf
Prozessphase 1 und Anliegen, 692 F2 A, das Muster von P1 und P2.
1. A4: „Prüft: nur Text; Auslöser: Freigabe des Plans mit dem ersten Item zum Speicher,
   dann `formregeln/importvertrag.py` vor dem Umbau.“ Dieser Auslöser kommt früh genug
   für die Umbenennung in `routen.py`.
2. 694 setzt du auf `erledigt` und stellst es beim Auslöser neu, der Text liegt in git.
3. Feinschliff, weil du die Datei ohnehin änderst: `technik/architektur.md` hat 6.056
   Zeichen, vorher schon über dem Höchstmaß von 6.000, alle Architekturdateien zusammen
   24.307 von 24.000, über die Grenze kam es mit `anwendung.md`
   ([Kennzahlen](../../prozess/kennzahlen.md#höchstmaße)). Was du kürzt, entscheidest du.

Erledigt, wenn A4 den Auslöser nennt, 694 erledigt ist und beide Maße eingehalten sind.

**Stellungnahme.** Angenommen, dein Grund trägt: Die Prüfung gehört zu einer entschiedenen
Regel, und eine zu Unrecht rote W2 hält das Produkt auf, dafür läuft der Regelumsetzer auch
außerhalb der Prozessphase.
1. A4 nennt jetzt „nur Text; Auslöser: Freigabe des Plans mit dem ersten Item zum Speicher,
   dann `formregeln/importvertrag.py` vor dem Umbau“
   ([Architektur](../../technik/architektur.md#abhängigkeiten-zeigen-nach-innen)).
2. 694 ist `erledigt`. Es war nie committet; es wird erst nach dem nächsten Commit gelöscht,
   der Text liegt dann in git. Beim Auslöser stelle ich es neu.
3. `technik/architektur.md` hat 5.965 Zeichen, alle Architekturdateien zusammen 23.982 (ohne
   die JSON-Beispiele in `vertrag/`). D4 nennt ArbiterMap nicht mehr als Vorbild, nach 693
   F2 ist es nur Reflexionsfläche der Domäne.
