const offenerPunkt = /^ TODO: \S/;
const werkzeugkommentar = /^ eslint-disable-next-line \S/;

function istErlaubt(kommentar) {
  return kommentar.type === "Line"
    && (offenerPunkt.test(kommentar.value) || werkzeugkommentar.test(kommentar.value));
}

export default {
  meta: {
    type: "suggestion",
    schema: [],
    messages: {
      form: "Kommentar nur als `// eslint-disable-next-line <Regel>` oder `// TODO: <was>`",
    },
  },
  create(kontext) {
    return {
      Program() {
        for (const kommentar of kontext.sourceCode.getAllComments()) {
          if (!istErlaubt(kommentar)) {
            kontext.report({loc: kommentar.loc, messageId: "form"});
          }
        }
      },
    };
  },
};
