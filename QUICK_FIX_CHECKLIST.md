# Quick Fix Checklist for WebSocket Errors

## ✅ Immediate Actions

### 1. Set Environment Variables in Netlify (MOST IMPORTANT)
- [ ] Go to Netlify Dashboard → Site Settings → Environment Variables
- [ ] Add `VITE_BACKEND_URL` = `https://stream-monitor-a4cr.onrender.com`
- [ ] Add `VITE_WS_URL` = `wss://stream-monitor-a4cr.onrender.com/ws` (note the `/ws`!)
- [ ] Click "Save"

### 2. Rebuild Frontend
- [ ] Go to Deploys tab in Netlify
- [ ] Click "Trigger deploy" → "Clear cache and deploy site"
- [ ] Wait 2-3 minutes for build to complete

### 3. Wake Up Backend (if needed)
- [ ] Visit: https://stream-monitor-a4cr.onrender.com/health
- [ ] Wait 30-60 seconds (Render free tier sleeps after inactivity)
- [ ] Should see: `{"status":"healthy",...}`

### 4. Test WebSocket Connection
- [ ] Open your Netlify site
- [ ] Open browser console (F12)
- [ ] Should see: `✅ WebSocket connected`
- [ ] No more error messages

## 🔍 Verification Steps

### Backend is Running
```bash
curl https://stream-monitor-a4cr.onrender.com/health
```
Expected: `{"status":"healthy","database":"..."}`

### WebSocket Endpoint Exists
Use a WebSocket testing tool or browser console:
```javascript
const ws = new WebSocket('wss://stream-monitor-a4cr.onrender.com/ws');
ws.onopen = () => console.log('Connected!');
ws.onerror = (e) => console.error('Error:', e);
```

### Environment Variables are Set
In Netlify build logs, you should see:
```
Environment variables set:
  VITE_BACKEND_URL
  VITE_WS_URL
```

## 🚨 Common Issues

### Issue: "WebSocket connection failed"
**Cause:** Backend is sleeping or not running
**Fix:** Visit backend health endpoint to wake it up

### Issue: "Connection to 'wss://.../' failed" (no /ws)
**Cause:** Environment variables not set in Netlify
**Fix:** Add variables in Netlify dashboard and rebuild

### Issue: "CORS error"
**Cause:** Backend doesn't allow your Netlify domain
**Fix:** Set `CORS_ORIGINS=*` in Render environment variables

### Issue: "Connection established but no data"
**Cause:** Simulator not running
**Fix:** Run simulator locally or deploy it to Render

## 📝 Expected Console Output (Success)

```
Connecting to WebSocket...
✅ WebSocket connected
📨 Received: {event: "new_data", data: {...}}
📨 Received: {event: "status_update", data: [...]}
```

## 🎯 Final Check

- [ ] No errors in browser console
- [ ] Green "Connected" indicator in dashboard
- [ ] Backend health endpoint responds
- [ ] Environment variables set in Netlify
- [ ] Frontend rebuilt after setting variables

## 💡 Pro Tips

1. **Always rebuild** after changing environment variables
2. **Clear cache** when rebuilding to ensure fresh build
3. **Check backend logs** on Render if WebSocket fails
4. **Use incognito mode** to test without browser cache
5. **Render free tier sleeps** - first request takes 30-60s

## 🆘 Still Stuck?

1. Check Render backend logs for errors
2. Check Netlify build logs for environment variables
3. Verify WebSocket URL includes `/ws` endpoint
4. Try connecting to backend directly with curl
5. Test WebSocket with a testing tool first
