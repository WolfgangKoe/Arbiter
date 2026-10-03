# Domänen-Regeln — nicht offensichtliche 9E-Erkenntnisse für die Karte (ArbiterMap)

> Destillierte 9E-Regel-Gotchas, die für die Kartendomäne (`backend/app/domain/`) zählen —
> nach Muster des Altprojekts `docs/spec/rules_insights.md`. Jede Regel unten ist gegen
> `reference/rules/core_rules.txt` verifiziert, mit Zeilenangabe. **Nichts aus
> dem Gedächtnis** — wo eine in den Skizzen behauptete Zahl von der Kernregel abweicht, ist das
> hier ausdrücklich benannt statt stillschweigend übernommen.

## 1 · Unit Coherency — 2″

**Regel:** Eine Einheit mit mehr als einem Modell muss beim Aufstellen und nach jeder
Bewegungsart als eine Gruppe enden: jedes Modell innerhalb von 2″ horizontal und 5″ vertikal
von mindestens einem anderen Modell der eigenen Einheit. Ab sechs oder mehr Modellen muss
jedes Modell zu **zwei** anderen Modellen der Einheit in Kohärenz stehen, nicht nur einem.

**Fundstelle:** `core_rules.txt:434` (Regeldefinition, nicht die Verzeichniszeile `:134`): „A
unit that has more than one model must be set up and finish any sort of move as a
single group, with all models within 2" horizontally and 5" vertically of at least one other
model from their unit. While a unit has six or more models, all models must instead be within
2" horizontally and 5" vertically of at least two other models from their unit."

**Für die Karte relevant:** Kohärenzprüfung ist eine **Post-Move-Prüfung** (nach jeder
Bewegungsart: Movement, Charge, Fight-Pile-in/Consolidate), nicht laufend während des Drags.
Verletzt ein Zug die Kohärenz, kann er laut Kernregel nicht ausgeführt werden — die Domäne muss
das als `verletzt`-Ergebnis melden (§3 `architecture.md`), der Spieler kann per Override
trotzdem bestätigen — noch nicht verdrahtet, Item `022` (Hälfte 2).

**Implementierte Auslegung — Kurzform pro Modell, bewusst, bislang unnotiert:**
`backend/app/domain/rule_checks.py::check_coherency` prüft je Modell nur, ob es genug eigene
Nachbarn im 2″-Radius hat (einen unter sechs Modellen der Einheit, zwei ab sechs) — nicht, ob
die Einheit als Ganzes zusammenhängt, wodurch zwei Paare derselben Einheit, die 10″
auseinanderstehen, nach dieser Kurzform ebenfalls als kohärent gelten, obwohl sie keine
„single group" im Sinn von `core_rules.txt:434` bilden. Die vollständige Lesart würde
zusätzlich verlangen, dass der aus den paarweisen Nachbarschaften gebildete Zusammenhang die
**ganze** Einheit umfasst — jedes Modell über eine Kette von Nachbarn mit jedem anderen Modell
der Einheit verbunden, nicht nur paarweise mit dem nächstgelegenen.

## 2 · Engagement Range — 1″

**Regel:** Ein Modell ist innerhalb der Engagement Range eines gegnerischen Modells, wenn es
sich innerhalb von 1″ horizontal und 5″ vertikal davon befindet. Sind zwei gegnerische Modelle
gegenseitig in Engagement Range, gilt das auch für ihre Einheiten. Modelle dürfen nicht
innerhalb der Engagement Range gegnerischer Modelle aufgestellt werden.

**Fundstelle:** `core_rules.txt:447`: „Engagement Range represents the zone of threat that
models present to their enemies. While a model is within 1" horizontally and 5" vertically of
an enemy model, those models are within Engagement Range of each other. […] Models cannot be
set up within Engagement Range of enemy models."

**Nicht zu verwechseln mit:** der Kohärenzdistanz (2″, §1 oben) — Engagement Range ist die
Bedrohungszone zwischen **gegnerischen** Modellen, Kohärenz die Zusammenhaltsdistanz innerhalb
der **eigenen** Einheit. Zwei unabhängige Mechaniken mit unterschiedlichen Zahlenwerten.

