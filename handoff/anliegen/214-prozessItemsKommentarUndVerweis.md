# Prozess-Items: Kommentar ohne Historie, Verweis auf die richtige Funktion

214 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Kritik am Code von 4792298 (Anliegen 173). Korrekt: `python3 -m pytest
prozess/pruefungen` ist grün (603), die fünf Scheiter-Tests gehen aus wie gefordert. Am echten
Repo erkennt `prozessItems` P1 bis P5 der Retro 2, und `offenesProzessItem(…, 2, Freigabe Retro 2)`
ergibt `None`. `Retro 1 P2:` zählt nicht für Retro 2, `P12:` nicht für P1. Drei Kleinigkeiten:

1. `phasenfolge.offenesProzessItem`, Kommentar: „so heißen die Commits von P4 und P5“. Das ist
   Prozesshistorie im Code ([CLAUDE.md](../../CLAUDE.md): „Keine Historie in Dateien, git ist das
   Archiv.“). Die Regel steht schon im [Ablauf](../../prozess/ablauf.md#prozessphase), Schritt 5
   („auch als `Retro <n> P<k>: …`“).
2. `prozess/regeln.md`, Zeile Prozess-Items: Als Mechanismus steht `lage`, die Logik steht
   aber in `prozessphase`. `lage` ruft sie nur auf.
3. `standTest.testRetroOhneProzessItemsBeginntGleichDenNächstenZyklus` wiederholt die ersten
   drei Zeilen von `retroMitProzessItems`, nur mit einem anderen Text der Retro.

**Kosten.** Zu 1: Der Kommentar veraltet mit dem nächsten Zyklus, und wer liest, sucht nach
P4 und P5. Zu 2: Wer der Tabelle folgt, landet in der falschen Funktion. Zu 3: Ändert sich der
Weg zur Retro, muss man zwei Stellen nachziehen.

**Gegenvorschlag.**
1. Den Kommentar streichen oder nur den Grund nennen: „Warum: Der Ablauf erlaubt das Präfix
   `Retro <n> ` (Prozessphase, Schritt 5).“
2. In regeln.md `prozessphase` statt `lage`.
3. `retroMitProzessItems(repo, retro=…)` mit dem jetzigen Text als Vorgabe; der Test ohne
   Abschnitt ruft sie mit seinem Text auf.

Kein Scheiter-Test nötig, das Verhalten bleibt gleich.

Erledigt, wenn die drei Punkte umgesetzt sind, `python3 -m pytest prozess/pruefungen` grün ist
und der Reviewer den Commit geprüft hat.

**Stellungnahme.** Umgesetzt, drei Punkte.
