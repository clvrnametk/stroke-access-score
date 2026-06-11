# Stroke Access Score — Design System

A complete token and component reference for the Stroke Access Score project. All values are drawn directly from the production codebase (`web/*.html`).

---

## 1. Design Tokens

### Color Palette

| Token | Hex | Usage |
|---|---|---|
| `--navy` | `#0f0f3c` | Primary brand color. Nav background, headings on light, dark section backgrounds |
| `--pink` | `#e10087` | Primary accent. CTAs, stat numbers, active states, highlights |
| `--bg` | `#f5f4f8` | Page background (off-white with slight purple tint) |
| `--text` | `#3c3c5a` | Body copy on light backgrounds |
| `--divider` | `#e0e0ec` | Borders, table rules, card separators |
| `--white` | `#ffffff` | Card backgrounds, inverted text |

**Extended palette (not tokenized but used consistently):**

| Hex | Usage |
|---|---|
| `#0a0a2e` | Stats strip background — darker than navy |
| `#1e1e60` | Subtle lighter navy, used for footer divider stroke |
| `#c2006e` | Pink hover state (darkened `--pink`) |
| `rgba(255,255,255,.05–.20)` | Frosted overlays on dark backgrounds at various opacities |

---

### Layout Widths

| Token | Value | Used on |
|---|---|---|
| `--page-width` | `1200px` | All pages — outer container max-width |
| `--content-width` | `960px` | About + Changelog — body copy column |

**Pattern:** All sections use `max-width: var(--page-width); margin: 0 auto;` centered in the viewport. Long-form reading pages additionally constrain their body to `--content-width` for comfortable line length.

---

### Spacing Scale

The project uses a loose 8px base grid. Common values:

| Value | Usage |
|---|---|
| `4px` | Tight gaps (nav link gaps: `gap: 4px`) |
| `8px` | Icon padding, compact inner spacing |
| `12px` | Card inner padding (compact) |
| `16px` | Mobile hero content padding, inner card spacing |
| `20px` | Button padding, card padding |
| `24px` | Standard section horizontal padding (all pages) |
| `28px` | Section heading bottom margin |
| `32px` | Button bottom margin |
| `40px` | Region toggle spacing, larger gaps |
| `56px` | Nav height, CTA bottom margin, section padding top/bottom |
| `64px` | About body top padding |
| `72px` / `80px` | Standard section vertical padding (`padding: 72px 24px 80px`) |
| `120px` | Map CTA hero section vertical padding |

---

### Z-Index Scale

| Value | Element |
|---|---|
| `0` | Pseudo-element overlays (`::before`, `::after`) |
| `1` | Content above overlays (`.hero > *`) |
| `400–500` | Sticky nav (`z-index: 500`) |
| `499` | Mobile nav drawer |
| `700` | Map detail card |
| `800` | Map legend, zoom controls |
| `9000` | Loading overlay, error panel |

---

## 2. Typography

### Typefaces

| Role | Family | Weights | Source |
|---|---|---|---|
| **Display / Headings** | Roboto Slab | 700 | Google Fonts |
| **Body / UI** | Roboto | 400, 500 | Google Fonts |

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@700&family=Roboto:wght@400;500&display=swap">
```

### Type Scale

All heading sizes use `clamp()` for fluid responsiveness: `clamp(min, vw-value, max)`.

| Element | Size (clamp) | Family | Weight | Line Height |
|---|---|---|---|---|
| Hero H1 (desktop) | `clamp(1.92rem, 5.2vw, 4rem)` | Roboto Slab | 700 | 1.1 |
| Hero H1 (mobile ≤768px) | `4rem` | Roboto Slab | 700 | 1.1 |
| Hero H1 (mobile ≤430px) | `2.4rem` | Roboto Slab | 700 | 1.1 |
| Impact number inline | `1.25em` of parent H1 | Roboto Slab | 700 | — |
| Page hero H1 (About/CL) | `clamp(2rem, 4vw, 3rem)` | Roboto Slab | 700 | 1.1 |
| Section H2 | `clamp(1.3rem, 3vw, 1.8rem)` | Roboto Slab | 700 | — |
| Section H2 (Findings) | `clamp(1.5rem, 3vw, 2.1rem)` | Roboto Slab | 700 | — |
| Large stat number | `clamp(2rem, 3vw, 2.8rem)` | Roboto Slab | 700 | 1 |
| Body copy | `0.97rem` / `1rem` | Roboto | 400 | 1.6 |
| Small body | `0.86rem–0.9rem` | Roboto | 400 | 1.5 |
| **Section label** (eyebrow) | `10px`, uppercase, tracking `2px` | Roboto | 700 | — |
| Nav links | `0.9rem` | Roboto | 500 | — |
| Button text | `0.9rem–1rem` | Roboto | 500 | — |
| Caption / meta | `0.82rem–0.85rem` | Roboto | 400 | — |

### Section Label Pattern

Used as an eyebrow above headings throughout the site:

```css
.section-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--pink);
  margin-bottom: 10px;
  display: block;
}
```

---

## 3. Color System — Semantic

### Score Tiers (SAS Score 0–100)

These colors are used consistently across the map choropleth, data table badges, and access level pills.

| Tier | Score Range | Map Color | Badge BG | Badge Text |
|---|---|---|---|---|
| Very Limited | 0–24 | `#d7191c` | `#fde8e8` | `#9b1c1c` |
| Limited | 25–40 | `#f07b4f` | `#fdf0e8` | `#9a3412` |
| Moderate-Low | 41–55 | `#fec44f` | `#fef9e7` | `#92400e` |
| Moderate | 56–70 | `#a6d96a` | `#f3f9e8` | `#3a5c1a` |
| Good | 71–85 | `#4dac26` | `#e8f5e9` | `#2d6a1e` |
| Strong | 86–100 | `#1a7837` | `#e0f0e5` | `#1a5c30` |

