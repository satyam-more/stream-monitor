# Fix WebSocket Connection on Netlify

## Problem
The frontend deployed on Netlify is trying to connect to the wrong WebSocket URL, causing connection errors.

## Root Cause
Environment variables in `.env.production` are NOT automatically used by Netlify. They must be set in the Netlify dashboard.

## Solution

### Step 1: Set Environment Variables in Netlify

1. Go to your Netlify dashboard: https://app.netlify.com
2. Select your site (stream-monitor)
3. Go to **Site settings** → **Environment variables**
4. Click **Add a variable** and add these two variables:

```
Variable name: VITE_BACKEND_URL
Value: https://stream-monitor-a4cr.onrender.com
```

```
Variable name: VITE_WS_URL
Value: wss://stream-monitor-a4cr.onrender.com/ws
```

**IMPORTANT:** Make sure the WebSocket URL includes `/ws` at the end!

### Step 2: Trigger a Rebuild

After adding the environment variables:

1. Go to **Deploys** tab
2. Click **Trigger deploy** → **Clear cache and deploy site**
3. Wait for the build to complete (2-3 minutes)

### Step 3: Verify the Fix

1. Open your Netlify site in the browser
2. Open browser console (F12)
3. You should see: `✅ WebSocket connected`
4. No more connection errors!

## Alternative: Check if Backend is Running

The backend on Render free tier sleeps after 15 minutes of inactivity. To wake it up:

1. Visit: https://stream-monitor-a4cr.onrender.com/health
2. Wait 30-60 seconds for it to wake up
3. You should see: `{"status":"healthy","database":"..."}`
4. Now try the frontend again

## Verify Backend WebSocket Endpoint

Test the WebSocket endpoint directly:

1. Install a WebSocket testing tool (like "Simple WebSocket Client" Chrome extension)
2. Connect to: `wss://stream-monitor-a4cr.onrender.com/ws`
3. You should see: Connection established
4. If it fails, the backend might not be running or configured correctly

## Backend CORS Configuration

Make sure the backend allows your Netlify domain:

1. Go to Render dashboard
2. Select your backend service
3. Go to **Environment** tab
4. Find `CORS_ORIGINS` variable
5. Set it to: `*` (allow all) or your specific Netlify URL
6. Click **Save Changes**
7. Backend will automatically redeploy

## Quick Test Commands

### Test Backend Health
```bash
curl https://stream-monitor-a4cr.onrender.com/health
```

### Test Backend API
```bash
curl https://stream-monitor-a4cr.onrender.com/api/sensors
```

## Expected Result

After fixing, you should see in the browser console:

```
Connecting to WebSocket...
✅ WebSocket connected
```

And the dashboard should show:
- Green "Connected" status
- Real-time data flowing (if simulator is running)
- No error messages

## Still Not Working?

If the issue persists:

1. **Check Backend Logs** on Render dashboard
2. **Check Browser Console** for specific error messages
3. **Verify Environment Variables** are set correctly in Netlify
4. **Clear Browser Cache** and hard refresh (Ctrl+Shift+R)
5. **Try Incognito Mode** to rule out caching issues

## Contact

If you need help, check:
- Backend logs on Render
- Frontend build logs on Netlify
- Browser console errors
