# Anforderung Aufstellen: schwer zu prüfen, sieben in einer Datei

340 · Kritik · von Stakeholder → Anforderungsautor (Domäne) · Runde 1/3 · offen
Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Zu [aufstellen.md](../../domaene/anforderungen/phasen/aufstellen.md), nach 97 (git):
schwer zu verstehen; grenzt sich nicht klar von der Missionsvorbereitung ab; sieben AUF-N in
einer Datei, die Tests je AUF-N in einer eigenen; aus AUF-N.M geht nicht hervor, wie die
Handlung in der App geht.

**Kosten.** Prüfen fällt schwer; wer AUF-7.3 korrigiert, liest alle 7.092 Zeichen.

**Gegenvorschlag.** Je AUF-N eine Datei wie bei den Tests.

**F1 · Schnitt.** A: Je Bereich ein Ordner, je Anforderung eine Datei mit sprechendem Namen
(`phasen/aufstellen/einheitInAufstellung.md` für AUF-7, `querschnitt/setzen.md` …),
Kennungen bleiben, Tests heißen gleich (`einheitInAufstellungTest.py`). Empfehlung A.

Antwort: .

**F2 · Missionsvorbereitung.** A: Neuer Bereich `missionsvorbereitung/`, Kürzel MIV, Begriff
*Missionsvorbereitung* (kein Regelbegriff: Schritte 1 bis 3 von Only War,
`core_rules.txt:2256`, `:2303`). AUF-2 wird MIV-1 · Ausgangslage; Roll-off und Wahl der Zone
bleiben in der *Aufstellung* (`:2322`). Empfehlung A.

Antwort: .

**F3 · Form der Kriterien.** A: Unter dem Zweck „Am Bildschirm:“ mit dem Handgriff; jedes
Kriterium nennt Lage, Handlung und Folge in einem Satz. B: Gegeben/Wenn/Dann in drei Zeilen.
Empfehlung A.

Antwort: Ich gehe mit deiner Empfehlung mit, aber so eine Struktur wie Gegeben/Wenn/Dann sollte dennoch aus den Sätzen hervorgehen und sichtbar sein. Dein Beispiel hier finde ich aus irgendeinem Grund immer noch nicht leicht zu verstehen. Eine Zeilenstruktur wie in B würde alles vielleicht unnötig aufblähen. Aber ich möchte an jedem Kriterium eine Art Use Case sehen und verstehen können. Ich finde ja schon den Zweck schwer verständlich. Ist der Zweck hier: "Ein Spieler, der an der Reihe ist, kann eine Einheit aufstellen" Akzeptanzkritierium 1: "Ein Spieler ist an der Reihe und hat noch eine Einheit aufzustellen. Er wählt diese Einheit aus und die Einheit ist ausgewählt." Und so weiter... Du kannst bestimmt verständlich fomrulieren. ABer das wäre der Anspruch.

**F4 · Bedienung des Setzens.** A: Ich beschreibe Setzen aus der *Ablage*, Umsetzen,
Zurücklegen, „zurück“, „gemeinsam übergehen“, „Aufstellen der Einheit beenden“ (Etappe 1)
als neue Anforderung, der Planer plant sie ein. Empfehlung A.

Antwort: .

**Stellungnahme:** Ich finde die Ansätze gut. In der Domäne vollziehen wir die Ordnerstruktur, die wir bereits in der Technik angefangen haben. In der Technik setzen wir einen lesbarere Umbenennung um. Wir spiegeln hier jetzt also die Ordnerstruktur und die Dateibenennung zwischen Domäne und Technik. Damit bleiben die einzelnen Dateien auch klein. Das heißt, die Anforderungen spiegeln sich strukturell, inhaltlich und in der Bezeichnung in der Technik wieder. Hierfür soll der Regelumsetzer eine Skript implementieren, der diesen "Spiegel" prüft und diesen einfordert. Wir müssen aber schauen, ab wann wir eine Übersichtsdatei brauchen, die uns hilft den Wald zu überblicken.

**Stellungnahme.** (Anforderungsautor) Angenommen in der Sache, noch nicht umgesetzt.
Zu F3, AUF-7 neu, je Kriterium ein Satz mit sichtbarem Gegeben/Wenn/Dann:
- Zweck: Der *Spieler* *an der Reihe* stellt eine seiner *Einheiten* auf: Er *setzt* ihre
  *Modelle* und beendet sie; dann ist der andere an der Reihe.
- AUF-7.3 **Gegeben** der *Spieler* *an der Reihe* stellt eine *Einheit* auf, **wenn** er
  ein *Modell* einer anderen seiner *Einheiten* *setzt*, **dann** sperrt Arbiter mit
  ‚Einheit begonnen‘.

Ob man vor dem *Setzen* auswählt (dein Beispiel), frage ich mit F4. Die Übersicht ist der Ordner mit sprechenden Dateinamen; eine Übersichtsdatei
schlage ich vor, wenn ein Ordner mehr als zehn hat.

**F5 · AUF-3.4 (339 F2).** „Models cannot be set up within Engagement Range“ steht nicht bei
Deploy Forces (`core_rules.txt:450`), gilt für jedes *Setzen*. A: AUF-3.4 wird QUE-1.3 in
`querschnitt/setzen.md`, neben ‚Base überdeckt‘: beides *Abstand* zwischen *Bases* (`:464`),
wie du vermutest. B: bleibt bei der Aufstellung. Empfehlung A, wie 339 F2 A.

Antwort: A

**F6 · Zeitpunkt.** A: nächste Domänenphase, in einem Zug: ich die Anforderungen, Testautor
benennt Tests um, Organisationsentwickler das Muster in `domaene/CLAUDE.md`, Regelumsetzer
das Spiegelskript, Planer Item und Links. B: jetzt. Empfehlung A: Jetzt fänden die Prüfungen
zu AUF-2 und AUF-3.4 mitten in Plan 4 Tests ohne Kriterium.

Antwort: A
