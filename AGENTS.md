# Englishire repository guidance

These instructions apply throughout this repository. Direct instructions from the repository owner take precedence.

## Repository and publication

- Repository: `desukara/Englishire`.
- Default branch: `main`.
- Production website: `https://englishire.com`.
- Hosting: GitHub Pages, published from the root of `main`.
- Treat repository files as genuine source code. Never replace them with previews, mock-ups, WebViews, explanatory prose, placeholder files, abbreviated excerpts, or rendered output.
- Never store passwords, authentication tokens, email credentials, verification codes, or other secrets in the repository.

## Non-negotiable preservation rules

- Preserve every journal article word-for-word unless the repository owner expressly authorises a specific wording change.
- Do not make minute, stylistic, grammatical, punctuation, spelling, formatting, “clarifying”, or inferred editorial changes to journal article wording.
- Do not change, replace, regenerate, optimise, rename, delete, crop, recompress, or otherwise alter the Englishire logo or existing images unless expressly authorised.
- Do not delete pages, sections, scripts, navigation, metadata, structured data, accessibility content, asset references, or functionality merely to simplify a task.
- Preserve complete files and confirm that no large section has been truncated or accidentally removed.
- If a required image is unavailable, retain the existing image reference or layout unless the owner directs otherwise.

## Editorial and design standard

- Outside protected journal articles, maintain consistent British English, an English/London tone, restrained royal presentation, and the established Englishire voice.
- Preserve the existing visual identity and responsive behaviour across mobile, tablet, and desktop.
- Prefer precise corrections over broad redesigns.

## Required change workflow

1. Inspect the current `main` branch before editing.
2. Identify the smallest complete set of source files required.
3. Create a dedicated branch named `agent/<short-description>` unless the owner instructs otherwise.
4. Make complete, scoped source-code changes only.
5. Review the full diff against `main`.
6. Confirm that protected journal content, logos, images, and unrelated files are unchanged.
7. Check relevant HTML, CSS and JavaScript syntax; duplicate IDs; internal links; asset paths; metadata; canonical URLs; accessibility; responsive behaviour; and GitHub Pages path handling.
8. Open a pull request describing every changed file and the validation performed.
9. Merge only when the requested work is complete, safe, and within the authority granted by the owner.
10. Allow one final GitHub Pages deployment for the completed change and verify the production result. Avoid repeated edits to `main` that create competing or cancelled deployments.

## Contact system

- The public enquiry address is `info@englishire.com`.
- The contact form uses the authorised Formspree HTTPS backend and must retain secure submission, accessible success/error feedback, spam protection, and the existing privacy disclosure unless the owner directs a replacement.
- Do not expose the private forwarding destination address in public website source or content.
- Do not revert the form to a `mailto:` submission action.

## Communication

- Report the branch name, commit SHA, pull-request result, deployment status, files changed, files deliberately left unchanged, and any remaining concern.
- If repository access is missing, expired, revoked, or does not include this repository, say so plainly and request reconnection; never pretend that a write or deployment occurred.
