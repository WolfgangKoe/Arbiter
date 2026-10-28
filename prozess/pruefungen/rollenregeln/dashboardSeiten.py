sitzungenJeSeite = 6

schalterStil = """
.seitenschalter{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin:4px 0 8px}
.seitenschalter button{background:var(--panel-2);color:var(--text);border:1px solid var(--border);
border-radius:5px;padding:5px 11px;font-size:.84rem;cursor:pointer;font-family:inherit}
.seitenschalter button[aria-current="page"]{background:var(--accent-text);color:var(--bg);
font-weight:700}
.seitenschalter button:disabled{opacity:.35;cursor:default}
.seitenschalter .seiten-stand{color:var(--text-muted);font-size:.82rem;margin-left:6px}
"""

schalterSkript = """
(function () {
  var schalter = document.getElementById("seitenschalter");
  var karten = Array.prototype.slice.call(document.querySelectorAll(".sitzungs-karte"));
  var proSeite = Number(schalter.dataset.proSeite);
  var seiten = Math.ceil(karten.length / proSeite);
  function knopf(text, ziel, gesperrt, aktiv) {
    var element = document.createElement("button");
    element.type = "button";
    element.textContent = text;
    element.disabled = gesperrt;
    if (aktiv) element.setAttribute("aria-current", "page");
    element.addEventListener("click", function () { zeigen(ziel); });
    return element;
  }
  function zeigen(seite) {
    karten.forEach(function (karte, nummer) {
      karte.hidden = Math.floor(nummer / proSeite) !== seite;
    });
    schalter.replaceChildren(knopf("‹ Zurück", seite - 1, seite === 0, false));
    for (var nummer = 0; nummer < seiten; nummer += 1) {
      schalter.appendChild(knopf(String(nummer + 1), nummer, false, nummer === seite));
    }
    schalter.appendChild(knopf("Weiter ›", seite + 1, seite === seiten - 1, false));
    var stand = document.createElement("span");
    stand.className = "seiten-stand";
    stand.textContent = "Session " + (seite * proSeite + 1) + "–" +
      Math.min(karten.length, (seite + 1) * proSeite) + " von " + karten.length +
      ", neueste zuerst";
    schalter.appendChild(stand);
  }
  if (seiten > 1) zeigen(0);
})();
"""


def seitenschalter(anzahlSitzungen: int) -> str:
    if anzahlSitzungen <= sitzungenJeSeite:
        return ""
    return (
        f'<nav class="seitenschalter" id="seitenschalter" data-pro-seite="{sitzungenJeSeite}" '
        'aria-label="Seitenauswahl"></nav>'
    )


def schalterSkriptFür(anzahlSitzungen: int) -> str:
    return f"<script>{schalterSkript}</script>" if anzahlSitzungen > sitzungenJeSeite else ""
