# Selfie Booth AI · Tutorials

Interactive tutorials for the Selfie Booth AI iOS app, shown at **selfieboothapp.com/tutorials**. Available in English, Spanish and French.

This repo holds only tutorial content. It contains no app code, keys or data.

## Structure

| Path | What it is |
|---|---|
| `index.html` | Tutorials section: app cover with the 360 spinner, chapter list, help |
| `viewer.html` | Full-screen guide viewer (top bar with back and EN/ES/FR) used by the website embed |
| `360/index.html` | 360 Photo Booth Guide: interactive, self-contained, EN/ES/FR |
| `assets/embed.js` | Script the website loads to show the section and open guides |
| `assets/cover-*.jpg` | App screens used on the cover |

## Website embed (WordPress page /tutorials)

```html
<div id="sbt-tutorials"></div>
<script src="https://tutorials.selfieboothapp.com/assets/embed.js" defer></script>
```

## Links

| Link | Opens |
|---|---|
| `selfieboothapp.com/tutorials` | Tutorials page |
| `selfieboothapp.com/tutorials#360` | Page with the 360 guide open |
| `selfieboothapp.com/tutorials#360.speed` | 360 guide open at a section |
| `tutorials.selfieboothapp.com/360/?lang=fr#speed` | Guide alone, in French, at a section |

Section ids: `create-event`, `select-features`, `screens`, `motion`, `camera`, `orientation`, `speed`, `overlays`, `audio`, `sharing`, `gallery`, `sharestation`, `datacapture`, `review`, `launch`, `eventgallery`, `quick`.

## Source files

Edit these, never the published files directly, then run `python3 src/build.py`:

| Source | Builds |
|---|---|
| `src/guide/template.html` (texts EN/ES/FR, pins, layout) + `src/guide/imgs.js` (screenshots) | `360/index.html` |
| `src/page/page.tpl.html` + `src/page/covers.json` | `index.html` |
| `src/page/embed.js`, `src/page/viewer.html` | `assets/embed.js`, `viewer.html` |

`page.tpl.html` is also the design preview: it includes a stand-in site header and footer that the build removes.

## Updating

Changes are made by editing these files and pushing to `main`. GitHub Pages republishes in about 1–2 minutes. Browsers may keep the old version for up to 10 minutes.
