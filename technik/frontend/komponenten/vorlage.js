export function ausVorlage(name) {
  return document.getElementById(name).content.firstElementChild.cloneNode(true)
}

export function ausSvgVorlage(name) {
  return ausVorlage(name).firstElementChild
}

export function mitSpieler(element, nummer) {
  element.classList.replace("spieler1", nummer === null ? "ohneSpieler" : `spieler${nummer}`)
  return element
}
