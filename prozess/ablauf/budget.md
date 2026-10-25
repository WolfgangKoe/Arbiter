# Budget

Gemessen wird nur die Belegung des Kontextfensters je Lauf, gleich für den Koordinator und
jede Rolle; der Stand zeigt sie. Die Zahl der Rollenläufe ist weder Budget noch Kennzahl.
Mechanismus: `standregeln/belegung.py`; der Stand nennt keine Rollenläufe (`standregeln/standTest.py`).
- Ab 120.000 Token meldet ein Hook; die Rolle beginnt nichts Neues und schließt ab, der
  Koordinator empfiehlt einen neuen Chat.
- Ab 150.000 Token sperrt ein Hook alles außer Schreiben im eigenen Pfad und der
  Schlussantwort. Beim Koordinator entscheidet der Stakeholder: freigeben (höhere Grenze in
  `.git/arbiter/belegungsgrenze.txt`), kürzen oder neuer Chat.
