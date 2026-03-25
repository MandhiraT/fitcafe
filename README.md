# FitCafe Sales Page

A responsive, mobile-first sales page for FitCafe weight loss coffee affiliate marketing.

## Features

- **Responsive Design**: Works on all devices (mobile, tablet, desktop)
- **SEO Optimized**: Includes meta tags, semantic HTML, and Open Graph tags
- **Fast Loading**: Lightweight vanilla HTML/CSS/JS with no external dependencies
- **Coffee-inspired Design**: Warm, trustworthy aesthetic with professional typography
- **Affiliate Ready**: Placeholder for affiliate links in CTA buttons

## File Structure

```
fitcafe-website/
├── index.html          # Main sales page
├── css/
│   └── style.css       # Stylesheet with responsive design
├── js/
│   └── script.js       # Minimal JavaScript for interactivity
├── assets/             # Placeholder directory for images and other assets
└── README.md           # This file
```

## Deployment Instructions

### GitHub Pages

1. **Create a new repository** on GitHub (e.g., `yourusername/fitcafe.coffee`)
2. **Push this folder** to the repository
3. **Enable GitHub Pages**:
   - Go to your repository Settings
   - Scroll down to "Pages" section
   - Under "Source", select "Deploy from a branch"
   - Choose the main branch (usually `main` or `master`)
   - Select `/ (root)` as the folder
   - Click "Save"
4. **Your site will be live** at `https://yourusername.github.io/fitcafe.coffee`

> **Note**: If you want to use a custom domain (fitcafe.coffee), you'll need to:
> - Add a `CNAME` file in the root with `fitcafe.coffee` as content
> - Configure DNS records with your domain registrar

### Vercel

1. **Sign up** for a [Vercel account](https://vercel.com/signup) if you don't have one
2. **Import your project**:
   - Click "New Project"
   - Connect your Git provider (GitHub, GitLab, etc.)
   - Select the repository containing this code
3. **Configure project settings**:
   - Framework Preset: **Other** (since this is static HTML)
   - Build and Output Settings: Leave defaults (no build step needed)
   - Root Directory: `/` (root of repository)
4. **Deploy** by clicking "Deploy"
5. **Your site will be live** at a `*.vercel.app` URL, and you can add a custom domain

## Customization

### Affiliate Links

Replace the affiliate link placeholder in `index.html`:

```html
<!-- Find this line in index.html -->
<a href="https://AFFILIATE-LINK-PLACEHOLDER.com" class="cta-button">Try FitCafe — You've Got 180 Days to Decide</a>

<!-- Replace with your actual affiliate link -->
<a href="https://your-affiliate-link.com" class="cta-button">Try FitCafe — You've Got 180 Days to Decide</a>
```

### Images

Add product images to the `assets/` folder:
- `product.jpg` - Main product image
- `fitcafe-social.jpg` - Social sharing image (for Open Graph tags)

Update image paths in `index.html` if needed.

### Analytics

To add Google Analytics, uncomment and configure the tracking code in `js/script.js`:

```javascript
// gtag('event', 'click', { event_category: 'CTA', event_label: 'Try FitCafe' });
```

Also add your Google Analytics tracking code to the `<head>` section of `index.html`.

## Technical Details

- **Framework**: Vanilla HTML/CSS/JS (no framework dependencies)
- **Fonts**: Google Fonts (Inter for body, Merriweather for headings)
- **Responsive**: Mobile-first approach with CSS Grid and Flexbox
- **Performance**: Optimized for fast loading with minimal HTTP requests
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge)

## License

This code is provided as-is for affiliate marketing purposes. Modify as needed for your specific requirements.