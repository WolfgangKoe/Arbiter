const vscode = require("vscode");
const { kriteriumMuster, testMuster, testsZu, kriteriumZu } = require("./suche");

function alsOrte(stellen) {
  return stellen.map((stelle) => new vscode.Location(
    vscode.Uri.file(stelle.datei), new vscode.Position(stelle.zeile, stelle.spalte)));
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
