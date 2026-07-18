STATUS: NEEDS-DECISION

# S166 — Mockup „Pflicht-Trigger-Kachel" (Explodes-Familie, B-028c1)

Lebensdauer: bis Stakeholder-Entscheidung. Nach Abnahme: Entscheidung in
`docs/spec/design_system.md` (neues §7) überführen, diese Datei löschen.

## a) Grundannahmen-Block (vor Detail-Entscheidungen zu bestätigen, S131-Pflicht)

1. **Die App würfelt nicht.** Jeder Wurf (Explodes-Gate, Schaden je Einheit) wird am
   Tisch gewürfelt; die App nimmt nur das Ergebnis entgegen (Tisch-Wurf-Baustein,
   `design_system.md` §6.3). Kein Engine-Selbstwurf wie im alten
   `resolve_mortal_wounds_effect`-Stand (S164) — der wird zurückgebaut.
2. **Pflicht-Trigger ≠ Gefechtsoption (GO).** Explodes ist ein **Pflicht-Ereignis** beim
   Tod des Modells — kein Verwenden/Nicht-Verwenden-Entscheid, kein `[Use]`-Button, keine
   CP. Die bestehende GO-Karte (`design_system.md` §6.1) ist für diesen Fall die falsche
   Komponente; ersetzt wird sie durch eine eigene „Pflicht-Trigger-Kachel".
3. **Anker am Trigger-Ort, nicht Vollbreite.** Die Kachel hängt am Eintrag der zerstörten
   Einheit, innerhalb der Zwei-Spalten-Aufteilung ihres Besitzers (`design_system.md`
   §6.2: reaktive Karten NUR inline am Trigger-Ort). Der S165-Verstoß (Vollbreiten-Kachel
   oberhalb der Spalten) wird hiermit nicht wiederholt.
4. **Explizite Erledigung in jedem Ausgang.** Auch „does not explode" ist ein sichtbarer,
   markierter Endzustand — kein stilles Verschwinden der Kachel.

Bitte VOR den Detail-Entscheidungen unten bestätigen oder korrigieren.

## b) Fachliche Einordnung — wörtliche Wahapedia-Zitate

**Generische Regel „Explodes"** (Quelle: `docs/work/wahapedia_core_rules/rules_appendix.txt:1253-1262`):

> „When destroyed, some models have an ability that gives them a chance to explode (or
> crash and burn, or lash out with death throes etc.) and inflict mortal wounds on nearby
> units. If a model has such an ability and is destroyed, then it is always the player
> controlling that model who rolls to see if it explodes (or similar), and it is always
> this player who rolls to see if nearby units suffer damage, and if they do, how much
> damage is inflicted."

Damit ist beleg­t: **beide Würfe** (Explodes-Gate UND Schaden) liegen fachlich beim
kontrollierenden Spieler — die App ist Erinnerer/Eingabe-Helfer, nicht Würfler
(Grundannahme 1 bestätigt durch den Regeltext selbst, nicht nur durch Projekt-Konvention).

**Vengeance of the Enchained** (Quelle: `docs/work/wahapedia_necrons/units_all.txt:689`,
The Silent King):

> „Vengeance of the Enchained: When this model is destroyed, roll one D6 before removing
> it from play. On a 4+ it explodes, and each unit within 2D6" suffers D6 mortal wounds."

**Datenbug bestätigt (B-028c1 Punkt 4):** `data/wh40k_9e/necrons/unit_abilities.yaml:391`
trägt aktuell `"On a 4+, each unit within 2D6\" suffers D6 mortal wounds."` — das Wort
„it explodes" fehlt. Nachrichtenkorrektur ist Teil des Umsetzungspakets (Punkt 4 im
Re-Scope), nicht Teil dieses Mockups.

**Weitere Explodes-Träger (Beleg für „Standard-Familie", nicht nur Einzelfall)** — alle
`docs/work/wahapedia_necrons/units_all.txt`:
- Canoptek Spyder (Z.416, Z.560): „On a 6 it explodes, and each unit within 3"/6" suffers
  1 mortal wound / D3 mortal wounds."
- C'tan „Reality Unravels" (Z.400, Z.654, Z.665, Z.678): „On a 4+ it explodes, and each
  unit within 6" suffers D3 mortal wounds."
- Ghost Ark „Wrecked" (Z.752): abweichende Variante — „On a 6 it explodes […] On any
  other result that model is wrecked" (kein reiner Explodes-Fall, hier nur als Beleg für
  Variationsbreite genannt, NICHT Teil des aktuellen Scopes).

**`auto_explode`-Stratagem** (Quelle: `docs/work/wahapedia_necrons/stratagems.txt:79`):

