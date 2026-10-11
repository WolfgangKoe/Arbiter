# Glossar

Begriff | englischer Regelbegriff | Code-Bezeichner | Definition
---|---|---|---
Ablage | – | Ablage | Ort neben der *Karte* für die nicht *aufgestellten* *Einheiten* eines *Spielers* mit ihren nicht *gesetzten* *Modellen*; jeder *Spieler* hat eine (Etappe 1, Anliegen 145 F1 A).
Abstand | distance | abstand | Kürzeste waagrechte Entfernung zwischen den *Bases* zweier *Modelle*, in *Zoll* (`core_rules.txt:464`); ohne Gelände stehen alle *Modelle* auf einer Ebene (`domaene/ziel.md`). *Bases*, die sich berühren oder *überdecken*, haben den *Abstand* 0.
an der Reihe | – | anDerReihe | Zustand des einen *Spielers*, der als Nächster eine *Einheit* aufstellt; zeitweise ist es keiner.
Armee | army | Armee | Alle *Modelle* unter dem Befehl eines *Spielers*, in *Einheiten* gegliedert (`core_rules.txt:305`, `:321`, `:420`).
aufgestellt | deployed | aufgestellt | Zustand einer *Einheit*, für die *Aufstellen der Einheit beenden* gelungen ist (`core_rules.txt:2322`).
Aufstellen der Einheit beenden | – | aufstellenDerEinheitBeenden | Handlung, mit der die *Spieler* die *Einheit in Aufstellung* abschließen.
Aufstellung | deploy forces | Aufstellung | Schritt 4 der Mission Only War: Die *Spieler* stellen abwechselnd je eine *Einheit* auf, bis beide alle aufgestellt haben (`core_rules.txt:2322`).
Aufstellungskarte | deployment map | Aufstellungskarte | Karte einer *Mission* mit ihren *Aufstellungszonen* (`core_rules.txt:2182`); einen Namen hat eine Zone nur, wenn die Karte ihn zeigt, etwa die des Angreifers (`open_play.txt:235`, `narrative_play.txt:2001`).
Aufstellungszone | deployment zone | Aufstellungszone (erste, zweite) | Fläche des *Spielfelds*, in der ein *Spieler* die *Modelle* seiner *Armee* aufstellt; die *Aufstellungskarte* der *Mission* legt sie fest (`core_rules.txt:2182`). Only War hat zwei ohne Namen, nur gezählt (`core_rules.txt:2322`).
Ausgangslage | – | Ausgangslage | Stand vor der *Aufstellung*: zwei *Armeen*, *Spielfeld* und *Aufstellungszonen* (Etappe 1); Werte in `domaene/daten/ausgangslage.yaml` und `onlyWar.yaml`.
ausgewählt | – | ausgewählt | Zustand einer *Einheit*, die ein *Spieler* angeklickt hat, gleich wer *an der Reihe* ist; erlaubt keine Handlung, zeigt nur, welche *Einheit* gemeint ist.
Auswahl | – | Auswahl | Die *ausgewählten* *Einheiten* eines *Spielers*, höchstens zwei; jeder *Spieler* hat eine (Anliegen 309, 345 F3 A).
Base | base | Base | Fläche, auf der ein *Modell* steht und von der aus gemessen wird (`core_rules.txt:464`); jedes *Modell* hat eine. In Etappe 1 rund, mit einem *Durchmesser*.
Durchmesser | diameter | durchmesser | Durchmesser einer runden *Base*, in Millimetern wie bei Markern (`core_rules.txt:2228`); ein *Zoll* sind 25,4 mm.
eingefahren | – | eingefahren | Zustand einer *Leiste*, die nur ihren *Griff* zeigt; nicht eingefahren zeigt sie auch ihren Inhalt (Anliegen 366 F1 A).
Einheit | unit | Einheit | Ein oder mehrere *Modelle* desselben Datenblatts, die zusammen bewegen und kämpfen (`core_rules.txt:420`).
Einheit in Aufstellung | – | einheitInAufstellung | Die eine nicht *aufgestellte* *Einheit*, deren *Modelle* gerade *gesetzt* werden; zeitweise ist es keine.
Formation | – | formation | Anordnung, in der Arbiter die *Modelle* einer *Einheit* auf einmal *setzt*: Reihen parallel zur *Spielfeldkante* ihrer *Aufstellungszone*, mittig untereinander, so dicht, dass jede *Base* zu jeder anderen mindestens den *Abstand* aus `domaene/daten/formation.yaml` hat (Anliegen 374 F2 A, 377 F1 A).
ganz in | wholly within | ganzIn | Eine *Base* liegt ganz in einer Fläche, wenn jeder ihrer Punkte in der Fläche liegt, ihr Rand eingeschlossen (`core_rules.txt:473`).
gemeinsam übergehen | – | gemeinsamÜbergehen | Handlung, mit der beide *Spieler* einvernehmlich eine *Sperre* aufheben; die gesperrte Handlung geschieht doch und steht im *Protokoll* (`domaene/ziel.md`).
gesperrt | – | gesperrt | Zustand eines *Modells*, das beim Loslassen an eine *Stelle* kam, die eine *Sperre* verbietet: Es steht dort mit dem *Grund*, nicht *gesetzt*, bis die *Spieler* *zurück* oder *gemeinsam übergehen* wählen (Etappe 1).
Gewinner | winner | gewinner | Der *Spieler*, der den *Roll-off* gewinnt (`core_rules.txt:506`).
Griff | – | leistenGriff | Schaltfläche am Rand einer *Leiste*, mit der die *Spieler* sie ein- und ausfahren; jede *Leiste* hat einen (Anliegen 366 F1 A, Vorbild `ArbiterMap/docs/spec/design_system.md:87`).
Grund | – | Grund | Kurzer Name einer *Sperre*, in Anforderungen in ‚…‘ hinter ihr; ihn prüft der Test, die *Spieler* lesen ihn als Satz.
Karte | – | Karte | Abbild des *Spielfelds* mit seinen *Aufstellungszonen* und *gesetzten* *Modellen*, maßstäblich in *Zoll*; sie bildet den Spielstand ab, nicht den exakten Tisch (`domaene/ziel.md`).
Kohärenz | unit coherency | kohärenz | Zustand einer *Einheit*, deren *Modelle* als eine Gruppe beisammenstehen (`core_rules.txt:434`); die 5″ senkrecht hält ohne Gelände jedes Paar ein (`domaene/ziel.md`).
Leiste | – | leiste | Bereich am Rand des Bildschirms neben der *Karte*, den die *Spieler* ein- und ausfahren; es gibt drei: links, rechts und unten (Anliegen 362, 366 F1 A).
Mission | mission | Mission | Anleitung für eine Schlacht: Armeen, *Spielfeld*, *Aufstellung*, erster Zug, Ende und Sieg; die Grundregeln enthalten nur Only War (`core_rules.txt:301`, `:2166`).
Missionsvorbereitung | – | Missionsvorbereitung | Schritte 1 bis 3 der *Mission* Only War vor der *Aufstellung*: Armeen, Missionsbriefing, *Spielfeld* (`core_rules.txt:2256`, `:2290`, `:2303`).
Modell | model | Modell | Eine Miniatur einer *Armee* (`core_rules.txt:305`).
Nahkampfreichweite | Engagement Range | nahkampfreichweite | Zwei *Modelle* verschiedener *Spieler* sind in Nahkampfreichweite, wenn ihr *Abstand* höchstens 1″ ist (`core_rules.txt:447`, „within“ `:473`); die 5″ senkrecht hält ohne Gelände jedes Paar ein (`domaene/ziel.md`).
Name | unit name | name | Name einer *Einheit*, wie ihn ihr Datenblatt nennt; jede *Einheit* hat einen (`core_rules.txt:552`, `:553`). Werte in `domaene/daten/ausgangslage.yaml` unter `Einheit`.
Protokoll | – | Protokoll | Liste, in der Arbiter festhält, wann die *Spieler* eine *Sperre* *gemeinsam übergehen*; stets einsehbar (`domaene/ziel.md`, Etappe 1).
Roll-off | roll-off | RollOff | Beide *Spieler* würfeln je einen W6, der höhere gewinnt; bei Gleichstand wird wiederholt, kein Würfel darf neu gewürfelt oder verändert werden (`core_rules.txt:506`).
setzen | set up | setzen | Handlung, die ein *Modell* an eine *Stelle* bringt; danach ist es gesetzt (`core_rules.txt:2322`).
Sperre | – | Sperre | Arbiter verweigert eine regelwidrige Handlung und nennt den *Grund*; Übergehen nach `domaene/ziel.md`.
Spieler | player | Spieler | Einer der zwei Menschen am Gerät; jeder führt eine *Armee* (`core_rules.txt:305`).
Spielfeld | battlefield | Spielfeld | Rechteckige Fläche, auf der die Schlacht geschlagen wird; die *Mission* nennt die Größe (`core_rules.txt:452`).
Spielfeldkante | battlefield edge | Spielfeldkante | Eine der vier Kanten des *Spielfelds* (`core_rules.txt:452`, `:2320`).
Stelle | – | Stelle | Ort, an den ein *Modell* *gesetzt* werden soll oder an dem es *gesetzt* ist: der Mittelpunkt seiner runden *Base*. Auch außerhalb des *Spielfelds*; ob dort *gesetzt* werden darf, sagen die Kriterien.
Tiefe | depth | Tiefe | Entfernung der Grenze einer *Aufstellungszone* von ihrer *Spielfeldkante*, in *Zoll* (`matched_play.txt:564`).
vernichtet | destroyed | vernichtet | Zustand eines *Modells*, das aus dem Spiel ist (`core_rules.txt:441`).
Zoll | inch | Zoll | Maßeinheit jeder Entfernung (`core_rules.txt:464`).
zurück | – | zurück | Handlung, mit der die *Spieler* eine *Sperre* hinnehmen, die sie *gemeinsam übergehen* könnten: Die gesperrte Handlung unterbleibt, ein *gesperrtes* *Modell* kommt an seine vorige *Stelle* oder in die *Ablage*, mit ihm seine *Formation* (Etappe 1, Anliegen 362 F6 A, 374 F1 A).
zurücklegen | – | zurücklegen | Handlung, die ein *gesetztes* *Modell* in die *Ablage* bringt; danach ist es nicht *gesetzt* (Etappe 1).
überdecken | – | überdecken | Zwei *Bases* überdecken sich, wenn sie mehr als Randpunkte gemeinsam haben; sich berühren ist kein Überdecken (Etappe 1, Anliegen 09 F12 A, git).
