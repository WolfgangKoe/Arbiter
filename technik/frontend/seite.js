// Regel: Die Seite holt den Spielstand per fetch und zeichnet ihn in einem Schritt (web.md, O1)

const svgNamensraum = "http://www.w3.org/2000/svg"

function element(tag, klassen, inhalt = "") {
  const neu = document.createElement(tag)
  neu.className = klassen
  neu.textContent = inhalt
  return neu
}

function svgElement(tag, klassen, attribute) {
  const neu = document.createElementNS(svgNamensraum, tag)
  neu.setAttribute("class", klassen)
  for (const [name, wert] of Object.entries(attribute)) {
    neu.setAttribute(name, wert)
  }
  return neu
}

function spielerKlasse(nummer) {
  return nummer === null ? "ohneSpieler" : `spieler${nummer}`
}

function kopfzeilenSpieler(spieler) {
  const feld = element("div", `kopfzeileSpieler spieler${spieler.nummer}`, spieler.name)
  if (spieler.anDerReihe) {
    feld.classList.add("anDerReihe")
    feld.append(element("span", "kopfzeileAnDerReihe", "an der Reihe"))
  }
  return feld
}

function kopfzeile(spielstand) {
  const [ersterSpieler, zweiterSpieler] = spielstand.spieler
  return [
    kopfzeilenSpieler(ersterSpieler),
    element("div", "kopfzeileTitel", "ARBITER"),
    kopfzeilenSpieler(zweiterSpieler),
  ]
}

function einheitenKarte(einheit) {
  const karte = element("section", "einheitenKarte")
  const name = element("div", "einheitenKartenName")
  name.append(element("span", "", einheit.name))
  if (einheit.inAufstellung) {
    karte.classList.add("inAufstellung")
    name.append(element("span", "einheitenKartenAbzeichen", "in Aufstellung"))
  }
  if (einheit.nichtGesetzt > 0) {
    name.append(element("span", "einheitenKartenModelle", String(einheit.nichtGesetzt)))
  }
  karte.append(name)
  return karte
}

function armeeKarte(spieler) {
  const karte = element("div", `armeeKarte spieler${spieler.nummer}`)
  karte.append(element("h2", "armeeKartenName", spieler.name))
  karte.append(...spieler.ablage.map(einheitenKarte))
  return karte
}

function spalte(inhalt) {
  const neu = element("aside", "spalte")
  neu.append(inhalt)
  return neu
}

function karte(spielstand) {
  const { breite, länge } = spielstand.spielfeld
  const zeichnung = svgElement("svg", "karte", {
    viewBox: `0 0 ${breite} ${länge}`,
    role: "img",
    "aria-label": "Karte",
  })
  zeichnung.append(svgElement("rect", "spielfeld", { x: 0, y: 0, width: breite, height: länge }))
  for (const zone of spielstand.zonen) {
    zeichnung.append(
      svgElement("rect", `aufstellungszone ${spielerKlasse(zone.spieler)}`, {
        x: zone.x, y: 0, width: zone.tiefe, height: länge,
      }),
    )
  }
  for (const modell of spielstand.modelle) {
    zeichnung.append(
      svgElement("circle", `modell ${spielerKlasse(modell.spieler)}`, {
        "cx": modell.x, "cy": modell.y, "r": modell.radius,
      }),
    )
  }
  const mitte = element("div", "spalte spalteMitte")
  mitte.append(zeichnung)
  return mitte
}

function zeichnen(spielstand) {
  const [ersterSpieler, zweiterSpieler] = spielstand.spieler
  document.querySelector(".kopfzeile").replaceChildren(...kopfzeile(spielstand))
  document.querySelector(".spielbereich").replaceChildren(
    spalte(armeeKarte(ersterSpieler)),
    karte(spielstand),
    spalte(armeeKarte(zweiterSpieler)),
  )
}

const antwort = await fetch("/api/spielstand")
zeichnen(await antwort.json())
