# FitCafe Sales Page - Deployment Guide

## Project Overview
This is a static sales page website for FitCafe weight loss coffee affiliate marketing. The site is built with vanilla HTML, CSS, and JavaScript for maximum performance and compatibility.

## Domain
- Primary domain: `fitcafe.coffee`

## Affiliate Integration
- **Affiliate Link Placeholder**: The CTA button currently points to `https://AFFILIATE-LINK-PLACEHOLDER.com`
- **To integrate your affiliate link**: Replace this URL with your actual affiliate link in `index.html` (line 248)

## Deployment Instructions

### GitHub Pages
1. Create a new GitHub repository (or use an existing one)
2. Push all files to the repository
3. Go to Repository Settings → Pages
4. Set Source to "Deploy from a branch"
5. Select your main branch and `/root` folder
6. Click Save
7. Your site will be available at `https://[username].github.io/[repository-name]/`
8. For custom domain (`fitcafe.coffee`):
   - Add a `CNAME` file in the root directory containing: `fitcafe.coffee`
   - Configure DNS records with your domain registrar to point to GitHub Pages

### Vercel
1. Sign up/login to Vercel (https://vercel.com)
2. Click "New Project"
3. Import your Git repository containing these files
4. Vercel will automatically detect it as a static site
5. In the "Environment Variables" section, no variables are needed
6. In the "Build & Output Settings", no configuration is needed (defaults work)
7. Click "Deploy"
8. Your site will be available at a `*.vercel.app` URL
9. For custom domain (`fitcafe.coffee`):
   - Go to your project dashboard
   - Click "Settings" → "Domains"
   - Add your domain `fitcafe.coffee`
   - Follow Vercel's instructions to configure DNS records

## Assets
- Product images should be placed in the `assets/` directory
- Update image paths in `index.html` when adding product images
- The current site includes placeholders for Open Graph images (`assets/og-image.jpg`)

## SEO
- Basic SEO is implemented with meta tags, semantic HTML, and Open Graph/Twitter Card tags
- The site is optimized for search engines with proper heading structure and content organization

## Performance
- The site is lightweight (no external dependencies)
- Mobile-first responsive design
- Fast loading times on all devices

## Maintenance
- To update content: Edit `index.html` directly
- To update styling: Edit `css/style.css`
- To add functionality: Edit `js/script.js`

## Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile and desktop devices

## Notes
- This is an affiliate site - no payment processing or user data collection
- All affiliate tracking should be handled through your affiliate link parameters
- Analytics can be added by including tracking code in `index.html` or `js/script.js`