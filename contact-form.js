"use strict";

(() => {
  const form = document.querySelector("#englishire-contact-form");

  if (!(form instanceof HTMLFormElement)) {
    return;
  }

  const status = document.querySelector("#englishire-email-enquiry-status");
  const submitButton = form.querySelector('button[type="submit"]');
  const directEmailLink = form.querySelector("[data-direct-email]");
  const successPage = form.dataset.successPage || "thank-you.html";

  const setStatus = (message) => {
    if (status instanceof HTMLElement) {
      status.textContent = message;
    }
  };

  if (directEmailLink instanceof HTMLAnchorElement) {
    directEmailLink.addEventListener("click", () => {
      const emailAddress =
        directEmailLink.dataset.emailAddress || "info@englishire.com";

      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(emailAddress).catch(() => {});
      }

      setStatus(
        "Your email application should open. The address info@englishire.com has also been copied where supported."
      );
    });
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!form.reportValidity()) {
      setStatus("Complete the required fields before sending your enquiry.");
      return;
    }

    setStatus("Sending your enquiry securely…");
    form.setAttribute("aria-busy", "true");

    if (submitButton instanceof HTMLButtonElement) {
      submitButton.disabled = true;
      submitButton.textContent = "Sending…";
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
          serviceMessage || "The enquiry service did not accept the submission."
        );
      }

      window.location.assign(new URL(successPage, window.location.href).href);
    } catch (error) {
      const timedOut =
        error instanceof DOMException && error.name === "AbortError";

      setStatus(
        timedOut
          ? "The enquiry service took too long to respond. Please try again, or email info@englishire.com directly."
          : "Your enquiry could not be sent just now. Please try again, or email info@englishire.com directly."
      );

      form.removeAttribute("aria-busy");

      if (submitButton instanceof HTMLButtonElement) {
        submitButton.disabled = false;
        submitButton.textContent = "Send Enquiry";
        submitButton.focus();
      }
    } finally {
      window.clearTimeout(timeout);
    }
  });
})();
