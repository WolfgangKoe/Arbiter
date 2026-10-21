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

// Warum: Die Sperre ändert den Stand nicht (D2); die Gründe der letzten 409 hält die Seite bis zur nächsten Handlung
let gründeDerLetztenSperre = []
let letzterSpielstand = null

function senden(pfad, methode, körper) {
  const optionen = { method: methode }
  if (körper) {
    optionen.headers = { "Content-Type": "application/json" }
    optionen.body = JSON.stringify(körper)
  }
  return fetch(pfad, optionen)
}

async function spielstandNeuHolen() {
  return await (await fetch("/api/spielstand")).json()
}

async function auswahlSenden(karte) {
  const pfad = `/api/spieler/${karte.dataset.spieler}/einheiten/${karte.dataset.einheit}/ausgewählt`
  await zeichneAntwort(await senden(pfad, karte.classList.contains("ausgewählt") ? "DELETE" : "PUT"))
}

async function zeichneAntwort(antwort) {
  // Warum: Bei einer Ablehnung (404) liefert Flask HTML; die Seite holt dann den Spielstand neu
  zeichnen(antwort.ok ? await antwort.json() : await spielstandNeuHolen())
}

async function ebeneSenden(kreis) {
  // Regel: V8, V9, nur ein Modell der Einheit, die in der Ablage ausgewählt trägt
  const ausgewählteKarte = document.querySelector(`.einheitenKarte.ausgewählt[data-spieler="${kreis.dataset.spieler}"][data-einheit="${kreis.dataset.einheit}"]`)
  if (!ausgewählteKarte) return
  await zeichneAntwort(await senden(`${modellPfad(kreis)}/ebene`, kreis.dataset.ebene ? "DELETE" : "PUT"))
}

async function handlungSenden(pfad, methode, körper) {
  const antwort = await senden(pfad, methode, körper)
  if (antwort.ok) {
    gründeDerLetztenSperre = []
    return zeichnen(await antwort.json())
  }
  if (antwort.status === 409) {
    const sperre = await antwort.json()
    gründeDerLetztenSperre = sperre.gründe
    return zeichnen(sperre.spielstand)
  }
  gründeDerLetztenSperre = []
  zeichnen(await spielstandNeuHolen())
}

function einheitenPfad(element) {
  return `/api/spieler/${element.dataset.spieler}/einheiten/${element.dataset.einheit}`
}

function modellPfad(kreis) {
  return `${einheitenPfad(kreis)}/modelle/${kreis.dataset.nummer}`
}

function modellLoslassen(kreis, stelle) {
  return handlungSenden(`${modellPfad(kreis)}/stelle`, "PUT", stelle)
}

function modellAufAblageLoslassen(kreis, ablage) {
  return handlungSenden(`${modellPfad(kreis)}/stelle?ablage=${ablage.dataset.spieler}`, "DELETE")
}

function karteAnklicken(stelle) {
  return handlungSenden("/api/karteAnklicken", "PUT", stelle)
}

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

function darunter(ereignis) {
  return document.elementFromPoint(ereignis.clientX, ereignis.clientY)
}

// Regel: V8, ein Zug beginnt erst bei mehr als 4 px Abweichung in x oder y
const zugschwelle = 4
let gezogen = null
let ziehenStart = null

function ziehenBeginnen(ereignis) {
  if (!ereignis.isPrimary || ereignis.button !== 0) return
  gezogen = ereignis.target.closest(".karte .modell")
  ziehenStart = { pointerId: ereignis.pointerId, ziel: ereignis.target, x: ereignis.clientX, y: ereignis.clientY, begonnen: false }
  if (!gezogen) return
  // Regel: V10, die Abfrage setzt die Stellen aller ausgewählten Kreise; hier nur zum Zurücksetzen
  const mitgezogene = gezogen.classList.contains("ausgewählt") ? document.querySelectorAll(".karte .modell.ausgewählt") : [gezogen]
  ziehenStart.kreise = [...mitgezogene].map(kreis => ({ kreis, x: Number(kreis.getAttribute("cx")), y: Number(kreis.getAttribute("cy")) }))
  gezogen.setPointerCapture(ereignis.pointerId)
  // Warum: Sonst markiert der Browser Text oder beginnt sein eigenes Ziehen und bricht unseres ab
  ereignis.preventDefault()
}

function browserZiehenVerhindern(ereignis) {
  ereignis.preventDefault()
}

function ziehenZurücknehmen(start) {
  for (const { kreis, x, y } of start.kreise) {
    kreis.setAttribute("cx", x)
    kreis.setAttribute("cy", y)
  }
}