### Hospital Certification Badges

| Level | Background | Usage |
|---|---|---|
| CSC | `#c0392b` (red) | Comprehensive Stroke Center |
| PSC | `#1d6fa4` (blue) | Primary Stroke Center |
| ASRH | `#6b7280` (grey) | Acute Stroke Ready Hospital |
| TSC | `#7c3aed` (purple) | Thrombectomy (legacy, removed from scoring) |

### Vulnerability Flags

| Flag | Color |
|---|---|
| Double Jeopardy | `#8b0000` (dark red) |
| SEV — Socioeconomic Vulnerability | `#e10087` (pink = `--pink`) |
| CRF — Clinical Risk | `#e67e22` (orange) |

---

## 4. Components

### Navigation Bar

- **Height:** 56px, `position: sticky; top: 0; z-index: 500`
- **Background:** `var(--navy)`, transitions to transparent on homepage hero (scroll-driven, fades to solid within 60px of scroll)
- **Logo:** Roboto Slab 700, 1.05rem, white
- **Links:** Absolutely centered (`left: 50%; transform: translateX(-50%); top: 0; bottom: 0`), Roboto 500 0.9rem, `rgba(255,255,255,.75)` → white on hover, `border-bottom: 2px solid var(--pink)` on active/hover
- **Mobile (≤768px):** Nav links hidden, hamburger shown. Mobile drawer slides in below nav at `top: 56px`

```css
nav {
  height: 56px;
  position: sticky; top: 0; z-index: 500;
  background: var(--navy);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 24px;
}
```

---

### Buttons

**Base button** — no border-radius (global reset: `border-radius: 0 !important`):

```css
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  padding: 0 20px; height: 44px;
  font-family: 'Roboto', sans-serif; font-size: .9rem; font-weight: 500;
  border: 2px solid currentColor; cursor: pointer;
}
```

| Variant | Background | Border | Text | Hover |
|---|---|---|---|---|
| `.btn-primary` | `var(--pink)` | `var(--pink)` | `#fff` | `bg: #c2006e` |
| `.btn-outline` | transparent | `rgba(255,255,255,.4)` | `rgba(255,255,255,.85)` | `border: #fff, bg: rgba(255,255,255,.08)` |
| `.btn-map-cta` (large) | `#fff` | `#fff` | `var(--navy)` | `bg: transparent, text: #fff` |

**ZIP Search button** — pill shape (exception: `border-radius: 999px !important` overrides global reset):

```css
.zip-search-btn {
  padding: 10px 26px;
  background: var(--pink); color: #fff; border: none;
  border-radius: 999px !important;
  font-weight: 500; font-size: .95rem;
}
```

**Model toggle pills** — same pill exception pattern, semi-transparent container:

```css
.model-toggle { background: rgba(255,255,255,.12); border-radius: 999px !important; padding: 3px; }
.model-btn { height: 27px; padding: 0 13px; border-radius: 999px !important; }
.model-btn.active { background: #fff; color: var(--navy); }
```

---

### Cards

**Findings card (light background):**

```css
.fcard {
  background: #fff; padding: 24px;
  border: 1px solid var(--divider);
  border-top: 3px solid var(--navy);
}
```

**Critical Findings card (dark background):**

