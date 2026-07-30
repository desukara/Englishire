"use strict";

(() => {
  const html = document.documentElement;
  const japanese = html.lang.toLowerCase().startsWith("ja");
  const path = window.location.pathname;
  const file = path.endsWith("/") ? "index.html" : path.split("/").pop() || "index.html";
  const eastokyoHref = "https://eastokyo.com/";

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
  const cssHref = japanese ? "../bilingual.css?v=20260722-3" : "bilingual.css?v=20260722-3";

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

  const normalisePublicationLanguage = () => {
    document.querySelectorAll('a[href="journal.html"],a[href$="/journal.html"],a[href="https://eastokyo.com/"]').forEach((link) => {
      link.href = eastokyoHref;
      link.textContent = "Eastokyo Magazine ↗";
      link.setAttribute("aria-label", japanese
        ? "Eastokyo Magazine、Englishireのデジタル出版物"
        : "Eastokyo Magazine, Englishire's digital publication");
    });

    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const replacements = [
      [/Englishire Journal/g, "Eastokyo Magazine"],
      [/The Journal/g, "Eastokyo Magazine"],
      [/the Journal/g, "Eastokyo Magazine"],
      [/Enter Eastokyo Magazine/g, "Open Eastokyo Magazine"]
    ];
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (!node.nodeValue || !/Journal/.test(node.nodeValue)) continue;
      node.nodeValue = replacements.reduce((value, [pattern, replacement]) => value.replace(pattern, replacement), node.nodeValue);
    }

    document.querySelectorAll('meta[name="description"],meta[property="og:description"],meta[name="twitter:description"]').forEach((meta) => {
      const content = meta.getAttribute("content");
      if (content) meta.setAttribute("content", content.replace(/Englishire Journal/g, "Eastokyo Magazine"));
    });
  };

  const rebuildHomepagePublicationGateway = () => {
    if (japanese || file !== "index.html") return;
    const section = document.querySelector("#englishire-school-media");
    if (!(section instanceof HTMLElement)) return;

    const label = section.querySelector(".section-label");
    const title = section.querySelector("#englishire-school-media-title");
    const summary = section.querySelector(".section-heading__summary");
    const grid = section.querySelector(".homepage-publications__grid");
    const footer = section.querySelector(".school-media__footer");

    if (label) label.textContent = "From Eastokyo Magazine";
    if (title) title.textContent = "The publication lives across the street.";
    if (summary) summary.textContent = "Read native Eastokyo editions on recruitment, continuity and the professional life of English teaching in Japan.";

    if (grid) {
      grid.innerHTML = `
        <article class="homepage-publication">
          <a class="homepage-publication__media" href="https://eastokyo.com/the-end-of-the-easy-teacher.html">
            <img src="media-rushed-recruitment.png" alt="Editorial image for The End of the Easy Teacher" width="1200" height="900" loading="lazy" decoding="async" />
          </a>
          <div class="homepage-publication__content">
            <p class="story-category">Cover Story · Recruitment</p>
            <h3><a href="https://eastokyo.com/the-end-of-the-easy-teacher.html">The End of the Easy Teacher</a></h3>
            <p>How Japan's English schools spent decades mistaking a desire to come to Japan for a desire to teach.</p>
            <a class="story-link" href="https://eastokyo.com/the-end-of-the-easy-teacher.html">Read at Eastokyo ↗</a>
          </div>
        </article>
        <article class="homepage-publication">
          <a class="homepage-publication__media" href="https://eastokyo.com/hiring-foreign-teachers-in-japan.html">
            <img src="hiring-foreign-teachers-in-japan.png" alt="Editorial image for The Hire You're Actually Making" width="1600" height="900" loading="lazy" decoding="async" />
          </a>
          <div class="homepage-publication__content">
            <p class="story-category">Essay · Hiring</p>
            <h3><a href="https://eastokyo.com/hiring-foreign-teachers-in-japan.html">The Hire You're Actually Making</a></h3>
            <p>Why a vacancy is a long-term decision about continuity, adaptability and institutional character.</p>
            <a class="story-link" href="https://eastokyo.com/hiring-foreign-teachers-in-japan.html">Read at Eastokyo ↗</a>
          </div>
        </article>
        <article class="homepage-publication">
          <a class="homepage-publication__media" href="https://eastokyo.com/city-life.html">
            <img src="media-staffing-contingency.png" alt="Editorial image for Eastokyo Magazine Issue 01" width="1200" height="900" loading="lazy" decoding="async" />
          </a>
          <div class="homepage-publication__content">
            <p class="story-category">Issue 01 · The Profession</p>
            <h3><a href="https://eastokyo.com/city-life.html">The Work Behind the Classroom</a></h3>
            <p>Eight essays on recruitment, retention, continuity, operations and the decisions that hold a school together.</p>
            <a class="story-link" href="https://eastokyo.com/city-life.html">Open the issue ↗</a>
          </div>
        </article>`;
    }

    if (footer) {
      footer.innerHTML = '<p>Eastokyo Magazine is Englishire\'s independent digital publication for the English-teaching profession in Japan.</p><a class="button button--text" href="https://eastokyo.com/">Open Eastokyo Magazine ↗</a>';
    }
  };

  if (japanese) {
    const nav = document.querySelector("#englishire-primary-navigation");
    if (nav instanceof HTMLElement) {
      nav.setAttribute("aria-label", "メインナビゲーション");
      nav.innerHTML = '<a href="teacher-cover.html">講師手配</a><a href="how-it-works.html">ご利用の流れ</a><a href="englishire-standard.html">Englishireの基準</a><a href="about.html">Englishireについて</a><a href="https://eastokyo.com/">Eastokyo Magazine ↗</a><a class="primary-nav__enquiry" href="contact.html">お問い合わせ</a>';
      nav.querySelectorAll("a").forEach((link) => {
        if (link.getAttribute("href") === file) link.setAttribute("aria-current", "page");
      });
    }

    const footerTop = document.querySelector(".site-footer__top");
    if (footerTop instanceof HTMLElement) {
      footerTop.innerHTML = '<div class="site-footer__brand"><a class="site-footer__masthead" href="index.html"><img src="../englishire-logo.png" width="1327" height="380" alt="Englishire" style="width:250px;height:auto;display:block;margin-bottom:.75rem"></a><p class="site-footer__statement">東京都内の学校向け英語講師の代講・短期手配。</p></div><nav class="site-footer__navigation" aria-label="サービス"><p class="site-footer__navigation-title">サービス</p><a href="teacher-cover.html">講師手配</a><a href="how-it-works.html">ご利用の流れ</a><a href="englishire-standard.html">Englishireの基準</a><a href="about.html">Englishireについて</a><a href="questions.html">よくあるご質問</a><a href="contact.html">お問い合わせ</a></nav><nav class="site-footer__navigation" aria-label="出版物と方針"><p class="site-footer__navigation-title">出版物と方針</p><a href="https://eastokyo.com/">Eastokyo Magazine ↗</a><a href="service-standards.html">サービス方針</a><a href="accessibility.html">アクセシビリティ</a><a href="editorial-policy.html">編集方針</a><a href="permissions.html">転載・利用許可</a></nav>';
    }

    const legal = document.querySelector(".site-footer__legal");
    if (legal instanceof HTMLElement) {
      legal.innerHTML = '<a href="privacy.html">プライバシー</a><a href="terms.html">利用規約</a><a href="cookies.html">Cookie</a>';
    }
  }

  normalisePublicationLanguage();
  rebuildHomepagePublicationGateway();

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
  core.src = japanese ? "../script-core.js?v=20260722-3" : "script-core.js?v=20260722-3";
  core.async = false;
  document.head.append(core);
})();