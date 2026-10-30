import { spielstandZeichnen } from "./anfragen.js"
import { leisteUmschalten } from "./leisten.js"
import {
  browserZiehenVerhindern,
  ziehenAbbrechen,
  ziehenBeenden,
  ziehenBeginnen,
  ziehenFolgen,
} from "./bedienung.js"

document.addEventListener("click", leisteUmschalten)
document.addEventListener("pointerdown", ziehenBeginnen)
document.addEventListener("dragstart", browserZiehenVerhindern)
document.addEventListener("pointermove", ziehenFolgen)
document.addEventListener("pointerup", ziehenBeenden)
document.addEventListener("pointercancel", ziehenAbbrechen)

await spielstandZeichnen()
