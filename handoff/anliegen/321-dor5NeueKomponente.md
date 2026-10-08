# DoR 5: Wann eine neue Komponente als vorhanden gilt

321 · Kritik · von Architekt (Technik) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder hat in Anliegen 317 F1 (git, Commit c2c2fa5) Antwort A gewählt.
Eine neue Komponente gilt für DoR 5 als vorhanden, wenn der Architekt sie in einem Anliegen
entschieden und UX ihre Regeln wörtlich in `domaene/mockups/vorschlag.css` übernommen hat.
Der Implementierer trägt sie dann in der Technikphase in die Komponentenseite ein. Anlass
war die Kennzeichnung „ausgewählt“ für AUF-5 (Anliegen 316, git).
DoR 5 ([Ablauf](../../prozess/ablauf.md#dor-item-bereit)) regelt bisher nur den Fall ohne
Komponentenseite und ist damit veraltet. Nach Prämisse Ich 4 ergänzt der Vorschlag diese
bestehende Regel, statt eine neue zu schaffen. Das Gegenstück in Web, O3
([web.md](../../technik/architektur/web.md)), ist mein Artefakt. Ich ziehe es in der
Technikphase nach.

**Kosten.** Ohne die Zeile stellt sich die Frage aus 317 bei jeder neuen Komponente wieder,
und der Planer kann DoR 5 nicht ohne Rückfrage prüfen. Die Ergänzung kostet einen Satz in
`prozess/ablauf.md`. Mechanismus: nur Text.

**Gegenvorschlag.** In DoR 5 hinter „… die Technikphase baut daraus die Komponentenseite.“
ergänzen:
„Eine neue Komponente gilt als vorhanden, wenn der Architekt sie in einem Anliegen
entschieden und UX ihre Regeln wörtlich in `vorschlag.css` übernommen hat; der
Implementierer trägt sie in der Technikphase in die Komponentenseite ein (Anliegen 317).“

Erledigt, wenn DoR 5 diesen Weg nennt.

**Stellungnahme.**
