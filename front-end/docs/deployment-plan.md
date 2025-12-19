# Deployment Plan: Client-Side SPA on Cloudflare Pages

## Overview
This document outlines how to deploy the React TypeScript SPA to Cloudflare Pages, a modern hosting platform optimized for static sites and SPAs.

---

## Why This Stack is Perfect for Client-Side SPA

### ✅ Our Architecture Already Supports SPA:

1. **Vite Build Output** - Generates optimized static assets
2. **React Router** - Client-side routing (no server needed)
3. **React Context** - Client-side state management
4. **Static Assets** - All JavaScript, CSS, and HTML are static files
5. **API Separation** - Backend API is separate (can be hosted anywhere)

### ✅ No Server-Side Rendering (SSR) Required:
- Pure client-side rendering
- All logic runs in the browser
- API calls to external backend
- Perfect for Cloudflare Pages

---

## Cloudflare Pages Benefits

### Performance
- ✅ **Global CDN** - 300+ edge locations worldwide
- ✅ **Instant Cache Invalidation** - Updates propagate in seconds
- ✅ **HTTP/3 Support** - Fastest protocol available
- ✅ **Automatic Compression** - Brotli and Gzip

### Developer Experience
- ✅ **Git Integration** - Auto-deploy on push
- ✅ **Preview Deployments** - Every PR gets a unique URL
- ✅ **Rollback Support** - One-click rollback to any version
- ✅ **Build Logs** - Detailed build output

### Cost
- ✅ **Free Tier** - 500 builds/month, unlimited bandwidth
- ✅ **No Credit Card Required** - Start for free
- ✅ **Generous Limits** - 20,000 requests/month on free tier

### Security
- ✅ **Free SSL/TLS** - Automatic HTTPS
- ✅ **DDoS Protection** - Built-in
- ✅ **Web Application Firewall** - Available
- ✅ **Access Control** - Password protect preview deployments

---

## Phase 1: Prepare Application for SPA Deployment

### Step 1.1: Install React Router (if not already installed)

```bash
npm install react-router-dom
```

### Step 1.2: Update Application for Client-Side Routing

**File: `src/main.tsx`**
```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { LocationProvider } from './contexts/LocationContext';
import { SearchProvider } from './contexts/SearchContext';
import { MapProvider } from './contexts/MapContext';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <LocationProvider>
        <MapProvider>
          <SearchProvider>
            <App />
          </SearchProvider>
        </MapProvider>
      </LocationProvider>
    </BrowserRouter>
  </React.StrictMode>
);
```

### Step 1.3: Configure Vite for SPA

