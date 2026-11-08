export function ausVorlage(name) {
  return document.getElementById(name).content.firstElementChild.cloneNode(true)
}

export function ausSvgVorlage(name) {
  return ausVorlage(name).firstElementChild
}

export function flächeSetzen(element, { x, y, breite, länge }) {
  element.setAttribute("x", x)
  element.setAttribute("y", y)
  element.setAttribute("width", breite)
  element.setAttribute("height", länge)
}

export function mitSpieler(element, nummer) {
  element.classList.replace("spieler1", nummer === null ? "ohneSpieler" : `spieler${nummer}`)
  return element
}
