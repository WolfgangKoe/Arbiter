# Die Prüfskripte sind nicht ordentlich strukturiert abgelegt

107 · Kritik · von Stakeholder → Organisationsentwickler (Prozess) · Runde 1/3 · angenommen

Kritik: Ich möchte mir die Prüfskripte gerne anschauen können. Je mehr dazukommen, desto unübersichtlicher wird der Inhalt des Ordners. Des Weiteren scheinen mir die Prüfskripte nicht den Kriterien für lesbaren Code zu entsprechen.

**Stellungnahme (Organisationsentwickler):**
Ich nehme beide Punkte an. Umsetzen wird der Regelumsetzer in der Prozessphase von Zyklus 2,
weil das Inkrement nicht davon abhängt ([Ablauf, Anliegen](../../prozess/ablauf.md#anliegen)).
- Ordnung: 48 Dateien in einem Ordner, Hooks, Prüfungen, Befehle und Tests gemischt. Wonach
  geordnet wird, fragt [113](113-ordnungDerPruefskripte.md); empfohlen sind Themenordner wie
  in `prozess/regeln.md`, die dann als Inhaltsverzeichnis dient.
- Lesbarkeit: Die Skripte halten die geprüften Regeln ein (ruff, Komplexität, Benennung),
  verletzen aber ungeprüfte: Indizes auf Tupel statt benannter Typen (wir.md 6), einen
  Erklärkommentar (wir.md 8), Hook-Protokoll und Repo-Pfade mehrfach gebaut, zwei Module mit
  mehreren Aufgaben. Fundstellen und Erledigt-Bedingung:
  [114](114-pruefskripteOrdnenUndLesbarMachen.md).
- Ursache: Die Regeln 6 bis 9 der Prämisse sind nur Text, und die Kritik am Code hat die
  Verstöße in den Prüfskripten nicht gemeldet. 114 baut Mechanismen für Regel 8 und für
  Typnamen; die Wirksamkeit der Kritik am Code nehme ich in die Retro 2.

wartet auf 113, 114 

Weitere Kritik: Was ist mit dieser Datei? /home/wolfgang/Dokumente/Arbiter_Structure/prozess/pruefungen/benennungRueckstand.txt

**Stellungnahme (Organisationsentwickler):**
Sie ist tot. Sie nahm Altdateien unter `technik/` von der Benennungsprüfung aus, solange sie
unverändert waren. Seit Anliegen 66 hat sie keinen Eintrag mehr, nur noch ihren Kopf. Ich nehme
die Kritik an: Der Regelumsetzer löscht die Datei samt Code, Tests und Ausnahme in ruff
([114](114-pruefskripteOrdnenUndLesbarMachen.md), Punkt D).

wartet auf 113, 114

Nachprüfung: Der Koordinator hat mich gebeten, dieses Anliegen nachzuprüfen. Die Datei "benennungRueckstand.txt" finde ich nicht mehr und ist daher wohl gelöscht. Der Teil des Anliegens ist erledigt. 107 ist voraussichtlich mit 114 abgeschlossen, bitte nach Abschluss von 114 dieses Anliegen hier nochmal zur Prüfung vorlegen.