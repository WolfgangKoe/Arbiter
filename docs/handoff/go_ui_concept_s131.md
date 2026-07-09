STATUS: ANSWERED

# GO-UI-Konzept — gemeinsames Verständnis (S131)

Temporär — löschen nach Übernahme der Entscheidungen in `docs/spec/design_colors.md`
(bzw. neuem `design_system.md`-Abschnitt) und `docs/goals/backlog.md`.

Kontext: S130 hat Gefechtsoptionen (GOs) in drei verschiedenen UI-Formen in die App
gebracht (`src/uiLayout/_common.py`, `src/gameMechanic/{fightPhase,movementPhase,
chargephase,moralePhase,psychicPhase}.py`). Der Stakeholder hat **Undo-Standard für
ALLE GOs (Option A)** entschieden, aber es fehlt ein Bild, wie GOs grundsätzlich
aussehen und sich verhalten. Dieses Dokument zeigt den IST-Zustand aus dem Code und
schlägt den SOLL-Standard vor.

## 1. Die 3 GO-Grundmuster (IST)

### a) Reaktive Box — Fire Overwatch, Counter-Offensive, Cut Them Down, Emergency Disembarkation

```
┌ second_player-Spalte ────────────────┐
│ ⚔ Reaction available — Fire Overwatch│
│ (1 CP)                               │
│ Warriors was declared a charge       │
│ target by Boyz.                      │
│ ▸ Rule text                          │
│ [Use — spend 1 CP]      [Pass]       │
└───────────────────────────────────────┘
```
Erscheint **automatisch** in der Spalte des betroffenen Spielers, sobald der
Phasen-Handler das Trigger-Fenster öffnet (Charge deklariert, Fall Back deklariert,
Gegner hat gerade gefochten, TRANSPORT zerstört). Klick auf **Use** bucht CP,
markiert die GO als verbraucht und ruft ggf. einen GO-spezifischen Effekt auf
(`spend_stratagem` + `on_spent`). Klick auf **Pass** merkt sich `decline_key` nur
für dieses eine Trigger-Vorkommen. **Kein Undo** — nach Use/Pass verschwindet die
Box; das Fenster ist einmalig pro Trigger-Vorkommen.

### b) Inline-Offer — Command Re-Roll (↻) an Damage-/Psychic-/Deny-Würfen

```
Roll 4 — Manifested! Deny failed. (3 mortal wounds)
[↻ Command Re-Roll (1 CP)]
[Reset]
```
Erscheint **direkt neben dem zuletzt gezeigten Wurfergebnis** (Damage-Block, Perils-
Manifest, Deny-Ergebnis) — kein Rahmen, kein Titel, kein Pass-Button („Pull, not
Push": ignorieren kostet nichts). Klick würfelt neu (`on_reroll` setzt das Feld
zurück auf editierbar) UND bucht sofort CP + Verbrauch. Verschwindet, sobald ein
späterer Wurf den aktuellen ersetzt oder die Phase endet. **Kein Undo** — das ist
exakt der S130-Rest-Befund (Backlog „GO-UI-Design-System ergänzen"): andere GOs
haben einen Rückgängig-Pfad, Command Re-Roll nicht.

### c) Auto-Effekt / Tab-Schalter — Insane Bravery, Desperate Breakout, alle proaktiven Stratagems

```
┌ Stratagems-Tab, first_player-Spalte ─┐
│ Core                                  │
│ ▾ Insane Bravery · 1 CP               │
│   Auto-pass this Morale test.         │
│   [↺ Rückgängig (+1 CP)]              │
│   — oder, falls ungenutzt: —          │
│   [Use — spend 1 CP]                  │
└────────────────────────────────────────┘
```
Aktivierung über die zentrale Stratagems-Liste (`gameProtocoll.py`, zwei feste
Spalten `first_player`/`second_player`, unabhängig von `active`). Wirkung ist
proaktiv/dauerhaft (Modifier oder Flag), zeigt sich erst später im Spielverlauf
(z. B. Morale-Phase: „Insane Bravery active — Confirm"-Button). **Hat bereits
Undo** (`stratagem_undo_visible`) — solange dasselbe Phasenfenster offen ist
(P21, S118 gefixt): CP zurück, Verbrauchs-Flag zurückgesetzt, Modifier entfernt.

## 2. SOLL-Standard (Vorschlag gemäß Entscheid Option A)

**Grundsatz:** Jede GO-Aktivierung, die CP bucht, bekommt einen sichtbaren Undo-Pfad,
solange das Aktivierungsfenster (Phase/Trigger) noch offen ist — Format a) und c)
haben das bereits strukturell gleich gelöst (`↺ Rückgängig (+N CP)` neben dem
verbrauchten Element). Muster b) (Command Re-Roll) ist der einzige Ausreißer.

