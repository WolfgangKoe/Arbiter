export function leisteUmschalten(ereignis) {
  const griff = ereignis.target.closest(".leistenGriff")
  if (!griff) return
  const ausgefahren = griff.getAttribute("aria-expanded") === "true"
  griff.setAttribute("aria-expanded", String(!ausgefahren))
}
