# messen.py: drei Erklärungen stehen weder im Code noch in S3 oder M1

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund (hält auf).** Plan 7 verlangt für jeden gelöschten Kommentar: „Was ein Kommentar
erklärt, steht danach im Namen, in einem einzeiligen Docstring oder in der Architektur; was
dort schon steht, entfällt.“ Von den 27 Kommentaren in Domäne, Katalog, `__main__.py` und dem
Einheitstest außerhalb von Anliegen 2540 trägt die Architektur (S1 bis S3, D4, W5), das
Glossar, ein Name oder ein Kriterium (AUF-6.1) alle bis auf drei in
[messen.py](../../technik/arbiter/domaene/messen.py):

1. `_ersterÜberdeckenderSchritt`, zwei Kommentare: Der Abstand der Mittelpunkte fällt bis
   zum nächsten Punkt des Wegs und steigt danach, darum genügen dahinter zwei Schritte und
   davor die Halbierung (`bisect_left`). [S3](../../technik/architektur.md) beschreibt nur das
   Raster, nicht diese Suche; ohne den Satz kann niemand prüfen, ob sie stimmt.
2. `_rückung`: „Zu weit vorn rückt hinein, zu weit hinten zurück; passt beides nicht, gilt
   vorn.“ [M1](../../technik/architektur.md) nennt nur den kürzesten Weg, nicht diesen Vorrang;
   `max(…) or min(…)` zeigt ihn nicht.
3. `anteilBisZurBerührung`: Der Docstring sagt „bis zur ersten Überdeckung …, sonst 1“. Der
   gelöschte Kommentar sagte, dass nur angehalten wird, wenn das Ende des Wegs überdeckt
   (heute AUF-29.1). Ohne ihn verspricht der Docstring etwas anderes, als der Code tut: Ein
   Weg quer durch eine *Base*, der frei endet, gibt 1.

Ob die Namen sonst genügen, urteilt der Reviewer; hier steht nur, was die Architektur nicht
trägt. In die Architektur gehört keiner der drei: Sie gelten nur in `messen.py`, und die
Architektur liegt schon über dem Höchstmaß (Anliegen 2570).

**Kosten.** Drei Docstrings. Ohne sie liest man in der Rechnung für das Anhalten (AUF-29)
nicht mehr, warum sie stimmt; sie wächst mit Etappe 2 (Normal Move).

**Gegenvorschlag.** Je ein einzeiliger Docstring:
- `_ersterÜberdeckenderSchritt`: „Erster Schritt mit Überdeckung; der Abstand fällt bis zum
  nächsten Punkt des Wegs und steigt danach.“
- `_rückung`: „Zu weit vorn rückt hinein, zu weit hinten zurück; passt beides nicht, gilt vorn.“
- `anteilBisZurBerührung`: „Der Anteil bis vor die erste Überdeckung auf dem Raster von S3,
  1, wenn das Ende des Wegs nichts überdeckt.“

Erledigt, wenn die drei Funktionen das sagen, im Wortlaut nach deiner Wahl.

**Stellungnahme.** Angenommen, alle drei. Die Docstrings stehen in
[messen.py](../../technik/arbiter/domaene/messen.py), sinngemäß nach dem Gegenvorschlag,
gekürzt auf 100 Zeichen (Prüfregel): `_ersterÜberdeckenderSchritt` ("bis zum nächsten Punkt,
dann steigt er"), `_rückung` im Wortlaut, `anteilBisZurBerührung` mit "1, wenn das Ende frei
ist". Gleiche Umsetzung wie Anliegen 2620.