// Regel: V10, höchstens eine Abfrage zugleich, danach nur mit dem jüngsten Punkt seines Zugs
let abfrageLäuft = false
let wartenderPunkt = null

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
    const antwort = await fetch(`${modellPfad(gezogen)}/stelleBeimLoslassen?x=${punkt.x}&y=${punkt.y}`).catch(() => null)
    const modelle = antwort?.ok && (await antwort.json()).modelle
    // Warum: Nach dem Zug ist die Antwort alt
    if (modelle && ziehenStart === zug) kreiseAnDieStellenSetzen(modelle)
  } finally {
    abfrageLäuft = false
    const nächster = wartenderPunkt
    wartenderPunkt = null
    if (nächster?.zug === ziehenStart)stelleBeimLoslassenAbfragen(nächster.punkt)
  }
}

function ziehenFolgen(ereignis) {
  if (!ziehenStart || ereignis.pointerId !== ziehenStart.pointerId) return
  const weite = Math.max(Math.abs(ereignis.clientX - ziehenStart.x), Math.abs(ereignis.clientY - ziehenStart.y))
  ziehenStart.begonnen ||= weite > zugschwelle
  if (!ziehenStart.begonnen || !gezogen) return
  // Warum: Das Ziehen ändert den Stand nicht (D2); die Kreise zeigen, was das Loslassen setzen würde
  const stelle = stelleAufDerKarte(ereignis)
  if (!stelle) return
  if (abfrageLäuft) {
    wartenderPunkt = { zug: ziehenStart, punkt: stelle }
  } else {
    stelleBeimLoslassenAbfragen(stelle)
  }
}

function ziehenAbbrechen(ereignis) {
  if (!ziehenStart || ereignis.pointerId !== ziehenStart.pointerId) return
  if (gezogen) ziehenZurücknehmen(ziehenStart)
  gezogen = null
  ziehenStart = null
}

function klicken(ereignis, ziel) {
  const einheitenKarte = ziel.closest(".einheitenKarte")
  if (einheitenKarte) return auswahlSenden(einheitenKarte)
  const modell = ziel.closest(".karte .modell")
  if (modell) return ebeneSenden(modell)
  if (!ziel.closest(".karte")) return
  const stelle = stelleAufDerKarte(ereignis)
  if (stelle) return karteAnklicken(stelle)
}

function ziehenBeenden(ereignis) {
  if (!ziehenStart || ereignis.pointerId !== ziehenStart.pointerId) return
  const start = ziehenStart
  const kreis = gezogen
  ziehenStart = null
  gezogen = null
  // Warum: Die Kreise bleiben bis zur Antwort, wo die Karte sie zuletzt zeigte; sonst blitzen sie am Anfang auf
  // Regel: Ohne Zug ist es ein Klick (V8), ein Zug wählt nie aus
  if (!start.begonnen) return klicken(ereignis, start.ziel)
  if (!kreis) return
  const stelle = stelleAufDerKarte(ereignis)
  const ablage = darunter(ereignis)?.closest(".armeeKarte")
  if (stelle) return modellLoslassen(kreis, stelle)
  if (ablage) return modellAufAblageLoslassen(kreis, ablage)
  // Regel: Ohne Ziel keine Anfrage, die Seite zeichnet den letzten Stand (V8)
  zeichnen(letzterSpielstand)
}

document.addEventListener("pointerdown", ziehenBeginnen)
document.addEventListener("dragstart", browserZiehenVerhindern)
document.addEventListener("pointermove", ziehenFolgen)
document.addEventListener("pointerup", ziehenBeenden)
document.addEventListener("pointercancel", ziehenAbbrechen)

function einheitenKarte(spieler, einheit) {
  const karte = ausVorlage("einheitenKarte")
  karte.classList.toggle("ausgewählt", einheit.ausgewählt)
  Object.assign(karte.dataset, { spieler: spieler.nummer, einheit: einheit.nummer })
  karte.querySelector(".einheitenKartenName span").textContent = einheit.name
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
  karte.dataset.spieler = spieler.nummer
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
    if (modell.ebene) kreis.dataset.ebene = "ja"
    Object.assign(kreis.dataset, { spieler: modell.spieler, einheit: modell.einheit, nummer: modell.nummer })
    zeichnung.append(kreis)
  }
  if (gründeDerLetztenSperre.length > 0) mitte.append(sperrmeldung(gründeDerLetztenSperre))
  mitte.append(knopfGruppe())
  return mitte
}

function sperrmeldung(gründe) {
  const liste = ausVorlage("sperrmeldung")
  for (const grund of gründe) {
    const eintrag = ausVorlage("sperrmeldungGrund")
    eintrag.textContent = grund
    liste.append(eintrag)
  }
  return liste
}

function knopf(text, handlung) {
  const neu = ausVorlage("knopf")
  neu.textContent = text
  neu.addEventListener("click", handlung)
  return neu
}

function knopfGruppe() {
  const gruppe = ausVorlage("knopfGruppe")
  gruppe.append(knopf("Aufstellen der Einheit beenden", () => handlungSenden("/api/aufstellenDerEinheitBeenden", "PUT")))
  return gruppe
}

function zeichnen(spielstand) {
  letzterSpielstand = spielstand
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
