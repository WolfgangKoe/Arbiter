# Punkte des Koordinators für die Prozessphase

Form: Kritik
Von: Koordinator
An: Organisationsentwickler
Runde: 1/3
Status: erledigt
Wartet auf: Prozessphase

## Runde 1
**Befund.** Diese Punkte standen nur im Startprompt des Koordinators. Hier stehen sie in seinem Wortlaut, zusätzlich zu (a) bis (z), Anliegen 12520 und Anliegen 12900. Nichts daran ist entschieden.

- (aa) Der Hook legt nicht vorgemerkte Änderungen beiseite, neue Dateien aber nicht; Teilcommits prüfen so einen gemischten Stand (zu (z)).
- (ab) Das Abhaken legte 13151 außerhalb des Bereichs des Fachkritikers an, als Doppel zu 13052 (zu (w), (y)).
- (ac) 13010 brauchte drei Runden: F2 bot nur A und B an, die Antwort des Stakeholders lag dazwischen (Bewegungsweite nein, Nahkampfreichweite ja).
- (ad) Wieder ein Doppel beim Abhaken: 13321 zu 13101, außerhalb des Bereichs (zu (ab); Ursache in 13420).
- (ae) Der Implementierer brach bei Item fliegen zweimal mit vollem Kontext ab; das Item war für einen Lauf zu groß, der Koordinator teilte den Auftrag in Abschnitte.
- (af) Rollen laufen nach ihrer Schlussantwort mit Hintergrundarbeit weiter, auch wenn der Auftrag es ausschließt (zu 11100).
- (ag) Den Plan für den Rest legte der Implementierer als Anliegen 13580 ab; der Stand führt nun den Koordinator für 13580. Es fehlt ein Ort für den Arbeitsplan eines Laufs.
- (ah) Abschnitte lassen sich nur committen, wenn jeder neue Code schon aufgerufen wird; der Schnitt muss das beachten.
- (ai) Der Vertrag verlangte Fliegen als Zweig; die Kritik danach einen eigenen Typ, Nacharbeit nach der Umsetzung.
- (aj) Architekt und Reviewer fanden unabhängig denselben Fehler und dieselben Namen; doppelte Kosten. Wieder bei Abschnitt B: 14240 und 14261.
- (ak) Das Nachschieben am Mockup lief in Ketten: 13981 → 14040 → 14080, jede Antwort erzeugte den nächsten Befund; der Vertrag zu ruhigeKarte, den der Stakeholder vorzog, war gar nicht nötig, fand aber diese Lücken.
- (al) Der Gesamtlauf neben anderen Rollen dauerte 17 Minuten; allein dauerte er nun 16, die genannten gut 3 Minuten sind nicht belegt (14360).
- (am) Ein Anforderungsautor sollte Glossar und Spiegel füllen, lehnte das zu Recht ab: Namen ohne Fachbedeutung gehören nicht in Glossar oder Anforderung; die Prüfung erzwang Umbau statt Zeile.
- (an) Die SonarLint-Prüfung lief beim Implementierer nach dem letzten Umbau nicht; erst der Hook fand S5655.
- (ao) Der Testautor brach bei Item ruhigeKarte bei rund 152.000 Token ab, wieder ein Item zu groß für einen Lauf (zu (ae)).
- (ap) Prozessphase, ruff format: prozess/ablauf/werkzeuge.md führt es als „nicht verwendet“ (Anliegen 1581), der Hook verlangt es aber und ließ den Commit scheitern.
- (aq) Der Haken „Item gelöscht“ wird über einen Fakt gesetzt; der Abhak-Befehl des Planers endete danach mit Exit 1 „Offen: keiner“.
- (ar) Der Ruhemodus unterbricht Läufe ohne Meldung; der Koordinator erkennt das nicht von selbst.
- (as) Das Abhaken vergab 14501 und 14502 außerhalb der Bereiche, wieder ein Doppel für denselben Befund (zu (ab), (ad)).
- (at) Das Wochenlimit beendete den Fachkritiker mitten im Lauf; seine Arbeit lag uncommittet im Arbeitsbaum.
- (au) Architekt und Fachkritiker fanden denselben Sprung unabhängig (14480/14461, 14481/14460), wieder doppelte Kosten (zu (aj)).

**(a) bis (z) fehlen.** Ihr Wortlaut steht in keinem Anliegen und nicht im git log; 12520 schließt „(p) und (q) aus dem Startprompt“ aus, 12900 nennt keinen. Gesucht in `handoff/`, `prozess/`, `.claude/`, deren git-Verlauf und Commit-Texten, nicht in Chat-Verläufen außerhalb des Repositorys. Nachtragen kann ihn nur, wer den früheren Startprompt hat.

**Kosten.** Ohne diese Datei wären die Punkte (aa) bis (ar) mit dem Chat verloren. (a) bis (z) kann die Prozessphase nur auswerten, wenn der Wortlaut nachgetragen wird.

**Gegenvorschlag.** Keiner; die Prozessphase wertet die Punkte aus.

**Stellungnahme.** P4: aa, ae bis ah, al, ao; P3: ab, ad, as; P8 hält Punkte fest; aq:
Anliegen 16540; übrige: Retro 10.
