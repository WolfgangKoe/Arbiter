import { zeichnen } from "./zeichnen.js"

let gründeDerLetztenSperre = []
let letzterSpielstand = null

const zurücklegenKnopf = { text: "Einheit zurücklegen", handlung: zurücklegen }
const beendenKnopf = { text: "Aufstellen der Einheit beenden", handlung: aufstellenDerEinheitBeenden }

function knöpfeZu(spielstand) {
  return spielstand.einheitInAufstellung ? [zurücklegenKnopf, beendenKnopf] : [beendenKnopf]
}

function neuZeichnen(spielstand) {
  letzterSpielstand = spielstand
  zeichnen(spielstand, gründeDerLetztenSperre, knöpfeZu(spielstand))
}

function senden(pfad, methode, körper) {
  const optionen = { method: methode }
  if (körper) {
    optionen.headers = { "Content-Type": "application/json" }
    optionen.body = JSON.stringify(körper)
  }
  return fetch(pfad, optionen)
}

async function spielstandHolen() {
  return await (await fetch("/api/spielstand")).json()
}

async function zeichneAntwort(antwort) {
  neuZeichnen(antwort.ok ? await antwort.json() : await spielstandHolen())
}

async function handlungSenden(pfad, methode, körper) {
  const antwort = await senden(pfad, methode, körper).catch(() => null)
  if (!antwort) return neuZeichnen(letzterSpielstand)
  if (antwort.ok) {
    gründeDerLetztenSperre = []
    return neuZeichnen(await antwort.json())
  }
  if (antwort.status === 409) {
    const sperre = await antwort.json()
    gründeDerLetztenSperre = sperre.gründe
    return neuZeichnen(sperre.spielstand)
  }
  gründeDerLetztenSperre = []
  neuZeichnen(await spielstandHolen())
}

function einheitenPfad({ spieler, einheit }) {
  return `/api/spieler/${spieler}/einheiten/${einheit}`
}

function modellPfad(modell) {
  return `${einheitenPfad(modell)}/modelle/${modell.nummer}`
}

export async function spielstandZeichnen() {
  neuZeichnen(await spielstandHolen())
}

export function letztenSpielstandZeichnen() {
  neuZeichnen(letzterSpielstand)
}

export async function auswahlSenden(einheit, ausgewählt) {
  await zeichneAntwort(await senden(`${einheitenPfad(einheit)}/ausgewählt`, ausgewählt ? "DELETE" : "PUT"))
}

export async function ebeneSenden(modell, istEbene) {
  await zeichneAntwort(await senden(`${modellPfad(modell)}/ebene`, istEbene ? "DELETE" : "PUT"))
}

export function modellLoslassen(modell, stelle) {
  return handlungSenden(`${modellPfad(modell)}/stelle`, "PUT", stelle)
}

function aufstellenDerEinheitBeenden() {
  return handlungSenden("/api/aufstellenDerEinheitBeenden", "PUT")
}

function zurücklegen() {
  return handlungSenden("/api/zurücklegen", "PUT")
}

export function karteAnklicken(stelle) {
  return handlungSenden("/api/karteAnklicken", "PUT", stelle)
}

export async function stellenBeimLoslassen(modell, punkt) {
  const antwort = await fetch(`${modellPfad(modell)}/stelleBeimLoslassen?x=${punkt.x}&y=${punkt.y}`).catch(() => null)
  return antwort?.ok ? (await antwort.json()).modelle : null
}