**Das Problem bei Command Re-Roll:** Undo bei a)/c) heißt „Zustand vor der
Entscheidung wiederherstellen" — dort gab es noch keinen neuen Fakt am Tisch. Beim
Re-Roll dagegen hat der Spieler das **neue Würfelergebnis bereits gesehen**, bevor
er „Undo" drücken könnte. Ein echtes Undo („der Re-Roll fand nie statt, der
Ursprungswurf zählt wieder") gibt dem Spieler Information zurück, die er im echten
Tischspiel nicht zurückgeben kann (er kennt beide Werte). Das ist regeltechnisch
nicht neutral — ein Vollrückgängig würde faktisch „würfle, bis es passt" erlauben.

**Vorschlag: abgeschwächter Undo — CP-Refund, aber der Re-Roll-Wert bleibt gültig.**
Der Button heißt nicht „Rückgängig", sondern korrigiert nur die Buchung, falls sich
der Spieler beim CP-Ausgeben vertan hat (z. B. Re-Roll versehentlich ausgelöst,
CP eigentlich zu knapp für den nächsten Zug). Das Würfelergebnis, das jetzt auf dem
Tisch liegt, bleibt stehen — es gibt keinen Weg zurück zum Ursprungswurf.

```
Roll 4 — Manifested! Deny failed. (3 mortal wounds)
[↺ CP zurückbuchen (+1 CP)]
```
Erscheint an derselben Stelle wie zuvor das ↻-Offer, aber erst NACH dem Re-Roll-
Klick, ersetzt den ↻-Button für den Rest des Fensters (wie bei a)/c): CP zurück,
Verbrauchs-Flag zurückgesetzt — der neu gewürfelte Wert bleibt als Ergebnis stehen.

**Alternative (nicht empfohlen, nur der Vollständigkeit halber):** echtes Undo inkl.
Wert-Rücksetzung. Technisch möglich (der App liegt der Ursprungswert noch vor, bis
ein Folgeschritt ihn überschreibt), aber regeltechnisch fragwürdig — siehe oben.
Falls der Stakeholder das dennoch will, sollte es ausdrücklich als Ausnahme markiert
werden, nicht als Standard-Semantik von „Undo".

## 3. Zuordnungsregel — welches Muster für welche GO-Art

| GO-Art | Muster | Beispiel | Undo |
|---|---|---|---|
| Reaktiv, eigenes Zeitfenster (Trigger → Use/Pass, danach vorbei) | a) Reaktive Box | Fire Overwatch, Counter-Offensive, Cut Them Down, Emergency Disembarkation | keiner (Fenster ist einmalig) |
| Wurf-Ersatz (ersetzt/wiederholt einen bereits sichtbaren Würfelwert) | b) Inline-Offer | Command Re-Roll (Damage/Psychic/Deny) | abgeschwächt: CP-Refund, Wert bleibt |
| Dauerhaft-proaktiv (Modifier/Flag, wirkt über mehrere Schritte, freie Spielerwahl wann) | c) Auto-Effekt / Tab-Schalter | Insane Bravery, Desperate Breakout, künftige ~56 Fraktions-Stratagems (z. B. Charge/Advance-Re-Roll als dauerhafter Modifier statt Inline) | voll: solange Phasenfenster offen |

Faustregel für neue GOs: **Hat die GO einen eigenen, einmaligen Trigger-Moment mit
Use/Pass-Entscheidung?** → a). **Ersetzt sie einen bereits gewürfelten/gezeigten
Wert?** → b). **Sonst** (proaktive Wahl, kein harter Trigger) → c), zentrale Liste.

## 4. Entscheidungsfragen an den Stakeholder

1. **Command-Re-Roll-Undo-Semantik:** abgeschwächter Undo (CP-Refund, Re-Roll-Wert
   bleibt gültig) — wie in §2 vorgeschlagen — oder soll es doch ein Vollrückgängig
   inkl. Wert-Rücksetzung geben (regeltechnisch fragwürdig, s. o.)?
   **Empfehlung:** abgeschwächter Undo.
