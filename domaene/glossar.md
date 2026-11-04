# Glossar

Begriff | englischer Regelbegriff | Code-Bezeichner | Definition
---|---|---|---
Abstand | distance | abstand | Kürzeste waagrechte Entfernung zwischen den *Bases* zweier *Modelle*, in *Zoll* (`core_rules.txt:464`); ohne Gelände stehen alle *Modelle* auf einer Ebene (`domaene/ziel.md`). *Bases*, die sich berühren oder *überdecken*, haben den *Abstand* 0.
am Zug | – | amZug | Zustand des einen *Spielers*, dessen Zug in der laufenden *Schlachtrunde* läuft; vor dem *ersten Zug* und nach der *Schlacht* ist es keiner (`core_rules.txt:639`).
an der Reihe | – | anDerReihe | Zustand des einen *Spielers*, der als Nächster eine *Einheit* aufstellt; zeitweise ist es keiner.
Angebot | – | Angebot | Was Arbiter nach BEW-8.3 bis zur nächsten Handlung zum *gemeinsam übergehen* bereithält: die *Modelle* der *Ebene*, das gezogene *Modell* und den Punkt des Loslassens (BEW-8.3, 8.4).
Anteile | – | Anteile | Je Anhalten nach BEW-3.1, 6.1 und 6.2 der Anteil der geraden Strecke beim Ziehen, bis zu dem die gezogenen *Modelle* kämen; 1 ist die ganze Strecke, von denen unter 1 gilt der kleinste (BEW-6.3).
Armee | army | Armee | Alle *Modelle* unter dem Befehl eines *Spielers*, in *Einheiten* gegliedert (`core_rules.txt:305`, `:321`, `:420`).
Armeeliste | – | Armeeliste | Spalte neben der *Karte* mit den nicht *aufgestellten* *Einheiten* eines *Spielers*, in der er eine per Klick auswählt; kein Ziel zum Hineinziehen. Jeder *Spieler* hat eine (Anliegen 145 F1 A, 2220 F4 A, 2221 F1 A, Vorbild `Arbiter-old/src/uiLayout/armyList.py`).
aufgestellt | deployed | aufgestellt | Zustand einer *Einheit*, für die *Aufstellen der Einheit beenden* gelungen ist (`core_rules.txt:2322`).
Aufstellen der Einheit beenden | – | aufstellenDerEinheitBeenden | Handlung, mit der die *Spieler* die *Einheit in Aufstellung* abschließen.
Aufstellung | deploy forces | Aufstellung | Schritt 4 der Mission Only War: Die *Spieler* stellen abwechselnd je eine *Einheit* auf, bis beide alle aufgestellt haben (`core_rules.txt:2322`).
Aufstellungskarte | deployment map | Aufstellungskarte | Karte einer *Mission* mit ihren *Aufstellungszonen* (`core_rules.txt:2182`); einen Namen hat eine Zone nur, wenn die Karte ihn zeigt, etwa die des Angreifers (`open_play.txt:235`, `narrative_play.txt:2001`).
Aufstellungszone | deployment zone | Aufstellungszone (erste, zweite) | Fläche des *Spielfelds*, in der ein *Spieler* die *Modelle* seiner *Armee* aufstellt; die *Aufstellungskarte* der *Mission* legt sie fest (`core_rules.txt:2182`). Only War hat zwei ohne Namen, gezählt (`core_rules.txt:2322`).
Ausgangslage | – | Ausgangslage | Stand vor der *Aufstellung*: zwei *Armeen*, *Spielfeld* und *Aufstellungszonen* (MIV-1); Werte in `domaene/daten/ausgangslage.yaml` und `onlyWar.yaml`.
ausgewählt | – | ausgewählt | Zustand einer *Einheit*, die ein *Spieler* angeklickt hat, gleich wer *an der Reihe* ist; ist ihre *Ebene* eines ihrer *Modelle*, ist von ihren *Modellen* nur dieses ausgewählt (Anliegen 980). Erlaubt keine Handlung, zeigt nur, was gemeint ist.
Auswahl | – | Auswahl | Die *ausgewählte* *Einheit* mit ihrer *Ebene*, höchstens eine für beide *Spieler* zusammen (Anliegen 309, 960 F3 A, 980).
Bewegungsphase | Movement phase | Bewegungsphase | Zweite *Phase* eines Zugs; darin bewegt der *Spieler* *am Zug* seine *Einheiten* (`core_rules.txt:644`, `:710`).
Bewegungsweite | Move (M) | bewegungsweite | Wie weit ein *Modell* in der *Normalen Bewegung* höchstens zieht, in *Zoll*; jedes *Modell* hat die aus dem *Profil* seiner *Modellart* (`core_rules.txt:565`, `:745`, Anliegen 4280 F1 B). Die Anzeige kürzt sie mit B ab.
Base | base | Base | Fläche, auf der ein *Modell* steht und von der aus gemessen wird (`core_rules.txt:464`); jedes *Modell* hat eine. Bis Etappe 4 rund, mit einem *Durchmesser*.
Datenblatt | datasheet | datenblatt | Werte, Ausrüstung und Fähigkeiten der *Modelle* einer *Einheit*; jede *Einheit* hat eines, es nennt ihren *Name* und ihre *Modellarten* (`core_rules.txt:552`, `:553`, `:564`). Werte in `domaene/daten/katalog/<fraktion>/datenblaetter.yaml`.
Durchmesser | diameter | durchmesser | Durchmesser einer runden *Base*, in Millimetern wie bei Markern (`core_rules.txt:2228`); ein *Zoll* sind 25,4 mm. Jedes *Modell* hat den seiner *Modellart* (Anliegen 4800 F2 B).
Distanz | distance a model moves | distanz | Länge der geraden Strecke von der *Stelle* eines *Modells* zu Beginn der laufenden *Bewegungsphase* bis zu seiner jetzigen, in *Zoll*; wie oft es dazwischen *gesetzt* wurde, zählt nicht (`core_rules.txt:745`, Anliegen 5180 F5, 5400 F1 A).
Ebene | – | ebene | Was Ziehen eines *Modells* einer *ausgewählten* *Einheit* bewegt: ist sie die ganze *Einheit*, alle ihre *gesetzten* *Modelle*; ist sie eines ihrer *Modelle*, nur das gezogene. Jede *ausgewählte* *Einheit* hat eine (Anliegen 980, Vorbild `ArbiterMap/…/model_selection.js:110`).
eingefahren | – | eingefahren | Zustand einer *Leiste*, die nur ihren *Griff* zeigt; nicht eingefahren zeigt sie auch ihren Inhalt (Anliegen 366 F1 A).
Einheit | unit | Einheit | Ein oder mehrere *Modelle* desselben *Datenblatts*, die zusammen bewegen und kämpfen (`core_rules.txt:420`, `:552`).
erster Zug | first turn | ersterZug | Der Zug, mit dem jede *Schlachtrunde* beginnt; ihn hat in allen derselbe *Spieler* (`core_rules.txt:639`, `:2329`).
Einheit in Aufstellung | – | einheitInAufstellung | Die eine nicht *aufgestellte* *Einheit*, deren *Modelle* gerade *gesetzt* werden; zeitweise ist es keine.
Einhüllende | – | Einhüllende | Rand der Fläche, die ein oder mehrere *Grenzkreise* zusammen bedecken, etwa je einer um jedes *Modell* einer *Einheit*; bei einem ist sie dieser. Die *Karte* zeigt sie statt der *Grenzkreise*, nur zur Anzeige (Anliegen 6410 Punkt 2, 8601, Vorbild `ArbiterMap/…/interaction_map.md:538`).
Eintrag | – | Eintrag | Zeile des *Protokolls* je *gemeinsam übergehen*: die *Einheit*, der die *Sperre* oder das Anhalten galt, ihr *Spieler* und jeder übergangene *Grund* (QUE-5.1, BEW-8.5, Anliegen 362 F4 A).
Fraktion | faction | fraktion | Zugehörigkeit einer *Einheit*, die ihr *Datenblatt* unter den Faction keywords nennt (`core_rules.txt:2483`, `:2484`). Arbiter führt je Fraktion ihre *Datenblätter*, bisher Orks und Necrons (Anliegen 4800 F2 B, 7005).
Fliegen | Flying, FLY | fliegen | Fähigkeit einer *Einheit*, deren *Datenblatt* FLY nennt: In *Normaler Bewegung*, *Vorrücken* und Fall Back ziehen ihre *Modelle* über andere hinweg und durch *Nahkampfreichweite*, enden aber weder darauf noch darin (`core_rules.txt:871`, `:884`, `:888`).
Formation | – | Formation | Anordnung, in der Arbiter die *Modelle* einer *Einheit* auf einmal *setzt*: Reihen parallel zur *Spielfeldkante* ihrer *Aufstellungszone*, mittig untereinander, so dicht, wie es `domaene/daten/formation.yaml` vorgibt (Anliegen 374 F2 A, 377 F1 A).
ganz in | wholly within | ganzIn | Eine *Base* liegt ganz in einer Fläche, wenn jeder ihrer Punkte in der Fläche liegt, ihr Rand eingeschlossen (`core_rules.txt:473`).
Geglitten | – | Geglitten | Was AUF-29.1 und 29.2 ergeben, wenn der Zeiger weiterrückt: die *Stellen*, an denen die *Karte* die gezogenen *Modelle* zeigt, und ob AUF-29 sie beim selben Ziehen angehalten hat (AUF-29.1, 29.2, BEW-17.1).
gemeinsam übergehen | – | gemeinsamÜbergehen | Handlung, mit der beide *Spieler* einvernehmlich eine *Sperre* oder ein Anhalten aufheben, um den Stand am Tisch abzubilden; es steht im *Protokoll*; nie bei ‚keine Kohärenz‘ und ‚Base überdeckt‘ (`domaene/ziel.md`, `core_rules.txt:434`, Anliegen 2361 F1 A, 8840 F1 A).
Gewinner | winner | gewinner | Der *Spieler*, der den *Roll-off* gewinnt (`core_rules.txt:506`).
gezeigt | – | Gezeigt | Was die *Karte* beim Ziehen zeigt, bevor jemand loslässt: je bewegt gezeigtes *Modell* die *Stelle*, an die Arbiter es beim Loslassen *setzen* würde, und ob AUF-29 es angehalten hat (AUF-24.3, 26.5, 28.1, 28.2, BEW-17.2, 20.1).
Grenzkreis | – | Grenzkreis | Leicht gezeigter Kreis auf der *Karte*, der eine Grenze für die *Base* eines *Modells* zeigt; nur Anzeige, er hält nichts an und sperrt nichts (Anliegen 6410, Vorbild `ArbiterMap/docs/spec/interaction_map.md:532`).
Griff | – | leistenGriff | Schaltfläche am Rand einer *Leiste*, mit der die *Spieler* sie ein- und ausfahren; jede *Leiste* hat einen (Anliegen 366 F1 A, Vorbild `ArbiterMap/docs/spec/design_system.md:87`).
Grund | – | Grund (baseÜberdeckt) | Kurzer Name einer *Sperre* oder eines übergangenen Anhaltens, in Anforderungen in ‚…‘ hinter ihr; ihn prüft der Test, die *Spieler* lesen ihn als Satz.
Karte | – | Karte | Abbild des *Spielfelds* mit seinen *Aufstellungszonen* und *gesetzten* *Modellen*, maßstäblich in *Zoll*; sie bildet den Spielstand ab, nicht den exakten Tisch (`domaene/ziel.md`).
Kohärenz | unit coherency | kohärenz | Zustand einer *Einheit*, deren *Modelle* als eine Gruppe beisammenstehen (`core_rules.txt:434`); die 5″ senkrecht hält ohne Gelände jedes Paar ein (`domaene/ziel.md`).
Kommandophase | Command phase | kommandophase | Erste *Phase* eines Zugs (`core_rules.txt:641`).
Leiste | – | leiste | Bereich am Rand des Bildschirms neben der *Karte*, den die *Spieler* ein- und ausfahren; es gibt drei: links, rechts und unten (Anliegen 362, 366 F1 A).
Mission | mission | Mission | Anleitung für eine Schlacht: Armeen, *Spielfeld*, *Aufstellung*, erster Zug, Ende und Sieg; die Grundregeln enthalten nur Only War (`core_rules.txt:301`, `:2166`).
Missionsvorbereitung | – | Missionsvorbereitung | Schritte 1 bis 3 der *Mission* Only War vor der *Aufstellung*: Armeen, Missionsbriefing, *Spielfeld* (`core_rules.txt:2256`, `:2290`, `:2303`).
Moralphase | Morale phase | moralphase | Siebte und letzte *Phase* eines Zugs (`core_rules.txt:665`).
Modell | model | Modell | Eine Miniatur einer *Armee* (`core_rules.txt:305`).
Modellart | – | modellart | Eine Zeile der Profile eines *Datenblatts*: eine Art *Modell* der *Einheit* mit eigenem *Profil* und *Durchmesser*; die Spalte No. nennt sie und wie viele *Modelle* es sind (`core_rules.txt:561`, `:564`, Anliegen 4800 F2 B). Jedes *Modell* hat eine.
Nahkampfreichweite | Engagement Range | nahkampfreichweite | Zwei *Modelle* verschiedener *Spieler* sind in Nahkampfreichweite, wenn ihr *Abstand* höchstens 1″ ist (`core_rules.txt:447`, „within“ `:473`); die 5″ senkrecht hält ohne Gelände jedes Paar ein (`domaene/ziel.md`).
Normale Bewegung | Normal Move | normaleBewegung | Bewegung einer *Einheit* in der *Bewegungsphase*, je *Modell* eine *Distanz* bis zu seiner *Bewegungsweite*; am Ende der *Bewegungsphase* in *Kohärenz* (`core_rules.txt:730`, `:745`, Anliegen 4280 F1 B, 5180 F5).
Name | unit name | name | Name einer *Einheit*, wie ihn ihr *Datenblatt* nennt; jede *Einheit* hat einen (`core_rules.txt:552`, `:553`). Werte: Schlüssel der *Datenblätter* in `domaene/daten/katalog/`.
Phase | phase | Phase (kommandophase, bewegungsphase, psiphase, schussphase, angriffsphase, nahkampfphase, moralphase) | Abschnitt eines Zugs; sieben in dieser Reihenfolge: *Kommandophase*, *Bewegungsphase*, Psiphase, Schussphase, Angriffsphase, Nahkampfphase, *Moralphase* (`core_rules.txt:639`).
Profil | profile | profil | Werte einer *Modellart* auf ihrem *Datenblatt*, darunter die *Bewegungsweite*; jede *Modellart* hat eines (`core_rules.txt:561`, `:562`, `:565`). Werte in `domaene/daten/katalog/<fraktion>/datenblaetter.yaml`.
Protokoll | – | Protokoll | Liste, in der Arbiter festhält, wann die *Spieler* eine *Sperre* oder ein Anhalten *gemeinsam übergehen*; stets einsehbar (`domaene/ziel.md`).
Roll-off | roll-off | RollOff | Beide *Spieler* würfeln je einen W6, der höhere gewinnt; bei Gleichstand wird wiederholt, kein Würfel darf neu gewürfelt oder verändert werden (`core_rules.txt:506`).
Schlacht | battle | Schlacht | Folge der *Schlachtrunden* nach der *Aufstellung*; sie endet nach der letzten *Schlachtrunde* der *Mission* (`core_rules.txt:2333`, `:2337`). Wert in `domaene/daten/onlyWar.yaml`.
Schlachtrunde | battle round | schlachtrunde | Teil der *Schlacht*, gezählt ab 1, in dem jeder *Spieler* einen Zug hat, zuerst der mit dem *ersten Zug* (`core_rules.txt:639`, `:667`).
setzen | set up | setzen | Handlung, die ein *Modell* an eine *Stelle* bringt; danach ist es gesetzt (`core_rules.txt:2322`).
Sperre | – | Sperre | Arbiter verweigert eine regelwidrige Handlung und nennt den *Grund*; *gemeinsam übergehen* nach `domaene/ziel.md`, außer ‚keine Kohärenz‘ und ‚Base überdeckt‘ (Anliegen 2361 F1 A, 8840 F1 A).
Spieler | player | Spieler | Einer der zwei Menschen am Gerät; jeder führt eine *Armee* (`core_rules.txt:305`).
Spielfeld | battlefield | Spielfeld | Rechteckige Fläche, auf der die Schlacht geschlagen wird; die *Mission* nennt die Größe (`core_rules.txt:452`).
Spielfeldkante | battlefield edge | Spielfeldkante | Eine der vier Kanten des *Spielfelds* (`core_rules.txt:452`, `:2320`).
Stelle | – | Stelle | Ort, an den ein *Modell* *gesetzt* werden soll oder an dem es *gesetzt* ist: der Mittelpunkt seiner runden *Base*. Auch außerhalb des *Spielfelds*; ob dort *gesetzt* werden darf, sagen die Kriterien.
Tiefe | depth | Tiefe | Entfernung der Grenze einer *Aufstellungszone* von ihrer *Spielfeldkante*, in *Zoll* (`matched_play.txt:564`).
Vorrücken | Advance | vorrücken | Bewegung einer *Einheit* in der *Bewegungsphase* statt der *Normalen Bewegung*, je *Modell* eine *Distanz* bis zu seiner *Bewegungsweite* plus *Vorrückwurf*; die *Einheit* ist danach bis zum Ende der *Bewegungsphase* vorgerückt, außer die *Spieler* nehmen es zurück (`core_rules.txt:754`, `:764`, Anliegen 6998 F1).
Vorrückwurf | Advance roll | vorrückwurf | Ein W6, den die *Spieler* für eine *Einheit* am Tisch würfeln, wenn sie *vorrückt*; Arbiter nimmt das Ergebnis per Klick auf einen *Grenzkreis* entgegen, je *Einheit* einen (`core_rules.txt:754`, `domaene/ziel.md`, Anliegen 6998 F1).
Weiterrücken | – | Weiterrücken | Was Arbiter beim Ziehen kennt, wenn der Zeiger weiterrückt: die zuvor *gezeigte* *Stelle* des gezogenen *Modells*, ohne sie seine *Stelle* vor dem Ziehen, und ob AUF-29 es beim selben Ziehen schon angehalten hat (AUF-29.1, BEW-17.1, 17.4).
Zoll | inch | Zoll | Maßeinheit jeder Entfernung (`core_rules.txt:464`).
zurücklegen | – | zurücklegen | Handlung, die alle *gesetzten* *Modelle* der *Einheit in Aufstellung* von der *Karte* nimmt, gleich welche *Ebene* sie hat; danach ist keines *gesetzt* (Anliegen 890 F1, 2062, 2220 F2).
überdecken | – | überdecken | Zwei *Bases* überdecken sich, wenn sie mehr als Randpunkte gemeinsam haben; sich berühren ist kein Überdecken (Anliegen 09 F12 A, git).
Übergangen | – | Übergangen | Ergebnis von *gemeinsam übergehen* nach BEW-8.4: das gezogene *Modell*, die neuen *Stellen* der gezogenen *Modelle*, die *Gründe*, die dort weiter sperren, und die *Gründe* des übergangenen Anhaltens für den *Eintrag* (BEW-8.5).
