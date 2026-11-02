# Lücken in BEW-5, BEW-6 und BEW-10 für später

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: 9760

## Runde 1
**Befund.** Diese Punkte warten (Kritik: Lücken abseits des Happy Path, *Sperren*, die nur der
Regeltext verlangt):
1. [BEW-6.2](../../domaene/anforderungen/phasen/bewegung/anhaltenVorDerGrenze.md) prüft nur die
   *Stelle* am Ende. Zieht jemand an einem Gegner vorbei durch dessen *Nahkampfreichweite* und
   lässt dahinter los, hält Arbiter nicht an und sperrt nicht. Der Regeltext verbietet das:
   „no model can be moved within Engagement Range“ (`core_rules.txt:745`, `:754`). ArbiterMap
   hält an der ersten Nahkampfzone auf der Strecke an (`ArbiterMap/docs/spec/interaction_map.md:402`).
2. [BEW-10.1](../../domaene/anforderungen/phasen/bewegung/fremdeModelle.md) lässt das *Modell*
   des anderen *Spielers* ohne *Grund* zurückspringen. Kein Stakeholder hat das entschieden:
   Die Quelle ist das Verhalten des Codes (Anliegen 6300).
   Das Ziel sagt dagegen: „Was nicht erlaubt ist, wird gesperrt“. Ähnliche Fälle sind
   verschieden geregelt: In der *Aufstellung* sperrt AUF-22.1 ‚nicht an der Reihe‘ und lässt
   *gemeinsam übergehen* zu, in den übrigen *Phasen* springt das *Modell* nach QUE-10.5 ohne
   *Grund* zurück (Anliegen 07).
3. [BEW-5.1](../../domaene/anforderungen/phasen/bewegung/vorruecken.md) bietet *Vorrücken*
   auch einer *Einheit* an, die in *Nahkampfreichweite* eines Gegners steht. Ab dort darf sie
   weder vorrücken noch eine *Normale Bewegung* machen (`core_rules.txt:724`, `:739`). In
   Etappe 2 kommt das nur vor, wenn die *Spieler* QUE-1.3 in der *Aufstellung* gemeinsam
   übergangen haben.

**Kosten.** In Zyklus 9 keine: Der Happy Path läuft ohne die drei Punkte. Bleiben sie liegen,
zieht in einer echten Partie ein *Modell* durch die *Nahkampfreichweite* (1), springt ein
fremdes *Modell* ohne Erklärung zurück (2) oder rückt eine *Einheit* vor, die im Nahkampf
steht (3).

**Gegenvorschlag.** 1: ein Kriterium, nach dem BEW-6.2 auf der ganzen Strecke anhält
(Regeltext, ArbiterMap). 2: eine Frage an den Stakeholder. A: wie QUE-10.5, ohne *Grund*
(Anliegen 07). B: eine *Sperre* wie AUF-22.1, die die *Spieler* *gemeinsam übergehen*
können (Ziel). Empfehlung: B, denn das Ziel verlangt die *Sperre*. 3: ein Kriterium, nach
dem Arbiter einer *Einheit* in *Nahkampfreichweite* eines Gegners *Vorrücken* nicht anbietet
(`core_rules.txt:724`).

**Stellungnahme.** 1: steht schon,
[BEW-6.2](../../domaene/anforderungen/phasen/bewegung/anhaltenVorDerGrenze.md) hält „auf der
Strecke“ an (Commit 7ad25ee, Anliegen 6985), Test
`testBew6_2ZiehtEinModellAufDerStreckeDurchDieNahkampfreichweiteHältArbiterEsDavorAn`.
2: Frage an den Stakeholder in Anliegen 9760 F2,
Empfehlung B. 3: umgesetzt,
[BEW-22.1](../../domaene/anforderungen/phasen/bewegung/keinVorrueckenAusDerNahkampfreichweite.md);
die *Normale Bewegung* aus der *Nahkampfreichweite* (`:739`) sperre ich nicht, sie verlangt Fall
Back, das in Etappe 2 fehlt. `angenommen` folgt, wenn 9760 erledigt ist.
