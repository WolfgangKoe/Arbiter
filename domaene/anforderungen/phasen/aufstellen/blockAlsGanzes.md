### AUF-24 · Block als Ganzes

Zweck: Beim Verschieben nach [AUF-21](einheitVerschieben.md) gilt die *Einheit* als Ganzes: Die *Spieler* sehen sie schon beim Ziehen am Ziel, und ihre *Modelle* sperren einander nicht (Anliegen 920, 923).
Am Bildschirm: ziehen, dann loslassen.

- AUF-24.2 **Wenn** AUF-21.1 oder 21.2 die *Modelle* einer *Einheit* *setzt*, **dann** sperrt QUE-1.2 keines davon wegen eines *Modells* derselben *Einheit*, weder an dessen voriger noch an dessen neuer *Stelle* (Vorbild `ArbiterMap/…/movement_service.py:450`).
- AUF-24.3 **Gegeben** die *Ebene* der *Einheit in Aufstellung* ist die ganze *Einheit*, **wenn** jemand eines ihrer *Modelle* zieht und noch nicht loslässt, **dann** zeigt die *Karte* jedes ihrer *gesetzten* *Modelle* an der *Stelle*, an die AUF-21.1 und 21.2 es beim Loslassen dort *setzen* würden, außer AUF-29 hält es an (Vorbild `ArbiterMap/…/interaction_map.md:391`, Anliegen 2090).
