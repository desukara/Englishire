"use strict";
(() => {
  const correction = document.createElement("link");
  correction.rel = "stylesheet";
  correction.href = "emergency-contrast.css?v=20260720-2";
  document.head.append(correction);

  const originalScript = document.createElement("script");
  originalScript.src = "script-original.js?v=20260720-2";
  originalScript.async = false;
  document.head.append(originalScript);
})();
