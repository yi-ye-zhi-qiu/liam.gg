//lang-chooser has NeedTranslate which is a table that can support any number of languages,
//this is inserted into the html element w/ id "lang-chooser" (see lang_chooser.js:36)

var NeedTranslate = [
    {
        中文: "我",
        ENG: "me",
    },
    {
        中文: "自己的",
        ENG: "portfolio",
    },
    {
        中文: "联系（liam xi）",
        ENG: "contact",
    },
    {
        中文: "请你看一下我写的",
        ENG: "check out some of my stuff!",
    },
    {
        中文: "IMDB 评价：介绍 叶秋-的-排序 你快看吧！",
        ENG: "Predicted IMDB ratings: The Liam-o-meter",
    },
    {
      中文: "叶秋，1月22号 2021年",
      ENG: "liam, jan 22 2021",
    }
];
var usable_codes = [
  {
    code: "cn",
    name: "中文",
  },
  // More country codes
];
var current_lang;
var translate = function({
    dropID = "lang-chooser", //id of html element to be made into language selector dropdown
    stringAttribute = "data-translate-text",
    chosenLang = "ENG",
    NeedTranslate = NeedTranslate,
    countryCodes = false,
    countryCodeData = [],
} = {}) {
    const root = document.documentElement;

    var supported_languages = Object.keys(NeedTranslate[0]);
    current_lang = chosenLang;

    (function createMLDrop() {
        var language_menu = document.getElementById(dropID);
        // Reset the menu
        language_menu.innerHTML = "";
        // Now build the options
        supported_languages.forEach((lang, langidx) => {
            let HTMLoption = document.createElement("option");
            HTMLoption.value = lang;
            console.log(lang)
            HTMLoption.textContent = lang;
            language_menu.appendChild(HTMLoption);

            if (lang === chosenLang) {
                language_menu.value = lang;
            }
        });
        language_menu.addEventListener("change", function(e) {

            current_lang = language_menu[language_menu.selectedIndex].value;
            translate_everything();
            // Here we update the 2-digit lang attribute if required
            if (countryCodes === true) {
                if (!Array.isArray(countryCodeData) || !countryCodeData.length) {
                    console.warn("Cannot access strings for language codes");
                    return;
                }
                // throws error still ... have to figure out country codes root.setAttribute("lang", updateCountryCodeOnHTML().code);
            }
        });
    })();

    function updateCountryCodeOnHTML() {
        return countryCodeData.find(this2Digit => this2Digit.name === current_lang);
    }

    function translate_everything() {
        let everyword = document.querySelectorAll(`[${stringAttribute}]`);
        everyword.forEach(each_word => {
            let old_word = each_word.textContent;
            let translated_word = translate_one_word(old_word, NeedTranslate);
            each_word.textContent = translated_word;
            each_word.classList.remove('中文', 'ENG')
            each_word.classList.add(current_lang)
        });
    }


};

function translate_one_word(each_word, NeedTranslate) {
    var word_matched_to_NeedTranslate = NeedTranslate.find(function(stringObj) {
        // Create an array of the objects values:
        let stringValues = Object.values(stringObj);
        // Now return if we can find that string anywhere in there
        return stringValues.includes(each_word);
    });
    if (word_matched_to_NeedTranslate) {
        return word_matched_to_NeedTranslate[current_lang];
    } else {
        // If we don't have a match in our language strings, return the original
        return each_word;
    }
}

translate({
    dropID: "lang-chooser",
    stringAttribute: "data-mlr-text", //any span tag w/ data-mlr-text will be translated as is specified in NeedTranslate table
    chosenLang: "ENG",
    NeedTranslate: NeedTranslate,
    countryCodes: true,
    countryCodeData: usable_codes,
});
