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
   danach am Bildschirm geschieht; jede Abweichung von ArbiterMap und Arbiter-old hat der
   Stakeholder als Frage entschieden. Das gilt für das Gebaute samt Frontend
   (`ArbiterMap/frontend/static/js/`), auch wo Regeln der Architektur oder eine Empfehlung an
   den Stakeholder die Bedienung festlegen; der Fachkritiker prüft die Fundstelle im Gebauten
   in [Schritt 5](domaenenphase.md) und an den Tests ([Technikphase](technikphase.md),
   Schritt 2; Anliegen 1841).

Mechanismus für 1 bis 6: nur Text. Fachliche Vollständigkeit ist Urteil
([Domänenphase](domaenenphase.md), Schritte 5, 7) und zeigt sich spätestens an den roten Tests.
