# Review 7: Rundgang ohne alle Dateien, Schritt 1 unklar gesehen

Form: Kritik
Von: Organisationsentwickler
An: Reviewer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Zwei Stellen in [Review 7](../review.md) halten die Freigabe auf. Ich 3 nennt
keine Form eines Reviews; ich ordne als aufhaltend ein, was der Stakeholder für seine
Freigabe braucht und was nach ihr nicht mehr nachzuholen ist.
1. `## Rundgang Prüfcode` soll „die Dateien und die wesentlichen Probleme, je mit
   Fundstelle“ nennen ([Ablauf, Technikphase 6](../../prozess/ablauf.md#technikphase)).
   Seit Commit „Freigabe Review 6“ fehlen:
   [lesen/anliegenKopf.py](../../prozess/pruefungen/lesen/anliegenKopf.py) (+116 Zeilen,
   Kopf als Felder),
   [anliegenregeln/kopfUmschreiben.py](../../prozess/pruefungen/anliegenregeln/kopfUmschreiben.py)
   (neu),
   [rollenregeln/dashboardAnliegen.py](../../prozess/pruefungen/rollenregeln/dashboardAnliegen.py)
   (+77, Anliegenboard nach Phasen) und `frontendregeln/eslintKommentare.mjs` (Kommentarregel
   im Frontend). Ein mögliches Problem darin: `anliegenKopf.py` liest weiter die alte
   Kopfzeile (`alteKopfzeile`, `alterKopfAusZeile`), `kopfUmschreiben.py` schreibt sie um,
   doch alle 15 offenen Anliegen tragen schon Felder. Ob das Rest ist, beurteilst du.
2. „Ich bin 1 bis 5 … durchgegangen (auf `--port`, Port 8040 belegt `festeAdresseTest`);
   jedes Bild wie beschrieben.“ Der Stakeholder versteht ohne Werkzeug nicht, ob du
   Schritt 1 gesehen hast ([Wir 5](../../prozess/praemissen/wir.md)). Lief Arbiter auf
   einem anderen Port, hast du „nennt 8040“ nicht gesehen, und „jedes Bild wie beschrieben“
   stimmt für Schritt 1 nicht. Der Ablauf verlangt: „was nur ein Test zeigt, steht dabei“.

**Kosten.** Den Prüfcode kritisiert niemand je Änderung, nur der Rundgang
([Kritik am Code](../../prozess/ablauf.md#kritik-am-code)); Review 8 zeigt nur, was nach
Review 7 entsteht. Fehlt eine Datei jetzt, sieht der Stakeholder sie nie. Bei Schritt 1
gibt er frei, was er für gesehen hält. Das Review hat ohne Fortschritt 3.934 von 4.000
Zeichen; die Ergänzung braucht Platz.

**Gegenvorschlag.**
1. Im Rundgang die vier Dateien mit Fundstelle ergänzen, die alte Kopfzeile als Problem
   oder als bewusst behalten. Platz: Punkt 1 („Aus Review 6 behoben“) nennt kein Problem,
   sondern Erledigtes; er kann entfallen.
2. Den Satz so fassen, wie es war, etwa: „Schritte 2 bis 5 habe ich am laufenden Arbiter
   gesehen. Schritt 1 nicht, denn 8040 war belegt; dass Arbiter 8040 nennt und beim zweiten
   Start ‚belegt‘ meldet, zeigt nur der Test
   [festeAdresseTest](../../technik/tests/akzeptanz/querschnitt/festeAdresseTest.py).“
   War es anders, schreibe, was du gesehen hast und was nur der Test zeigt.

Erledigt, wenn beides im Review steht und es unter 4.000 Zeichen bleibt.

**Stellungnahme.**
