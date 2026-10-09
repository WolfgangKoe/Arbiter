# Aufstellung lesbar: Landkarte, Fragen an Armee und Ausgangslage

344 · Kritik · von Architekt (Technik) → Implementierer · Runde 1/3 · offen

## Runde 1
**Befund.** Aus [339](339-klasseAufstellungErklaertUndGeprueft.md) (F1 B, Stakeholder):
[aufstellen.py](../../technik/arbiter/domaene/phasen/aufstellen.py) ist schwer zu lesen.
1. Modul und Klasse `Aufstellung` haben keinen Docstring ([Es, S](../../prozess/praemissen/es.md#solid)).
   Abfragen, Handlungen und Hilfen stehen gemischt, nicht nach der Gliederung der
   Anforderung (AUF-1, AUF-7, AUF-3, AUF-5).
2. Ob zwei *Spieler* verschiedene *Armeen* ohne gemeinsames *Modell* haben, prüft
   `Aufstellung.__init__` mit `_teilenSichArmeeOderModell`; das ist eine Eigenschaft der
   `Ausgangslage`, die beide trägt.
3. Zu welcher *Einheit* ein *Modell* gehört, sucht `_einheitVon` durch alle *Einheiten*
   beider *Armeen*; das ist eine Frage an die `Armee`.
4. Die Regel *Nahkampfreichweite* ist eine Methode der Klasse, obwohl sie nur die *Stellen*
   und die eigenen *Modelle* braucht; *Base überdeckt* liegt schon als Funktion außerhalb
   (`querschnitt.baseÜberdeckt`). Die Klasse trägt so eine Regel und ruft die andere auf.

**Kosten.** Der Stakeholder versteht die Klasse nicht; AUF-5.5 und die Kohärenz wachsen in
die Mischung. Jetzt: ein Lauf, keine neuen Akzeptanztests.

**Gegenvorschlag.** Vor AUF-5.5. Erledigt, wenn
- `python3 -m pytest technik/tests` und `python3 -m pytest prozess/pruefungen` grün sind,
  ohne Änderung an Akzeptanztests (Verhalten unverändert);
- Modul und Klasse je einen einzeiligen Docstring haben, der ihre Aufgabe nennt;
- die Klasse gegliedert ist: Zustand und Abfragen, dann AUF-1 (Wahlen, *an der Reihe*),
  AUF-7 und AUF-3 (*setzen*, *Aufstellen der Einheit beenden*, Sperren), AUF-5
  (Auswählen); eine Hilfe steht beim Abschnitt, der sie nutzt;
- `Ausgangslage` die Prüfung auf zwei verschiedene *Spieler* mit getrennten *Armeen* beim
  Erzeugen selbst trägt (`ValueError`, wie heute) und `Aufstellung.__init__` nur Zustand
  anlegt;
- `Armee` beantwortet, zu welcher ihrer *Einheiten* ein *Modell* gehört, und `_einheitVon`
  nur noch die zwei *Armeen* fragt;
- *Nahkampfreichweite* eine Funktion des Moduls ist, in der Form von
  `querschnitt.baseÜberdeckt` (*Modell*, *Stelle*, *Stellen*, dazu die eigenen *Modelle*);
  die Methode der Klasse ruft sie nur auf, wie `_baseÜberdeckt`. Wohin die Funktion zieht,
  entscheidet [345](345-spiegelZwischenAnforderungUndCode.md);
- je ein Einheitstest für die zwei neuen Fragen an `Ausgangslage` und `Armee` besteht;
- keine neue Klasse entsteht. Die Auswahl als eigene Klasse braucht erst den Begriff im
  Glossar (345, F3); sie kommt als eigenes Anliegen.

**Stellungnahme.**