> „Use this Stratagem in any phase, when a NECRONS VEHICLE model from your army is
> destroyed. Do not roll to see if that model explodes: it does so automatically. If that
> model has the TITANIC keyword, this Stratagem costs 3CP; otherwise it costs 1 CP."

Das ist die einzige Stelle im Explodes-Komplex, an der tatsächlich ein Verwenden/
Nicht-Verwenden-Entscheid mit CP-Kosten existiert — daher als **eigene GO** (Baustein 4,
Standard-GO-Karte) statt Teil der Pflicht-Kachel modelliert (Re-Scope Punkt 3).

## c) Komponenten-/Anker-Vorschlag

| Baustein | Vorschlag | Beleg |
|---|---|---|
| Pflicht-Trigger-Kachel | Eigene Komponente, KEIN `[Use]`-Button, KEIN CP-Kosten-Feld — sonst gleiche Bauform wie die GO-Karte (ein `st.container(border=True)`, Header-Zeile + Rule-text-Akkordeon) | `design_system.md` §6.1 (Bauform-Vorbild), §1.2 (Card/Panel) |
| Anker | Am Eintrag der zerstörten Einheit, innerhalb der Spieler-Spalte (nicht Vollbreite) | `design_system.md` §6.2 |
| Explodes-Wurf-Eingabe | Tisch-Wurf-Baustein: Label `Explodes roll (D6) · needs {roll_threshold}+`, Zahlenfeld, Confirm | `design_system.md` §6.3 |
| Ziel-Auswahl nach Erfolg | Multi-Select über beide Armeen (Reichweite misst der Tisch, App zählt nicht nach) + je Ziel ein Tisch-Wurf-Feld für die Mortal-Wounds-Zahl | analog Vorgeschichte S164 (`mortal_wounds_target`), jetzt ohne Engine-Würfeln |
| „does not explode"-Ausgang | Eigener, sichtbar markierter Endzustand (`resolved`-Chip + Klartext „does not explode"), keine kommentarlose Entfernung | Grundannahme 4 |
| Farbe der Kachel (**Vorschlag, keine Festlegung**) | DESTROYED-Rot `#c04040` (bereits etabliert für den Status „zerstört", `design_colors.md` §2) statt Gold-Primary (GO-„ready", §6.5) — ein Gold-Rahmen würde fälschlich „wählbare GO" signalisieren | `design_colors.md` §2 (DESTROYED-Farbe), §0 (Farbentscheidungen trifft der Nutzer — **bitte bestätigen oder Alternative nennen**) |
| `auto_explode` | Normale GO-Karte (Gold-Rahmen, `[Use]`, CP-Anzeige im Header `1 CP`/`3 CP` bei TITANIC), zentrale Stratagems-Liste (proaktiv) | `design_system.md` §6.1/§6.2/§6.5 |

**Offene Farb-Entscheidung:** Da `design_colors.md` bislang kein Token für „Pflicht-Trigger,
kein GO" kennt, ist der Rot-Vorschlag oben eine Empfehlung, keine Festlegung — Farb­ent­scheidungen
trifft laut Spec-Kopf ausdrücklich der Stakeholder. Antwort: Ich würde hier bei dem Standard-Goldschema bleiben. Ist nicht nur für GOs vorbehalten.

## d) HTML-Mockup

`docs/handoff/S166_MOCKUP_EXPLODES.html` (im Browser öffnen). Zwei Varianten, echte
Layout-Alternative:

- **Variante A — progressiv:** immer nur der aktuelle Schritt (Wurf → Ziel-Auswahl+Schaden
  → Abschluss) sichtbar, vorherige Schritte bleiben als erledigte Zeile stehen. Kompakter,
  aber der Spieler sieht den Gesamtablauf nicht auf einen Blick.
- **Variante B — eine aufgeklappte Kachel:** alle drei Schritte gleichzeitig in einer
  Kachel sichtbar (spätere Felder inaktiv, bis der vorherige Schritt bestätigt ist). Größerer
  Platzbedarf, aber der ganze Ablauf ist von Anfang an erkennbar.

Zusätzlich, klar getrennt: der `auto_explode`-GO-Baustein (Abschnitt 4 im Mockup) im
Standard-GO-Karten-Look, damit der Unterschied Pflicht-Kachel vs. echte GO auf einen Blick
sichtbar ist.

**Frage an den Stakeholder:** Variante A oder B (oder Elemente aus beiden kombinieren)?

Danke für das Mockup - Das hilft, damit ich deine Vorstellung sehe. Ich würde diesen aber in dieser Form eher ablehnen, weil es sich nur grob an unseren UI-Komponenten orientiert, die ich mir vorstelle. Das Design-System ist einfach noch nicht wirklich gut. Ich möchte nicht noch mehr UI-Komponenten haben. 

