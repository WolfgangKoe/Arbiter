// Regel: technik/architektur/web.md O3 und vorschlag.css: Farbwerte stehen nur in `:root`, sonst als Variable.
import stylelint from "stylelint";

const regelName = "arbiter/farbenNurInRoot";
const meldungen = stylelint.utils.ruleMessages(regelName, {
  verboten: (wert) => `Farbwert in „${wert}“ nur in :root, sonst var(--…)`,
});
const farbwert = /#[0-9a-f]{3,8}\b|\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(/i;
const urlInhalt = /url\([^)]*\)/gi;

function regel(eingeschaltet) {
  return (wurzel, ergebnis) => {
    const gueltig = stylelint.utils.validateOptions(ergebnis, regelName, {actual: eingeschaltet});
    if (!gueltig) {
      return;
    }
    wurzel.walkDecls((deklaration) => {
      const wert = deklaration.value.replace(urlInhalt, "");
      if (deklaration.parent.selector !== ":root" && farbwert.test(wert)) {
        stylelint.utils.report({
          message: meldungen.verboten(deklaration.value),
          node: deklaration,
          result: ergebnis,
          ruleName: regelName,
        });
      }
    });
  };
}

regel.ruleName = regelName;
regel.messages = meldungen;

export default stylelint.createPlugin(regelName, regel);
