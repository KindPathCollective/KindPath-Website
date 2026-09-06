# KindPath Collective — Public Website

Static site for KindPath Collective Inc: an NDIS advocacy and support
service based on Bundjalung Country, Northern NSW.

## Structure

- `content/policies/*.md` — source text for each practice-standard/policy
  page, extracted from the organisation's governance folio. Edit these,
  not the generated HTML.
- `build.py` — static site generator. Regenerates every `.html` file from
  the templates and content in this script plus `content/policies/`.
- `assets/` — logo and stylesheet.
- `policies/` — generated policy pages (do not hand-edit; rebuild instead).
- `index.html`, `about.html`, `services.html`, `contact.html` — generated
  top-level pages (do not hand-edit; rebuild instead).

## Editing content

Home/About/Services/Contact copy lives directly in `build.py` (see the
`build_home`, `build_about`, `build_services`, `build_contact` functions).
Policy copy lives in `content/policies/*.md` — edit the markdown, then
rebuild.

## Building

```bash
python build.py
```

Regenerates all HTML from the current content. No other build step or
dependency beyond `pip install markdown`.

## Previewing locally

```bash
python -m http.server 8090
```

Then open http://localhost:8090.

## Deploying

This is plain static HTML/CSS with no server-side dependency — deploy the
whole repo root to any static host (GitHub Pages, Netlify, Cloudflare
Pages, etc.).

## Content provenance note

The policy pages are drawn from KindPath Collective's internal governance
folio (Phase 1). As of this site's creation, KindPath Collective Inc is
still working toward NDIS Quality and Safeguards Commission registration;
supports are currently delivered by the founders as sole traders. The
policy pages are deliberately framed as "the practice standard we operate
to now, in preparation for registration" rather than a claim of current
registration — keep that framing if you update this content, until
registration is actually complete.