Ich gebe dir mal ein paar Beispiele mit Screenshots im Handoff aus der bestehenden Anwendung.
1. Für die "Explosion" würde ich mich an der UI orientieren, wie es schon für Psi-Kräfte implementiert ist (s.Bildschirmfoto vom 2026-07-18 11-51-02 oder Bildschirmfoto vom 2026-07-18 11-54-10). Im Prinzip ist es dieselbe Mechanik. Da ist ja auch die GO für den Command reroll korrekt eingefügt. Auf eine ähnliche Weise für ich den Auto-explode integrieren.
2. Die Auswahl betroffener Einheiten funktioniert aktuell und kann hier genauso erfolgen. Aus UX Sicht ist es aber noch viel Scrollen. Daher würde ich hier ergänzend eine weitere Einheitenauswahl implementieren, ähnlich wie es bei der heroischen Intervention ist (s. Bildschirmfoto vom 2026-07-18 11-51-51 und Bildschirmfoto vom 2026-07-18 12-01-39). Hier muss man dann in der anderen Spalte einen Abschnitt mit eigenen und gegnerischen Einheiten darstellen. Man wählt die betroffenen Einheiten aus. Neben den Buttons der ausgewählten Einheiten erscheint dann ein Feld wie in Bildschirmfoto vom 2026-07-18 12-07-09, wo man den Schaden eintragen kann, der wird dann auch interaktiv der Einheit zugewiesen (also der LP-Balken in der unitCard sinkt). Ist man fertig, ist ganz unten ein Button mit "Confirm all" wie wir es am Ende der Attackensequenz haben und es braucht natürlich auch eine Reset-Logik, falls man doch noch etwas korrigieren möchte.
3. Und weil du mir eine schöne HTML gebaut hast, kannst du das bitte nochmal tun und zwar mit den gezeigten Komponenten aus den Screenshots und dies nochmal vorlegen. Das wäre gut, denn damit könnten wir nämlich schon den größeren Umbau der UI für die Einheiten-Selektion vorbereiten.

## e) Befund Teilaufgabe A — Screenshot-Einordnung (doppelter Rule-Text)

**Fundstelle:** `src/uiLayout/_common.py:406-416` (`_render_mortal_wounds_on_destroy_card`)
ruft `render_reactive_ability_box(...)` mit `context_caption=ability.rule_text` (Zeile 413)
auf. `render_reactive_ability_box` reicht das als `expanded_content` weiter
(`_context_caption_renderer(context_caption)`, Zeile 1015) an `render_go_card`
(`_common.py:1454`). `render_go_card` rendert **zweimal** denselben String: einmal im
„Rule text"-Akkordeon (`_common.py:1543-1545`, `if rule_text: … st.caption(rule_text)`)
und ein zweites Mal über `expanded_content()` (`_common.py:1547-1548`) — genau das Bild im
Screenshot.

**Ist das ein generisches Render-Muster oder ein lokaler Bug?** Lokaler Bug. Ich habe alle
8 Aufrufstellen von `context_caption=` geprüft (`grep -n "context_caption=" src/uiLayout/
_common.py src/gameMechanic/*.py`): jede andere Stelle übergibt einen eigenständigen
„warum ist diese Karte gerade aufgetaucht"-Text, NIE den Rule-Text selbst — Beispiele:
`chargePhase.py:181` `f"{unit.name_en} was declared a charge target"`,
`psychicPhase.py:210` `"A Psychic test manifest roll was just made."`,
`_common.py:1599` `f"{unit.name_en} (TRANSPORT) was destroyed."`. Nur
`_common.py:413` übergibt `ability.rule_text` — dieselbe Zeichenkette, die bereits im
Akkordeon steht. `render_go_card`/`_context_caption_renderer` selbst sind also nicht
fehlerhaft; der Aufrufer hat versehentlich den Rule-Text statt eines eigenen
Trigger-Hinweises übergeben.

**Empfehlung:** KEIN neues Backlog-Item. `_render_mortal_wounds_on_destroy_card` ist genau
die alte GO-Karten-Implementierung für Vengeance of the Enchained, die B-028c1 (Re-Scope
S165) ohnehin durch die Pflicht-Trigger-Kachel ersetzt — der Doppel-Text verschwindet mit
dem Umsetzungspaket, wenn diese Funktion durch die neue Komponente abgelöst wird. Kein
gesonderter Fix nötig, keine weitere Suche in anderen Karten — das Muster ist nicht
systemisch.

Zur Kenntnis genommen.

## f) Lebensdauer