**Formtreu, nicht gegen einen Bounding-Kreis:** Engagement Range (dieser Abschnitt) und Unit
Coherency (§1) messen Rand-zu-Rand gegen die tatsächliche Modell-Kontur — Kreis, Ellipse (ovale
Base) oder Rechteck (Hull) —, nicht gegen einen Umkreis um die große Halbachse der Kontur. Ein
Umkreis überschätzt die Reichweite quer zur Längsachse einer ovalen oder rechteckigen Kontur und
meldet dort Kontakt/Kohärenz, wo der wahre Rand noch entfernt ist (Item 068).

**Exakte Paar-Distanz (107., Item 068 AK-2):** `is_within_contours`/`contour_edge_distance_units`
rechnen inzwischen für **jedes** Konturpaar randgetreu exakt, auch Oval–Oval, Hull–Hull und
Oval–Hull — über eine Stützfunktions-Separation entlang der Trennachse beider Konturen
(`geometry.py`), kein Umkreis-Ersatz mehr. Die vormalige Einschränkung (Umkreis-Ersatz für eine
Seite eines Nicht-Kreis-Paars, Zweig E-F2) ist damit geschlossen.

**Sperr-/Nahkampfzone formtreu (107., Item 068 AK-3):** Die gesperrte Fläche für den Mittelpunkt
eines gezogenen Modells (§3 unten, `core_rules.txt:729`, BASE_CONTACT) und die davorliegende
Bedrohungszone (THREAT_ZONE, dieser Abschnitt) sind die Minkowski-Summe der Kontur des gezogenen
und der fremden Modell-Kontur — für THREAT_ZONE zusätzlich um die Engagement Range (1″)
aufgeweitet —, kein Kreis mehr um die Summe der Umkreisradien. Je Kontur trägt eine
punktsymmetrische Kernform bei: Kreis → nur ein Restradius, Ellipse → ein 64-Eck auf ihrem Rand,
Rechteck → seine vier Ecken. Die Summe zweier Kernformen ist die konvexe Hülle aller paarweisen
Eckensummen, ihr Restradius die Summe der beiden Restradien. Stehen sich zwei Kreise gegenüber,
läuft die Berechnung weiterhin über den alten, reinen Kreisweg (leeres Kernpolygon) — byte-gleiches
Verhalten zu vorher. Die Klemmung beim Ziehen (`last_allowed_point_before_blocked_discs`) hält am
Rand dieser Form an, nicht am Rand eines Kreises; der Server prüft dabei nur den **Endpunkt** des
Zugs gegen die aktiven Scheiben, nicht den Weg dorthin (core_rules.txt:729 „along any path").

**Gezeichnete Zone seit Brief 3 kleiner als die Prüffläche (108. Sitzung, Item 068 F-1 a):**
Was am Bildschirm als Nahkampfzone eingefärbt wird, ist seither nur noch die fremde Kontur
plus Engagement Range (1″), ohne den `moving`-Anteil der Minkowski-Summe oben
(`geometry.threat_zone_display_discs_for_model`) — sonst verschmelzen mehrere dicht
stehende fremde Modelle am Bildschirm zu einer gemeinsamen, zu großen Blase (Befund der
107. Sitzung). Die **Prüfung** (Klemmung beim Ziehen) läuft unverändert gegen die volle
Minkowski-Summe beider Konturen wie oben beschrieben — kein Regelunterschied, nur Anzeige.
Jede fremde Base bekommt ihre eigene Teilfläche; überlappende Teilflächen vereinen sich
(`fill-rule: nonzero`). Dafür bringt `geometry._offset_polygon_subpath` jedes Kern-Polygon vor dem
Versatz auf denselben Umlaufsinn — das rohe Konturpolygon läuft andersherum als das der
Minkowski-Summe, ohne Angleichung wanderte der 1″-Saum nach innen (109. Sitzung, Brief 4).

## 3 · Kampfberechtigung — ½″ (verifiziert, nicht 2″)

**Regel:** Beim Nahkampf können nur die Modelle einer Einheit angreifen, die entweder selbst
innerhalb der Engagement Range einer gegnerischen Einheit stehen, **oder** die innerhalb von
½″ eines anderen Modells der eigenen Einheit stehen, das seinerseits innerhalb von ½″ eines
gegnerischen Modells steht.

**Fundstelle:** `core_rules.txt:2001`: „When a unit makes close combat attacks, only the
models in that unit that are either within Engagement Range of an enemy unit, or that are
within ½" of another model from their own unit that is itself within ½" of an enemy unit, can
fight." Bestätigt in der direkt folgenden Kurzfassung derselben Zeile: „A model can fight if it
is in Engagement Range of an enemy unit. A model can fight if it is within ½" of another model
from their own unit that is within ½" of an enemy unit."

**Ausdrücklich zur Klarstellung (Stakeholder-Auftrag):** Die in einer Stakeholder-Skizze
(`unitshape and modeldistribution.pdf`) mit „half an inch" beschriftete Kampf-Kettendistanz ist
**korrekt** — das ist genau dieser ½″-Wert aus `core_rules.txt:2001`, keine 2″. Die 2″ aus §1
sind die Unit-Coherency-Distanz, eine andere Mechanik mit anderem Zweck (Zusammenhalt der
Einheit vs. Kampfberechtigungs-Kette). Diese Verwechslung wurde im Skizzen-Extrakt als offene
Frage geführt (`interaction_map_extract.md` Abschnitt 8, Punkt 2) und ist damit geklärt — nicht
erneut anzweifeln.

## 4 · Messung erfolgt pro Modell, nicht vom Einheiten-Mittelpunkt

**Regel:** Alle Distanzen werden in Zoll zwischen den **nächstgelegenen Punkten der Bases**
der zu messenden Modelle gemessen. Hat ein Modell keine Base (viele Fahrzeuge), wird zum
nächstgelegenen Punkt des Modells selbst gemessen — das heißt „zum Hull des Modells messen".

**Fundstelle:** `core_rules.txt:463` (Überschrift „Measuring Distances") und direkt darunter,
`core_rules.txt:464`: „Distances are measured in inches (") between the closest points of the
bases of the models you're measuring to and from. If a model does not have a base, such as is
the case with many vehicles, measure to the closest point of any part of that model; this is
called measuring to the model's hull. You can measure distances whenever you wish."

**Für die Karte relevant (direkte Konsequenz):** Reichweiten, Kohärenz-, Engagement- und
Kampfberechtigungsprüfungen laufen **pro Modell-Paar**, nicht zwischen abstrakten
Einheiten-Mittelpunkten. Bei einer Mehrmodell-Einheit hat *jedes* Modell seinen eigenen
Distanz-/Reichweitenkreis; die für die Einheit geltende Aussage („ist die Zieleinheit in
Reichweite") ist die **Vereinigung** aller Einzelmodell-Prüfungen — deckt sich mit der belegten
Skizzen-Beobachtung überlappender Radiuskreise (siehe `design_system.md` §6) und mit der
Kernregel-Definition von „within"/„wholly within" unten (§5), die ebenfalls modellweise
definiert ist. Der „nächstgelegene Punkt der Base" ist der Rand der tatsächlichen Kontur — bei
einer ovalen oder rechteckigen Base/Hull nicht der Rand eines Umkreises um sie herum (Item 068,
Beleg §2 oben).

## 5 · „Within" vs. „wholly within" — Modell- und Einheitenebene

**Regel:** Eine Regel, die von Modellen „within" (innerhalb) einer Distanz spricht, gilt schon,
wenn irgendein Teil der Base (oder des Hull) innerhalb der angegebenen Distanz liegt. „Wholly
within" gilt erst, wenn die **gesamte** Base (bzw. der gesamte Hull) innerhalb liegt. Für
Einheiten gilt dieselbe Unterscheidung entsprechend aggregiert: „within" = irgendein Modell der
Einheit ist within; „every model in that unit is within" = jedes Modell einzeln within; „wholly
within" = jedes Modell wholly within.

**Fundstelle:** Appendix, `rules_appendix.txt:951`: „A model is wholly within a specified
distance if every part of its base (or hull) is within that distance. A unit is wholly within
if every model in that unit is [wholly within]." Und `rules_appendix.txt:955`: „A model is
within a specified distance if any part of its base (or hull) is within that distance. A unit
is within if any model in that unit is [within]." (Identische Formulierung auch im
Grundregelwerk selbst unter „Within and Wholly Within", `core_rules.txt:471–474`.)

**Für die Karte relevant:** Die Domäne braucht für Distanzprüfungen zwei unterscheidbare
Prädikate — `is_within(model, distance, target)` (irgendein Teil der Base/des Hull) und
`is_wholly_within(model, distance, target)` (die gesamte Base/der gesamte Hull) — sowie deren
Aggregation auf Einheitenebene in beiden belegten Varianten (irgendein Modell / jedes Modell
einzeln / jedes Modell wholly). Eine reine Mittelpunkt-zu-Mittelpunkt-Distanz erfüllt keines
dieser Prädikate korrekt und würde insbesondere bei großen Bases (Fahrzeuge, Monster) falsche
Ergebnisse liefern. Beide Prädikate entscheiden auf **quadrierten Ganzzahl-Distanzen** — die
Positionen liegen als Ganzzahl-Grid-Einheiten vor, nicht als Float
([`interaction_map.md`](interaction_map.md) §2).

## 6 · Messung bei Modellen ohne Base — „Hull" statt „Base"

**Regel:** Für Modelle ohne physische Base (insbesondere viele Fahrzeug-Modelle) wird nicht zur
Base, sondern zum nächstgelegenen Punkt eines beliebigen Teils des Modells gemessen — das
Regelwerk nennt das „measuring to the model's hull". Dieselbe Base-oder-Hull-Formulierung zieht
sich durch die within/wholly-within-Definition (§5) und die Konturprüfung bei Sichtlinien-Regeln
(`core_rules.txt:2543`, dort für Terrain-Traits, für ArbiterMap nicht relevant — Gelände ist
laut `docs/genesis/context.md` §2 bewusst nicht Teil des PoC).

**Fundstelle:** `core_rules.txt:464` (siehe Zitat in §4) und `rules_appendix.txt:951+955`
(siehe Zitat in §5) — beide verwenden durchgängig „base (or hull)".

**Korrektur zum Ausgangsauftrag:** In den lokalen Regeltexten (`core_rules.txt`,
`rules_appendix.txt`) kommt der Begriff „Hovering" bzw. „hover" an keiner Stelle vor — eine
Volltextsuche über beide Dateien ergibt null Treffer. Die für die Karte relevante, tatsächlich
belegte Regel ist die allgemeinere Base-oder-Hull-Unterscheidung aus §4–§5: **jedes** Modell
ohne Base (nicht nur eine als „hovering" bezeichnete Untergruppe) misst zum Hull statt zur
Base. Für die Domäne bedeutet das: Ein Modell-Datensatz braucht ein Flag
„hat_base: bool" (bzw. äquivalent eine Unterscheidung Base-Radius vs. Hull-Kontur); es gibt
keine dritte, gesondert zu behandelnde „Hovering"-Kategorie in der Kernregel. Basegrößen selbst
liegen laut `docs/genesis/research/basesize_probe.md` ohnehin nicht vollständig in den Wahapedia-Dumps vor
und werden für den PoC manuell gepflegt (`docs/genesis/context.md` §5).

**Abstand zwischen zwei Modellen — nächster Punkt zu nächstem Punkt (Item 035, 81. Sitzung):**
Gemessen wird zwischen den nächstgelegenen Punkten der Base-Kanten (`core_rules.txt:464` „between
the closest points of the bases"; `:467` „closest distance between bases (or hulls)"); ohne Base
gilt der Hull wie oben. **Runde Base:** Mittelpunktabstand minus beide Radien als quadrierter
Ganzzahlvergleich — die bestehende Semantik von `geometry.py::is_within`. **Ovale Base (zwei
Halbachsen):** kein geschlossener Ganzzahl-Ausdruck (Lotfußpunkt = Gleichung vierten Grades);
gerechnet per **Bisektion auf dem Parameterwinkel**, Höchstfehler **0,0011 Grid-Einheiten** gegen
die Float-Referenz über 189 Lagen (`tests/backend/test_baseform_naeherung.py`), Ergebnis Ganzzahl
in Grid-Einheiten ([ADR-0007](../organisation/decisions/0007-positions-grid-hundertstel-zoll.md));
Funktion `backend/app/domain/base_shape.py::ellipse_edge_distance_units`, Ellipse achsenparallel
im Ursprung. *Vorbehalt:* Verschiebung und Drehung (Blickrichtung) leistet der Aufrufer per
Koordinatentransformation, nicht die Funktion.

## 7 · Was hier bewusst nicht steht

- Advance-/Charge-Wurf-Mechanik (2W6, Ring-Vorzeichnung) — das ist UI-/Interaktionsverhalten,
  siehe [`design_system.md`](design_system.md) §5, nicht Domänenregel.
- Volle Schuss-/Nahkampf-Auflösungssequenz (Hit/Wound/Save/Damage) — gehört, sobald die volle
  Spiellogik folgt (`docs/genesis/context.md` §1), in eine eigene Prozess-Spec analog zum Altprojekt
  `docs/spec/processes.md`; für den Karten-PoC nicht Teil dieses Dokuments.
- Aura-Reichweiten-Sonderfälle einzelner Fraktionen — Domänenregeln in diesem Dokument sind
  bewusst nur die kernregelweiten, generischen Distanzmechaniken (INV-4,
  `architecture_invariants.md`: keine Fraktionslogik im Backend).
- **Positionsquantisierung und Distanzmetrik** (Grid-Auflösung 0,01″, euklidische Norm,
  quadrierte Ganzzahlvergleiche) — das ist eine **Repräsentationsentscheidung**, keine 9E-Regel,
  und steht deshalb nicht hier, sondern in [`interaction_map.md`](interaction_map.md) §2 mit
  Begründung in
  [ADR-0007](../organisation/decisions/0007-positions-grid-hundertstel-zoll.md). Die Regelwerte
  selbst (2″, 1″, ½″) sind davon unberührt — sie werden nur in Einheiten umgerechnet
  (2″ = 200 Einheiten).
- **Tiefe und Form der Aufstellungszone im PoC** (9″-Band, wahlweise quer oder längs) — das
  Regelwerk legt Zonen **je Mission als Grafik** fest (`core_rules.txt:2182`) und kennt keine
  allgemeine Zahl. Die 9″ sind eine Setzung des Stakeholders für den PoC, keine Regelzahl, und
  stehen deshalb in [`interaction_map.md`](interaction_map.md), nicht hier. Was *regelseitig* für
  das Aufstellen gilt, steht in §8.

## 8 · Aufstellung — „wholly within" auf eine Fläche statt auf eine Distanz

**Regel:** Modelle werden **wholly within** der eigenen Aufstellungszone aufgestellt — die volle
Base, nicht ihr Mittelpunkt. Beim Aufstellen gelten zusätzlich zwei Schranken: Kohärenz (§1) muss
schon im Moment des Aufstellens gehalten werden, und kein Modell darf in Engagement Range (§2)
eines gegnerischen Modells gesetzt werden. Modelle einer Einheit, die sich nicht regelkonform
unterbringen lassen, **gelten als zerstört** — die Regel lehnt nicht die Aufstellung ab, sie
vernichtet die überzähligen Modelle.

**Fundstelle:** `core_rules.txt:2322` („Models must be set up wholly within their own deployment
zone.") · `core_rules.txt:2327` („… their base must still be wholly within their deployment zone")
· `core_rules.txt:434` und die Kurzfassung `:444-445` (Kohärenz beim Aufstellen: „must be
set up **and** finish any sort of move … in unit coherency"; ab sechs Modellen zwei Nachbarn statt
einem) · `core_rules.txt:447` und `:450` („Models cannot be set up within Engagement Range of enemy
models.") · `core_rules.txt:441` („any models that cannot be set up are considered to have been
destroyed") — dieser Satz steht wörtlich im Absatz über Modelle, die **während der Schlacht** zu
einer Einheit hinzukommen, nicht im Absatz „4. DEPLOY FORCES" (`:2321–2323`), der keine
entsprechende Formulierung enthält; die Übertragung auf die Aufstellung selbst ist eine Analogie,
keine wörtliche Aufstellungsregel — Auslegungsfrage offen in Item
[`028`](../../steering/backlog/items/028-zerstoerte-modelle-verschwinden.md).

**Base statt Kontur — und der Überhang großer Modelle:** `:2322` sagt nur „wholly within their own
deployment zone", und „wholly within" heißt nach §5 ausdrücklich Base **oder** Hull. Dass für die
Aufstellungszone die **Base** entscheidet, steht wörtlich erst in `core_rules.txt:2327`: Große
Modelle — typischerweise `AIRCRAFT` — mit Flügeln oder Aufbauten, die deutlich über ihre Base
hinausragen, „can overhang a deployment zone if it is not possible to set them up otherwise …, but
when setting them up on the battlefield their base must still be wholly within their deployment
zone." Die Zonenkante ist damit die weichere der beiden Grenzen: Über sie darf die Kontur eines
solchen Modells ragen, über die **Feldkante** dagegen kein Teil des Modells, die Base eingeschlossen
(`core_rules.txt:729`; `:2327` nennt genau diesen Unterschied als Anlass der Klarstellung). Für die
Karte heißt das: Die Zonenprüfung klemmt auf dem Base-Radius und nicht auf einer Hüllkontur — die
Überhang-Erlaubnis ist damit schon eingelöst und braucht keine eigene Ausnahme im Code.

**Für die Karte relevant:** Das „wholly within" aus §5 wird hier auf eine **Fläche** angewandt, nicht
auf eine Distanz. Der Bereich gültiger Modell-**Mittelpunkte** ist deshalb nicht die Zone selbst,
sondern die um den Base-Radius auf allen vier Seiten eingerückte Zone — dieselbe Konstruktion, die
`geometry.clamp_position_to_field` schon für die Feldkante benutzt. Ist die Zone für einen Radius zu
flach, gibt es keine gültige Stelle: Funktionen, die eine Stelle *konstruieren*, melden das als
Fehler statt ein leeres Ergebnis zu liefern; das Prädikat „liegt die volle Base in der Zone?"
antwortet darauf schlicht mit Nein. „Eigene" Zone heißt außerdem: die beiden Zonen einer Form dürfen
einander nicht überlappen, sonst gehörte eine Stelle zu beiden — eine Zonentiefe, die für zwei Zonen
nebeneinander zu groß ist, wird deshalb gemeldet und nicht still gekürzt. Die Kohärenzschranke
macht die Formation zur Domänenfrage statt zur Darstellungsfrage: Der Mittenabstand einer Reihe
ergibt sich aus Base-Radius und Modellzahl, und ab sechs Modellen entscheidet der **übernächste**
Nachbar, nicht der direkte. Implementiert in `backend/app/domain/deployment.py`.

**Engagement Range beim Aufstellen — geometrisch, nicht code-erzwungen:** Die
Engagement-Range-Schranke aus dem ersten Absatz prüft der Aufstellungs-Endpunkt heute
nicht selbst; sie hält trotzdem, weil die beiden Zonen einer Form bei der heutigen
Zonentiefe (9″) an gegenüberliegenden Feldkanten liegen. Der Mindestabstand ihrer
Ränder — 26″ bei `VERTICAL` (44″-Feldbreite), 42″ bei `HORIZONTAL` (60″-Feldhöhe) —
überschreitet die 1″-Schwelle (`ENGAGEMENT_RANGE_UNITS`) um ein Vielfaches, selbst mit
dem größten Katalog-Base auf beiden Seiten: Die Radius-Anteile heben sich beim
Rand-zu-Rand-Abstand exakt weg, nur Zonentiefe und Feldmaß entscheiden. Das ist eine
geometrische, keine geprüfte Garantie — wächst `DEPLOYMENT_ZONE_DEPTH_INCHES` oder
schrumpft das Feld, kann sie lautlos brechen, ohne dass ein Endpunkt-Check das
auffinge. Ein Test bewacht deshalb die Ungleichung aus den Konstanten:
`tests/backend/domain/test_deployment.py::test_opposing_zones_make_an_engagement_range_breach_geometrically_impossible`
wird rot, statt dass die Annahme still bricht.
