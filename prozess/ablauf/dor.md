# DoR (Item bereit)

1. Format und Höchstmaß von Anforderung und Item (`domaene/CLAUDE.md`), die Kriterien-IDs
   existieren.
2. Keine vagen Wörter; kursive Fachbegriffe stehen im Glossar (Wortanfang).
3. Regelbasierte Kriterien nennen ihre Fundstelle.
4. Abhängigkeiten erledigt, kein offenes Anliegen zum Item.
5. Bei einer Oberfläche: Mockup aus vorhandenen Komponenten. Gibt es noch keine
   Komponentenseite, bringt das Mockup sein CSS als Vorschlag mit; die Technikphase baut
   daraus die Komponentenseite. Eine neue Komponente gilt als vorhanden, wenn der Architekt
   sie in einem Anliegen entschieden und UX ihre Regeln wörtlich in
   `domaene/mockups/vorschlag.css` übernommen hat; der Implementierer trägt sie in der
   Technikphase in die Komponentenseite ein (Anliegen 317).
6. Bei einer Bedienung nennt die Anforderung jede Geste (Klick, Ziehen, Auswahl) und was
   danach am Bildschirm geschieht. Gleicht eine Geste einer gebauten, nennt sie diese als
   Vorbild am laufenden Arbiter („wie in der *Aufstellung* ziehen“) und worin die neue
   abweicht. Jede Abweichung von ArbiterMap und Arbiter-old hat der Stakeholder als Frage
   entschieden. Das gilt für das Gebaute samt Frontend (`ArbiterMap/frontend/static/js/`),
   auch wo Regeln der Architektur oder eine Empfehlung an den Stakeholder die Bedienung
   festlegen; der Fachkritiker prüft die Fundstelle im Gebauten in
   [Schritt 5](domaenenphase.md) und an den Tests ([Technikphase](technikphase.md),
   Schritt 2; Anliegen 1841). Ändert sich ein Kriterium nach der Freigabe Plan, auch aus
   einer Kritik, prüft es der Fachkritiker nach dieser Regel, bevor es getestet wird; weicht
   es von ArbiterMap oder Arbiter-old ab, fragt der Anforderungsautor vorher den Stakeholder
   (Retro 10, P1).
7. Ein Mensch versteht jedes Kriterium, ohne ein anderes nachzulesen: **Gegeben**, **wenn**
   und **dann** sind Sätze. Ein Bezug auf ein anderes Kriterium steht nur in Klammern zur
   Orientierung, nie statt eines Satzes oder Satzteils: „**Gegeben** die *Sperre* ‚Base
   überdeckt‘ (QUE-1.2)“, nicht „**Gegeben** eine *Sperre* nach QUE-1.2“ (Anliegen 16100).
   Mechanismus: `kriterienregeln/bezuege.py` beim Schreiben
   ([Kriterienregeln](../regeln/kriterienregeln.md)); ob der Satz ohne Nachlesen verständlich
   ist, Urteil des Fachkritikers in [Schritt 5](domaenenphase.md).

Mechanismus für 1 bis 6: nur Text. Fachliche Vollständigkeit ist Urteil
([Domänenphase](domaenenphase.md), Schritte 5, 7) und zeigt sich spätestens an den roten Tests.
