// Findet Kriterium und Tests in den Dateien selbst, ohne Python und ohne Sprachserver.
const fs = require("fs");
const path = require("path");

const kriteriumMuster = /[A-ZÄÖÜ]+-\d+\.\d+/;
const testMuster = /test[A-ZÄÖÜ][A-Za-zÄÖÜäöüß]*?\d+_\d+/;

function dateien(ordner, endung) {
  if (!fs.existsSync(ordner)) return [];
  return fs.readdirSync(ordner, { withFileTypes: true }).flatMap((eintrag) => {
    const pfad = path.join(ordner, eintrag.name);
    if (eintrag.isDirectory()) return eintrag.name === "__pycache__" ? [] : dateien(pfad, endung);
    return pfad.endsWith(endung) ? [pfad] : [];
  });
}

// Alle Zeilen einer Datei, auf die der Regelausdruck passt: { datei, zeile (ab 0), spalte }.
function stellen(ordner, endung, muster) {
  const gefunden = [];
  for (const datei of dateien(ordner, endung)) {
    fs.readFileSync(datei, "utf8").split("\n").forEach((text, zeile) => {
      const treffer = muster.exec(text);
      if (treffer) gefunden.push({ datei, zeile, spalte: treffer.index });
    });
  }
  return gefunden;
}

// AUF-1.3 -> alle `def testAuf1_3…` unter technik/tests/akzeptanz
function testsZu(wurzel, kriterium) {
  const [, kürzel, anforderung, nummer] = /^([A-ZÄÖÜ]+)-(\d+)\.(\d+)$/.exec(kriterium);
  const name = kürzel[0] + kürzel.slice(1).toLowerCase();
  const muster = new RegExp(`def (test${name}${anforderung}_${nummer})(?!\\d)`, "i");
  return stellen(path.join(wurzel, "technik/tests/akzeptanz"), ".py", muster);
}

// testAuf1_3Eins -> die Zeile `- AUF-1.3 …` unter domaene/anforderungen
function kriteriumZu(wurzel, testName) {
  const [, name, anforderung, nummer] = /^test([A-ZÄÖÜ][A-Za-zÄÖÜäöüß]*?)(\d+)_(\d+)/.exec(testName);
  const muster = new RegExp(`^- ${name.toUpperCase()}-${anforderung}\\.${nummer}(?!\\d)`);
  return stellen(path.join(wurzel, "domaene/anforderungen"), ".md", muster);
}

module.exports = { kriteriumMuster, testMuster, testsZu, kriteriumZu };
