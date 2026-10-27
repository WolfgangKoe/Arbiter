# Neue Begriffe, Kürzel BEW und Annahmen zu Plan 8

Form: Fragen
Von: Anforderungsautor
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Für Plan 8 habe ich [QUE-9](../../domaene/anforderungen/querschnitt/ersterZug.md),
[QUE-10](../../domaene/anforderungen/querschnitt/schlachtrunden.md),
[BEW-1](../../domaene/anforderungen/phasen/bewegung/normaleBewegung.md) und
[BEW-2](../../domaene/anforderungen/phasen/bewegung/sperrenBeimZiehen.md) geschrieben, mit
neuen Begriffen, einem neuen Kürzel und Werten, die weder Regel noch Ziel festlegen.

**Kosten.** Ohne Antwort baut Etappe 2 auf Annahmen.

**Gegenvorschlag.** Antwortest du „.“, gelten alle Empfehlungen.

**F1 · Gibst du die neuen Begriffe im [Glossar](../../domaene/glossar.md) frei?** A: Ja. B: Mit
deinen Änderungen. Empfehlung: A.
Antwort: B, siehe Kommentar.

**F2 · Neues Kürzel BEW für `phasen/bewegung`?** A: Ja. B: Alle Phasen unter AUF. Empfehlung: A.
Antwort: Rückfrage, siehe Klärung.

**F3 · Wie wird der Weg gemessen?** A: Jedes Ziehen eine gerade Strecke, ihre Summe je *Modell*
höchstens *M*. B: Der Weg des Zeigers. Empfehlung: A.
Antwort: A.

**F4 · Overlord M 6″** wie Arbiter-old und ArbiterMap? A: 6″. B: Dein Wert. Empfehlung: A.
Antwort: A, siehe Kommentar.

**F5 · Knöpfe** „Erster Zug“ je *Armeeliste*, „Phase beenden“, „Bewegung der Einheit beenden“?
A: So. B: Deine Beschriftung. Empfehlung: A.
Antwort: A.

**Stellungnahme.**
Kommentar: Beachte meine Rückfrage zu F2. Und meine Kommentare zu den anderen Antworten.
Kommentar: Meine Antworten, Kommentare und Rückfrage wurde nicht übernommen.
Kommentar: Zu F1: B Wir machen es wie A außer statt "Normal Move" nehmen wir "Normale Bewegung" und "B", wie in deutschen Übersetzungen üblich Zu F2: Rückfrage: Wozu brauchen wir ein Kürzel? Zu F3: A Źu F4: WIr nehmen A, bitte prüfe, ob wir die YAML-Dateien aus Arbiter-old einfach übernehmen wollen oder eine Datenbank anlegen. Zu F5: A

**Klärung.** Deine Antworten kamen nicht an, weil unter den Fragen die Zeile `Antwort:`
fehlte; mein Fehler, jetzt steht sie überall. Umgesetzt: F1 B im Glossar, in BEW-1 und BEW-2,
die *Sperre* heißt ‚weiter als B‘; F3 bis F5 standen schon so. Plan, Items und Etappe 2
berichtigt der Planer (Anliegen 4420), das Mockup Ux
(Anliegen 4421).

Wozu ein Kürzel: Jedes Kriterium heißt `<Kürzel>-<n>.<m>`, sein Test trägt die Kennung im
Namen (`testBew2_1…`, [Es 4](../../prozess/praemissen/es.md)); daran ordnet die Prüfung
Kriterium und Test zu, und du siehst den Bereich, ohne die Datei zu öffnen. Ein neues ist
nicht nötig: Heute gilt AUF für alle Phasen ([Domäne](../../domaene/CLAUDE.md)), AUF steht
aber für Aufstellen.

**F6 · Welches Kürzel tragen die Anforderungen der Bewegungsphase?** A: BEW, je Phase ein
eigenes; eine Zeile der Domäne ändert sich (neu). B: AUF wie heute; BEW-1 und BEW-2 heißen
AUF-30 und AUF-31 (Domäne).
Empfehlung: A. Du liest an der Kennung die Phase ab (Absicht 3, 5).
Annahme: Ich schreibe weiter BEW.
Antwort: A

Daten aus Arbiter-old, geprüft: Einfach übernehmen passt nicht. Sie haben englische
Schlüssel und die Quelle nur im Kopf; die Domäne verlangt Schlüssel aus dem Glossar und eine
Fundstelle je Wert. Die Necrons tragen `oc` (`Arbiter-old/data/wh40k_9e/necrons/units.yaml:37`),
das die Profile der 9. Edition nicht kennen (`core_rules.txt:561`). Eine Datenbank für
Katalogwerte schließt [Architektur, A3](../../technik/architektur.md) heute aus. Etappe 2
braucht nur *B* und *Durchmesser* von vier *Einheiten*; die Daten der Orks und Necrons sind
[Etappe 8](../../domaene/etappen/08-datenUndStartseite.md).

**F7 · Wann entscheiden wir über die Daten aus Arbiter-old?** A: Mit Etappe 8; bis dahin
trage ich nur die Werte ein, die eine Etappe braucht, je mit Fundstelle (Domäne). B: Jetzt,
der Planer zieht die Übernahme vor (neu).
Empfehlung: A. Für Orks gegen Necrons reicht das; in Etappe 8 prüft der Architekt YAML oder
Datenbank, ich jeden Wert.
Antwort: Wir entscheiden es für den nächsten Zyklus, damit die Daten sauber aufgesetzt werden. Der Architekt soll prüfen, wie wir das Datenmodell aufbauen können. Vielleicht ist dieses aus Arbiter-old brauchbar und muss vor allem mit Begriffen aus dem Glossar bestückt werden.
