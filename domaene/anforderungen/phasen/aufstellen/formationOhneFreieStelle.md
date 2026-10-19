### AUF-27 · Formation ohne freie Stelle

Zweck: Passt die *Formation* nirgends in die eigene *Aufstellungszone*, ohne eine *Base* zu *überdecken*, steht sie trotzdem, und die *Spieler* ziehen ihre *Modelle* frei (Anliegen 992 F1 C, Vorbild `ArbiterMap/backend/app/services/deployment_service.py:108`).
Am Bildschirm: auf die *Karte* klicken, dann ziehen.

- AUF-27.1 **Wenn** AUF-18.7 keine *Stelle* findet, an der sich keine *Bases* *überdecken* und alle *ganz in* der eigenen *Aufstellungszone* liegen, **dann** *setzt* Arbiter die *Formation* nach AUF-18.2 und 18.3, QUE-1.2 sperrt keines ihrer *Modelle*, und Arbiter nennt keinen *Grund* (Anliegen 992 F1 C).
- AUF-27.2 **Gegeben** ein *Modell*, dessen *Base* die eines anderen *gesetzten* *Modells* *überdeckt*, **wenn** jemand es nach AUF-26.2 oder seine *Einheit* nach AUF-26.3 zieht, **dann** hält Arbiter es an dieser *Base* nicht an (Vorbild `ArbiterMap/backend/app/domain/geometry.py:734`).
