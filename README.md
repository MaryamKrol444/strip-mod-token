# OpenRoom — independent field notes

A complete, non-explicit, adult-only static editorial site. The repository contains **nine finished HTML documents**, shared local assets, an XML sitemap and indexing-friendly robots.txt. No framework, database, analytics, account collection or production Node runtime is required.

## GitHub Pages deployment

Polska instrukcja: **[WDROZENIE.md](WDROZENIE.md)**.

The `.github/workflows/pages.yml` workflow builds and deploys the public-only `.site/` artifact from `arena/385c2232-strip-mod-token`. It reads the actual address from GitHub Pages, supports the `/strip-mod-token/` project prefix, runs structural checks and deploys via Actions. An administrator must first choose **Settings → Pages → Source: GitHub Actions**; the connected integration received HTTP 403 when attempting to enable Pages. The target address is `https://maryamkrol444.github.io/strip-mod-token/`; check Actions for actual deployment status.

`SITE_URL` accepts an HTTPS origin **or** an origin plus project path. Local checked-in HTML continues to use root paths and `example.com`; the deployment build replaces these with the actual Pages address, including canonical, OG, sitemap and internal/asset paths. No fictional domain is published by the workflow.

## Public files

| URL | HTML file | Original article words* | Images | FAQs | External resource CTAs |
| --- | --- | ---: | ---: | ---: | ---: |
| `/` | `index.html` | 3,000+ | 5 | 8 | 2 |
| `/stripchat-token-generator/` | `stripchat-token-generator/index.html` | 3,000+ | 5 | 8 | 4 |
| `/stripchat-live/` | `stripchat-live/index.html` | 3,000+ | 5 | 8 | 1 |
| `/strip-chat-sites/` | `strip-chat-sites/index.html` | 3,000+ | 5 | 8 | 4 |
| Supporting | `about/`, `contact/`, `privacy-policy/`, `terms/`, `disclaimer/` | Short publication policies | — | — | — |

\* Checked from original Markdown, excluding common source notes, disclosure, video warning, author box and navigation. The generated `content-manifest.json` counts total rendered article material, so its figures are higher.

Run `.venv/bin/python scripts/package_site.py` to create the downloadable `openroom-html.zip` bundle (ignored by Git). It contains only public files plus launch and audit notes; rebuild and repackage after configuring the production domain.

Also deploy `assets/`, `sitemap.xml` and `robots.txt`. Each HTML document is complete and readable without JavaScript; CSS and images are shared local files. Clean directory routes work with ordinary static hosting.

## Editorial decisions and exceptions

Read **[LINK_AUDIT.md](LINK_AUDIT.md)** before changing CTAs.

- Official giveaway rules were checked on **15 October 2026**. Registration is not a guaranteed award. No universal first-purchase bonus, permanent crypto bonus or authenticated three-platform price list was verified, so none is presented as fact.
- Two supplied articles were excluded for misleading promotional assurances. The supplied `spy-mode` URL was also excluded because it literally contains `mod`, prohibited by the URL rule. No replacement URLs were introduced. Consequently the homepage and live guide have fewer than the requested 3–4 CTAs; the link-quality and URL exclusions take precedence.
- The supplied YouTube video advertises “unlimited” tokens. It appears on each main guide **only as a clearly rebutted promotional claim for critical review**. It is not advice, evidence or an endorsed token method. An explicit warning precedes a click-to-load privacy-enhanced player. Nothing contacts YouTube before the reader opts in, and there is no autoplay.
- The editorial byline is an **organization**, not a fabricated person. There are no invented credentials, firsthand tests, testimonials, quotes, statistics or star ratings. AI-assisted authorship and limits are disclosed.
- External commercial resource buttons conservatively use `rel="sponsored nofollow noopener"`, context text and a new-tab announcement. No actual affiliate account or commission agreement was supplied; the disclosure does not invent one.
- Illustrations are original, non-explicit diagrams and conceptual UI mockups, explicitly labeled **not platform screenshots**. All 20 article images are WebP, lazy-loaded and have accurate intrinsic dimensions and descriptive alt text. The social image is also original.

## Preview

```sh
python3 scripts/serve.py
# 0.0.0.0:3000; use PORT=... to change the port
```

This server accepts the preview proxy host, uses relative asset paths, permits embedding in Arena and serves **only public site paths**. It does not expose `.git`, Markdown, tests, package files or directory listings. It supplies security headers and disables camera/microphone access on this information site. Use a production static host for launch.

## Editing and rebuilding

Generated HTML is checked in as requested. Edit `content/*.md` for the four articles; shared layout, metadata, source notes and supporting-page text live in `scripts/build.py`. Edit `assets/styles.css` for appearance and `assets/video.js` for the opt-in player.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py
```

No network is needed to render the pages after installing dependencies. To regenerate the checked-in illustrations:

```sh
.venv/bin/python scripts/make_images.py
```

The illustration script uses DejaVu fonts under `/usr/share/fonts/truetype/dejavu/`; adapt those paths on another OS. Font binaries are not downloaded by visitors.

## Required before production launch

1. **Supply the real domain.** No production origin was provided. The checked-in canonical, OG and sitemap origin is deliberately `https://example.com`, not an invented live domain. Rebuild with the real origin:

   ```sh
   SITE_URL=https://your-real-domain.tld .venv/bin/python scripts/build.py
   SITE_URL=https://your-real-domain.tld .venv/bin/python tests/check_site.py
   ```

2. **Add verified publisher details** to supporting policies: legal identity, private privacy/contact route, hosting/log retention practices, and any jurisdiction-specific information. No fake email, street address or data controller has been inserted. The current public correction route uses the repository's enabled GitHub issues; it must never receive private information. Policies explicitly disclose these limits and need publisher/legal review before launch.
3. Recheck external resources, official terms and the promotion. The audit is a dated text review, not continuous monitoring or a malware certification. Reassess the supplied video if it changes; it must never become an endorsed unlimited-credit claim.
4. Confirm the actual commercial/affiliate relationships and update the disclosure if applicable.
5. Upload **only** the public files listed above. Do not publish the repository as a whole. Configure appropriate security and cache headers at the host; preserve the no-tracking, opt-in video behavior.

## Validation

```sh
.venv/bin/python tests/check_site.py
npm ci                          # development-only browser tools
npm run test:browser             # start the preview first
```

The deterministic test covers all nine documents: title/description limits, one H1, heading hierarchy, canonical/OG values, local links and fragments, TOC coverage, original word counts, intrinsic WebP dimensions, approved CTA counts/attributes/URL restrictions, contextual crosslinks, visible/schema FAQ parity, Article author/date, source notes, video template, robots and sitemap.

Browser checks use npm-packaged Chromium (no separate browser download), Playwright and axe-core. They inspect all nine pages at **1440px and 390px**, check horizontal overflow, WCAG A/AA automated rules, keyboard skip links, image decoding, TOC behavior, third-party requests before consent, opt-in playback creation, no-JavaScript content and private-file denial. The player request is intercepted in QA; playback availability on YouTube is **not** certified. Local screenshots go to ignored `.cache/qa/`.

Automated axe results are not a full manual accessibility certification. No field Core Web Vitals or Lighthouse score is claimed. The implementation uses system fonts, small shared CSS, 20 small WebPs across four pages, no framework and a tiny optional-player script to keep the baseline light. FAQPage markup matches visible answers; search engines decide eligibility for rich results and no rich-result placement is promised.
