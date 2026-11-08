import {
  auswahlSenden,
  eingabenDerAbfrage,
  letztenSpielstandZeichnen,
  modellAnklickenSenden,
  modellLoslassen,
  spielfeldAnklicken,
  stellenBeimLoslassen,
} from "./anfragen.js"

const zugschwelle = 4
let gezogen = null
let ziehenStart = null
let abfrageLäuft = false
let wartenderPunkt = null

function punktAufDemSpielfeld(ereignis) {
  const zeichnung = document.querySelector(".spielfeld")
  return new DOMPoint(ereignis.clientX, ereignis.clientY).matrixTransform(zeichnung.getScreenCTM().inverse())
}

function imSpielfeld(punkt) {
  const { width, height } = document.querySelector(".spielfeld .spielfläche").getBBox()
  return punkt.x >= 0 && punkt.x <= width && punkt.y >= 0 && punkt.y <= height
}

function stelleAufDemSpielfeld(ereignis) {
  const punkt = punktAufDemSpielfeld(ereignis)
  return imSpielfeld(punkt) ? { x: punkt.x, y: punkt.y } : null
}

function stelleDesZugs(ereignis, start, gezogenerKreis) {
  const punkt = stelleAufDemSpielfeld(ereignis)
  if (!punkt) return null
  const vorigeStelle = start.kreise.find(({ kreis }) => kreis === gezogenerKreis)
  const { greifpunkt } = start
  return { x: vorigeStelle.x + punkt.x - greifpunkt.x, y: vorigeStelle.y + punkt.y - greifpunkt.y }
}

function ziehenZurücknehmen(start) {
  for (const { kreis, x, y } of start.kreise) {
    kreis.setAttribute("cx", x)
    kreis.setAttribute("cy", y)
  }
}

function kreiseAnDieStellenSetzen(modelle) {
  for (const { spieler, einheit, nummer, x, y } of modelle) {
    const kreis = document.querySelector(`.spielfeld .modell[data-spieler="${spieler}"][data-einheit="${einheit}"][data-nummer="${nummer}"]`)
    kreis.setAttribute("cx", x)
    kreis.setAttribute("cy", y)
  }
}

function stelleDesGezogenen(modelle, kennung) {
  return modelle.find(({ spieler, einheit, nummer }) =>
    spieler === Number(kennung.spieler) && einheit === Number(kennung.einheit) && nummer === Number(kennung.nummer))
}

function antwortMerken(zug, eingaben, antwort, kennung) {
  zug.beantwortet = eingaben
  if (!antwort.modelle) return
  const gezeigt = stelleDesGezogenen(antwort.modelle, kennung)
  zug.letzte200 = eingaben
  zug.weiter = { zuvor: gezeigt && { x: gezeigt.x, y: gezeigt.y }, angehaltenAufDemWeg: antwort.angehaltenAufDemWeg }
  kreiseAnDieStellenSetzen(antwort.modelle)
}

async function stelleBeimLoslassenAbfragen(punkt) {
  abfrageLäuft = true
  const zug = ziehenStart
  try {
    const kennung = gezogen.dataset
    const eingaben = eingabenDerAbfrage(punkt, zug.weiter)
    const antwort = await stellenBeimLoslassen(kennung, eingaben)
    if (antwort && ziehenStart === zug) antwortMerken(zug, eingaben, antwort, kennung)
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
  const modell = ziel.closest(".spielfeld .modell")
  if (modell) return modellAnklickenSenden(modell.dataset)
  if (!ziel.closest(".spielfeld")) return
  const stelle = stelleAufDemSpielfeld(ereignis)
  if (stelle) return spielfeldAnklicken(stelle)
}

export function ziehenBeginnen(ereignis) {
  if (!ereignis.isPrimary || ereignis.button !== 0) return
  gezogen = ereignis.target.closest(".spielfeld .modell")
  ziehenStart = { pointerId: ereignis.pointerId, ziel: ereignis.target, x: ereignis.clientX, y: ereignis.clientY, begonnen: false }
  if (!gezogen) return
  const mitgezogene = gezogen.classList.contains("ausgewählt") ? document.querySelectorAll(".spielfeld .modell.ausgewählt") : [gezogen]
  ziehenStart.kreise = [...mitgezogene].map(kreis => ({ kreis, x: Number(kreis.getAttribute("cx")), y: Number(kreis.getAttribute("cy")) }))
  ziehenStart.greifpunkt = punktAufDemSpielfeld(ereignis)
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
  const stelle = stelleDesZugs(ereignis, ziehenStart, gezogen)
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
  const eingaben = eingabenBeimLoslassen(start, stelleDesZugs(ereignis, start, kreis))
  if (eingaben) return modellLoslassen(kreis.dataset, eingaben)
  letztenSpielstandZeichnen()
}

function eingabenBeimLoslassen(start, stelle) {
  if (!stelle) return start.letzte200
  const { beantwortet } = start
  if (beantwortet?.x === stelle.x && beantwortet?.y === stelle.y) return beantwortet
  return eingabenDerAbfrage(stelle, start.weiter)
}
