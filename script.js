"use strict";

(() => {
  const html = document.documentElement;
  const japanese = html.lang.toLowerCase().startsWith("ja");
  const path = window.location.pathname;
  const file = path.endsWith("/") ? "index.html" : path.split("/").pop() || "index.html";

  const pairs = {
    "index.html": "index.html",
    "how-it-works.html": "how-it-works.html",
    "questions.html": "questions.html",
    "contact.html": "contact.html",
    "service-standards.html": "service-standards.html",
    "thank-you.html": "thank-you.html",
  };

  const cssHref = japanese ? "../bilingual.css?v=20260722-1" : "bilingual.css?v=20260722-1";
  if (!document.querySelector('link[href*="bilingual.css"]')) {
    const stylesheet = document.createElement("link");
    stylesheet.rel = "stylesheet";
    stylesheet.href = cssHref;
    document.head.append(stylesheet);
  }

  const equivalent = pairs[file];
  const targetHref = japanese
    ? `../${equivalent || "index.html"}`
    : equivalent
      ? `ja/${equivalent}`
      : "ja/index.html";
  const targetLabel = japanese ? "English" : "日本語";
  const targetLang = japanese ? "en" : "ja";

  const headerInner = document.querySelector(".site-header__inner");
  const menuButton = document.querySelector("#englishire-mobile-nav-toggle");
  if (headerInner instanceof HTMLElement && !headerInner.querySelector(".language-switch")) {
    const controls = document.createElement("div");
    controls.className = "site-header__controls";

    const switcher = document.createElement("a");
    switcher.className = "language-switch";
    switcher.href = targetHref;
    switcher.hreflang = targetLang;
    switcher.lang = targetLang;
    switcher.textContent = targetLabel;
    switcher.setAttribute(
      "aria-label",
      japanese ? "View this page in English" : "このページを日本語で表示"
    );
    controls.append(switcher);

    if (menuButton instanceof HTMLElement) {
      controls.append(menuButton);
    }

    const navigation = headerInner.querySelector(".primary-nav");
    if (navigation) {
      headerInner.insertBefore(controls, navigation);
    } else {
      headerInner.append(controls);
    }
  }

  const footerTop = document.querySelector(".site-footer__top");
  if (footerTop instanceof HTMLElement && !footerTop.querySelector(".site-footer__language")) {
    const languageBlock = document.createElement("div");
    languageBlock.className = "site-footer__language";

    const title = document.createElement("p");
    title.className = "site-footer__navigation-title";
    title.textContent = japanese ? "言語" : "Language";

    const footerSwitcher = document.createElement("a");
    footerSwitcher.href = targetHref;
    footerSwitcher.hreflang = targetLang;
    footerSwitcher.lang = targetLang;
    footerSwitcher.textContent = targetLabel;

    const note = document.createElement("p");
    note.textContent = japanese
      ? "日本語での書面対応可。口頭対応は英語のみ。"
      : "Japanese writing welcome. Calls and meetings are conducted in English.";

    languageBlock.append(title, footerSwitcher, note);
    footerTop.append(languageBlock);
  }

  if (equivalent && !document.querySelector(`link[rel="alternate"][hreflang="${targetLang}"]`)) {
    const alternate = document.createElement("link");
    alternate.rel = "alternate";
    alternate.hreflang = targetLang;
    alternate.href = new URL(targetHref, window.location.href).href;
    document.head.append(alternate);
  }

  const core = document.createElement("script");
  core.src = japanese ? "../script-core.js" : "script-core.js";
  core.async = false;
  document.head.append(core);
})();
