# Ablage der Katalogwerte

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Katalogwerte sind die Werte eines Datenblatts: *B*, Zahl der *Modelle*,
*Durchmesser* der *Base*, später Waffen und Fähigkeiten. Heute stehen zwei davon für vier
*Einheiten* in [ausgangslage.yaml](../../domaene/daten/ausgangslage.yaml); alle Datenblätter
der Orks und Necrons kommen in [Etappe 8](../../domaene/etappen/08-datenUndStartseite.md).
Du willst vorher entscheiden, wie sie aufgebaut sind (Anliegen 4280 F7,
[4621](4621-datenmodellDerKatalogwerte.md)). Ich habe [Arbiter-old](../../Arbiter-old/data/wh40k_9e/)
gelesen und eine Probe in `/tmp` geladen. Brauchbar: je Fraktion eine Datei je Art
(`units.yaml`, `weapons.yaml`). Nicht brauchbar, vier Funde:
1. Werte als Text: `move: 5"`, `ws: 3+`; Arbiter-old schneidet das Zollzeichen ab
   (`src/gameObjects/loader.py:943`). Ein *B* von „-“ (`core_rules.txt:565`) bricht das
   Laden ab, steht es nicht in Anführung.
2. Die 9. Edition hat ein Profil je *Modell* (`core_rules.txt:561`): Der Boss Nob hat A 3,
   die Boyz A 2. Arbiter-old hat eins je *Einheit*, Abweichungen nur in 13 von 110
   Datenblättern (`model_groups`).
3. Fähigkeiten tragen ihr Verhalten als Daten (`trigger`, `effect`), ein Interpreter führt es
   aus: `_apply_persistent_effect` (`loader.py:948`) ist eine Kette aus `if` und `elif`,
   `abilityEngine.py` hat 988 Zeilen. Das machte Arbiter-old unwartbar; ein Kriterium führt
   nicht mehr zu seinem Code ([Architektur, T2](../../technik/architektur.md)).
4. Werte, die das Profil der 9. Edition nicht kennt: `oc`, `fnp`.

**Kosten.** Ohne Entscheidung trägt der Anforderungsautor Werte in ein Format ein, das
spätestens in Etappe 8 umgebaut wird, samt dem Code, der es liest.

**Gegenvorschlag.** Antworte je Frage im Dashboard; „.“ heißt: Die Empfehlung gilt.

**F1 · Wo stehen die Katalogwerte?** A: als YAML in `domaene/daten/`, Arbiter liest sie beim
Start (Architektur A3, Speicher P3). B: in einer Datenbank (Anliegen 4280).
Empfehlung: A. Am Bildschirm gleich. Die Werte ändern sich in einer Partie nie, und jeder
braucht seine Fundstelle; in YAML liest du beides im Diff jedes Commits. Eine Datenbank
müsste trotzdem aus einer lesbaren Datei befüllt werden: Schema, Einlesen und Abgleich kämen
dazu (ArbiterMap: `backend/app/repository/schema.sql`, 10.000 Zeichen). Die Datenbank hält
die Partien ([Speicher, P2](../../technik/architektur/speicher.md)).
Antwort: A

**F2 · Wie sind die Werte aufgebaut?** A: wie Arbiter-old, nur mit Schlüsseln aus dem Glossar
(Arbiter-old, Anliegen 4621). B: Gliederung aus Arbiter-old, aber nur Werte: je Datenblatt
seine Modellarten mit eigenem Profil, Zahlen in der Einheit des Glossars
(`bewegungsweite: 5`), der *Durchmesser* bei der Modellart; Fähigkeiten nur mit Name und
Regeltext, was sie bewirken, steht im Code ihrer Anforderung wie heute jede Sperre
(Arbiter-old, Regeltext, Architektur D4). C: je Datenblatt eine Datei
(`ArbiterMap/data/poc/units/orks_boyz.yaml`) (ArbiterMap).
Empfehlung: B. Die Ausgangslage nennt dann je *Einheit* Datenblatt und Zahl der *Modelle*
statt zehnmal `32`. A übernimmt die vier Funde; C verteilt 110 Datenblätter und 184 Waffen
auf Hunderte Dateien. Im Code: `katalog/` liest das neue Format und prüft jeden Wert wie
heute den *Durchmesser*, die Domäne bleibt. Die Fundstelle steht am Zeilenende wie heute;
Datenblatt, Profil und Modellart legt der Anforderungsautor im Glossar an.
Antwort: B

**F3 · Wann übernehmen wir die Werte?** A: Jede Etappe trägt nur die Werte nach, die ihre
Kriterien brauchen, alle Datenblätter in Etappe 8 (Etappe 8, Absicht 3). B: alle Datenblätter
der Orks und Necrons jetzt (Arbiter-old).
Empfehlung: A. Einheiten und Waffen der beiden Fraktionen sind in Arbiter-old rund 6.900
Zeilen; jeden Wert übersetzt der Anforderungsautor mit Fundstelle, der Reviewer liest ihn
nach. Etappe 2 braucht zwei Werte von vier Einheiten.
Antwort: A, aber bitte darauf achten, dass wir bereits eine Struktur anlegen, die wir jederzeit passend ergänzen oder bei Bedarf beliebig füllen können, ohne das die Systematik bricht! Bei der Struktur des Datenmodells also sorgfältig sein.

**Stellungnahme.**
