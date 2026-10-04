# Schnitt der ersten Oberfläche: Start, Spielstand, Loslassen, Bildschirmtest

146 · Fragen · von Planer (Domäne) → Architekt · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder wünscht ein Frontend im Browser, ähnlich wie ArbiterMap
([145](145-ersteOberflaecheImBrowser.md)). Plan 3 soll mit der ersten Oberfläche von
[Etappe 1](../../domaene/etappen/01-aufstellen.md) beginnen ([Plan](../plan.md), „Danach“).
Ich schlage zwei Items vor:
- (a) *Karte zeigt die Ausgangslage*: Spielfeld, Aufstellungszonen, je Spieler die Ablage,
  gesetzte Modelle, wer an der Reihe ist.
- (b) *Setzen durch Ziehen*: mit Maus und Touch; bei einer Sperre zeigt die Karte den Grund,
  der Zustand bleibt unverändert (D2).

Für den Schnitt fehlen mir technische Antworten:
1. **Start.** Der Stakeholder will die App mit einem Befehl starten und die Adresse genannt
   bekommen (wie `arbitermap-demo`). Was braucht das an `web/` und `frontend/`, und gehört
   es in Item (a)?
2. **Spielstand zwischen Anfragen.** A3 legt den Spielstand in die Datenbank, Auslöser „eine
   Sitzung überleben“. Fachlich verlangt noch kein Kriterium, eine Partie nach einem Neustart
   fortzusetzen. Reicht in Plan 3 ein Spielstand, der mit dem Server endet, oder brauchst du
   die Datenbank schon jetzt?
3. **Loslassen.** Anliegen 03 (in git) hat entschieden: eine Anfrage je Zug, die Fachlogik
   bleibt die einzige Prüfinstanz, die Karte rechnet nicht mit. Gilt das weiter, und wie
   fasst `web/` eine Sperre mit mehreren Gründen für die Karte?
4. **Voraussetzungen.** Komponentenseite, CSS (mit oder ohne Tailwind wie ArbiterMap),
   Werkzeug für den Bildschirmtest, Maus und Touch, eslint und stylelint (ablauf.md, DoD).
   Was davon ist technisches Neuland mit Wegwerf-Versuch, und was muss vor dem ersten
   Mockup stehen?
5. **Größe.** Passt (a) mit den Voraussetzungen aus 4 in einen Zyklus? Kann (b) im selben
   Zyklus folgen, oder schneidest du anders?

**Kosten.** Ohne Antworten schneide ich zu groß oder in der falschen Reihenfolge: Die
erste Oberfläche bringt Start, Karte, Ziehen, Mockup und Bildschirmtest zugleich; in
ArbiterMap hat das Frontend rund 230.000 Zeichen JavaScript, davon 85.402 für das Ziehen.

**Gegenvorschlag.** Antworten hier oder in [architektur.md](../../technik/architektur.md)
(Oberfläche), vor der Domänenphase von Zyklus 3. Danach schneide ich die Items, der
Anforderungsautor fasst die Kriterien.

**Stellungnahme (Architekt).**
1. bis 3.: Aufbau in [153](153-frontendBackendUndDatenbank.md). Der Start gehört in (a).
   Anliegen 03 gilt weiter; eine Sperre kommt mit allen Gründen. Die Datenbank kommt mit der
   ersten Handlung über HTTP, nicht mit (a) (153, F1).
4. Neuland, je mit Wegwerf-Versuch: Bildschirmtest (Playwright mit Chromium), Ziehen mit
   Pointer Events (Maus und Touch), Spielstand aus den Handlungen. Kein Neuland: Start,
   Auslieferung, CSS ohne Tailwind, eslint und stylelint. Vor dem ersten Mockup fehlt die
   Komponentenseite: [155](155-technikBrauchtPlatzUndErstesMockup.md), Punkt 2.
5. (a) als reine Anzeige mit Start, Komponentenseite und Bildschirmtest füllt einen Zyklus.
   (b) danach in zwei Schnitten: erst Wählen per Klick (Gewinner, Zone, Einheit) mit
   Speicher, dann Setzen durch Ziehen, das größte Neuland.
