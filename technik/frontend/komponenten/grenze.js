import { ausSvgVorlage, mitSpieler } from "./vorlage.js"

function kreis(daten) {
  const neu = ausSvgVorlage("grenzeKreis")
  neu.setAttribute("cx", daten.x)
  neu.setAttribute("cy", daten.y)
  neu.setAttribute("r", daten.radius)
  return neu
}

function kennung({ spieler, einheit, wurf }) {
  return `grenze-${spieler}-${einheit}-${wurf ?? "bewegung"}`
}

export function grenze(eintrag, { breite, länge }) {
  const maske = ausSvgVorlage("grenzeMaske")
  maske.setAttribute("id", kennung(eintrag))
  for (const fläche of [maske, maske.querySelector("rect")]) {
    fläche.setAttribute("width", breite)
    fläche.setAttribute("height", länge)
  }
  maske.append(...eintrag.kreise.map(kreis))
  const gruppe = mitSpieler(ausSvgVorlage("grenze"), eintrag.spieler)
  gruppe.setAttribute("mask", `url(#${kennung(eintrag)})`)
  gruppe.classList.toggle("nahkampfreichweite", Boolean(eintrag.nahkampfreichweite))
  gruppe.classList.toggle("wählbar", Boolean(eintrag.wählbar))
  gruppe.append(...eintrag.kreise.map(kreis))
  return [maske, gruppe]
}
