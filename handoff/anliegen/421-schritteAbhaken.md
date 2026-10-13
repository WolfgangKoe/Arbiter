# Schritte des Zyklus abhaken

421 · Anliegen · von Stakeholder → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** Auftrag des Stakeholders: In der Technik- und der Prozessphase stehen die Schritte
des Ablaufs (etwa Tests, Kritik, Umsetzung, DoD durch den Reviewer, Abnahme, Items löschen,
Review, Kritik, Moderation, Freigabe) ausdrücklich im Plan oder einem Artefakt des Zyklus.
Jede Rolle hakt ihren Schritt ab, wenn er vollständig umgesetzt ist, samt der Kritik daran.
Gab es ein Hindernis, steht dort, welches und was getan wurde, um es zu beseitigen.

**Kosten.** Heute nennt der Stand nur „Items von Plan 5: Tests, Umsetzung, Abnahme“. Dass die
Items nach der Abnahme stehen blieben, weil der Planer nicht löschen durfte, sah man nur in
Anliegen 417.

**Gegenvorschlag.** Wie im Befund.

**Stellungnahme (Organisationsentwickler).** Bestehende Regeln (Ich 4):
- Der [Ablauf](../../prozess/ablauf.md) nennt die Schritte je Phase nummeriert, mit Rolle;
  daraus entsteht die Liste.
- Der Stand leitet den nächsten Schritt aus Dateien und Commits ab; in der Prozessphase hakt
  schon heute ein Commit `P<k>: …` je Prozess-Item ab.
- Ein Hindernis wird heute ein Anliegen; was getan wurde, steht in seiner Stellungnahme.
- [Ich 2](../../prozess/praemissen/ich.md): Den Plan schreibt nur der Planer, er hat schon
  4.000 Zeichen. Die Liste braucht eine eigene Datei, und dass jede Rolle darin abhakt, eine
  Ausnahme. Vorbild: Eine eigene Zeile in `prozess/regeln.md` zählt bei gleichzeitigen Läufen
  als getrennt.
- [Wir 4](../../prozess/praemissen/wir.md) steht nicht entgegen: Die Liste ist der Zustand
  des laufenden Zyklus. Wie Kommentare und Stellungnahmen bleibt sie, bis der Planer sie im
  nächsten Zyklus neu anlegt; git bewahrt die alte. Wir 3: Das Hindernis steht dort in einem
  Satz mit Link aufs Anliegen, die Diskussion nur im Anliegen.
- Claude Code hat eine eigene Aufgabenliste (Tasks). Sie liegt außerhalb des Projekts und
  nicht in git, du liest sie nur mit Werkzeug (Wir 5); darum nicht.

„Samt der Kritik“: Der Autor hakt seine Arbeit ab, die Kritik ist eine eigene Zeile. Der
Kritiker hakt sie ab, wenn seine Anliegen dazu erledigt sind, also umgesetzt und nachgeprüft;
ohne Befund sofort. So läuft keine Rolle ein zweites Mal, nur um abzuhaken.

**F1 · Wo stehen die Schritte, wer hakt ab?**
A: In `handoff/schritte.md`. Der Planer legt sie mit dem Plan an, je Schritt eine Zeile
`- [ ] <Rolle>: <Schritt>`, in der Technikphase je Item. Jede Rolle setzt in ihren Zeilen
`[x]` und schreibt ein Hindernis darunter: `Hindernis: <was>; beseitigt: <wie> (Anliegen
<nr>)`. Die Zeile Freigabe verlinkt dein Feld `Freigabe:` ohne eigenen Haken. Jede Rolle
bekommt die Datei als Schreibpfad. Später nennt der Stand die erste offene Zeile als nächsten
Schritt.
B: Wie A, nur kommt der Haken aus git: Die Rolle meldet fertig, der Koordinator committet mit
festem Betreff je Schritt, Stand und Dashboard zeigen die Liste mit Haken und offenen
Anliegen. Keine Rolle schreibt in eine gemeinsame Datei; du liest die Liste nur im Dashboard,
und der Regelumsetzer baut sie.
Empfehlung: A. Am nächsten an deinem Wortlaut: Du liest die Liste ohne Werkzeug, die Rolle
hakt selbst ab und schreibt das Hindernis dazu.
Antwort: .

**F2 · Prüft eine Sperre, dass eine Rolle nur ihre Zeilen ändert?** (nur bei A)
A: Ja, von Anfang an: Die Schreibgrenze lässt in `handoff/schritte.md` nur Zeilen mit der
eigenen Rolle ändern. Anlass: Anliegen 384, Rollen schrieben an der Grenze vorbei.
B: Nein, nur Text, bis eine Rolle eine fremde Zeile ändert.
Empfehlung: A. Ohne Sperre hakt eine Rolle auch für andere ab, und der Haken sagt nichts.
Antwort: .

Antworte im Formular als Kommentar, etwa „F1 A, F2 A“, und setze `offen`. Danach passe ich
Ablauf, Ich 2 und die Schreibpfade an; den Code beauftragt der Koordinator beim Regelumsetzer.
Kommentar: Ich bin mir nicht sicher, ob ich deinen Entwurf korrekt verstanden habe. Vielleicht kann ich es mir von der Textbeschreibung her nur schwer vorstellen. Ich möchte ehrlich gesagt vermeiden ein neues Artefakt zu generieren, wenn wir schon eines namens "Plan.md" haben. Ich finde es auch schwierig, wenn die jeweiligen Rollen diesen Plan lesen und bearbeiten müssen. Ich würde mir am liebsten einen script-basierten Ablauf wünschen, mit dem ein Plan abgehakt oder mit Kommentaren ergänzt wird. Evtl. lässt ist das sehr kompliziert? Des weiteren war meine Beschreibung eher eine sehr grobe Idee und kein Vorschlag, an dem du dich möglichst gut annähern müsstest. Denk vernünftig darüber nach. Ich möchte Transparenz über den Fortschritt und die Hindernisse, denen das Team begegnet. EIne Art "lebender Plan" für jede Phase in einem Zyklus. Der Aufwand für die Pflege dieser Transparenz soll so niedrig wie möglich sein. D.h. wenn einfach ein Standardskript gestartet werden kann, wäre das gut, wenn ein Formular ausgefüllt werden muss, so dass dieser im Plan eingefügt und parallel dazu ein Anliegen im Handoff erzeugt wird, ist das gut. So schreibt jede Rolle das, was nötig ist. Dann kann auch ich hier über das Dashboard einen Haken oder Kommentar setzen, weil auch ich manchmal der Flaschenhals war. Verstehst du, was ich meine?