Nach Stakeholder-Abnahme: Entscheidung (Variante A/B, Farb-Bestätigung) in
`docs/spec/design_system.md` als neues §7 überführen, `docs/goals/backlog_details.md`
B-028c1 auf den nächsten Umsetzungsschritt aktualisieren, diese Datei sowie das HTML-Mockup
löschen (Lebensdauer laut Datei-Kopf: bis Stakeholder-Entscheidung).

Die gerade erstellte HTML kannst du schon mal löschen.

## g) Mockup V2 (nach Stakeholder-Feedback)

`docs/handoff/S166_MOCKUP_EXPLODES_V2.html` (im Browser öffnen, interaktiv). Übernimmt
ausschließlich Bestandskomponenten statt neu erfundener Bauformen: der Explodes-Gate-Wurf
nutzt den Tisch-Wurf-Baustein §6.3 (Vorbild „Bildschirmfoto vom 2026-07-18 11-51-02" —
Smite/Attempt Manifest), die `auto_explode`-GO steht als Standard-GO-Karte §6.1 direkt am
Wurf-Anker (Vorbild „11-54-10" — Command-Re-Roll-Karte im Psi-Flow) und ersetzt den Wurf
bei `[Use]` automatisch, ganz wie die Stratagem-Regel es verlangt. Für die Ziel-Auswahl
nach einem Erfolg erscheint in der Orks-Spalte (rechts) ein Panel im Heroic-Intervention-
Stil (Vorbild „11-51-51" + „12-01-39"): zwei beschriftete Einheitsgruppen (Necrons/Orks)
als Toggle-Buttons, je ausgewählter Einheit ein Zahlenfeld „MORTAL WOUNDS (D6)" (Vorbild
„12-07-09") mit live sinkendem LP-Balken (unitCard-Bestandskomponente), unten „Confirm
all" + „Reset". Der Fehlschlag-Ausgang nutzt bewusst die bestehende Hinweis-Konvention
§3 (`warning`, Streamlit-Amber) statt Rot, der Erfolgs-Ausgang die `success`-Konvention
(Grün) — beides ohne neues Farb-Token, komplett im Gold-Standardschema für alles
Interaktive (Stakeholder-Entscheid: Gold nicht GOs vorbehalten). Jeder Abschnitt trägt
eine dezente „Baustein: …"-Quellenangabe.

**Offene Abnahme-Frage:** Passt diese Zuordnung der Bausteine (Tisch-Wurf + GO-Karte für
den Explodes-Wurf, Heroic-Intervention-Panel für die Ziel-Auswahl in der anderen Spalte,
warning/success statt eigener Farben) so, oder braucht es Korrekturen, bevor diese
Struktur den größeren Umbau der Einheiten-Selektions-UI vorbereitet?

Antwort: Dieses Mockup passt deutlich besser. Folgende Korrekturwünsche:
1. Wird eine Einheit für den Schaden gewählt, sollte die dazugehörige unitCard in der armyList nach oben gezogen werden. Dann kann man sich die zusätzliche Healthbar in dem Mockup sparen.
2. Den Text "D6 Mortal Wounds" kann wie ein Spaltenname über allen number-Feldern stehen. Das spart Platz, ist nicht redundant und sieht insgesamt ordentlich aus.
3. Der Text "Tap a unit to toggle; confirm when ready." kann entfallen.
4. Auf die Eingabe des exakten Würfelwurfes verzichten wir. Stattdessen bitte zwei Buttons mit "Explodes!" und einem passenden Wort, welches das Gegenteil beschreibt. 
5. Den Hinweisblock mit Resolved [number] - Explodes oder ... kann gerne darunter sein, sollte dann aber nicht in dem Kasten mit der Auswahlliste für die Einheiten erscheinen, der dann erscheinen soll. Da braucht es dann einen Text wie "[unitName] explodes. Every unit within [explosionRange] suffers [number] mortal wounds." Die Farbe des Hinweiskastens sollte blau sein. Bitte für die Auswahlliste KEINE CARD-ansicht verwenden. Belasse es so einfach wie in der UI für Heroic Intervention. 
6. Das Wort "DESTROYED" bitte in der bisherigen Farbe in der unitCard belassen.
7. Die GO für "auto_explode" sollte dann den spezifischen Namen der GO aus der YAML laden.

Ich hoffe, dass ich an alles gedacht habe. Hast du alles verstanden? Im Zweifelsfall bitte nachfragen, ich möchte nicht, dass du etwas implementierst, was wir am ende wieder mühsam umbauen müssen.

Koordinator-Vorschlag zu Korrekturwunsch 4: Gegenteil-Button-Wortlaut „Does not explode" (konsistent mit Grundannahme 4) — im S167-Planning bestätigen.