# Kein Test bindet spielstand.json an Backend und Frontend

331 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** [Vertrag](../../technik/architektur/vertrag.md), Absatz „Prüft V1 bis V3“, verlangt
zwei Hälften: das Backend mit dem Flask-Testclient und das Frontend mit einem Bildschirmtest,
dem Playwright `spielstand.json` per `page.route` statt des Servers liefert; „Tests lesen die
Datei“. Die Commits 4603003 bis aad7540 haben die Dienst-Tests und den Ablauf gegen den echten
Server, aber keinen Test, der `technik/architektur/vertrag/spielstand.json` liest
(`grep -rn spielstand.json technik/` ist leer). Die Dienst-Tests prüfen einzelne Felder
(`ausgewählt`, `inAufstellung`, `modelle[].x`), nie die ganze Form.

Beispiel: Benennt der Implementierer `nichtGesetzt` im Backend in `ungesetzt` um und zieht das
Frontend mit, bleiben alle 60 Tests grün; der Vertrag ist dann falsch, und wer nach ihm baut
(nächste Seite, Mockup), liest ein Feld, das es nicht gibt. Umgekehrt merkt kein Test, wenn das
Frontend ein Feld liest, das V1 nicht nennt.

Zweitens der Platz: `auf5Test.py` hat 19.750 von 20.000 Zeichen
([Kennzahlen](../../prozess/kennzahlen.md)), die Tests zu AUF-5.5 stehen noch aus. Darüber wird
nach [T1](../../technik/architektur.md#tests) die Anforderung geteilt, nicht der Test.

**Kosten.** Ohne Vertragstest gehen Backend und Frontend auseinander, sobald einer allein ändert;
die gleichzeitigen Läufe (Grund aus Anliegen 327) haben dann keinen gemeinsamen Maßstab außer
dem Gesamtablauf. Die zwei Tests unten kosten etwa 1.500 Zeichen, die `auf5Test.py` nicht mehr
hat; mit AUF-5.5 wird die Datei ohnehin zu groß.

**Gegenvorschlag.**
1. Dienst-Test zu AUF-5.6: den Stand des Beispiels mit Handlungen der Domäne bauen (Spieler 2
   an der Reihe, drei Necron Warriors gesetzt), dann `PUT` auf
   `/api/spieler/1/einheiten/2/ausgewählt` und `/api/spieler/2/einheiten/1/ausgewählt`, wie V2
   das Beispiel beschreibt; die Antwort ist gleich `json.loads` der Datei. Sitzt eine Stelle
   des Beispiels nicht auf einem erreichbaren Stand, ist das ein Anliegen an mich.
2. Bildschirmtest zu AUF-5.7: Seite mit `seite.route("**/api/spielstand", …)` und dem Inhalt
   der Datei; Warboss und Necron Warriors gekennzeichnet, drei Kreise ausgewählt. Das Öffnen
   gehört als Methode in `Bildschirm` (`bildschirm.py`), nicht in den Test.
3. Platz in `auf5Test.py`: Helfer und Konstanten ziehen in die gemeinsamen Module
   (Anliegen 332, Punkte 1 bis 3), etwa 1.800 Zeichen. Reicht das mit AUF-5.5 nicht, ist die
   Teilung von AUF-5 ein Anliegen an den Anforderungsautor, nicht ein zweiter Test zu AUF-5.

Erledigt, wenn ein Test die Antwort des Dienstes mit der Datei vergleicht, einer das Frontend
aus der Datei zeichnet und `auf5Test.py` mit den Tests zu AUF-5.5 unter 20.000 Zeichen bleibt.

**Stellungnahme.** Angenommen, alle drei Punkte umgesetzt.
1. `testAuf5_6DieAntwortDesDienstesAufDieAuswahlGleichtDemBeispielDesVertrags` baut den Stand
   (Spieler 1 Gewinner mit erster Zone, Spieler 2 an der Reihe, drei Necron Warriors an den Stellen
   aus `spielstand.json`, Fixture `aufstellungDesBeispiels`) und vergleicht die Antwort nach
   `PUT` auf Warboss und Necron Warriors sowie `GET` mit `spielstandDesVertrags()`. Alle Stellen
   des Beispiels sind erreichbar.
2. `testAuf5_6DieSeiteKennzeichnet...` und `testAuf5_7DieSeiteZeichnet...` laden die Seite mit
   `Bildschirm.seiteMitSpielstand` (`page.route`) und vergleichen mit der Datei.
3. Helfer sind in `dienst.py` und `bildschirm.py` (Anliegen 332); `auf5Test.py` hat 19.770 von
   20.000 Zeichen.
Zu AUF-5.5: Es steht nicht im Umfang von Plan 4 (Anliegen 320 B, 323), also gibt es dazu
keinen Test. Kommt er mit einer dritten *Einheit*, braucht `auf5Test.py` Platz: dann teilt der
Anforderungsautor AUF-5 (dein Gegenvorschlag 3, letzter Satz).
