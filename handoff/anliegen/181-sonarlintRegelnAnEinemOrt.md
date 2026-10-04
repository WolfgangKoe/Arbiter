# SonarLint: Sperre und VS Code mit denselben Regeln

181 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
Kritik am Code zu Commit `f76a862` (P2 der [Retro 2](../retro.md)). Was
[180](180-sonarlintPruefungZuschneiden.md) nennt, wiederhole ich nicht.

**Befund.** Die sechs abgeschalteten Namensregeln stehen nur in `sonarlint.py`
(`abgeschalteteRegeln`). Der Server liest sie über die Antwort auf `workspace/configuration`.
VS Code kennt dieselbe Einstellung `sonarlint.rules`; beim Stakeholder ist sie leer.
[regeln.md](../../prozess/regeln.md) hält fest: „in VS Code melden sie weiter“.
Ausprobiert mit `sonarlint.py`, ohne die Abschaltung und mit `technik/tests/einheit`:
284 Funde, davon 276 Namensregeln (S1542 146, S117 105, S100 17, S116 8). Übrig bleiben die
8 echten Funde (S5778, [179](179-sonarlintMeldetEinheitstests.md)). Diese 276 sieht der
Stakeholder in VS Code. Die Erkennung von Testdateien stimmt dagegen überein:
`sonarlint.testFilePattern` ist in der Erweiterung 6.0.1 leer, `isTest: False` trifft das.

**Kosten.** Laut [Ablauf, Werkzeuge](../../prozess/ablauf.md#technikphase) ist SonarLint „die
Sicht des Stakeholders“. Heute geht in dieser Sicht jeder echte Fund unter 276 Meldungen
unter, die nach [wir.md](../../prozess/praemissen/wir.md) 1 nie behoben werden. Ob die Sperre
und VS Code dasselbe melden, sieht er nicht mehr. Die Liste steht nur im Code. Wer eine
Regel abschaltet, ändert die Sperre, aber nicht die Sicht.

**Einschränkung.** `.vscode/settings.json` hilft nicht. `sonarlint.rules` hat in der
Erweiterung 6.0.1 den Geltungsbereich `application` (`package.json`), also liest VS Code die
Einstellung nur aus den Benutzereinstellungen, nicht aus dem Projekt. Dort wirkt sie auf
alle Projekte des Stakeholders.

**Gegenvorschlag.** Die Liste bleibt einmal, in `sonarlint.py`.
1. `python3 prozess/pruefungen/sonarlint.py --einstellung` gibt aus dieser Liste den Block
   `"sonarlint.rules": {"python:S100": {"level": "off"}, …}` aus, zum Einfügen in die
   Benutzereinstellungen. Ein Test prüft, dass der Block genau `abgeschalteteRegeln` nennt.
2. Ob der Stakeholder ihn einfügt, entscheidet er; er gilt dann auch für andere Projekte.
   Die Frage dazu stellst du ihm als Anliegen.

Erledigt, wenn der Block erzeugt wird und die Frage gestellt ist.

**Stellungnahme (Regelumsetzer).** Angenommen: `sonarlint.py --einstellung` gibt den Block aus, ein Test prüft ihn gegen `abgeschalteteRegeln`. Die Frage an den Stakeholder steht in [182](182-sonarlintNamensregelnInVsCode.md).
