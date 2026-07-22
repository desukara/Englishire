"use strict";

/**
 * Englishire
 * Homepage progressive enhancements
 *
 * The website remains usable when JavaScript is disabled.
 */

(() => {
  const html = document.documentElement;

  const reducedMotionQuery = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  );

  const finePointerQuery = window.matchMedia("(pointer: fine)");

  const desktopNavigationQuery = window.matchMedia("(min-width: 64rem)");

  html.classList.add("js-enabled");

  /**
   * Return an HTMLElement when the selector exists.
   *
   * @param {string} selector
   * @returns {HTMLElement | null}
   */
  const getElement = (selector) => {
    const element = document.querySelector(selector);

    return element instanceof HTMLElement ? element : null;
  };

  /**
   * Set the current year in the footer.
   */
  const setCurrentYear = () => {
    const yearElement = getElement("#englishire-current-year");

    if (!yearElement) {
      return;
    }

    yearElement.textContent = String(new Date().getFullYear());
  };

  /**
   * Initialise the responsive navigation menu.
   */
  const initialiseMobileNavigation = () => {
    const toggleButton = getElement("#englishire-mobile-nav-toggle");

    const navigation = getElement("#englishire-primary-navigation");

    if (!toggleButton || !navigation) {
      return;
    }

    const navigationLinks = Array.from(navigation.querySelectorAll("a"));

    const backgroundRegions = Array.from(
      document.querySelectorAll("main, footer")
    ).filter((region) => region instanceof HTMLElement);

    const previousInertStates = new Map();

    const menuIsOpen = () => {
      return toggleButton.getAttribute("aria-expanded") === "true";
    };

    /**
     * @param {boolean} open
     * @param {boolean} restoreFocus
     */
    const setMenuState = (open, restoreFocus = false) => {
      toggleButton.setAttribute("aria-expanded", String(open));

      navigation.classList.toggle("is-open", open);

      html.classList.toggle("navigation-open", open);

      backgroundRegions.forEach((region) => {
        if (open) {
          previousInertStates.set(region, region.inert);
          region.inert = true;
        } else {
          region.inert = previousInertStates.get(region) || false;
        }
      });

      if (!open) {
        previousInertStates.clear();
      }

      if (open) {
        const firstLink = navigationLinks[0];

        if (firstLink instanceof HTMLElement) {
          window.requestAnimationFrame(() => {
            firstLink.focus();
          });
        }
      }

      if (!open && restoreFocus) {
        toggleButton.focus();
      }
    };

    toggleButton.addEventListener("click", () => {
      setMenuState(!menuIsOpen());
    });

    navigation.addEventListener("click", (event) => {
      const eventTarget = event.target;

      const link =
        eventTarget instanceof Element ? eventTarget.closest("a") : null;

      if (link && !desktopNavigationQuery.matches) {
        setMenuState(false);
      }
    });

    document.addEventListener("click", (event) => {
      if (!menuIsOpen() || desktopNavigationQuery.matches) {
        return;
      }

      const eventTarget = event.target;

      if (!(eventTarget instanceof Node)) {
        return;
      }

      const clickedInsideNavigation = navigation.contains(eventTarget);

      const clickedToggle = toggleButton.contains(eventTarget);

      if (clickedInsideNavigation || clickedToggle) {
        return;
      }

      setMenuState(false);
    });

    document.addEventListener("keydown", (event) => {
      if (!menuIsOpen() || desktopNavigationQuery.matches) {
        return;
      }

      if (event.key === "Escape") {
        setMenuState(false, true);

        return;
      }

      if (event.key !== "Tab") {
        return;
      }

      const focusableElements = [toggleButton, ...navigationLinks].filter(
        (element) =>
          element instanceof HTMLElement &&
          !element.hasAttribute("disabled") &&
          element.getAttribute("aria-hidden") !== "true"
      );

      if (!focusableElements.length) {
        return;
      }

      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];

      if (event.shiftKey && document.activeElement === firstElement) {
        event.preventDefault();
        lastElement.focus();
      } else if (!event.shiftKey && document.activeElement === lastElement) {
        event.preventDefault();
        firstElement.focus();
      }
    });

    const handleDesktopChange = (event) => {
      if (event.matches) {
        setMenuState(false);
      }
    };

    if (typeof desktopNavigationQuery.addEventListener === "function") {
      desktopNavigationQuery.addEventListener("change", handleDesktopChange);
    } else {
      desktopNavigationQuery.addListener(handleDesktopChange);
    }
  };

  /**
   * Create the vertical reading progress bar.
   */
  const createReadingProgress = () => {
    if (document.querySelector(".englishire-progress")) {
      return;
    }

    const progressTrack = document.createElement("div");

    const progressBar = document.createElement("div");

    progressTrack.className = "englishire-progress";

    progressBar.className = "englishire-progress__bar";

    progressTrack.setAttribute("aria-hidden", "true");

    progressTrack.append(progressBar);
    document.body.append(progressTrack);

    let animationFrameRequested = false;

    const updateProgress = () => {
      const documentHeight = html.scrollHeight - html.clientHeight;

      const rawProgress =
        documentHeight > 0 ? window.scrollY / documentHeight : 0;

      const progress = Math.min(Math.max(rawProgress, 0), 1);

      progressBar.style.transform = `scaleY(${progress})`;

      animationFrameRequested = false;
    };

    const requestProgressUpdate = () => {
      if (animationFrameRequested) {
        return;
      }

      animationFrameRequested = true;

      window.requestAnimationFrame(updateProgress);
    };

    updateProgress();

    window.addEventListener("scroll", requestProgressUpdate, {
      passive: true,
    });

    window.addEventListener("resize", requestProgressUpdate, {
      passive: true,
    });

    window.addEventListener("load", requestProgressUpdate, {
      once: true,
    });
  };

  /**
   * Highlight the navigation link whose section is
   * currently visible.
   */
  const activateSectionNavigation = () => {
    if (!("IntersectionObserver" in window)) {
      return;
    }

    const navigationLinks = Array.from(
      document.querySelectorAll('#englishire-primary-navigation a[href^="#"]')
    ).filter((link) => link instanceof HTMLAnchorElement);

    if (!navigationLinks.length) {
      return;
    }

    const sectionEntries = navigationLinks
      .map((link) => {
        const selector = link.getAttribute("href");

        if (!selector || selector === "#") {
          return null;
        }

        let section = null;

        try {
          section = document.querySelector(selector);
        } catch (error) {
          return null;
        }

        if (!(section instanceof HTMLElement)) {
          return null;
        }

        return {
          link,
          section,
        };
      })
      .filter(Boolean);

    if (!sectionEntries.length) {
      return;
    }

    const sectionVisibility = new Map();

    const setActiveLink = (activeLink) => {
      navigationLinks.forEach((link) => {
        if (link === activeLink) {
          link.setAttribute("aria-current", "location");
        } else {
          link.removeAttribute("aria-current");
        }
      });
    };

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          sectionVisibility.set(entry.target, {
            isIntersecting: entry.isIntersecting,

            ratio: entry.intersectionRatio,

            top: entry.boundingClientRect.top,
          });
        });

        const visibleSections = sectionEntries
          .map(({ link, section }) => {
            const visibility = sectionVisibility.get(section) || {
              isIntersecting: false,
              ratio: 0,
              top: Number.POSITIVE_INFINITY,
            };

            return {
              link,
              section,
              ...visibility,
            };
          })
          .filter(({ isIntersecting }) => isIntersecting)
          .sort((first, second) => {
            if (second.ratio !== first.ratio) {
              return second.ratio - first.ratio;
            }

            return Math.abs(first.top) - Math.abs(second.top);
          });

        if (visibleSections.length) {
          setActiveLink(visibleSections[0].link);
        }
      },
      {
        rootMargin: "-18% 0px -58% 0px",

        threshold: [0.01, 0.15, 0.35, 0.6],
      }
    );

    sectionEntries.forEach(({ section }) => {
      observer.observe(section);
    });
  };

  /**
   * Calculate the combined height of the
   * announcement bar and site header.
   *
   * @returns {number}
   */
  const getHeaderOffset = () => {
    const announcementBar = getElement("#englishire-announcement-bar");

    const header = getElement("#englishire-site-header");

    const announcementHeight = announcementBar
      ? announcementBar.getBoundingClientRect().height
      : 0;

    const headerHeight = header ? header.getBoundingClientRect().height : 0;

    return announcementHeight + headerHeight + 18;
  };

  /**
   * Scroll to a section while accounting for the
   * header and announcement bar.
   *
   * @param {HTMLElement} target
   */
  const scrollToTarget = (target) => {
    const targetPosition =
      target.getBoundingClientRect().top + window.scrollY - getHeaderOffset();

    window.scrollTo({
      top: Math.max(targetPosition, 0),

      behavior: reducedMotionQuery.matches ? "auto" : "smooth",
    });
  };

  /**
   * Improve same-page anchor navigation.
   */
  const enhanceAnchorNavigation = () => {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach((link) => {
      link.addEventListener("click", (event) => {
        const selector = link.getAttribute("href");

        if (!selector || selector === "#") {
          return;
        }

        let target = null;

        try {
          target = document.querySelector(selector);
        } catch (error) {
          return;
        }

        if (!(target instanceof HTMLElement)) {
          return;
        }

        event.preventDefault();

        scrollToTarget(target);

        if (window.location.hash !== selector) {
          window.history.pushState(null, "", selector);
        }

        const temporaryTabIndex = !target.hasAttribute("tabindex");

        if (temporaryTabIndex) {
          target.setAttribute("tabindex", "-1");
        }

        const focusDelay = reducedMotionQuery.matches ? 0 : 450;

        window.setTimeout(() => {
          target.focus({
            preventScroll: true,
          });

          if (temporaryTabIndex) {
            target.addEventListener(
              "blur",
              () => {
                target.removeAttribute("tabindex");
              },
              {
                once: true,
              }
            );
          }
        }, focusDelay);
      });
    });

    window.addEventListener("popstate", () => {
      if (!window.location.hash) {
        return;
      }

      let target = null;

      try {
        target = document.querySelector(window.location.hash);
      } catch (error) {
        return;
      }

      if (target instanceof HTMLElement) {
        scrollToTarget(target);
      }
    });
  };

  /**
   * Add subtle movement to editorial images.
   */
  const enhanceImageMovement = () => {
    if (reducedMotionQuery.matches || !finePointerQuery.matches) {
      return;
    }

    const imageElements = document.querySelectorAll(
      [
        ".editorial-image--hero img",
        ".featured-story__media img",
        ".media-story__media img",
        ".article-hero__figure img",
        ".article-page .image-placeholder",
      ].join(", ")
    );

    imageElements.forEach((imageElement) => {
      if (!(imageElement instanceof HTMLElement)) {
        return;
      }

      imageElement.style.willChange = "transform";

      let pointerFrame = null;

      let latestPointerEvent = null;

      const handlePointerMove = (event) => {
        latestPointerEvent = event;

        if (pointerFrame !== null) {
          return;
        }

        pointerFrame = window.requestAnimationFrame(() => {
          const bounds = imageElement.getBoundingClientRect();

          if (!bounds.width || !bounds.height) {
            pointerFrame = null;

            return;
          }

          const horizontal =
            (latestPointerEvent.clientX - bounds.left) / bounds.width - 0.5;

          const vertical =
            (latestPointerEvent.clientY - bounds.top) / bounds.height - 0.5;

          const rotateX = vertical * -0.9;

          const rotateY = horizontal * 0.9;

          imageElement.style.transform =
            `perspective(1200px) ` +
            `rotateX(${rotateX}deg) ` +
            `rotateY(${rotateY}deg) ` +
            "scale(1.018)";

          pointerFrame = null;
        });
      };

      const resetImage = () => {
        if (pointerFrame !== null) {
          window.cancelAnimationFrame(pointerFrame);
          pointerFrame = null;
        }

        imageElement.style.transform =
          "perspective(1200px) " +
          "rotateX(0deg) " +
          "rotateY(0deg) " +
          "scale(1)";
      };

      imageElement.addEventListener("pointermove", handlePointerMove, {
        passive: true,
      });

      imageElement.addEventListener("pointerleave", resetImage);

      imageElement.addEventListener("pointercancel", resetImage);
    });
  };

  /**
   * Remove broken-image icons without inventing substitute imagery.
   * The surrounding layout returns to one useful text column when its
   * intended image is not present in the supplied archive.
   */
  const handleUnavailableImages = () => {
    const images = document.querySelectorAll("img");

    images.forEach((image) => {
      if (!(image instanceof HTMLImageElement)) {
        return;
      }

      const markUnavailable = () => {
        image.classList.add("is-image-unavailable");

        const mediaContainer = image.closest(
          [
            "figure",
            ".service-hero__media",
            ".featured-story__media",
            ".media-story__media",
            ".story-card__media",
            ".journal-feature__media",
            ".journal-case-study__media",
            ".homepage-publication__media",
            ".article-hero__figure",
          ].join(", ")
        );

        if (mediaContainer instanceof HTMLElement) {
          mediaContainer.classList.add("is-image-unavailable");
        }

        const mediaLayout = image.closest(
          [
            ".service-hero__layout",
            ".journal-feature__layout",
            ".journal-case-study__layout",
            ".journal-case-study",
            ".homepage-publication__layout",
            ".article-hero__layout",
            ".featured-story",
            ".media-story",
            ".story-card",
          ].join(", ")
        );

        if (mediaLayout instanceof HTMLElement) {
          mediaLayout.classList.add("has-missing-media");
        }
      };

      image.addEventListener("error", markUnavailable, {
        once: true,
      });

      if (image.complete && image.naturalWidth === 0) {
        markUnavailable();
      }
    });
  };

  /**
   * Submit the enquiry securely to Formspree and continue only after
   * the service confirms that it has accepted the submission.
   */
  const initialiseEmailEnquiryForm = () => {
    const form = getElement("#englishire-email-enquiry-form");

    if (!(form instanceof HTMLFormElement)) {
      return;
    }

    const status = getElement("#englishire-email-enquiry-status");
    const submitButton = form.querySelector('button[type="submit"]');

    form.addEventListener("submit", async (event) => {
      event.preventDefault();

      if (!form.reportValidity()) {
        if (status) {
          status.textContent =
            "Kindly complete the required fields before sending your enquiry.";
        }

        return;
      }

      if (status) {
        status.textContent = "Your enquiry is being sent securely.";
      }

      form.setAttribute("aria-busy", "true");

      if (submitButton instanceof HTMLButtonElement) {
        submitButton.disabled = true;
        submitButton.textContent = "Sending…";
      }

      try {
        const response = await fetch(form.action, {
          method: "POST",
          body: new FormData(form),
          headers: {
            Accept: "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("The enquiry service did not accept the submission.");
        }

        window.location.assign("thank-you.html");
      } catch (error) {
        if (status) {
          status.textContent =
            "We could not send your enquiry just now. Kindly try again or email info@englishire.com directly.";
        }

        form.removeAttribute("aria-busy");

        if (submitButton instanceof HTMLButtonElement) {
          submitButton.disabled = false;
          submitButton.textContent = "Send Enquiry";
        }
      }
    });
  };

  /**
   * Keep only one FAQ item open at a time.
   */
  const enhanceFAQs = () => {
    const faqItems = Array.from(
      document.querySelectorAll(".frequently-asked .faq-item")
    ).filter((item) => item instanceof HTMLDetailsElement);

    if (!faqItems.length) {
      return;
    }

    faqItems.forEach((item) => {
      item.addEventListener("toggle", () => {
        if (!item.open) {
          return;
        }

        faqItems.forEach((otherItem) => {
          if (otherItem !== item) {
            otherItem.open = false;
          }
        });
      });
    });
  };

  /**
   * Add restrained transitions between local pages.
   */
  const enablePageTransitions = () => {
    if (
      reducedMotionQuery.matches ||
      typeof document.body.animate !== "function"
    ) {
      return;
    }

    let navigationStarted = false;

    let pageTransitionAnimation = null;

    document.addEventListener("click", (event) => {
      const eventTarget = event.target;

      const link =
        eventTarget instanceof Element
          ? eventTarget.closest("a[href]")
          : null;

      if (!(link instanceof HTMLAnchorElement)) {
        return;
      }

      if (
        event.defaultPrevented ||
        navigationStarted ||
        event.button !== 0 ||
        event.metaKey ||
        event.ctrlKey ||
        event.shiftKey ||
        event.altKey ||
        link.hasAttribute("download") ||
        link.target === "_blank" ||
        link.hasAttribute("data-no-transition")
      ) {
        return;
      }

      const destination = new URL(link.href, window.location.href);

      const current = new URL(window.location.href);

      const sameDocument =
        destination.origin === current.origin &&
        destination.pathname === current.pathname &&
        destination.search === current.search;

      const samePageHash = sameDocument && Boolean(destination.hash);

      const localDocument =
        destination.origin === current.origin &&
        !samePageHash &&
        destination.protocol !== "mailto:" &&
        destination.protocol !== "tel:";

      if (!localDocument) {
        return;
      }

      event.preventDefault();

      navigationStarted = true;

      const animation = document.body.animate(
        [
          {
            opacity: 1,
            transform: "translateY(0)",
          },
          {
            opacity: 0,
            transform: "translateY(-7px)",
          },
        ],
        {
          duration: 230,

          easing: "cubic-bezier(0.4, 0, 1, 1)",

          fill: "forwards",
        }
      );

      pageTransitionAnimation = animation;

      animation.addEventListener(
        "finish",
        () => {
          window.location.assign(destination.href);
        },
        {
          once: true,
        }
      );

      animation.addEventListener(
        "cancel",
        () => {
          navigationStarted = false;
        },
        {
          once: true,
        }
      );
    });

    window.addEventListener("pageshow", () => {
      navigationStarted = false;

      if (pageTransitionAnimation) {
        pageTransitionAnimation.cancel();
        pageTransitionAnimation = null;
      }

      document.body.getAnimations().forEach((animation) => {
        const effectTarget = animation.effect ? animation.effect.target : null;

        if (effectTarget === document.body) {
          animation.cancel();
        }
      });

      document.body.style.removeProperty("opacity");

      document.body.style.removeProperty("transform");
    });
  };

  /**
   * Ensure links opening a new tab use safe rel values.
   */
  const secureExternalLinks = () => {
    const externalLinks = document.querySelectorAll('a[target="_blank"]');

    externalLinks.forEach((link) => {
      const relValues = new Set(
        (link.getAttribute("rel") || "").split(/\s+/).filter(Boolean)
      );

      relValues.add("noopener");
      relValues.add("noreferrer");

      link.setAttribute("rel", Array.from(relValues).join(" "));
    });
  };

  /**
   * Update the reading progress when images and
   * page sections change the document height.
   */
  const observePageHeight = () => {
    if (!("ResizeObserver" in window)) {
      return;
    }

    let resizeFrame = null;

    const resizeObserver = new ResizeObserver(() => {
      if (resizeFrame !== null) {
        window.cancelAnimationFrame(resizeFrame);
      }

      resizeFrame = window.requestAnimationFrame(() => {
        window.dispatchEvent(new Event("resize"));

        resizeFrame = null;
      });
    });

    resizeObserver.observe(document.body);
  };

  /**
   * Correct the initial position when the page
   * loads with a section hash.
   */
  const handleInitialHash = () => {
    if (!window.location.hash) {
      return;
    }

    let target = null;

    try {
      target = document.querySelector(window.location.hash);
    } catch (error) {
      return;
    }

    if (!(target instanceof HTMLElement)) {
      return;
    }

    window.setTimeout(() => {
      scrollToTarget(target);
    }, 100);
  };

  /**
   * Initialise all enhancements.
   */
  const initialise = () => {
    setCurrentYear();
    initialiseMobileNavigation();
    createReadingProgress();
    activateSectionNavigation();
    enhanceAnchorNavigation();
    enhanceImageMovement();
    enhanceFAQs();
    handleUnavailableImages();
    initialiseEmailEnquiryForm();
    enablePageTransitions();
    secureExternalLinks();
    observePageHeight();
    handleInitialHash();
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialise, {
      once: true,
    });
  } else {
    initialise();
  }
})();