**File: `vite.config.ts`** (update)
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@contexts': path.resolve(__dirname, './src/contexts'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@services': path.resolve(__dirname, './src/services'),
      '@types': path.resolve(__dirname, './src/types'),
      '@utils': path.resolve(__dirname, './src/utils'),
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false, // Set to true for debugging production
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'maps-vendor': ['@react-google-maps/api'],
          'chart-vendor': ['chart.js', 'react-chartjs-2'],
        },
      },
    },
  },
  server: {
    port: 3000,
    open: true,
  },
});
```

### Step 1.4: Create SPA Fallback Configuration

**File: `public/_redirects`** (Cloudflare Pages uses this)
```
# SPA fallback - redirect all routes to index.html
/*    /index.html   200
```

**Alternative: File: `public/_headers`** (Optional - for security headers)
```
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(self), microphone=(), camera=()
```

---

## Phase 2: Environment Variables for Production

### Step 2.1: Update Environment Configuration

**File: `.env.production`**
```env
# Production Google Maps API Key (restricted to your domain)
VITE_GOOGLE_MAPS_API_KEY=your_production_api_key

# Production API URL (your backend API)
VITE_API_BASE_URL=https://api.yourdomain.com

# Optional: Analytics
VITE_ANALYTICS_ID=your_analytics_id
```

### Step 2.2: Configure Cloudflare Pages Environment Variables

Environment variables will be set in Cloudflare Pages dashboard:
1. Go to Settings → Environment Variables
2. Add production variables
3. Add preview/development variables separately

---

## Phase 3: Cloudflare Pages Setup

### Step 3.1: Create Cloudflare Account

1. Go to [Cloudflare Pages](https://pages.cloudflare.com/)
2. Sign up for free account
3. Verify email address

### Step 3.2: Connect Git Repository

1. Click **"Create a project"**
2. Connect your Git provider:
   - GitHub
   - GitLab
   - Bitbucket
3. Authorize Cloudflare to access your repository
4. Select your repository

### Step 3.3: Configure Build Settings

**Build Configuration:**
```yaml
Framework preset: Vite
Build command: npm run build
Build output directory: dist
Root directory: front-end/map-search-app
Node version: 18 or 20
```

**Environment Variables (in Cloudflare dashboard):**
```
VITE_GOOGLE_MAPS_API_KEY = your_api_key
VITE_API_BASE_URL = https://api.yourdomain.com
NODE_VERSION = 18
```

### Step 3.4: Deploy

1. Click **"Save and Deploy"**
2. Wait for build to complete (usually 1-3 minutes)
3. Your site will be available at: `https://your-project.pages.dev`

---

## Phase 4: Custom Domain Setup

### Step 4.1: Add Custom Domain

1. In Cloudflare Pages project, go to **Custom domains**
2. Click **"Set up a custom domain"**
3. Enter your domain (e.g., `map-search.yourdomain.com`)

### Step 4.2: Configure DNS

**If domain is already on Cloudflare:**
- DNS records are automatically configured
- SSL certificate is automatically provisioned

**If domain is elsewhere:**
1. Add CNAME record pointing to `your-project.pages.dev`
2. Wait for DNS propagation (5-30 minutes)
3. SSL certificate will be automatically provisioned

---

## Phase 5: Backend API Deployment Options

### Option 1: Cloudflare Workers (Recommended)

**Benefits:**
- Same platform as frontend
- Serverless, scales automatically
- Global edge network
- Free tier: 100,000 requests/day

**Setup:**
```bash
# Install Wrangler CLI
npm install -g wrangler

# Create new Worker
wrangler init api

# Deploy
wrangler deploy
```

**Example Worker for Location API:**
```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': 'https://your-domain.com',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Route handling
    if (url.pathname === '/api/locations' && request.method === 'GET') {
      const locations = await getLocations(); // Your logic here
      return new Response(JSON.stringify(locations), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    return new Response('Not Found', { status: 404, headers: corsHeaders });
  },
};
```

### Option 2: Cloudflare D1 (Database)

**For persistent storage:**
```bash
# Create D1 database
wrangler d1 create locations-db

# Run migrations
wrangler d1 execute locations-db --file=./schema.sql
```

### Option 3: External API (Vercel, Railway, Render, etc.)

**If you prefer separate backend:**
- Deploy Node.js/Express API to Vercel, Railway, or Render
- Update `VITE_API_BASE_URL` to point to deployed API
- Ensure CORS is configured correctly

---

## Phase 6: CI/CD Pipeline

### Automatic Deployments

**Cloudflare Pages automatically:**
1. Builds on every push to main branch
2. Creates preview deployments for PRs
3. Runs build command and deploys
4. Invalidates cache globally

### Branch Deployments

**Production (main branch):**
- Deploys to: `https://your-domain.com`
- Uses production environment variables

**Preview (feature branches):**
- Deploys to: `https://branch-name.your-project.pages.dev`
- Uses preview environment variables
- Perfect for testing before merge

### Build Configuration File

**File: `wrangler.toml`** (optional, for advanced config)
```toml
name = "map-search-app"
compatibility_date = "2024-01-01"

[build]
command = "npm run build"
cwd = "front-end/map-search-app"

[build.upload]
format = "service-worker"
dir = "dist"

[[env.production]]
name = "map-search-app-production"
route = "your-domain.com/*"

[[env.preview]]
name = "map-search-app-preview"
```

---

## Phase 7: Performance Optimization

### Step 7.1: Enable Caching

**File: `public/_headers`**
```
# Cache static assets for 1 year
/assets/*
  Cache-Control: public, max-age=31536000, immutable

# Cache HTML for 1 hour
/*.html
  Cache-Control: public, max-age=3600

# Cache API responses for 5 minutes
/api/*
  Cache-Control: public, max-age=300
```

### Step 7.2: Code Splitting

Already configured in `vite.config.ts`:
- React vendor chunk
- Maps vendor chunk
- Chart vendor chunk
- Lazy load routes with `React.lazy()`

### Step 7.3: Image Optimization

**Use Cloudflare Images (optional):**
```typescript
// Instead of direct image URLs
const imageUrl = 'https://imagedelivery.net/your-account/image-id/public';
```

---

## Phase 8: Monitoring & Analytics

### Step 8.1: Cloudflare Web Analytics

1. Enable in Cloudflare Pages dashboard
2. Add analytics script to `index.html`:
```html
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' 
        data-cf-beacon='{"token": "your-token"}'></script>
```

### Step 8.2: Error Tracking

**Option 1: Sentry**
```bash
npm install @sentry/react
```

**File: `src/main.tsx`**
```typescript
import * as Sentry from '@sentry/react';

Sentry.init({
  dsn: 'your-sentry-dsn',
  environment: import.meta.env.MODE,
  tracesSampleRate: 1.0,
});
```

### Step 8.3: Performance Monitoring

**Use Cloudflare's built-in analytics:**
- Page load times
- Core Web Vitals
- Geographic distribution
- Traffic patterns

---

## Phase 9: Security Best Practices

### Step 9.1: Content Security Policy

**File: `public/_headers`**
```
/*
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://maps.googleapis.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://maps.googleapis.com https://api.yourdomain.com
```

### Step 9.2: API Key Security

**Restrict Google Maps API Key:**
1. Go to Google Cloud Console
2. Edit API key restrictions
3. Add HTTP referrers:
   - `https://your-domain.com/*`
   - `https://*.pages.dev/*` (for preview deployments)

### Step 9.3: Environment Variables

**Never commit:**
- `.env`
- `.env.local`
- `.env.production`

**Always use:**
- Cloudflare Pages environment variables
- Different keys for development/production

---

## Phase 10: Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Build succeeds locally (`npm run build`)
- [ ] Preview build works (`npm run preview`)
- [ ] Environment variables configured
- [ ] API keys restricted to production domain
- [ ] CORS configured on backend API
- [ ] Error tracking set up
- [ ] Analytics configured

### Deployment
- [ ] Push to main branch (or merge PR)
- [ ] Monitor build logs in Cloudflare
- [ ] Verify deployment at preview URL
- [ ] Test all features in production
- [ ] Check mobile responsiveness
- [ ] Verify API connections
- [ ] Test Google Maps functionality

### Post-Deployment
- [ ] Set up custom domain
- [ ] Configure DNS
- [ ] Verify SSL certificate
- [ ] Test from different locations
- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Set up alerts for downtime

---

## Deployment Commands

### Local Development
```bash
npm run dev              # Start dev server
npm run build            # Build for production
npm run preview          # Preview production build
npm run type-check       # Check TypeScript
npm run lint             # Run linter
```

### Cloudflare Deployment
```bash
# Manual deployment (if needed)
npm run build
npx wrangler pages deploy dist

# Deploy specific branch
npx wrangler pages deploy dist --branch=staging
```

---

## Troubleshooting

### Build Fails on Cloudflare

**Check:**
- Node version matches local (18 or 20)
- All dependencies in `package.json`
- Build command is correct
- Environment variables are set

**Solution:**
```bash
# Test build locally with production settings
npm run build -- --mode production
```

### 404 on Client-Side Routes

**Cause:** Missing SPA fallback configuration

**Solution:** Ensure `public/_redirects` exists:
```
/*    /index.html   200
```

### API CORS Errors

**Cause:** Backend not configured for frontend domain

**Solution:** Update backend CORS:
```typescript
// Allow your Cloudflare Pages domain
const allowedOrigins = [
  'https://your-domain.com',
  'https://your-project.pages.dev',
];
```

### Environment Variables Not Working

**Cause:** Variables must be prefixed with `VITE_`

**Solution:**
```env
# ✅ Correct
VITE_API_KEY=abc123

# ❌ Wrong
API_KEY=abc123
```

---

## Cost Estimate

### Cloudflare Pages (Free Tier)
- **Builds:** 500/month (more than enough)
- **Bandwidth:** Unlimited
- **Requests:** 20,000/month
- **Storage:** 25GB

### Cloudflare Workers (Free Tier)
- **Requests:** 100,000/day
- **CPU Time:** 10ms per request
- **Storage:** 1GB

### Total Monthly Cost
- **Development:** $0
- **Small Production App:** $0
- **High Traffic:** ~$5-20/month (if exceeding free tier)

---

## Migration Path

### From Development to Production

1. **Week 1:** Develop locally with mock API
2. **Week 2:** Deploy to Cloudflare Pages preview
3. **Week 3:** Set up Cloudflare Workers API
4. **Week 4:** Configure custom domain and go live

### Scaling Strategy

**As traffic grows:**
1. Enable Cloudflare caching
2. Add Cloudflare Workers KV for data
3. Implement Cloudflare D1 for database
4. Use Cloudflare R2 for file storage
5. Enable Cloudflare Images for optimization

---

## Summary

### ✅ Our SPA Architecture:
- **Frontend:** React + TypeScript + Vite → Cloudflare Pages
- **Backend:** API (Cloudflare Workers or external)
- **Database:** Cloudflare D1 or external
- **CDN:** Cloudflare's global network
- **SSL:** Automatic and free
- **Deployment:** Automatic on git push

### ✅ Perfect for Client-Side SPA:
- No server-side rendering needed
- All routing handled client-side
- Static assets served from CDN
- API calls to separate backend
- Fast, scalable, and cost-effective

### 🚀 Ready to Deploy:
Follow the phases above to deploy your React TypeScript SPA to Cloudflare Pages with zero infrastructure management and excellent performance worldwide.