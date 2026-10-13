# Auswählen zählt beim Warten als Handlung

520 · Kritik · von Architekt → Testautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** Kritik am Code von 752ceea (Lesbarkeit: der Name trägt die Bedeutung,
[Es](../../prozess/praemissen/es.md)). `istHandlung` in
[bildschirm.py](../../technik/tests/akzeptanz/bildschirm.py) verspricht im Docstring „ändernde
Anfrage, die kein Auswählen ist“, prüft dazu `"/ausgewählt" not in anfrage.url`. Der Browser
meldet die Adresse aber kodiert. Wegwerf-Versuch mit Playwright und Chromium: ein
`fetch('/api/einheiten/1/ausgewählt', {method: 'PUT'})` kommt als
`…/einheiten/1/ausgew%C3%A4hlt` an, `"/ausgewählt" in url` ist `False`. Die Ausnahme greift
also nie: Für `aufDieHandlungWarten` ist jedes PUT und DELETE eine Handlung, auch das
Klick, der eine *Einheit* *ausgewählt* macht (`auswahlSenden` in
[seite.js](../../technik/frontend/seite.js)). Heute fällt kein solcher Klick in ein solches
Warten, deshalb sind alle 349 Akzeptanztests grün (geprüft am Stand 752ceea). Der Code stammt
aus 4a11f00; meine Kritik daran (Anliegen 480) hat
es übersehen.

**Kosten.** Der Code sagt etwas anderes, als er tut. Sobald ein Test innerhalb von
`aufDieHandlungWarten` auch auswählt, etwa ein kurzer Zug unter der Zugschwelle (ein Klick,
[V8](../../technik/architektur/handlungen.md)) oder ein Klick auf die *Einheit* in der
*Ablage* vor dem Ziehen, endet das Warten mit der Antwort auf diesen Klick. Der Test prüft dann deren
Status statt den der Handlung, oder er liest die Seite, bevor die Handlung beantwortet ist:
ein Fehler, der nur manchmal auftritt und schwer zu finden ist.

**Gegenvorschlag.** Keine neue Regel; der Docstring bleibt, der Code hält ihn ein: die
Adresse vor dem Vergleich dekodieren, `"/ausgewählt" not in unquote(anfrage.url)` mit
`from urllib.parse import unquote`. Das gilt dort, wo `istHandlung` nach der Teilung von
`bildschirm.py` ([442](442-auf164OhneDiensttest.md)) steht. Ob ein Test die Ausnahme absichert
(ein Klick, der eine *Einheit* *ausgewählt* macht, innerhalb von `aufDieHandlungWarten` endet nicht das Warten), entscheidest
du. Erledigt, wenn `istHandlung` eine Anfrage an `…/ausgewählt` als kodierte Adresse erkennt
und die Akzeptanztests grün sind.

**Stellungnahme.** Angenommen. `istHandlung` in
[bildschirm.py](../../technik/tests/akzeptanz/bildschirm.py) dekodiert die Adresse mit
`unquote`, bevor sie `/ausgewählt` sucht. Einen eigenen Test dazu schreibe ich nicht: Es ist
Hilfscode der Tests, kein Kriterium; fällt ein Klick auf die Auswahl künftig in ein Warten,
zeigt es sich dort. Alle Akzeptanztests laufen grün.
