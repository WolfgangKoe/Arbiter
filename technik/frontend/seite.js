// Regel: Die Seite holt den Spielstand per fetch und zeichnet ihn in einem Schritt; das Markup steht in den Vorlagen der Seite (web.md, O1)

function ausVorlage(name) {
  return document.getElementById(name).content.firstElementChild.cloneNode(true)
}

function ausSvgVorlage(name) {
  // Warum: Ein Element der Karte behält den SVG-Namensraum nur innerhalb eines <svg> der Vorlage
  return ausVorlage(name).firstElementChild
}

function mitSpieler(element, nummer) {
  element.classList.replace("spieler1", nummer === null ? "ohneSpieler" : `spieler${nummer}`)
  return element
}

function kopfzeilenSpieler(spieler) {
  const feld = mitSpieler(ausVorlage("kopfzeileSpieler"), spieler.nummer)
  feld.firstChild.nodeValue = spieler.name
  if (!spieler.anDerReihe) {
    feld.classList.remove("anDerReihe")
    feld.querySelector(".kopfzeileAnDerReihe").remove()
  }
  return feld
}

function kopfzeile(spielstand) {
  const [ersterSpieler, zweiterSpieler] = spielstand.spieler
  return [
    kopfzeilenSpieler(ersterSpieler),
    ausVorlage("kopfzeileTitel"),
    kopfzeilenSpieler(zweiterSpieler),
  ]
}

async function auswahlSenden(spieler, einheit) {
  const pfad = `/api/spieler/${spieler.nummer}/einheiten/${einheit.nummer}/ausgewählt`
  const antwort = await fetch(pfad, { method: einheit.ausgewählt ? "DELETE" : "PUT" })
  zeichnen(await antwort.json())
}

function einheitenKarte(spieler, einheit) {
  const karte = ausVorlage("einheitenKarte")
  karte.classList.toggle("ausgewählt", einheit.ausgewählt)
  karte.addEventListener("click", () => auswahlSenden(spieler, einheit))
  karte.querySelector(".einheitenKartenName span").textContent = einheit.name
  if (!einheit.inAufstellung) {
    karte.classList.remove("inAufstellung")
    karte.querySelector(".einheitenKartenAbzeichen").remove()
  }
  if (einheit.nichtGesetzt > 0) {
    karte.querySelector(".einheitenKartenModelle").textContent = String(einheit.nichtGesetzt)
  } else {
    karte.querySelector(".einheitenKartenModelle").remove()
  }
  return karte
}

function armeeKarte(spieler) {
  const karte = mitSpieler(ausVorlage("armeeKarte"), spieler.nummer)
  karte.querySelector(".armeeKartenName").textContent = spieler.name
  karte.append(...spieler.ablage.map(einheit => einheitenKarte(spieler, einheit)))
  return karte
}

function spalte(inhalt) {
  const neu = ausVorlage("spalte")
  neu.append(inhalt)
  return neu
}

function flächeSetzen(element, { x, y, breite, länge }) {
  element.setAttribute("x", x)
  element.setAttribute("y", y)
  element.setAttribute("width", breite)
  element.setAttribute("height", länge)
}

function karte(spielstand) {
  const { breite, länge } = spielstand.spielfeld
  const mitte = ausVorlage("karte")
  const zeichnung = mitte.querySelector(".karte")
  zeichnung.setAttribute("viewBox", `0 0 ${breite} ${länge}`)
  flächeSetzen(zeichnung.querySelector(".spielfeld"), { x: 0, y: 0, breite, länge })
  for (const zone of spielstand.zonen) {
    const fläche = mitSpieler(ausSvgVorlage("aufstellungszone"), zone.spieler)
    flächeSetzen(fläche, zone)
    zeichnung.append(fläche)
  }
  for (const modell of spielstand.modelle) {
    const kreis = mitSpieler(ausSvgVorlage("modell"), modell.spieler)
    kreis.setAttribute("cx", modell.x)
    kreis.setAttribute("cy", modell.y)
    kreis.setAttribute("r", modell.radius)
    kreis.classList.toggle("ausgewählt", modell.ausgewählt)
    zeichnung.append(kreis)
  }
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
