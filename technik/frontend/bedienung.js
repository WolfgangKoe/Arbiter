import {
  auswahlSenden,
  ebeneSenden,
  karteAnklicken,
  letztenSpielstandZeichnen,
  modellAnklickenSenden,
  modellLoslassen,
  stellenBeimLoslassen,
} from "./anfragen.js"

const zugschwelle = 4
let gezogen = null
let ziehenStart = null
let abfrageLäuft = false
let wartenderPunkt = null

function punktAufDerKarte(ereignis) {
  const zeichnung = document.querySelector(".karte")
  return new DOMPoint(ereignis.clientX, ereignis.clientY).matrixTransform(zeichnung.getScreenCTM().inverse())
}

function stelleAufDerKarte(ereignis) {
  const zeichnung = document.querySelector(".karte")
  const punkt = punktAufDerKarte(ereignis)
  const { width, height } = zeichnung.querySelector(".spielfeld").getBBox()
  const imSpielfeld = punkt.x >= 0 && punkt.x <= width && punkt.y >= 0 && punkt.y <= height
  return imSpielfeld ? { x: punkt.x, y: punkt.y } : null
}

function stelleDesZugs(ereignis, start) {
  if (!stelleAufDerKarte(ereignis)) return null
  const punkt = punktAufDerKarte(ereignis)
  const { greifpunkt, vorigeStelle } = start
  return { x: vorigeStelle.x + punkt.x - greifpunkt.x, y: vorigeStelle.y + punkt.y - greifpunkt.y }
}

function einheitAusgewählt(modell) {
  return document.querySelector(`.einheitenKarte.ausgewählt[data-spieler="${modell.spieler}"][data-einheit="${modell.einheit}"]`) !== null
}

function ziehenZurücknehmen(start) {
  for (const { kreis, x, y } of start.kreise) {
    kreis.setAttribute("cx", x)
    kreis.setAttribute("cy", y)
  }
}

function kreiseAnDieStellenSetzen(modelle) {
  for (const { spieler, einheit, nummer, x, y } of modelle) {
    const kreis = document.querySelector(`.karte .modell[data-spieler="${spieler}"][data-einheit="${einheit}"][data-nummer="${nummer}"]`)
    kreis.setAttribute("cx", x)
    kreis.setAttribute("cy", y)
  }
}

async function stelleBeimLoslassenAbfragen(punkt) {
  abfrageLäuft = true
  const zug = ziehenStart
  try {
    const modelle = await stellenBeimLoslassen(gezogen.dataset, punkt)
    if (modelle && ziehenStart === zug) kreiseAnDieStellenSetzen(modelle)
  } finally {
    abfrageLäuft = false
    const nächster = wartenderPunkt
    wartenderPunkt = null
    if (nächster?.zug === ziehenStart) stelleBeimLoslassenAbfragen(nächster.punkt)
  }
}

function klicken(ereignis, ziel) {
  const einheitenKarte = ziel.closest(".einheitenKarte")
  if (einheitenKarte) return auswahlSenden(einheitenKarte.dataset, einheitenKarte.classList.contains("ausgewählt"))
  const modell = ziel.closest(".karte .modell")
  if (modell) {
    if (!einheitAusgewählt(modell.dataset)) return modellAnklickenSenden(modell.dataset)
    return ebeneSenden(modell.dataset, Boolean(modell.dataset.ebene))
  }
  if (!ziel.closest(".karte")) return
  const stelle = stelleAufDerKarte(ereignis)
  if (stelle) return karteAnklicken(stelle)
}

export function ziehenBeginnen(ereignis) {
  if (!ereignis.isPrimary || ereignis.button !== 0) return
  gezogen = ereignis.target.closest(".karte .modell")
  ziehenStart = { pointerId: ereignis.pointerId, ziel: ereignis.target, x: ereignis.clientX, y: ereignis.clientY, begonnen: false }
  if (!gezogen) return
  const mitgezogene = gezogen.classList.contains("ausgewählt") ? document.querySelectorAll(".karte .modell.ausgewählt") : [gezogen]
  ziehenStart.kreise = [...mitgezogene].map(kreis => ({ kreis, x: Number(kreis.getAttribute("cx")), y: Number(kreis.getAttribute("cy")) }))
  ziehenStart.greifpunkt = punktAufDerKarte(ereignis)
  ziehenStart.vorigeStelle = { x: Number(gezogen.getAttribute("cx")), y: Number(gezogen.getAttribute("cy")) }
  gezogen.setPointerCapture(ereignis.pointerId)
  ereignis.preventDefault()
}

export function browserZiehenVerhindern(ereignis) {
  ereignis.preventDefault()
}

export function ziehenFolgen(ereignis) {
  if (!ziehenStart || ereignis.pointerId !== ziehenStart.pointerId) return
  const weite = Math.max(Math.abs(ereignis.clientX - ziehenStart.x), Math.abs(ereignis.clientY - ziehenStart.y))
  ziehenStart.begonnen ||= weite > zugschwelle
  if (!ziehenStart.begonnen || !gezogen) return
  const stelle = stelleDesZugs(ereignis, ziehenStart)
  if (!stelle) return
  if (abfrageLäuft) {
    wartenderPunkt = { zug: ziehenStart, punkt: stelle }
  } else {
    stelleBeimLoslassenAbfragen(stelle)
  }
}

export function ziehenAbbrechen(ereignis) {
  if (!ziehenStart || ereignis.pointerId !== ziehenStart.pointerId) return
  if (gezogen) ziehenZurücknehmen(ziehenStart)
  gezogen = null
  ziehenStart = null
}

export function ziehenBeenden(ereignis) {
  if (!ziehenStart || ereignis.pointerId !== ziehenStart.pointerId) return
  const start = ziehenStart
  const kreis = gezogen
  ziehenStart = null
  gezogen = null
  if (!start.begonnen) return klicken(ereignis, start.ziel)
  if (!kreis) return
  const stelle = stelleDesZugs(ereignis, start)
  if (stelle) return modellLoslassen(kreis.dataset, stelle)
  letztenSpielstandZeichnen()
}
