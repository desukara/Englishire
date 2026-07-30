# Englishire × Eastokyo Brand Integrity Audit

## Canonical roles

- **Englishire** is the temporary English teacher-cover service for Tokyo schools.
- **Eastokyo Education Review** is Englishire's independent digital publication for the English-teaching profession in Tokyo and across Japan.
- The service and publication share ownership and visual ancestry, but they have different jobs and different primary routes.

## Canonical cross-site routes

### From Englishire

- Publication label: **Eastokyo Education Review**
- Publication destination: `https://eastokyo.com/`
- Retired visible label: **Englishire Journal** / **Journal**

### From Eastokyo

- Service label: **Englishire**
- General service destination: `https://englishire.com/`
- Teacher-cover request destination: `https://englishire.com/contact.html`
- Service process destination: `https://englishire.com/how-it-works.html`

## Header rules

### Englishire

The primary navigation should prioritise Teacher Cover, How It Works, Englishire standards/about, Eastokyo Education Review and the teacher-cover enquiry. Japanese pages should expose Eastokyo Education Review as the publication route rather than hiding the publishing relationship.

### Eastokyo

The publication masthead returns to the Eastokyo homepage. The canonical navigation vocabulary is:

1. Latest
2. Magazine
3. About
4. Contribute
5. Englishire

Contact and Editorial Policy remain prominent in the footer.

## Footer rules

### Englishire

The footer distinguishes service, company, publication and policy routes. Eastokyo Education Review is never labelled Journal.

### Eastokyo

The publication footer contains:

- Magazine
- About
- Contribute
- Editorial Policy
- Contact
- Request teacher cover through Englishire

Publisher language should state that Eastokyo is Englishire's independent digital magazine for the English-teaching profession.

## Shared-brand assets

- Englishire logo and favicon family remain the parent-brand assets.
- Eastokyo adds the publication name and descriptor; it does not revive the former standalone crow/travel identity.
- Eastokyo publication copy must not refer to hotels, restaurants, nightlife, travel recommendations or generic Tokyo culture coverage.

## Implementation in this pass

- `script.js` normalises retired Journal links and labels across Englishire's English pages.
- Japanese Englishire navigation and footer now include Eastokyo Education Review.
- Page metadata containing `Englishire Journal` is corrected at runtime.
- Eastokyo's shared magazine script normalises publication headers and footers across pages.
- Eastokyo's Genki2 guide copy has been rewritten for the English-teaching profession.

## Follow-up checks

Static source should gradually be updated to match the runtime normalisation, especially old `Journal` metadata and sitemap naming. Runtime normalisation protects the current user experience, but new files should use the canonical language directly.