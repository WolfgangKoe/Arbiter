import { ausVorlage } from "./vorlage.js"

function knopf(spielernummer, { text, handlung }) {
  const neu = ausVorlage("knopf")
  neu.textContent = text
  neu.addEventListener("click", handlung.bind(null, spielernummer))
  return neu
}

export function knopfGruppe(knöpfe, spielernummer) {
  const gruppe = ausVorlage("knopfGruppe")
  gruppe.append(...knöpfe.map(knopf.bind(null, spielernummer)))
  return gruppe
}
