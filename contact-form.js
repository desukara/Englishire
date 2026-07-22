"use strict";

(() => {
  const form = document.querySelector("#englishire-contact-form");

  if (!(form instanceof HTMLFormElement)) {
    return;
  }

  const japanese = document.documentElement.lang.toLowerCase().startsWith("ja");
  const standardsHref = "service-standards.html";
  const existingContextLink = document.querySelector(
    '.contact-enquiry a[href="service-standards.html"]'
  );

  if (!existingContextLink) {
    const standardsNotice = document.createElement("p");
    standardsNotice.className = "email-enquiry-form__notice";
    standardsNotice.innerHTML = japanese
      ? '送信前に、応答、正式確定、費用、安全管理、言語に関する<a href="service-standards.html">サービス対応基準</a>をご確認ください。'
      : 'Before submitting, review our <a href="service-standards.html">Service Standards</a> for response, confirmation, commercial and safeguarding expectations.';
    form.before(standardsNotice);
  }

  const footerLegal = document.querySelector(".site-footer__legal");
  if (
    footerLegal instanceof HTMLElement &&
    !footerLegal.querySelector(`a[href="${standardsHref}"]`)
  ) {
    const footerLink = document.createElement("a");
    footerLink.href = standardsHref;
    footerLink.textContent = japanese ? "対応基準" : "Service Standards";
    footerLegal.prepend(footerLink);
  }

  const status = document.querySelector("#englishire-email-enquiry-status");
  const submitButton = form.querySelector('button[type="submit"]');
  const successPage = form.dataset.successPage || "thank-you.html";
  const idleButtonText = japanese ? "お問い合わせを送信" : "Send Enquiry";

  const setStatus = (message) => {
    if (status instanceof HTMLElement) {
      status.textContent = message;
    }
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!form.reportValidity()) {
      setStatus(
        japanese
          ? "必須項目を入力してから送信してください。"
          : "Complete the required fields before sending your enquiry."
      );
      return;
    }

    setStatus(
      japanese ? "お問い合わせを安全に送信しています…" : "Sending your enquiry securely…"
    );
    form.setAttribute("aria-busy", "true");

    if (submitButton instanceof HTMLButtonElement) {
      submitButton.disabled = true;
      submitButton.textContent = japanese ? "送信中…" : "Sending…";
    }

    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 20000);

    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" },
        signal: controller.signal,
      });

      let responseData = null;
      try {
        responseData = await response.json();
      } catch (error) {
        responseData = null;
      }

      if (!response.ok) {
        const serviceMessage =
          responseData && Array.isArray(responseData.errors)
            ? responseData.errors
                .map((item) => item && item.message)
                .filter(Boolean)
                .join(" ")
            : "";

        throw new Error(
          serviceMessage ||
            (japanese
              ? "お問い合わせサービスが送信を受け付けませんでした。"
              : "The enquiry service did not accept the submission.")
        );
      }

      window.location.assign(new URL(successPage, window.location.href).href);
    } catch (error) {
      const timedOut =
        error instanceof DOMException && error.name === "AbortError";

      setStatus(
        japanese
          ? timedOut
            ? "送信サービスからの応答に時間がかかっています。もう一度お試しいただくか、info@englishire.com へメールでご連絡ください。"
            : "現在、お問い合わせを送信できませんでした。もう一度お試しいただくか、info@englishire.com へメールでご連絡ください。"
          : timedOut
            ? "The enquiry service took too long to respond. Please try again, or email info@englishire.com directly."
            : "Your enquiry could not be sent just now. Please try again, or email info@englishire.com directly."
      );

      form.removeAttribute("aria-busy");

      if (submitButton instanceof HTMLButtonElement) {
        submitButton.disabled = false;
        submitButton.textContent = idleButtonText;
        submitButton.focus();
      }
    } finally {
      window.clearTimeout(timeout);
    }
  });
})();
