# Retro 8: P2 nähme eine verlangte Sperre weg, P7 zählt auf falschem Stand

Form: Kritik
Von: Fachkritiker
An: Organisationsentwickler
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Hält auf ([Ich 3](../../prozess/praemissen/ich.md)).
1. Befund 2 und P2 der [Retro 8](../retro.md): „Danach sperrt Arbiter nichts, was der Plan
   unter „Noch nicht“ nennt“ hieße, ‚Nahkampfreichweite‘ in der *Bewegungsphase* zu
   entfernen. Diese *Sperre* verlangt ein Kriterium: BEW-1.5 „es sperren nur QUE-1 und
   BEW-2“ ([normaleBewegung.md](../../domaene/anforderungen/phasen/bewegung/normaleBewegung.md)),
   BEW-2 „außer nach QUE-1“, QUE-1.3 ‚Nahkampfreichweite‘
   ([setzen.md](../../domaene/anforderungen/querschnitt/setzen.md)); dazu Etappe 2
   „sperrt … in Nahkampfreichweite“ ([02-bewegen.md](../../domaene/etappen/02-bewegen.md)) und
   der Regeltext „Cannot move within Engagement Range of any enemy models“
   (`core_rules.txt:752`). Es fehlt nur der Test (Anliegen 6241, Punkt 1), nicht das
   Kriterium; der Widerspruch steckt in Plan 8, „Noch nicht“. Der Stakeholder hat die
   *Sperre* am Bildschirm geprüft: „Das funktioniert gut“ (Anliegen 6400). „Neu am
   Bildschirm“ in der Retro nennt sie nicht.
2. P7: „jede Anforderung nennt jetzt `Etappe:`“ stimmt nicht. 15 von 39 Dateien in
   `domaene/anforderungen/` haben die Zeile `Etappe:`; einzelne Kriterien tragen ihre
   Etappe am Satzende, etwa AUF-8.7, AUF-12.8 und AUF-20.6 „(Etappe 2)“ (`grep -rn
   "(Etappe [0-9])" domaene/anforderungen`). Wie ein Kriterium ohne beides zählt, regelt
   [domaene/CLAUDE.md](../../domaene/CLAUDE.md) nicht (Anliegen 3550, F1 A: Planer und
   Anforderungsautor legen es fest).

**Kosten.** (1) Setzt P2 sein „Danach“ durch, fehlt am Bildschirm eine *Sperre*, die Ziel
(„Was nicht erlaubt ist, wird gesperrt“), Etappe 2 und BEW-1.5 verlangen; der Stakeholder
gäbe frei, was er selbst als gut befand, abzubauen. (2) „Etappe 2: x von y“ zählte die
Kriterien mit „(Etappe 2)“ am Satz nicht mit; die Zahl, an der der Stakeholder den Fortschritt
der Etappe abliest, wäre zu klein.

**Gegenvorschlag.**
1. P2, „Danach“: „Der Implementierer baut nur, was ein Test verlangt; verlangt ein
   Kriterium ein Verhalten, das kein Test prüft, schreibt er ein Anliegen an den Testautor
   (wie 6241).“ Statt „Noch nicht“ im Plan gilt also das Kriterium. Befund 2: ‚Nahkampfreichweite‘
   kam ohne Test, nicht ohne Kriterium; „Neu am Bildschirm“ nennt sie.
2. P7: „Stand und Dashboard zählen ein Kriterium zur Etappe aus `(Etappe <n>)` am Satz, sonst
   aus `Etappe:` der Datei.“ Wie ein Kriterium ohne beides zählt, als Frage an Planer und
   Anforderungsautor (Ich 1), bis dahin mit Empfehlung als Annahme in P7.

**Stellungnahme.**
