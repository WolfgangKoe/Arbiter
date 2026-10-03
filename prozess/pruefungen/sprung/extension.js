// Strg+Klick auf ein Kriterium zeigt seine Tests, Strg+Klick auf einen Test springt zum
// Kriterium. Bei mehreren Zielen zeigt VS Code die Liste.
const vscode = require("vscode");
const { kriteriumMuster, testMuster, testsZu, kriteriumZu } = require("./suche");

function alsOrte(stellen) {
  return stellen.map((s) => new vscode.Location(
    vscode.Uri.file(s.datei), new vscode.Position(s.zeile, s.spalte)));
}

const anbieter = {
  provideDefinition(dokument, position) {
    const wurzel = vscode.workspace.getWorkspaceFolder(dokument.uri)?.uri.fsPath;
    if (!wurzel) return undefined;
    const kriterium = dokument.getWordRangeAtPosition(position, new RegExp(kriteriumMuster.source));
    if (kriterium) return alsOrte(testsZu(wurzel, dokument.getText(kriterium)));
    const test = dokument.getWordRangeAtPosition(position, new RegExp(testMuster.source));
    if (test) return alsOrte(kriteriumZu(wurzel, dokument.getText(test)));
    return undefined;
  },
};

function activate(kontext) {
  kontext.subscriptions.push(vscode.languages.registerDefinitionProvider(
    [{ language: "markdown" }, { language: "python" }], anbieter));
}

module.exports = { activate };
