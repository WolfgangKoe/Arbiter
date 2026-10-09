# Anforderung Aufstellen: schwer zu prüfen, sieben in einer Datei

340 · Kritik · von Stakeholder → Anforderungsautor (Domäne) · Runde 1/3 · offen
Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Zu [aufstellen.md](../../domaene/anforderungen/phasen/aufstellen.md), nach 97 (git):
schwer zu verstehen; grenzt sich nicht klar von der Missionsvorbereitung ab; sieben AUF-N in
einer Datei, die Tests je AUF-N in einer eigenen; aus AUF-N.M geht nicht hervor, wie die
Handlung in der App geht.

**Kosten.** Prüfen fällt schwer, die Übersicht geht verloren; wer AUF-7.3 korrigiert, liest
alle 7.092 Zeichen.

**Gegenvorschlag.** Je AUF-N eine Datei wie bei den Tests.

**Stellungnahme.** (Anforderungsautor) Trifft zu. AUF-2 (*Armeen*, *Spielfeld*, Zonen) ist
nicht Schritt 4 Deploy Forces (`core_rules.txt:2321`), sondern Schritt 1 und 3 (`:2256`,
`:2303`). Die Kriterien nennen Zustände statt Handgriffe und verweisen aufeinander („Sonst“).
AUF-1, AUF-3 und AUF-7 haben keine Bedienung am Bildschirm, nur die Krücke AUF-6. Ich ändere
nichts vor deinen Antworten, umgesetzt in der nächsten Domänenphase, nicht in Plan 4.

**F1 · Schnitt.** A: Je Bereich ein Ordner, je Anforderung eine Datei mit sprechendem Namen:
`phasen/aufstellen/reihenfolge.md` (AUF-1), `sperrenBeimSetzen.md`, `anzeige.md`,
`auswaehlen.md`, `vorlaeufigerStart.md`, `einheitInAufstellung.md`, ebenso
`querschnitt/setzen.md`, `karte.md`, `bedienung.md`; Kennungen bleiben. B: wie A, Dateien
`auf1.md` bis `auf7.md`. C: eine Datei, nur F3.
Empfehlung A. Kosten: Testautor benennt 9 Testdateien um (`auf1Test.py` →
`reihenfolgeTest.py`), Inhalt bleibt; Organisationsentwickler ändert das Muster in
`domaene/CLAUDE.md`, Architekt T1, Planer Links. `rueckverfolgung.py` und `benennung.py`
bleiben: eine Datei mit einer Anforderung gehört schon heute zu `<datei>Test.py`; dass es nur
eine ist, prüft nur Text. B spart das Umbenennen, der Name sagt aber nichts.

Antwort: .

**F2 · Missionsvorbereitung.** A: Neuer Bereich `missionsvorbereitung/`, Kürzel MIV, Begriff
*Missionsvorbereitung* (kein Regelbegriff: Schritte 1 bis 3 von Only War). AUF-2 wird
MIV-1 · Ausgangslage, gleicher Inhalt, AUF-2.4 bis 2.7 erlöschen. Roll-off und Wahl der Zone
bleiben in der *Aufstellung*, die Regel stellt sie in Schritt 4 (`:2322`). B: AUF-2 wird OBJ-2.
Empfehlung A: OBJ gilt „gleich welche Mission“, AUF-2 ist Only War. Kosten: `auf2Test.py` wird
`missionsvorbereitung/ausgangslageTest.py`, `testAuf2_4…` wird `testMiv1_1…` (Testautor);
Planer ersetzt Kennungen.

Antwort: .

**F3 · Form der Kriterien.** A: Unter dem Zweck eine Zeile „Am Bildschirm:“ mit dem Handgriff
in 1–2 Sätzen (ziehen, loslassen, klicken, was man sieht) oder „noch keine Bedienung“. Jedes
Kriterium nennt Handlung oder Lage und Folge, ohne „Sonst“. AUF-7.3 etwa: „Setzt der *Spieler*
*an der Reihe* ein *Modell* einer nicht *aufgestellten* *Einheit*, während eine andere
*Einheit in Aufstellung* ist: *Sperre* ‚Einheit begonnen‘.“ Bedeutung, Kennungen und Tests
bleiben. B: Gegeben/Wenn/Dann in drei Zeilen; bricht „je ein Satz“, etwa doppelt so lang.
Empfehlung A. Kosten: ein Lauf von mir; ändert sich eine Bedeutung, ist es ein neues
Kriterium mit neuem Test.

Antwort: Ich gehe mit deiner Empfehlung mit, aber so eine Struktur wie Gegeben/Wenn/Dann sollte dennoch aus den Sätzen hervorgehen und sichtbar sein. Dein Beispiel hier finde ich aus irgendeinem Grund immer noch nicht leicht zu verstehen. Eine Zeilenstruktur wie in B würde alles vielleicht unnötig aufblähen. Aber ich möchte an jedem Kriterium eine Art Use Case sehen und verstehen können. Ich finde ja schon den Zweck schwer verständlich. Ist der Zweck hier: "Ein Spieler, der an der Reihe ist, kann eine Einheit aufstellen" Akzeptanzkritierium 1: "Ein Spieler ist an der Reihe und hat noch eine Einheit aufzustellen. Er wählt diese Einheit aus und die Einheit ist ausgewählt." Und so weiter... Du kannst bestimmt verständlich fomrulieren. ABer das wäre der Anspruch.

**F4 · Bedienung des Setzens.** Etappe 1 verlangt Setzen aus der *Ablage*, Umsetzen,
Zurücklegen, „zurück“, „gemeinsam übergehen“, „Aufstellen der Einheit beenden“; keine
Anforderung beschreibt das. A: Ich schreibe es mit F1 bis F3, der Planer plant es ein. B: erst
auf Anforderung des Planers.
Empfehlung A: Erst dann zeigt die Anforderung, wie die Aufstellung in der App geht.

Antwort: .

**Stellungnahme:** Ich finde die Ansätze gut. In der Domäne vollziehen wir die Ordnerstruktur, die wir bereits in der Technik angefangen haben. In der Technik setzen wir einen lesbarere Umbenennung um. Wir spiegeln hier jetzt also die Ordnerstruktur und die Dateibenennung zwischen Domäne und Technik. Damit bleiben die einzelnen Dateien auch klein. Das heißt, die Anforderungen spiegeln sich strukturell, inhaltlich und in der Bezeichnung in der Technik wieder. Hierfür soll der Regelumsetzer eine Skript implementieren, der diesen "Spiegel" prüft und diesen einfordert. Wir müssen aber schauen, ab wann wir eine Übersichtsdatei brauchen, die uns hilft den Wald zu überblicken.