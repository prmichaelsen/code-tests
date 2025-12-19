# Google Maps API Setup Guide

## Step-by-Step Instructions to Get Your Google Maps API Key

### Prerequisites
- A Google account (Gmail account)
- A credit/debit card (required for verification, but you won't be charged unless you exceed free tier)

---

## Step 1: Go to Google Cloud Console

1. Navigate to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account

---

## Step 2: Create a New Project (or Select Existing)

### Create New Project:
1. Click the project dropdown at the top of the page (next to "Google Cloud")
2. Click **"NEW PROJECT"** button in the top right
3. Enter a project name (e.g., "Map Search Project")
4. Leave organization as "No organization" (unless you have one)
5. Click **"CREATE"**
6. Wait for the project to be created (takes a few seconds)
7. Select your new project from the dropdown

### Or Select Existing Project:
1. Click the project dropdown
2. Select an existing project from the list

---

## Step 3: Enable Billing (Required)

**Important**: Google requires billing to be enabled, but provides $200 free credit per month and 28,000 free map loads. You won't be charged unless you explicitly exceed the free tier.

1. In the left sidebar, click **"Billing"** or go to [Billing](https://console.cloud.google.com/billing)
2. Click **"LINK A BILLING ACCOUNT"**
3. If you don't have a billing account:
   - Click **"CREATE BILLING ACCOUNT"**
   - Enter your billing information (name, address)
   - Add a payment method (credit/debit card)
   - Accept terms and click **"START MY FREE TRIAL"** or **"SUBMIT AND ENABLE BILLING"**
4. Link the billing account to your project

---

## Step 4: Enable Google Maps JavaScript API

1. In the left sidebar, click **"APIs & Services"** → **"Library"**
   - Or go directly to [API Library](https://console.cloud.google.com/apis/library)

2. In the search bar, type: **"Maps JavaScript API"**

3. Click on **"Maps JavaScript API"** from the results

4. Click the **"ENABLE"** button

5. Wait for the API to be enabled (takes a few seconds)

---

## Step 5: Create API Credentials (API Key)

1. In the left sidebar, click **"APIs & Services"** → **"Credentials"**
   - Or go to [Credentials](https://console.cloud.google.com/apis/credentials)

2. Click **"+ CREATE CREDENTIALS"** at the top

3. Select **"API key"** from the dropdown

4. Your API key will be created and displayed in a popup
   - **Copy this key immediately** and save it somewhere safe
   - Example format: `AIzaSyDyzXYDJaMcu0wYaYBSua3HvTfT6ZSpASQ`

5. Click **"CLOSE"** (you can restrict the key in the next step)

---

## Step 6: Restrict Your API Key (Highly Recommended)

**Security Best Practice**: Always restrict your API keys to prevent unauthorized use and unexpected charges.

### Option A: Restrict by HTTP Referrers (Recommended for Web Apps)

1. On the Credentials page, find your newly created API key
2. Click the **pencil icon** (Edit) next to your API key
3. Under **"Application restrictions"**:
   - Select **"HTTP referrers (web sites)"**
4. Click **"+ ADD AN ITEM"**
5. Add your website referrers:
   - For local development: `localhost/*` or `http://localhost:*/*`
   - For production: `yourdomain.com/*` and `*.yourdomain.com/*`
   - Example entries:
     ```
     http://localhost:*/*
     http://127.0.0.1:*/*
     https://yourdomain.com/*
     https://*.yourdomain.com/*
     ```
6. Click **"DONE"**

### Option B: Restrict by API

1. Scroll down to **"API restrictions"**
2. Select **"Restrict key"**
3. Click **"Select APIs"** dropdown
4. Check **"Maps JavaScript API"**
5. Click **"OK"**

### Save Restrictions

1. Scroll to the bottom and click **"SAVE"**
2. Wait for changes to propagate (can take up to 5 minutes)

---

## Step 7: Use Your API Key

### In HTML (Direct Script Tag):
```html
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY_HERE&callback=initMap" async defer></script>
```

### In React (Environment Variable):

1. Create a `.env` file in your project root:
```env
VITE_GOOGLE_MAPS_API_KEY=YOUR_API_KEY_HERE
```

2. Add `.env` to your `.gitignore`:
```
.env
.env.local
```

3. Use in your code:
```javascript
const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
```

### In JavaScript (Dynamic Loading):
```javascript
const loadGoogleMaps = (apiKey) => {
  const script = document.createElement('script');
  script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&callback=initMap`;
  script.async = true;
  script.defer = true;
  document.head.appendChild(script);
};
```

---

## Step 8: Test Your API Key

### Simple Test HTML:
```html
<!DOCTYPE html>
<html>
<head>
  <title>Google Maps Test</title>
  <style>
    #map { height: 400px; width: 100%; }
  </style>
</head>
<body>
  <h1>Google Maps API Test</h1>
  <div id="map"></div>
  
  <script>
    function initMap() {
      const map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 37.7749, lng: -122.4194 }, // San Francisco
        zoom: 12
      });
      
      new google.maps.Marker({
        position: { lat: 37.7749, lng: -122.4194 },
        map: map,
        title: 'Test Marker'
      });
    }
  </script>
  
  <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY_HERE&callback=initMap" async defer></script>