2. **Label-Konvention:** soll der abgeschwächte Undo-Button bewusst anders
   heißen als „↺ Rückgängig" (z. B. „↺ CP zurückbuchen"), damit Spieler den
   Unterschied zum Vollrückgängig bei a)/c) sofort sehen? **Empfehlung:** ja,
   eigener Text — sonst wird stillschweigend ein Vollrückgängig suggeriert.
3. **Proaktive Fraktions-Stratagems (~56, aktuell nur teilintegriert):** alle
   künftigen als Muster c) in die zentrale Liste, oder gibt es Fälle mit
   eigenem Trigger-Fenster, die eher zu a) gehören (z. B. „beim Erklären eines
   Angriffs")? **Empfehlung:** Regel aus §3 anwenden statt Einzelfalldiskussion —
   Trigger-Moment vorhanden → a), sonst c).
4. **Reichweite des Undo-Standards:** gilt „Undo Pflicht" auch rückwirkend für a)
   (reaktive Box), obwohl dort aktuell bewusst keiner existiert (Fenster ist
   einmalig, „Pass" ist bereits die Undo-Alternative vor der Entscheidung)?
   **Empfehlung:** nein — a) braucht keinen Undo, weil vor der Entscheidung
   „Pass" existiert und nach der Entscheidung (z. B. Fire Overwatch schießt)
   der Spieleffekt bereits am Tisch sichtbar ist, genau wie beim Re-Roll-Wert.


Anmerkungen zu deinem Konzept:
1. Eine Grundannahme scheint zu sein, dass in der App gewürfelt wird. Das ist so nicht korrekt. Die Spieler würfeln auf dem Tisch! Die App sieht das nicht. Der Schiedsrichter greift eben dann, wenn die Entscheidung endgültig gesetzt ist (z.B. am Ende einer Phase, eines Zuges oder einer Runde) Es muss möglich sein, "Versehen" oder "Vergessen" zu korrigieren. Die Aufgabe der App ist mehr dafür zu sorgen: "Schau, jetzt kommt diese Regel oder diese Fähigkeit infrage. Das musst du aber entscheiden." Ohne die App war die Entscheidung oft nicht möglich, weil man nicht daran gedacht hat. Ist das verständlich? Sonst müssten wir den Sinn der App nochmal nachschärfen.

2. Ich sehe, dass wir drei Dinge unterscheiden, einen Reroll (das macht neben dem Command-Reroll auch noch andere GO), eine Reaktiven und eine Proaktive GO. Wobei ein Re-Roll manchmal pro-aktiv oder reaktiv sein kann, das ist eher ein Effect. Ich bin mir daher nicht sicher, ob wir dies als Sonderfall behandeln sollten. Hier ist vielleicht eher nochmal eine Recherche und ANalyse erforderlich, was ungeachtet der aktuellen UI eine gute Einteilung ist. 

3. Dann zur UI selbst. Die reaktive Box und die inline-Offer sind im wesentlichen dieselbe Komponente, denn sie erscheinen in der gameActionArea. Ich bevorzuge die schlankere Version. Da kommt die inline Offer am nächsten dran. Ich habe aber ein kleines Problem damit, dass die einfach "auftaucht". Lieber wäre mir, dass man es in einer Runde immer sieht und sie dann hervorgehoben und aktiviert wird, wenn der Trigger kommt. So ist es grundsätzlich im Blick und man ist nicht überrascht. Dieses Verhalten wünsche ich mir auch bei den Tab-Schaltern. Die würde ich in der Tat so lassen. Aktuell vermute ich, dass man die Spieler sich die Liste anschauen und damit ihre Phase planen. Generell möchte ich, dass Inline und Tab-Schalter konsistent verhalten, dieselben Begriffe in der FUnktion verwenden und vergleichbare Farben verwenden. Das soll sich entweder aus dem aktuellen Design-System ergeben oder es muss ergänzt werden. Sobald die Entscheidung steht, werden wir feststellen, dass wir auch die UI an anderen Stellen besser vereinheitlichen müssen. Daran arbeite ich aktuell. Denn die Buttons in der Bewegungsphase sind aktuell funktinoial. In anderen Phasen gibt es hier wieder Boxen und dann wieder BOxen oder inlin- Offers. Im Sinne der ganzheitlichen Betrachtungsweise sollten wir hier vielleicht gleich die UI-Komponenten festlegen und nicht mit verschiedeen Konzepten fahren. Zum konkreten Verhalten der GO-Komponenten in der UI siehe Punkt 4.

