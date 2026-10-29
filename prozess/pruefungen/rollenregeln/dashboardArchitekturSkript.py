architekturStil = """
.architektur{position:relative;padding:10px 0 20px}
.ak-zeile{display:flex;flex-wrap:wrap;gap:8px 40px;justify-content:center;margin-bottom:64px}
.ak{background:var(--panel);border:1.5px solid var(--c-subagent);border-radius:7px;
padding:6px 9px;min-width:140px;flex:0 1 auto}
.ak.leer{border-style:dashed;background:none}
.ak.unbekannt{border-color:var(--c-warnung)}
.ak.offen.ordner{flex:1 1 100%}
.ak-kopf{cursor:default}
.ak.ordner>.ak-kopf{cursor:pointer}
.ak-name{color:var(--accent-text);font-weight:600;font-size:.86rem}
.ak.datei .ak-name{color:var(--text)}
.ak-zahl{color:var(--text-muted);font-size:.72rem;display:block}
.ak-kinder{display:none;flex-wrap:wrap;gap:8px;margin-top:8px}
.ak.offen>.ak-kinder{display:flex}
.ak-kinder>.ak{flex:0 1 auto}
.ak-pfeile{position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;
background:none;max-width:none}
.pfeil{stroke:var(--text-muted);stroke-width:1.5;fill:none}
.pfeil.verboten{stroke:var(--c-warnung);stroke-width:2.5}
.pfeil-spitze{fill:var(--text-muted)}.pfeil-spitze.verboten{fill:var(--c-warnung)}
.pfeil-text{fill:var(--text);font-size:10px;font-weight:600;paint-order:stroke;
stroke:var(--bg);stroke-width:3px}
.pfeil-text.verboten{fill:var(--c-warnung)}
"""

architekturSkript = """
(function () {
  var wurzel = document.getElementById("architektur");
  var kanten = JSON.parse(document.getElementById("architektur-kanten").textContent);
  var ns = "http://www.w3.org/2000/svg";
  var bild = document.createElementNS(ns, "svg");
  bild.setAttribute("class", "ak-pfeile");
  wurzel.appendChild(bild);
  function sichtbar(kasten) {
    for (var eltern = kasten.parentElement.closest(".ak"); eltern;
         eltern = eltern.parentElement.closest(".ak")) {
      if (!eltern.classList.contains("offen")) return false;
    }
    return true;
  }
  function vertreter(pfad) {
    var beste = null;
    wurzel.querySelectorAll(".ak").forEach(function (kasten) {
      var name = kasten.dataset.pfad;
      var passt = pfad === name || pfad.indexOf(name + "/") === 0;
      if (passt && sichtbar(kasten) && (!beste || name.length > beste.dataset.pfad.length)) {
        beste = kasten;
      }
    });
    return beste;
  }
  function enthalten(aussen, innen) { return aussen.contains(innen) || innen.contains(aussen); }
  function mitte(rechteck) {
    return [rechteck.left + rechteck.width / 2, rechteck.top + rechteck.height / 2];
  }
  function rand(rechteck, richtungX, richtungY) {
    var mitteXY = mitte(rechteck);
    var faktorX = richtungX ? rechteck.width / 2 / Math.abs(richtungX) : Infinity;
    var faktorY = richtungY ? rechteck.height / 2 / Math.abs(richtungY) : Infinity;
    var faktor = Math.min(faktorX, faktorY);
    return [mitteXY[0] + richtungX * faktor, mitteXY[1] + richtungY * faktor];
  }
  function relativ(kasten) {
    var ort = wurzel.getBoundingClientRect();
    var rechteck = kasten.getBoundingClientRect();
    return {left: rechteck.left - ort.left, top: rechteck.top - ort.top,
            width: rechteck.width, height: rechteck.height};
  }
  function zusammenfassen() {
    var summe = {};
    kanten.forEach(function (kante) {
      var von = vertreter(kante.von);
      var nach = vertreter(kante.nach);
      if (!von || !nach || enthalten(von, nach)) return;
      var schluessel = von.dataset.pfad + ">" + nach.dataset.pfad + (kante.text || "");
      var eintrag = summe[schluessel] || (summe[schluessel] = {
        von: von, nach: nach, anzahl: 0, erlaubt: true, text: kante.text});
      eintrag.anzahl += kante.anzahl;
      eintrag.erlaubt = eintrag.erlaubt && kante.erlaubt;
    });
    return Object.keys(summe).map(function (schluessel) { return summe[schluessel]; });
  }
  function spitzen() {
    return '<defs><marker id="spitze" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" ' +
      'markerHeight="7" orient="auto"><path class="pfeil-spitze" d="M0 0L10 5L0 10z"/></marker>' +
      '<marker id="spitzeVerboten" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" ' +
      'markerHeight="7" orient="auto"><path class="pfeil-spitze verboten" d="M0 0L10 5L0 10z"/>' +
      '</marker></defs>';
  }
  function zeichnen() {
    var inhalt = spitzen();
    zusammenfassen().forEach(function (pfeil) {
      var von = relativ(pfeil.von);
      var nach = relativ(pfeil.nach);
      var vonMitte = mitte(von);
      var nachMitte = mitte(nach);
      var richtungX = nachMitte[0] - vonMitte[0];
      var richtungY = nachMitte[1] - vonMitte[1];
      var anfang = rand(von, richtungX, richtungY);
      var ende = rand(nach, -richtungX, -richtungY);
      var klasse = pfeil.erlaubt ? "" : " verboten";
      inhalt += '<line class="pfeil' + klasse + '" x1="' + anfang[0] + '" y1="' + anfang[1] +
        '" x2="' + ende[0] + '" y2="' + ende[1] + '" marker-end="url(#spitze' +
        (pfeil.erlaubt ? "" : "Verboten") + ')"/>' +
        '<text class="pfeil-text' + klasse + '" text-anchor="middle" x="' +
        (anfang[0] + (ende[0] - anfang[0]) * 0.4) + '" y="' +
        (anfang[1] + (ende[1] - anfang[1]) * 0.4 - 4) + '">' +
        (pfeil.text || pfeil.anzahl) + '</text>';
    });
    bild.innerHTML = inhalt;
  }
  wurzel.addEventListener("click", function (ereignis) {
    var kopf = ereignis.target.closest(".ak-kopf");
    var kasten = kopf && kopf.parentElement;
    if (!kasten || !kasten.classList.contains("ordner")) return;
    kasten.classList.toggle("offen");
    zeichnen();
  });
  window.addEventListener("resize", zeichnen);
  zeichnen();
})();
"""
