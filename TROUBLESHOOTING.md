# Troubleshooting Scan Errors

## How to Debug Scan Errors

### Step 1: Check Backend Terminal
The backend terminal shows detailed error messages. Look for:
- Error messages starting with "Error processing scan"
- Traceback information
- Any warnings or exceptions

### Step 2: Check the Error in Frontend
1. When you see "Scan Error", look at the error details section
2. Click "Show Technical Details" to see the full traceback
3. Note the error type and message

### Step 3: Common Errors and Solutions

#### Error: "No pages were crawled"
**Cause:** Website blocks crawlers or has no crawlable links
**Solution:**
- Try a different website
- Check if the website is accessible in a browser
- Try with a smaller max_pages value (5-10)

#### Error: "Invalid URL format"
**Cause:** URL doesn't start with http:// or https://
**Solution:**
- Make sure URL starts with `http://` or `https://`
- Example: `https://example.com` (not `example.com`)

#### Error: "Failed to crawl website"
**Cause:** Network issues, timeout, or website unreachable
**Solution:**
- Check your internet connection
- Try a different website
- The website might be down or blocking requests

#### Error: Playwright/NotImplementedError
**Cause:** Playwright browser initialization failed (Windows/Python 3.13 issue)
**Solution:**
- This is automatically handled - the crawler falls back to HTTP-only mode
- No action needed, but JavaScript-rendered content won't be captured

### Step 4: Test with a Simple Website
Try scanning a simple, well-known website first:
- `https://example.com`
- `https://httpbin.org/html`
- `https://www.wikipedia.org` (use small max_pages like 5)

### Step 5: Check Backend Logs
In the backend terminal, you should see:
```
Starting crawl for https://example.com (max_pages: 10)
Using HTTP-only crawling mode (no JavaScript rendering)
Crawl completed. Found X pages
Running SEO audit...
Analyzing keywords...
Detecting duplicates...
Analyzing performance...
Analysis complete!
```

If you see errors in these steps, that's where the problem is.

### Step 6: Debug Endpoint
You can check scan status using the debug endpoint:
```
http://localhost:8000/api/debug/scan/{scan_id}
```

Replace `{scan_id}` with your actual scan ID from the URL.

## Still Having Issues?

1. **Check Backend Terminal** - Look for the actual error message
2. **Try a Different Website** - Some websites block crawlers
3. **Reduce Max Pages** - Start with 5-10 pages
4. **Check URL Format** - Must start with http:// or https://
5. **Restart Backend** - Sometimes a restart helps

## Getting Help

When reporting an error, please include:
1. The error message from the frontend
2. The error from the backend terminal
3. The website URL you tried to scan
4. The max_pages value you used