```css
.cf-item {
  background: rgba(255,255,255,.05); padding: 24px;
  border: 1px solid rgba(255,255,255,.1);
  border-top: 3px solid var(--pink);
}
```

**Stat box (dark strip):**

```css
.stat-box {
  flex: 1 1 180px; min-width: 140px; max-width: 220px;
  border: 2px solid rgba(255,255,255,.2); padding: 20px;
  background: rgba(255,255,255,.05);
}
```

---

### Badges / Pills

**Score badge** (table): tinted background + matching dark text (see Score Tiers table above)

**Access level pill** (table): solid background + white or dark text:

```css
.access-pill {
  display: inline-block; padding: 2px 9px;
  font-size: .74rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: .5px;
}
```

**Hospital cert badge** (map + table): solid color + white text:

```css
.fac-badge { padding: 2px 8px; font-size: .68rem; font-weight: 700; letter-spacing: .8px; }
.fac-badge.csc  { background: #c0392b; color: #fff; }
.fac-badge.psc  { background: #1d6fa4; color: #fff; }
```

---

### Section Label (Eyebrow)

Used above section headings on all pages:

```html
<span class="section-label">About This Project</span>
<h2>Heading</h2>
```

```css
/* 10px — uppercase — tracked — pink */
font-size: 10px; font-weight: 700; text-transform: uppercase;
letter-spacing: 2px; color: var(--pink);
```

---

## 5. Layout Structure

### Global Reset

```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0; padding: 0;
  border-radius: 0 !important; /* intentional — rounded shapes require explicit override */
}
html {
  scroll-behavior: smooth;
  overflow-x: clip;
  background: #0f0f3c; /* nav color shows during iOS rubber-band overscroll */
  scrollbar-gutter: stable; /* prevents nav shift when scrollbar appears/disappears */
}
body {
  font-family: 'Roboto', sans-serif;
  color: var(--text); background: var(--bg);
  font-size: 16px; line-height: 1.5;
  overflow-x: clip;
}
```

> **Note on `border-radius: 0 !important`:** This is intentional and project-wide. Any component that requires rounded corners (pills, circles, spinners) must use `border-radius: Xpx !important` to override it.

---

### Page Container Pattern

Every page centers its content using a max-width container:

```css
/* Data / Home — wider layout */
.inner, .hero-inner, .controls, .table-outer {
  max-width: var(--page-width); /* 1200px */
  margin: 0 auto;
  padding: 0 24px; /* consistent horizontal gutters */
}

/* About / Changelog — reading-width body */
.about-body, .cl-body {
  max-width: var(--content-width); /* 960px */
  margin: 0 auto;
  padding: 64px 24px 80px;
}
```

---

### Section Anatomy

Standard section structure used on all content pages:

```
[Full-width dark section]          ← hero/banner, background: var(--navy)
  └─ .inner (max-width centered)
       └─ .section-label (eyebrow)
       └─ h1/h2
       └─ p.summary

[Full-width light/dark strip]      ← stats strip, background: #0a0a2e
  └─ .inner (max-width centered)

[Full-width body section]          ← content, background: var(--bg) or #fff
  └─ .inner/.about-body (centered, narrower for reading pages)
```

Standard section vertical padding: `72px 24px 80px` (top/bottom varies by section importance).

---

### Map Page Layout

The map page uses a different layout model — fully fixed, no scroll:

```css
html, body { overflow-x: hidden; scrollbar-gutter: stable; }
nav { position: sticky; top: 0; height: 56px; z-index: 500; }
#map-shell {
  position: fixed;
  top: 56px; left: 0; right: 0; bottom: 0;
  z-index: 0;
}
#detail-card {
  position: absolute;
  top: 136px; left: 16px; width: 380px;
  max-height: calc(100% - 152px);
  z-index: 700;
}
```

---

## 6. Responsive Breakpoints

| Breakpoint | Key behaviors |
|---|---|
| `≤ 900px` | 3-col findings grid → 2-col; critical findings row → 1-col |
| `≤ 768px` | Desktop nav hidden → hamburger + mobile drawer; model toggle hidden in nav (appears in drawer); hero switches to portrait background image; hero content inset `padding: 0 16px` on text; zip-search stretches full width |
| `≤ 600px` | Findings grid → 1-col; footer stacks |
| `≤ 480px` | Stat boxes → column layout; hero padding reduces to `44px 16px`; zip-search input + button stack vertically; zip-search-inner `border-radius: 16px !important` |
| `≤ 430px` | Hero h1 further reduced; stat box `max-width: 300px` removed |

### Mobile Hero (≤768px)

