"use strict";

(() => {
  const html = document.documentElement;
  const japanese = html.lang.toLowerCase().startsWith("ja");
  const path = window.location.pathname;
  const file = path.endsWith("/") ? "index.html" : path.split("/").pop() || "index.html";

  const pairs = {
    "index.html": "index.html",
    "teacher-cover.html": "teacher-cover.html",
    "how-it-works.html": "how-it-works.html",
    "englishire-standard.html": "englishire-standard.html",
    "questions.html": "questions.html",
    "contact.html": "contact.html",
    "about.html": "about.html",
    "service-standards.html": "service-standards.html",
    "privacy.html": "privacy.html",
    "cookies.html": "cookies.html",
    "terms.html": "terms.html",
    "accessibility.html": "accessibility.html",
    "editorial-policy.html": "editorial-policy.html",
    "permissions.html": "permissions.html",
    "thank-you.html": "thank-you.html"
  };

  const equivalent = pairs[file] || null;
  const unavailable = !equivalent;
  const targetHref = equivalent ? (japanese ? `../${equivalent}` : `ja/${equivalent}`) : null;
  const targetLabel = japanese ? "English" : "日本語";
  const targetLang = japanese ? "en" : "ja";
  const cssHref = japanese ? "../bilingual.css?v=20260722-2" : "bilingual.css?v=20260722-2";

  if (!document.querySelector('link[href*="bilingual.css"]')) {
    const stylesheet = document.createElement("link");
    stylesheet.rel = "stylesheet";
    stylesheet.href = cssHref;
    document.head.append(stylesheet);
  }

  const makeSwitcher = () => {
    const element = document.createElement(unavailable ? "button" : "a");
    element.className = "language-switch";
    element.textContent = targetLabel;
    element.lang = targetLang;
    if (unavailable) {
      element.type = "button";
      element.disabled = true;
      element.setAttribute("aria-disabled", "true");
      element.title = japanese ? "このページの英語版はありません" : "日本語版は準備中です";
    } else {
      element.href = targetHref;
      element.hreflang = targetLang;
      element.setAttribute("aria-label", japanese ? "View this page in English" : "このページを日本語で表示");
    }
    return element;
  };

  const headerInner = document.querySelector(".site-header__inner");
  const menuButton = document.querySelector("#englishire-mobile-nav-toggle");
  if (headerInner instanceof HTMLElement && !headerInner.querySelector(".language-switch")) {
    const controls = document.createElement("div");
    controls.className = "site-header__controls";
    controls.append(makeSwitcher());
    if (menuButton instanceof HTMLElement) controls.append(menuButton);
    const navigation = headerInner.querySelector(".primary-nav");
    navigation ? headerInner.insertBefore(controls, navigation) : headerInner.append(controls);
  }

  if (japanese) {
    const nav = document.querySelector("#englishire-primary-navigation");
    if (nav instanceof HTMLElement) {
      nav.setAttribute("aria-label", "メインナビゲーション");
      nav.innerHTML = '<a href="teacher-cover.html">講師手配</a><a href="how-it-works.html">ご利用の流れ</a><a href="about.html">Englishireについて</a><a href="questions.html">よくあるご質問</a><a class="primary-nav__enquiry" href="contact.html">お問い合わせ</a>';
    }
    document.querySelectorAll(".site-footer__navigation-title").forEach((item) => {
      if (item.textContent.trim().toLowerCase() === "services") item.textContent = "サービス";
      if (item.textContent.trim().toLowerCase() === "enquiries") item.textContent = "お問い合わせ";
    });
    document.querySelectorAll(".site-footer__legal a").forEach((link) => {
      const href = link.getAttribute("href") || "";
      if (href.includes("privacy")) { link.textContent = "プライバシー"; link.setAttribute("href", "privacy.html"); }
      if (href.includes("terms")) { link.textContent = "利用規約"; link.setAttribute("href", "terms.html"); }
      if (href.includes("cookies")) { link.textContent = "Cookie"; link.setAttribute("href", "cookies.html"); }
    });
  }

  const footerTop = document.querySelector(".site-footer__top");
  if (footerTop instanceof HTMLElement && !footerTop.querySelector(".site-footer__language")) {
    const block = document.createElement("div");
    block.className = "site-footer__language";
    const title = document.createElement("p");
    title.className = "site-footer__navigation-title";
    title.textContent = japanese ? "言語" : "Language";
    const note = document.createElement("p");
    note.textContent = japanese ? "メールは日本語対応可。電話・面談は英語のみ。" : "Japanese writing welcome. Calls and meetings are conducted in English.";
    block.append(title, makeSwitcher(), note);
    footerTop.append(block);
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
