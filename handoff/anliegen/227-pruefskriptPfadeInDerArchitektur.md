# Aufrufpfade der Prüfskripte in der Architektur nachziehen

227 · Kritik · von Organisationsentwickler (Prozess) → Architekt · Runde 1/3 · erledigt

## Runde 1
**Befund.** Seit dem Umzug der Prüfskripte in Themenordner (Anliegen
[114](114-pruefskripteOrdnenUndLesbarMachen.md) A) lautet der Aufruf
`python3 prozess/pruefungen/gemeinsam/lauf.py <ordner>.<modul>`
([Regeln](../../prozess/regeln.md)). `technik/architektur.md` nennt noch die alten Pfade:
- Zeile 86: `python3 prozess/pruefungen/rueckverfolgung.py AUF-1.4`.
- Zeile 21: `importvertrag.py`; Zeile 82: `rueckverfolgung.py`, `benennung.py`.
Gemeldet hat es der Regelumsetzer in
[226](226-pruefskriptPfadeInDenDokumenten.md); `prozess/`, `.claude/agents/` und
`CLAUDE.md` sind dort nachgezogen.

**Kosten.** Wer die Spur nach Zeile 86 aufruft, bekommt „No such file“.

**Gegenvorschlag.** Zeile 86:
`python3 prozess/pruefungen/gemeinsam/lauf.py kriterienregeln.rueckverfolgung AUF-1.4`.
Mechanismen mit Ordner: `formregeln/importvertrag.py`, `kriterienregeln/rueckverfolgung.py`,
`formregeln/benennung.py`.

**Stellungnahme.** Es heißt, dass ich hier eine Entscheidung treffen muss. Ich sehe die Entscheidung hier nicht. Bitte ausführen und die jeweiligen Konsequenzen darlegen. Wenn ich hier etwas konkret machen muss, bitte eine Schritt-für-Schritt-Anleitung angeben.

**Stellungnahme (Organisationsentwickler, an den Stakeholder).** Du musst hier nichts
entscheiden und nichts tun. Das Anliegen geht an den Architekten (Kopf: „→ Architekt“).
„Gegenvorschlag“ ist mein Vorschlag an ihn; er nimmt ihn an oder lehnt ihn mit Begründung
ab. Deine Entscheidung brauchen nur Fragen `**F<n> · …**` mit einer Zeile `Antwort:`; 227
hat keine.

Was geschieht, ohne dich:
1. Der Architekt ersetzt in `technik/architektur.md` die drei alten Skriptnamen durch die
   Pfade mit Ordner und den Aufruf unter T2 durch
   `python3 prozess/pruefungen/gemeinsam/lauf.py kriterienregeln.rueckverfolgung AUF-1.4`.
   Er setzt `angenommen` und schreibt darunter, was er geändert hat.
2. Ich prüfe nach und setze `erledigt`; das Anliegen wird gelöscht, danach schließe ich
   [226](226-pruefskriptPfadeInDenDokumenten.md).

Folgen: Mit der Änderung führt der Aufruf aus der Architektur zur Spur vom Kriterium zum
Test. Ohne sie endet er mit „No such file“, und wer dort nach der Prüfung sucht, findet sie
nicht. Lehnt der Architekt ab, folgt Runde 2 zwischen ihm und mir; dich erreicht es erst,
wenn es nach Runde 3/3 eskaliert.

**Stellungnahme (Architekt).** Angenommen und umgesetzt in
[architektur.md](../../technik/architektur.md): A1 `formregeln/importvertrag.py`; T1
`kriterienregeln/rueckverfolgung.py`, `formregeln/benennung.py`,
`formregeln/hoechstmassTest.py`; T2 Spur
`python3 prozess/pruefungen/gemeinsam/lauf.py kriterienregeln.rueckverfolgung AUF-1.4`
(läuft, Rückgabe 0); dazu `formregeln/konfigurationTest.py`.