```css
.hero {
  background-image: url('./home-hero-bg-5-mobile.png'); /* portrait image */
  background-position: bottom center;
}
.hero::before { background: rgba(15,15,60,.38); } /* lighter overlay — image shows through */
.hero h1 { font-size: 4rem; padding: 0 16px; }
.impact-inline { font-size: 5rem; }
.hero .subhead { font-size: .85rem; padding: 0 16px; }
```

---

## 7. Background / Overlay Patterns

### Hero Sections

Dark section backgrounds with a `::before` overlay pattern:

```css
.hero {
  position: relative;
  background: var(--navy) url('./image.png') center / cover no-repeat;
}
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background: rgba(15,15,60,.60); /* 60% opacity navy overlay */
  pointer-events: none; z-index: 0;
}
.hero > * { position: relative; z-index: 1; } /* lift content above overlay */
```

### Map Background Section

Uses a directional gradient for text legibility on the left while showing the image on the right:

```css
.map-cta-section::before {
  background: linear-gradient(
    to right,
    rgba(15,15,60,.60) 0%,
    rgba(15,15,60,.60) 45%,
    rgba(15,15,60,.35) 100%
  );
}
```

### Homepage Transparent Nav

Nav fades from transparent to `#0f0f3c` over the first 60px of scroll (scroll-driven, not CSS transition):

```js
function syncNavBg() {
  const opacity = Math.min(window.scrollY / 60, 1);
  nav.style.backgroundColor = opacity >= 1
    ? '#0f0f3c'
    : `rgba(15,15,60,${opacity.toFixed(3)})`;
}
window.addEventListener('scroll', syncNavBg, { passive: true });
```

---

## 8. Iconography & Visual Language

- **No icon font** — SVG inline only
- **Share icon:** Box-with-arrow-up (standard iOS/Android share metaphor), 14–15px
- **Search icon:** Magnifying glass via inline SVG in input fields
- **Hospital markers on map:** Leaflet `circleMarker` — CSC: radius 9, red `#c0392b`; PSC: radius 7, blue `#1d6fa4`
- **Arrows:** Plain text `→` used in CTAs and links

---

## 9. Animation & Transition

The project uses minimal animation, preferring instant or near-instant transitions:

| Element | Transition |
|---|---|
| Nav links | `color .2s, border-color .2s` |
| Buttons | `background .15s` |
| Nav background (homepage) | Scroll-driven (no CSS transition) |
| Detail card (map) | `transform .32s cubic-bezier(.4,0,.2,1)` slide-in |
| Loading overlay fade | `opacity .4s` |
| Model toggle pills | `background .15s, color .15s` |

> Rule of thumb: interaction feedback ≤ 0.2s, panel reveals ≤ 0.35s, loading fades ≤ 0.5s.

---

## 10. Accessibility Notes

- **Minimum touch target:** 44×44px (hamburger, drawer links)
- **Focus states:** Inherited from browser defaults — not explicitly styled
- **Color contrast:** All text on `--navy` uses white or near-white. Text on `--bg` uses `--text` (`#3c3c5a`). Score tier text-on-tinted-background passes AA
- **`aria-label`:** Used on hamburger, share buttons, model toggle
- **`scrollbar-gutter: stable`:** Prevents layout shift when scrollbar appears (all pages)
- **`pointer-events: none`:** Applied to all `::before`/`::after` overlays so they don't intercept clicks

---

## 11. Key Implementation Notes

### Border Radius Override Pattern

The global `border-radius: 0 !important` reset means ALL rounded shapes need explicit override:

```css
/* Pill shapes */
border-radius: 999px !important;

/* Cards on map */
border-radius: var(--r-card); /* 24px, defined in map.html :root */

/* Small rounded elements */
border-radius: var(--r-sm); /* 12px */
```

### Font Rendering

Both `Roboto` (UI) and `Roboto Slab` (display) are loaded from Google Fonts with `display=swap`. Declare `'Roboto Slab', serif` for headings, `'Roboto', sans-serif` for body/UI.

### CSS Custom Properties for Layout Control

Adjusting page width on a given page is a single-line change:

```css
:root {
  --page-width: 1200px;   /* outer container */
  --content-width: 960px; /* reading column (About, Changelog) */
}
```

### Scoring Model Toggle

The site supports two scoring models (`Primary` / `Sensitivity`) via `window.SASActiveModel`, stored in `localStorage('sas_model')`. Any component that displays scores should read the active model rather than hard-reading `sas_score` directly.

---

*Design system extracted from production codebase — stroke-access-score.vercel.app*
*Last updated: June 2026*
