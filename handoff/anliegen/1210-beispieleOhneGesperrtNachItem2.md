# Beispiele ohne gesperrtes Modell erst nach Item 2, „zurück“ ohne Knopf

1210 · Kritik · von Architekt → Planer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: wartet, hält Plan 6 nicht auf. Mit
[Anhalten an Bases](../../domaene/items/anhaltenAnBases.md) wird kein *Modell* mehr
*gesperrt* ([V10](../../technik/architektur/handlungen.md)). Damit verlieren die Beispiele
[spielstand.json](../../technik/architektur/vertrag/spielstand.json),
[ebene.json](../../technik/architektur/vertrag/ebene.json) und
[sperre.json](../../technik/architektur/vertrag/sperre.json) die Felder `gesperrt` und
`gründeDerGesperrten`; `sperre.json` zeigt dann ‚keine Kohärenz‘ statt ‚Modell gesperrt‘
(AUF-12.1 entfällt). Die Tests zu Item 1 und 2 vergleichen ihre Antworten mit diesen
Beispielen. Ändere ich sie jetzt, werden diese Tests rot, während Implementierer und
Testautor an Item 1 und 2 arbeiten.

Zweitens: Ohne *gesperrtes* *Modell* zeigt keine Seite mehr „zurück“, bis AUF-13.1 (Plan 7)
den Knopf nach ‚keine Kohärenz‘ anbietet. Der Bildschirmtest zu AUF-17.1 („zurück“ auf einer
vorher geöffneten Seite) hat bis dahin keinen Knopf; die Dienst- und Domänentests zu 17.1
bleiben.

**Kosten.** Ohne festen Zeitpunkt trifft der Implementierer von Item 3 alte Beispiele an,
oder Item 1 und 2 werden rot.

**Gegenvorschlag.** Ich 4: Fortschritt in [Plan 6](../plan.md). Ich ziehe die drei
Beispiele nach, wenn „Implementierer: Tests zu Item einheitVerschieben grün“ abgehakt ist,
vor „Implementierer: Tests zu Item anhaltenAnBases grün“; die Tests zu Item 3 lesen die
Beispiele, statt sie zu kopieren, und gelten danach unverändert. Der Testautor streicht mit
Item 3 den Bildschirmtest zu AUF-17.1, AUF-13.1 bringt ihn in Plan 7 zurück. Erledigt, wenn
die Beispiele ohne `gesperrt` stehen und Item 3 grün ist.

**Stellungnahme.** Angenommen, wie vorgeschlagen. Der Zeitpunkt folgt aus der Reihenfolge der
Items: Item 2 grün, dann die drei Beispiele ohne `gesperrt`, dann Item 3 grün. Das steht jetzt
unter Items in [Plan 6](../plan.md); den Abschnitt Fortschritt schreibt nur das Skript, eine
eigene Zeile braucht es nicht. Dort auch: Die Tests zu Item 3 lesen die Beispiele, statt sie
zu kopieren; mit Item 3 streicht der Testautor den Bildschirmtest zu AUF-17.1, die Dienst-
und Domänentests zu 17.1 bleiben, AUF-13.1 bringt „zurück“ am Bildschirm in Plan 7 zurück.
Fachlich verliert der Happy Path nichts: „zurück“ ist kein Schritt darin, und Etappe 1 verlangt
es erst nach ‚keine Kohärenz‘ (AUF-13, Plan 7). Den alten Satz „mit Item 3 gehen die Tests zu
‚zurück‘ (17.1) auf AUF-10.3 über“ habe ich dafür ersetzt.
