# Gefechtsoptionen-Klassifikation

> Stand S131 (2026-07-09). Quelle für [`../spec/design_system.md`](../spec/design_system.md)
> §6.2 (Orte-Zuordnung der GO-Karte). Ursprünglich als Recherche-Auftrag S131 Aufgabe 2
> erstellt, jetzt dauerhafte Referenz — bei neuen/geänderten Fraktions-Stratagems hier
> nachziehen.

Grundlage für das Design-System: **UI-unabhängige** Einteilung aller Gefechtsoptionen (GOs) —
Stratagems + vergleichbare optionale Regeln. Verworfenes Vorkonzept „reaktive Box / Inline-Reroll /
proaktiver Tab" gemischt Kategorie und Effekt; Re-Roll ist ein **Effekt**, kein Kategorie-Bucket
(ein Re-Roll kann proaktiv *oder* reaktiv ausgelöst werden — siehe Command Re-Roll vs. Lurking
Murderers unten). Wichtig: Die App würfelt nicht — sie kann nur **erinnern**, dass eine Regel jetzt
greift; das Würfeln/Eintragen bleibt Tisch-Sache.

## 1. Klassifikations-Vorschlag — drei orthogonale Achsen

**(a) Wann entscheidbar — proaktiv / reaktiv.** Proaktiv = der Spieler bestimmt Zeitpunkt *und*
Ziel selbst, ohne auf ein Ereignis außerhalb seiner Kontrolle zu warten (eigene Phase, „vor der
Schlacht", eigene Einheitenaktivierung). Reaktiv = die Option ist nur als Antwort auf ein
Ereignis nutzbar, das der Spieler nicht selbst terminiert (gegnerische Deklaration, eigenes
zerstörtes Modell, ein bereits gefallener Wurf, ein unmittelbar bevorstehender Test mit
ungewissem Ausgang). Diese Achse bestimmt, ob die App die Option als normale Auswahlliste in der
Phase zeigen kann oder aktiv **unterbrechen/erinnern** muss.

**(b) Entscheidungs-Moment — vor_wurf / nach_wurf / bei_ereignis / phasenweit / spielweit.**
Verfeinert (a) um den *Anlass*: Re-Roll-artige Optionen hängen an einem konkreten Wurf (davor
oder danach); viele Fraktions-Stratagems hängen an einem Ereignis, das die aktive Einheit selbst
auslöst („wenn Einheit X zum Schießen/Kämpfen ausgewählt wird" — technisch proaktiv, aber ein
enges Zeitfenster, kein freier Phasen-Zeitraum); andere gelten für die ganze Phase oder die ganze
Partie. `bei_ereignis` ist damit der größte Topf — bewusst so belassen, weil „welches Ereignis"
stark fraktionsspezifisch ist (siehe YAML `event`-Feld, wo vorhanden).

**(c) Effekt-Typ** (der eigentlich verworfene Kategorie-Kandidat, hier korrekt als *Effekt* statt
Kategorie): Re-Roll, Modifier (±X auf Wurf/Statur), Auto-Ergebnis (Wurf entfällt/wird erzwungen),
Zusatz-Aktion (Bewegung/Schuss/Angriff außer der Reihe, inkl. Reanimate als Tisch-Wurf-Aktion),
Zustands-Flag (Keyword/Fähigkeit/Relikt/Restriktion gewährt oder entzogen), **Direkter Schaden**
(Mortal Wounds — eigene Kategorie ergänzt, passt in keinen der vier Wahapedia-Vorschläge sauber).

Die drei Achsen sind unabhängig: z. B. Command Re-Roll = reaktiv/nach_wurf/Re-Roll, Lurking
Murderers = proaktiv/phasenweit/Re-Roll — gleicher Effekt, andere Achsen a+b.

## 2. Klassifikations-Tabelle (95 GOs: 7 Core + 60 Necrons + 28 Orks)

Adeptus Custodes hat keine `stratagems.yaml` (nur `faction_abilities.yaml`/Ka'tahs, separat
kategorisiert in `docs/spec/faction_abilities.md`) — daher hier nicht enthalten.

| Name | Fraktion | CP | (a) Wann | (b) Moment | (c) Effekt | Phase |
|---|---|---|---|---|---|---|
| Command Re-Roll | Shared | 1 | reaktiv | nach_wurf | Re-Roll | move+psyc+shoo+char+figh |
| Cut Them Down | Shared | 1 | reaktiv | bei_ereignis | Direkter Schaden | movement |
| Desperate Breakout | Shared | 2 | proaktiv | phasenweit | Zusatz-Aktion | movement |
| Emergency Disembarkation | Shared | 1 | reaktiv | bei_ereignis | Zusatz-Aktion | any |
| Fire Overwatch | Shared | 1 | reaktiv | bei_ereignis | Zusatz-Aktion | charge |
| Counter-Offensive | Shared | 2 | reaktiv | bei_ereignis | Zusatz-Aktion | fight |
| Insane Bravery | Shared | 2 | reaktiv | vor_wurf | Auto-Ergebnis | morale |
| Hand of the Phaeron | Necrons | 2 | proaktiv | spielweit | Zustands-Flag | before_battle |
| Dynastic Heirlooms | Necrons | 1 | proaktiv | spielweit | Zustands-Flag | before_battle |
| Rarefied Nobility | Necrons | 1 | proaktiv | spielweit | Zustands-Flag | before_battle |
| Strange Echoes | Necrons | 1 | proaktiv | phasenweit | Zustands-Flag | command |
| The Deathless Arise | Necrons | 1 | proaktiv | phasenweit | Modifier | command |
| Reconstitution Protocols | Necrons | 1 | proaktiv | phasenweit | Modifier | command |
| Stellar Alignment Protocol | Necrons | 1 | proaktiv | phasenweit | Modifier | command |
| Dimensional Corridor | Necrons | 1 | proaktiv | phasenweit | Zusatz-Aktion | movement |
| Burrowing Nightmares | Necrons | 1 | proaktiv | phasenweit | Zusatz-Aktion | movement |
| Prismatic Dimensional Breach | Necrons | 1 | proaktiv | phasenweit | Zusatz-Aktion | movement |
| Dimensional Destabilisation | Necrons | 1 | proaktiv | bei_ereignis | Zusatz-Aktion | movement |
| Aetheric Interception | Necrons | 1 | reaktiv | bei_ereignis | Zusatz-Aktion | movement |
| Enslaved Protectors | Necrons | 1 | reaktiv | phasenweit | Zustands-Flag | charge |
| Techno-Oracular Targeting | Necrons | 1 | proaktiv | vor_wurf | Auto-Ergebnis | shooting |
| Extermination Protocols | Necrons | 2 | proaktiv | bei_ereignis | Re-Roll | shooting |
| Fractal Targeting | Necrons | 1 | proaktiv | phasenweit | Modifier | shooting |
| Disintegration Capacitors | Necrons | 1 | proaktiv | bei_ereignis | Auto-Ergebnis | shooting |
| Malevolent Arcing | Necrons | 1 | proaktiv | bei_ereignis | Direkter Schaden | shooting |
| Relentless Onslaught | Necrons | 1 | proaktiv | bei_ereignis | Modifier | shooting |
| Reanimation Prioritisation | Necrons | 2 | reaktiv | bei_ereignis | Zusatz-Aktion | shooting |
| Solar Pulse | Necrons | 1 | proaktiv | phasenweit | Zustands-Flag | shooting |
| Atavistic Instigation | Necrons | 1 | proaktiv | bei_ereignis | Direkter Schaden | shooting |
| Shield-Piercer Projectors | Necrons | 1 | proaktiv | bei_ereignis | Zustands-Flag | shooting |
| Flensing Capacitors | Necrons | 1 | proaktiv | bei_ereignis | Auto-Ergebnis | shooting |
| Storm of Flensing Blades | Necrons | 2 | proaktiv | phasenweit | Zusatz-Aktion | fight |
| Judgement of the Triarch | Necrons | 1 | proaktiv | bei_ereignis | Modifier | shoo+figh |
| Eternal Protectors | Necrons | 1 | proaktiv | phasenweit | Modifier | fight |
| Disruption Fields | Necrons | 1 | proaktiv | bei_ereignis | Modifier | fight |
| Whirling Onslaught | Necrons | 1 | reaktiv | bei_ereignis | Modifier | any |
| Entropic Strike | Necrons | 2 | proaktiv | bei_ereignis | Zustands-Flag | fight |
| Self-Destruction | Necrons | 1 | proaktiv | bei_ereignis | Direkter Schaden | fight |
| Resurrection Protocols (Infantry) | Necrons | 1 | reaktiv | bei_ereignis | Zusatz-Aktion | any |
| Resurrection Protocols (Character) | Necrons | 2 | reaktiv | bei_ereignis | Zusatz-Aktion | any |
| Quantum Deflection | Necrons | 1 | reaktiv | bei_ereignis | Zustands-Flag | any |
| Curse of the Phaeron | Necrons | 1 | reaktiv | bei_ereignis | Auto-Ergebnis | any |
| Shadows of Drazak | Necrons | 1 | reaktiv | bei_ereignis | Modifier | any |
| Revenge of the Doomstalker | Necrons | 2 | reaktiv | bei_ereignis | Zusatz-Aktion | any |
| Rapid Reanimation | Necrons | 1 | reaktiv | nach_wurf | Modifier | any |
| Talent for Annihilation | Necrons | 1 | proaktiv | bei_ereignis | Direkter Schaden | shooting |
| Translocation Crypt | Necrons | 1 | proaktiv | spielweit | Zustands-Flag | before_battle |
| Reclaim a Lost Empire | Necrons | 1 | proaktiv | phasenweit | Zustands-Flag | shooting |
| Blood Rites | Necrons | 1 | proaktiv | bei_ereignis | Modifier | fight |
| Methodical Destruction | Necrons | 2 | proaktiv | phasenweit | Modifier | shooting |
| Empyric Damping | Necrons | 1 | reaktiv | bei_ereignis | Zustands-Flag | psychic |
| Exalted Cryptek | Necrons | 1 | proaktiv | spielweit | Zustands-Flag | before_battle |
| The Swarm Descends | Necrons | 1 | proaktiv | spielweit | Zustands-Flag | before_battle |
| Overkill Protocols | Necrons | 1 | proaktiv | phasenweit | Modifier | command |
| Aggression Overrides | Necrons | 1 | proaktiv | phasenweit | Modifier | command |
| Stalking Annihilator | Necrons | 1 | proaktiv | phasenweit | Zustands-Flag | shooting |
| Hyperdense Particle Beams | Necrons | 1 | proaktiv | bei_ereignis | Modifier | shooting |
| Enhanced Gloom Prism | Necrons | 1 | reaktiv | vor_wurf | Modifier | psychic |
| Canoptek Overdrive | Necrons | 1 | reaktiv | bei_ereignis | Zusatz-Aktion | fight |
| A Moment of Clarity | Necrons | 2 | proaktiv | phasenweit | Zustands-Flag | command |
| Canoptek Reinforcement | Necrons | 1 | proaktiv | phasenweit | Zusatz-Aktion | movement |
| Swift Dismemberment | Necrons | 1 | proaktiv | phasenweit | Zustands-Flag | charge |
| Weaponised Bodies | Necrons | 2 | proaktiv | bei_ereignis | Direkter Schaden | charge |
| Efficient Disintegration | Necrons | 2 | reaktiv | bei_ereignis | Modifier | any |
| Hyperphase Impalement | Necrons | 1 | proaktiv | bei_ereignis | Zustands-Flag | fight |
| Lurking Murderers | Necrons | 1 | proaktiv | phasenweit | Re-Roll | fight |
| Murderous Demise | Necrons | 2 | reaktiv | bei_ereignis | Zusatz-Aktion | fight |
| Big Boss | Orks | 1 | proaktiv | spielweit | Zustands-Flag | before_battle |
| Extra Gubbinz | Orks | 1 | proaktiv | spielweit | Zustands-Flag | before_battle |
| Blitz Brigade | Orks | 1 | proaktiv | spielweit | Zustands-Flag | before_battle |
| Dread Waaagh! | Orks | 1 | proaktiv | spielweit | Zustands-Flag | before_battle |
| Kult of Speed | Orks | 1 | proaktiv | spielweit | Zustands-Flag | before_battle |
| Stompa Mob | Orks | 1 | proaktiv | spielweit | Zustands-Flag | before_battle |
| Careen! | Orks | 1 | reaktiv | bei_ereignis | Zusatz-Aktion | any |
| Breakin' Heads | Orks | 2 | reaktiv | bei_ereignis | Auto-Ergebnis | morale |
| Orks is Never Beaten | Orks | 2 | reaktiv | bei_ereignis | Zusatz-Aktion | fight |
| Get Stuck In, Ladz! | Orks | 1 | proaktiv | bei_ereignis | Zusatz-Aktion | fight |
| Hit 'Em Harder | Orks | 2 | proaktiv | bei_ereignis | Modifier | fight |
| Gun Crazy Show Offs | Orks | 2 | proaktiv | phasenweit | Zusatz-Aktion | shooting |
| Ramming Speed | Orks | 2 | proaktiv | bei_ereignis | Direkter Schaden | charge |
| Tough as Squig-Hide | Orks | 2 | reaktiv | bei_ereignis | Zustands-Flag | any |
| Showin' Off | Orks | 1 | proaktiv | bei_ereignis | Modifier | shooting |
| Ded Sneaky | Orks | 1 | proaktiv | phasenweit | Zusatz-Aktion | movement |
| Wreckaz | Orks | 2 | proaktiv | phasenweit | Modifier | shoo+figh |
| Drive By Dakka | Orks | 1 | proaktiv | phasenweit | Zusatz-Aktion | shooting |
| Get Da Loot | Orks | 1 | proaktiv | phasenweit | Zustands-Flag | command |
| Unbridled Carnage | Orks | 2 | proaktiv | phasenweit | Modifier | fight |
| Mystic Chanting | Orks | 1 | reaktiv | phasenweit | Zustands-Flag | psychic |
| Opening Salvo | Orks | 1 | proaktiv | bei_ereignis | Modifier | shooting |
| Krush 'Em | Orks | 1 | proaktiv | bei_ereignis | Modifier | fight |
| Hold On, Boyz! | Orks | 2 | proaktiv | phasenweit | Zusatz-Aktion | movement |
| Kustom Ammo | Orks | 2 | proaktiv | phasenweit | Zusatz-Aktion | shooting |
| Turbo-Boostas | Orks | 2 | proaktiv | phasenweit | Zusatz-Aktion | movement |
| Stomp, Stomp, Stomp! | Orks | 1 | proaktiv | phasenweit | Direkter Schaden | fight |
| Stompa-Porta | Orks | 4 | proaktiv | spielweit | Zusatz-Aktion | before_battle |

## 3. Befunde für das Design-System

**Größte Cluster** (von 95): `proaktiv/phasenweit/Zusatz-Aktion` (12), `reaktiv/bei_ereignis/
Zusatz-Aktion` (12), `proaktiv/spielweit/Zustands-Flag` (12 — alle „vor der Schlacht"-Grants),
`proaktiv/phasenweit/Modifier` (10), `proaktiv/bei_ereignis/Modifier` (9). Zusammen ~57 % aller
GOs. Design-Konsequenz: drei UI-Grundmuster decken den Großteil ab — (1) „vor der Schlacht"-Liste
(einmalig, keine Zeitdruck-UI nötig), (2) „Einheit wählen → Effekt bis Phasenende" (phasenweit,
egal ob proaktiv oder reaktiv terminiert), (3) „Ereignis X ist eingetreten → jetzt entscheiden"
(bei_ereignis, braucht eine Erinnerungs-/Prompt-Komponente).

**GOs, die in keine Achse sauber passen:** keine — alle 95 ließen sich auf (a)/(b)/(c) abbilden.
Einzige Erweiterung war Achse (c) um „Direkter Schaden" (Mortal Wounds, 8×) — passte in keine der
vier Wahapedia-Vorschlagskategorien (Re-Roll/Modifier/Auto-Ergebnis/Zusatz-Aktion/Zustands-Flag),
weil es kein Charakteristik-Modifier ist, sondern ein eigener Tisch-Würfelwurf (z. B. „1 W6 je
Modell, bei 6 = 1 Mortal Wound"). Reanimate (3×, Necron-Modelle zurückholen) wurde bewusst unter
Zusatz-Aktion gefasst statt eigener Kategorie — strukturell wie „zusätzliche Handlung mit
Tisch-Würfelergebnis", nicht wie Direkter Schaden (kein Gegner-Ziel).

**„Nach dem Wurf am Tisch"-Fenster (App sieht das Ergebnis nicht):** 11 von 95 GOs hängen an
einem konkreten Einzelwurf (`vor_wurf`/`nach_wurf` ODER Effekt-Typ Re-Roll/Auto-Ergebnis) —
Command Re-Roll, Insane Bravery, Techno-Oracular Targeting, Extermination Protocols,
Disintegration Capacitors, Flensing Capacitors, Curse of the Phaeron, Rapid Reanimation,
Enhanced Gloom Prism, Lurking Murderers, Breakin' Heads. Für diese kann die App bestenfalls
**erinnern und den Ergebnis-Eintrag anbieten** — nie selbst würfeln oder prüfen. Die übrigen 84
sind Buffs/Grants/Restriktionen, die die App vollständig aus YAML-Feldern ableiten und als
Zustand darstellen kann.

**Datenqualitäts-Befund (Stichprobe):** `Extermination Protocols` (Necrons) ist in
`wahapedia_necrons/stratagems.txt` ein **Doppel-Stratagem** (Reroll-Klausel + separate
Damage-roll-Klausel „+1 auf Damage bei Gauss-Waffen"); die lokale YAML erfasst nur die
Reroll-Klausel. Ändert die Achsen-Einordnung hier nicht (Kern-Effekt bleibt Re-Roll), ist aber
ein Beleg für den bekannten Gotcha „YAML kann unvollständig sein" — relevant, falls das
Design-System später die volle Regeltext-Darstellung pro GO anzeigen soll (dann müsste die YAML
nachgezogen werden, kein Scope dieser Aufgabe).

**Stichproben-Verifikation gegen Wahapedia-Text** (Selbstprüfung, 6 statt geforderter 5): Command
Re-Roll + Insane Bravery gegen `core_rules.txt:3124-3267`; Lurking Murderers, Breakin' Heads,
Careen!, Extermination Protocols gegen `wahapedia_necrons/stratagems.txt` bzw.
`wahapedia_orks/stratagems.txt` — alle sechs inhaltlich deckungsgleich (bis auf die oben genannte
Extermination-Protocols-Lücke).