</body>
</html>
```

Replace `YOUR_API_KEY_HERE` with your actual API key and open in a browser.

---

## Troubleshooting

### Error: "This API key is not authorized to use this service or API"
- **Solution**: Make sure you enabled the Maps JavaScript API in Step 4
- Wait 5 minutes for changes to propagate
- Check that your API restrictions allow your domain

### Error: "RefererNotAllowedMapError"
- **Solution**: Your HTTP referrer restrictions are blocking the request
- Add your domain/localhost to the allowed referrers list
- For local development, add: `http://localhost:*/*`

### Error: "ApiNotActivatedMapError"
- **Solution**: The Maps JavaScript API is not enabled
- Go back to Step 4 and enable the API

### Map Shows "For development purposes only" Watermark
- **Solution**: Billing is not enabled on your project
- Go back to Step 3 and enable billing
- You won't be charged unless you exceed the free tier

### API Key Not Working After Creation
- **Solution**: Wait 5-10 minutes for the key to propagate through Google's systems
- Clear your browser cache
- Try in an incognito/private window

---

## Monitoring Usage

### Check Your API Usage:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Click **"APIs & Services"** → **"Dashboard"**
4. View usage statistics for Maps JavaScript API
5. Set up billing alerts to avoid unexpected charges:
   - Go to **"Billing"** → **"Budgets & alerts"**
   - Create a budget alert (e.g., alert at $10, $50, $100)

---

## Free Tier Limits

### Maps JavaScript API Free Tier:
- **$200 free credit per month** (applies to all Google Maps Platform APIs)
- **28,000 map loads per month** (equivalent to $200 credit)
- **Dynamic Maps**: $7 per 1,000 loads (after free tier)
- **Static Maps**: $2 per 1,000 loads

### Typical Usage for Development:
- Local development: Very low usage (< 100 loads/day)
- Small project: Usually stays within free tier
- **You will receive email alerts** if approaching limits

---

## Security Best Practices

### DO:
✅ Always restrict your API keys
✅ Use environment variables for API keys
✅ Add `.env` to `.gitignore`
✅ Use different keys for development and production
✅ Set up billing alerts
✅ Regularly review API usage

### DON'T:
❌ Commit API keys to public repositories
❌ Share API keys publicly
❌ Use the same key for multiple projects
❌ Leave keys unrestricted
❌ Ignore billing alerts

---

## Alternative: Use Existing API Key

The project currently includes an API key in [`front-end/map-search-test/index.html`](../front-end/map-search-test/index.html):
```
AIzaSyDyzXYDJaMcu0wYaYBSua3HvTfT6ZSpASQ
```

**Note**: This key may be restricted or rate-limited. For production use or if you encounter issues, create your own API key following the steps above.

---

## Quick Reference

### Essential Links:
- [Google Cloud Console](https://console.cloud.google.com/)
- [API Library](https://console.cloud.google.com/apis/library)
- [Credentials](https://console.cloud.google.com/apis/credentials)
- [Billing](https://console.cloud.google.com/billing)
- [Maps JavaScript API Documentation](https://developers.google.com/maps/documentation/javascript/)
- [Pricing Calculator](https://mapsplatform.google.com/pricing/)

### Support:
- [Google Maps Platform Support](https://developers.google.com/maps/support)
- [Stack Overflow - google-maps](https://stackoverflow.com/questions/tagged/google-maps)

---

## Summary Checklist

- [ ] Created Google Cloud account
- [ ] Created new project (or selected existing)
- [ ] Enabled billing (required, but free tier available)
- [ ] Enabled Maps JavaScript API
- [ ] Created API key
- [ ] Restricted API key (HTTP referrers and/or API restrictions)
- [ ] Saved API key securely
- [ ] Added API key to `.env` file
- [ ] Added `.env` to `.gitignore`
- [ ] Tested API key with simple map
- [ ] Set up billing alerts (recommended)

**Estimated Time**: 10-15 minutes

---

## Need Help?

If you encounter issues:
1. Check the Troubleshooting section above
2. Review [Google Maps Platform documentation](https://developers.google.com/maps/documentation)
3. Search [Stack Overflow](https://stackoverflow.com/questions/tagged/google-maps)
4. Contact [Google Maps Platform Support](https://developers.google.com/maps/support)