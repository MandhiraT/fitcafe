# FitCafe Deployment to Coolify

## Deployment Status
**Date:** 2026-03-25  
**Status:** Ready for deployment  
**Target:** https://coolify.thequietself.com/  
**Domain:** FITCAFECOFFEE.COM  
**VPS IP:** 91.107.193.144

## Source Files
Location: `/home/mandhira/.openclaw/workspace-jarvis/fitcafe-website/`

### File Structure:
```
fitcafe-website/
├── index.html          # Main sales page
├── css/
│   └── style.css       # Stylesheet
├── js/
│   └── script.js       # JavaScript
├── assets/             # Images (placeholder)
└── README.md           # Documentation
```

## Deployment Instructions

### Option 1: Automated Script (Recommended)

```bash
# Make script executable
chmod +x /home/mandhira/.openclaw/workspace-jarvis/fitcafe-deploy.sh

# Run deployment
bash /home/mandhira/.openclaw/workspace-jarvis/fitcafe-deploy.sh
```

### Option 2: Manual Deployment via Coolify Dashboard

1. **Access Coolify Dashboard**
   - URL: https://coolify.thequietself.com/
   - Login with admin credentials

2. **Create New Application**
   - Click "+ New Resource"
   - Select "Application"
   - Choose "Git Repository" as source

3. **Configure Repository**
   - Repository URL: (push to GitHub first, or use local path)
   - Branch: `main`
   - Build Pack: **Static**

4. **Configure Build Settings**
   - Install Command: (leave empty)
   - Build Command: (leave empty)
   - Start Command: (leave empty)
   - Output Directory: `/` (root)

5. **Configure Domain**
   - Primary Domain: `fitcafecoffee.com`
   - Add www redirect: `www.fitcafecoffee.com`

6. **Deploy**
   - Click "Deploy" button
   - Wait for build to complete (~2-5 minutes)

### Option 3: Direct API Call

```bash
# Get application UUID first
curl -X GET "https://coolify.thequietself.com/api/v1/applications" \
  -H "Authorization: Bearer 4|coZt0OWYqoQIbUuo3fo29Yh6QRkKwxxpJU1l2pPod84e5dd0" \
  -H "Accept: application/json"

# Trigger deployment (replace UUID)
curl -X POST "https://coolify.thequietself.com/api/v1/deploy" \
  -H "Authorization: Bearer 4|coZt0OWYqoQIbUuo3fo29Yh6QRkKwxxpJU1l2pPod84e5dd0" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"uuid": "YOUR-APP-UUID-HERE"}'
```

## DNS Configuration

**Required DNS Records:**

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | 91.107.193.144 | 3600 |
| A | www | 91.107.193.144 | 3600 |

**Where to Configure:**
- Go to your domain registrar (where you bought FITCAFECOFFEE.COM)
- Access DNS management
- Add the records above

**SSL Certificate:**
- Coolify will automatically provision Let's Encrypt SSL
- Wait 5-10 minutes after DNS propagation
- Verify at: https://fitcafecoffee.com

## Testing Deployment

After deployment:

```bash
# Test homepage
curl -I https://fitcafecoffee.com

# Expected response:
# HTTP/2 200
# content-type: text/html
# server: Coolify

# Check SSL certificate
curl -vI https://fitcafecoffee.com 2>&1 | grep -E "(SSL|subject|expire)"
```

## Troubleshooting

### Issue: Application not found
**Solution:** Create application manually in Coolify dashboard first

### Issue: Domain not resolving
**Solution:** 
- Wait 24-48 hours for DNS propagation
- Check DNS with: `nslookup fitcafecoffee.com`
- Verify DNS records are correct

### Issue: SSL certificate error
**Solution:**
- Ensure DNS is properly configured
- Wait 10-15 minutes for auto-provisioning
- Check Coolify dashboard for certificate status

### Issue: Build fails
**Solution:**
- Verify build pack is set to "Static"
- Check build logs in Coolify dashboard
- Ensure all files are committed to git

## Post-Deployment Checklist

- [ ] DNS records configured
- [ ] SSL certificate active
- [ ] Homepage loads correctly
- [ ] CSS/JS files load
- [ ] Mobile responsive design works
- [ ] Affiliate link updated in index.html
- [ ] Google Analytics configured (if needed)
- [ ] Social media meta tags verified

## Support

Coolify Documentation: https://coolify.io/docs/  
API Reference: https://coolify.io/docs/api-reference

---

**Last Updated:** 2026-03-25  
**Deployed By:** Jarvis Subagent
