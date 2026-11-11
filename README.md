# Grey Creatives Design

Branding and graphic design portfolio. Plain HTML, CSS and JavaScript. No build step to deploy.

## Pages
- `index.html` Home (hero, open book of identities, logo globe, services, process, contact)
- `work.html` All brand identities, with filters
- `work/<brand>.html` One page per brand, with the full gallery
- `logos.html` Logo-only page (globe + pinboard), the one to send to logo-only clients
- `404.html`

## Deploy (GitHub + Vercel)
Vercel settings: Framework preset "Other", no build command, no output directory. `vercel.json` turns on clean URLs.

```bash
cd grey-creatives-design
git init
git add .
git commit -m "Grey Creatives Design portfolio"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/grey-creatives-design.git
git push -u origin main
```

Later changes:

```bash
git add .
git commit -m "Describe your change"
git push
```

## Things to set after the first deploy
- Your live address is assumed to be `https://greycreativesdesign.vercel.app`. If Vercel gives you a different one, use Find and Replace in VS Code (Ctrl+Shift+H) to swap `greycreativesdesign.vercel.app` for the real domain in every file. This is what makes the link preview image work.
- The footer links to your studio site at `https://greycreatives.vercel.app/`. Change or remove it in `_tools/build.py` (STUDIO_URL) or directly in the HTML.

## Editing
- Colours, fonts and spacing: `assets/css/site.css` (the tokens are at the top).
- Brand text, galleries, palettes, services, process: `_tools/projects.json`.
- Header, footer and the brand pages are generated from `_tools/build.py` so they stay identical. If you have Python, run `python3 _tools/build.py` after editing the JSON. If not, edit the HTML files directly; they are plain HTML.
- Add a brand: put its images in `assets/img/projects/<slug>/01.webp, 02.webp...`, add an entry to `projects.json`, then run the build script.
