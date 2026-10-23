import { spielstandZeichnen } from "./anfragen.js"
import {
  browserZiehenVerhindern,
  ziehenAbbrechen,
  ziehenBeenden,
  ziehenBeginnen,
  ziehenFolgen,
} from "./bedienung.js"

document.addEventListener("pointerdown", ziehenBeginnen)
document.addEventListener("dragstart", browserZiehenVerhindern)
document.addEventListener("pointermove", ziehenFolgen)
document.addEventListener("pointerup", ziehenBeenden)
document.addEventListener("pointercancel", ziehenAbbrechen)

await spielstandZeichnen()
