# Die Architekturkarte ist lesbar und bricht nicht ab

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Nachprüfung von [3120](3120-architekturkarteImDashboard.md): Die Tests sind
grün, die Zahlen stimmen. Angesehen habe ich das Bild als Screenshot mit
`google-chrome --headless=new --screenshot` unter `/tmp`:
1. Seite und Web stehen 15 Punkte auseinander (Spaltenabstand 135, Kasten 120). Die Aufschrift
   „HTTP“ verdecken die Kästen, man liest „TTI“; die Spitze ist kaum zu sehen.
2. Der Pfeil Web → Domäne schneidet die untere linke Ecke von Anwendung, und die 11 steht auf
   dessen unterem Rand. Man kann sie für einen Pfeil zu Anwendung halten.
3. Ein Ordner unter `technik/arbiter/`, den die Tabelle nicht kennt, bricht die Karte ab.
   Probe: `regeln/neu.py` importiert die Domäne, `kastenLage["regeln"]` wirft `KeyError`.
   Der Hook `laufLog` schluckt den Fehler, das Dashboard bleibt still auf altem Stand; der
   Server liefert den Tokenbericht nicht.
4. `from arbiter import web` und `from .. import domaene` zählt die Karte nicht; der Pfeil
   fehlt. In der Domäne fängt der Importvertrag sie, die Karte zeigt sie nicht.

Kein Fehler der Karte: Domäne und Seite zeigen „keine Datei“, und die Fußzeile zählt nur
`technik/architektur/vertrag/`. `oberflaeche.md`, `vertrag.md` und `handlungen.md`
(zusammen 16.835 Zeichen) liegen noch außerhalb der Gliederung; das ändert das Umordnen in
[3051](3051-architekturUmordnenInPlan8.md), nicht die Karte.

**Kosten.** Ohne 1 und 2 liest der Stakeholder die Karte falsch. Ohne 3 fällt der
Tokenbericht aus, sobald ein Ordner entsteht, den die Architektur nicht vorsieht, also gerade
dann, wenn die Karte ihn zeigen soll. Ohne 4 kann ein falscher Import ohne Pfeil bleiben.
Hält nicht auf: Randfälle des Bildes, darum wartet es auf die Prozessphase.

**Gegenvorschlag.**
1. „HTTP“ steht lesbar über der Linie; Seite und Web rücken so weit auseinander, dass Spitze
   und Aufschrift Platz haben.
2. Die Lage der Kästen ist so gewählt, dass kein erlaubter Pfeil (Tabelle, Web → Domäne,
   Seite → Web) einen Kasten schneidet, der nicht sein Anfang oder Ende ist, und keine
   Aufschrift in einem Kasten steht. Ein Test prüft das an `kastenLage` mit Strecke gegen
   Rechteck für jedes dieser Paare.
3. Ein unbekannter Ordner bekommt keinen Kasten; die Fußzeile nennt ihn („Ordner ohne
   Kasten: regeln“), seine Pfeile zählen als verboten. Test an einem Baum unter `tmp_path`.
4. Bei `from arbiter import <name>` und relativ bis `arbiter` zählt jeder importierte Name
   als Import in seinen Kasten. Test wie 3.

Bestehende Regel, die das abdeckt: [Regeln](../../prozess/regeln/rollenregeln.md), Zeile
„Architektur“ (P7). Erledigt, wenn die Tests zu 2 bis 4 grün sind und ein Screenshot der
Karte unter `/tmp` „HTTP“ und alle Zahlen lesbar zeigt. Feedback des Stakeholders aus
[2740](2740-gemesseneUndBeschriebeneArchitektur.md) nehme ich hier vor der Prozessphase auf.

**Stellungnahme.**
