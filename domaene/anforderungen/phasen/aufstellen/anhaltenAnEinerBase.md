### AUF-26 · Klemmen beim Ziehen

Zweck: Beim Verschieben hält Arbiter ein *Modell* oder die *Einheit* in der eigenen *Aufstellungszone*, ohne *Grund* und ohne „zurück“, und zeigt es schon beim Ziehen dort; vor fremden *Bases* hält [AUF-29](anhaltenAufDemWeg.md) an (Anliegen 374, 984, Vorbild `ArbiterMap/backend/app/services/movement_service.py:254`).
Am Bildschirm: ziehen und loslassen.

- AUF-26.1 **Wenn** jemand ein *Modell* nach AUF-8.2 an einer *Stelle* loslässt, an der seine *Base* nicht *ganz in* der eigenen *Aufstellungszone* liegt, **dann** rückt Arbiter es auf kürzestem Weg hinein und nennt keinen *Grund* (`core_rules.txt:2322`, Vorbild `:254`).
- AUF-26.5 **Gegeben** ein *Modell*, das nach AUF-20.4 allein gezogen wird, **wenn** jemand es zieht und noch nicht loslässt, **dann** zeigt die *Karte* es an der *Stelle*, an die AUF-8.2 und 26.1 es beim Loslassen dort *setzen* würden, außer AUF-29 hält es an (Anliegen 987 F2 A, 2090).