4. Das Akkordeon-Verhalten in den Tab-Schaltern gefällt mir aktuell nicht. Da klappt manches automatishc zu, wenn es aufgeklappt bleiben sollte. Ich versuche es mal etwas umzubauen.

```
┌ Stratagems-Tab, first_player-Spalte ───────────┐
│ Core                                           │

┌────────────────────────────────────────────────┐
│ ▾ Insane Bravery · 1 CP  [Use]                 │
│                       — oder, falls genutzt: — │
│                           [↺]                  │
│[keyword_1][keyword_2][keyword_3]...            │
└────────────────────────────────────────────────┘
│   Regeltext, der ausgeklappt werden kann       │
│                                                │
└────────────────────────────────────────────────┘
```

Die doppelte CP-Anzeige sollte hier verschwinden, das steht ja ganz oben im Header. 
Den Ausklappmechanismus braucht es nach meinem Dafürhalten nur, um den genauen Regeltext lesen zu können, falls erforderlich. Ansonsten reicht mir die Funktion und die Anzeige relevanter Schlüsselwörter. Das sieht so ähnlich aus wie in der Unitcard. Nur dass wir eben keine Lebenspunktebalken haben. 
Einen Knopf wie "Pass" braucht es m.E. nicht. Wenn man passt, drückt man einfach den Knopf "Use" nicht. 

Inline sähe es entsprechend aus:

```
 ▾ command-ReRoll · 1 CP  [Use]
                        — oder, falls genutzt: — 
                           [↺]

│   Regeltext, der ausgeklappt werden kann       │
│                                                │
└────────────────────────────────────────────────┘
```
Das Design aber nochmal prüfen!!!


5. Zu den Postionen. In der Tab-Schalter-ANsicht sollte alles passen. Die GOs bleiben entsprechend auf der Seite des jeweiligen Spielers. Inline kann ich es mir noch nicht vorstellen, aber da sollte es entsprechend genauso sein. Der Command-reroll wird in der Bewegungsphase auf den Advancedwurf angewendet, wenn gewünscht. Es ist dann aber der aktive Spieler, also muss es in die Button-UI rein. Das müssen wir sauberer lösen. Mach hier bitte einen Vorschlag.
Bei der Attackenabfolge sind manche Reaktive GOs auf bestimmte Würfe innerhalb der Phase getriggert. Der Inline-Ort muss dann z.B. beim Treffer- Verwundungs, Rüstungs-, Rettungs- und Schadenzuweisungsbereich sein. Manches triggert auch bei Auswahl eines gegnerischen Modells. Insbesondere hier ist die UI aktuell sehr inkonsistent über alle Phasen gestaltet. An sich gefällt mir die Darstellung in der heroischen Intervention am besten (s. Bildschirmfoto vom 2026-07-09 18-26-00). Sie ist schlank und einfach. Man müsste diese wohl etwas ausbauen und die Buttons und Bezeichnungen ausbauen und anders anordnen, aber wenn wir die Zielauswahl mitder komplizierteren Subgruppen und Waffenauswahl (s. Bildschirmfoto vom 2026-07-09 18-27-11) damit hinbekommen, wird die UI insgesamt etwas "schöner". Ich überlege sogar, ob wir die Auswahl der Einheiten nicht stärker in die GameActionArea ziehen und dort dann auch nur die Buttons der auswählbaren Einheiten angezeigt wird, die handeln können - eben ähnlich in der heroischen Intervention. Bei Auswahl einer Einheit über den Button und Auswahl der gegnerischen Einheit Button in der anderen PlayerArea, wird dann die entsprechende UnitCard hochgezogen. Der Vergleich der Profilwerte könnte über ein Dropdown erfolgen, aber das stellen wir erstmal zurück. Die Zielauswahl ist mit all den Daten, die erst später relevant sind, etwas zu überladen. 

Was mir bewusst ist! In Punkt 5 gehen wir in ein anderes Thema, aber es zeigt, dass wir in der UI noch Chaos und kein konsistentes Design-System haben. Lass uns das hier lösen, sonst nervt es mich immer wieder. Aus meiner Sicht wäre es Teil dieser Session, das alles gut zu recherchieren, zu konzipieren und zu planen. Es wäre auch okay, das über mehrere Sessions zu machen.