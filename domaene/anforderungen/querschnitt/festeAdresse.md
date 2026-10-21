### QUE-8 · Feste Adresse

Zweck: Arbiter läuft immer unter derselben Adresse, damit ein Lesezeichen zur laufenden Partie führt; ist sie belegt, weicht Arbiter nicht aus ([QUE-2.1](karte.md), Anliegen 1650, 1653).
Am Bildschirm: Arbiter starten, die genannte Adresse öffnen.

- QUE-8.1 **Wenn** jemand Arbiter nach QUE-2.1 startet, **dann** ist die genannte Adresse bei jedem Start `http://127.0.0.1:8040/` (Anliegen 1650 F1).
- QUE-8.2 **Gegeben** die Adresse nach QUE-8.1 ist schon belegt, etwa weil Arbiter schon läuft, **wenn** jemand Arbiter startet, **dann** startet Arbiter nicht und meldet die Adresse als belegt (Anliegen 1650 F2).
