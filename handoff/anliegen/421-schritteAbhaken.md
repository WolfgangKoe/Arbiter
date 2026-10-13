# Schritte des Zyklus abhaken

421 · Anliegen · von Stakeholder → Organisationsentwickler · Runde 2/3 · rückfrage

## Runde 1
**Befund.** Auftrag des Stakeholders: Die Schritte von Technik- und Prozessphase stehen im
Plan; jede Rolle hakt ihren ab, wenn er samt Kritik umgesetzt ist, und nennt Hindernisse und
was dagegen getan wurde.

**Kosten.** Der Stand nennt nur „Items von Plan 5: Tests, Umsetzung, Abnahme“; dass die Items
nach der Abnahme stehen blieben, sah man nur in Anliegen 417.

**Gegenvorschlag.** Wie im Befund.

**Stellungnahme (Organisationsentwickler).** Vorschlag: eine eigene Datei, in der jede Rolle
ihre Zeilen von Hand abhakt.
Kommentar: Ich bin mir nicht sicher, ob ich deinen Entwurf korrekt verstanden habe. Vielleicht kann ich es mir von der Textbeschreibung her nur schwer vorstellen. Ich möchte ehrlich gesagt vermeiden ein neues Artefakt zu generieren, wenn wir schon eines namens "Plan.md" haben. Ich finde es auch schwierig, wenn die jeweiligen Rollen diesen Plan lesen und bearbeiten müssen. Ich würde mir am liebsten einen script-basierten Ablauf wünschen, mit dem ein Plan abgehakt oder mit Kommentaren ergänzt wird. Evtl. lässt ist das sehr kompliziert? Des weiteren war meine Beschreibung eher eine sehr grobe Idee und kein Vorschlag, an dem du dich möglichst gut annähern müsstest. Denk vernünftig darüber nach. Ich möchte Transparenz über den Fortschritt und die Hindernisse, denen das Team begegnet. EIne Art "lebender Plan" für jede Phase in einem Zyklus. Der Aufwand für die Pflege dieser Transparenz soll so niedrig wie möglich sein. D.h. wenn einfach ein Standardskript gestartet werden kann, wäre das gut, wenn ein Formular ausgefüllt werden muss, so dass dieser im Plan eingefügt und parallel dazu ein Anliegen im Handoff erzeugt wird, ist das gut. So schreibt jede Rolle das, was nötig ist. Dann kann auch ich hier über das Dashboard einen Haken oder Kommentar setzen, weil auch ich manchmal der Flaschenhals war. Verstehst du, was ich meine?
Stellungnahme: Ja. Neuer Vorschlag in Runde 2.

## Runde 2
**Befund.** Dein Kommentar oben: kein neues Artefakt, ein lebender Plan je Phase mit
Fortschritt und Hindernissen, Pflege per Skript oder Formular; ein Hindernis wird zugleich ein
Anliegen; auch du hakst im Dashboard ab oder kommentierst.

**Kosten.** Wie in Runde 1.

**Gegenvorschlag.** Wie im Befund.

**Stellungnahme (Organisationsentwickler).** Machbar, ohne dass eine Rolle den Plan liest oder
von Hand bearbeitet. Bestehende Regeln (Ich 4): Der Stand leitet den nächsten Schritt schon
aus Dateien und Commits ab, ein Commit `P<k>:` hakt ein Prozess-Item ab, Hindernisse sind
Anliegen. Wir 4 steht nicht entgegen: Der Abschnitt ist der Zustand des laufenden Zyklus und
entsteht mit jedem Plan neu.

So sähe der Plan aus, Abschnitt `## Fortschritt`, nur vom Skript geschrieben:
```
- [x] Testautor: Tests zu Item 1
- [x] Fachkritiker: Kritik an den Tests umgesetzt
- [ ] Planer: abgenommene Items löschen
  Hindernis: darf nicht löschen (Anliegen 417); beseitigt: Commit „…“
- [ ] Stakeholder: Freigabe Review 5
```
1. Die Schritte kommen aus dem Ablauf. Was ein Fakt belegt (Commit, gelöschte Datei,
   Freigabe), hakt ein Hook nach jedem Rollenlauf selbst ab.
2. Was Urteil ist (Abnahme, DoD, Kritik umgesetzt), hakt die Rolle am Ende ihres Laufs mit
   einem Befehl ab; ein Hindernis meldet sie ebenso, das Skript legt das Anliegen an.
3. Im Dashboard hakst du einen Schritt ab oder kommentierst ihn; der Kommentar wird ein
   Anliegen an die Rolle des Schritts.

Den Code baut der Regelumsetzer, ich passe Ablauf und Ich 2 an.

**F1 · So umsetzen?**
A: Ja, alle drei Teile. B: Erst 1 und 3, ohne Befehl für die Rollen.
Empfehlung: A. Ohne 2 fehlen die Hindernisse, die du sehen willst.
Antwort: .

**F2 · Zählt der Abschnitt zum Höchstmaß des Plans (4.000 Zeichen)?**
A: Nein, er wächst mit dem Zyklus. B: Ja, der übrige Plan wird kürzer.
Empfehlung: A. Der Plan hat heute schon 4.000.
Antwort: .
