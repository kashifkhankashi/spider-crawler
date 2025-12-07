from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
import asyncio
from datetime import datetime
import uuid

from app.crawler.spider import WebsiteCrawler
from app.audit.seo_audit import SEOAuditor
from app.analysis.keywords import KeywordAnalyzer
from app.analysis.duplicates import DuplicateDetector
from app.analysis.page_power import PagePowerAnalyzer
from app.performance.pagespeed import PageSpeedAnalyzer

app = FastAPI(title="Website Analysis Tool", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for scan results
scan_results: Dict[str, Dict[str, Any]] = {}
scan_status: Dict[str, str] = {}  # 'pending', 'processing', 'completed', 'error'


class ScanRequest(BaseModel):
    url: HttpUrl
    max_pages: Optional[int] = 200  # Increased to 200
    include_external: Optional[bool] = False


class ScanResponse(BaseModel):
    scan_id: str
    status: str
    message: str


async def process_scan(scan_id: str, url: str, max_pages: int, include_external: bool):
    """Background task to process the full scan"""
    print(f"\n[PROCESS_SCAN] Starting scan {scan_id} for {url}")
    try:
        scan_status[scan_id] = "processing"
        print(f"[PROCESS_SCAN] Status set to processing for {scan_id}")
        
        # Validate URL
        if not url or not url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL format: {url}. URL must start with http:// or https://")
        
        # Step 1: Crawl website
        print(f"Starting crawl for {url} (max_pages: {max_pages})")
        try:
            crawler = WebsiteCrawler(max_pages=max_pages, include_external=include_external)
            crawl_results = await crawler.crawl(url)
            print(f"Crawl completed. Found {len(crawl_results.get('pages', []))} pages")
        except Exception as e:
            error_detail = str(e) if str(e) else f"{type(e).__name__} occurred"
            print(f"[PROCESS_SCAN] Crawl failed: {error_detail}")
            print(f"[PROCESS_SCAN] Error type: {type(e).__name__}")
            print(f"[PROCESS_SCAN] Error repr: {repr(e)}")
            import traceback
            tb = traceback.format_exc()
            print(f"[PROCESS_SCAN] Traceback:\n{tb}")
            # Always raise with a message
            if not error_detail or error_detail.strip() == "":
                error_detail = f"Crawl failed with {type(e).__name__} exception"
            raise Exception(f"Failed to crawl website: {error_detail}") from e
        
        # Check if we got any pages
        if not crawl_results.get('pages'):
            raise Exception("No pages were crawled. The website might be blocking crawlers, unreachable, or have no crawlable links.")
        
        # Step 2: SEO Audit
        print("Running SEO audit...")
        try:
            auditor = SEOAuditor(crawl_results)
            seo_audit = auditor.audit()
        except Exception as e:
            print(f"SEO audit failed: {e}")
            seo_audit = {"score": 0, "issues": [], "warnings": [], "summary": {"total_issues": 0, "total_warnings": 0, "total_pages": 0}}
        
        # Step 3: Keyword Analysis
        print("Analyzing keywords...")
        try:
            keyword_analyzer = KeywordAnalyzer(crawl_results)
            keywords = keyword_analyzer.analyze()
        except Exception as e:
            print(f"Keyword analysis failed: {e}")
            keywords = {"keywords": {"rake": [], "ngrams": {"unigrams": [], "bigrams": [], "trigrams": []}, "tfidf": []}, "keyword_clusters": [], "total_keywords": 0}
        
        # Step 4: Duplicate Detection
        print("Detecting duplicates...")
        try:
            duplicate_detector = DuplicateDetector(crawl_results)
            duplicates = duplicate_detector.detect()
        except Exception as e:
            print(f"Duplicate detection failed: {e}")
            duplicates = {"duplicates": [], "total_duplicates": 0, "methods_used": []}
        
        # Step 5: Page Power Analysis
        print("Analyzing page power...")
        try:
            page_power_analyzer = PagePowerAnalyzer(crawl_results)
            page_power = page_power_analyzer.analyze()
        except Exception as e:
            print(f"Page power analysis failed: {e}")
            page_power = {"page_power": {}, "top_pages": [], "average_power": 0}
        
        # Step 6: Performance Analysis (sample pages)
        print("Analyzing performance...")
        try:
            pagespeed_analyzer = PageSpeedAnalyzer()
            performance = await pagespeed_analyzer.analyze_sample(crawl_results, sample_size=5)
        except Exception as e:
            print(f"Performance analysis failed: {e}")
            performance = {"error": str(e), "results": []}
        
        print("Analysis complete!")
        
        # Combine all results
        result = {
            "crawl_results": crawl_results,
            "seo_audit": seo_audit,
            "keywords": keywords,
            "duplicates": duplicates,
            "page_power": page_power,
            "performance": performance,
            "scan_id": scan_id,
            "timestamp": datetime.now().isoformat()
        }
        
        scan_results[scan_id] = result
        scan_status[scan_id] = "completed"
        
    except Exception as e:
        import traceback
        import sys
        error_trace = traceback.format_exc()
        error_type = type(e).__name__
        
        # Try multiple ways to get error message
        error_msg = ""
        
        # Method 1: Direct string conversion
        try:
            error_msg = str(e).strip()
        except:
            pass
        
        # Method 2: Get from exception args
        if not error_msg and hasattr(e, 'args') and e.args:
            try:
                error_msg = str(e.args[0]).strip() if e.args[0] else ""
            except:
                pass
        
        # Method 3: Extract from traceback
        if not error_msg:
            traceback_lines = error_trace.split('\n')
            for i, line in enumerate(traceback_lines):
                # Look for exception type followed by message
                if error_type in line and i + 1 < len(traceback_lines):
                    next_line = traceback_lines[i + 1].strip()
                    if next_line and not next_line.startswith('File'):
                        error_msg = next_line
                        break
                # Look for common error patterns
                if any(pattern in line for pattern in ['Error:', 'Exception:', 'Failed', 'cannot', 'unable', 'invalid']):
                    if line.strip() and not line.strip().startswith('File'):
                        error_msg = line.strip()
                        break
        
        # Method 4: Use repr if available
        if not error_msg:
            try:
                error_repr = repr(e)
                if error_repr and error_repr != f"{error_type}()":
                    error_msg = error_repr
            except:
                pass
        
        # Final fallback - construct meaningful message
        if not error_msg or error_msg.strip() == "":
            # Get the last few lines of traceback for context
            traceback_lines = error_trace.split('\n')
            last_lines = [l for l in traceback_lines[-10:] if l.strip() and not l.strip().startswith('File')]
            context = last_lines[0] if last_lines else "Unknown location"
            error_msg = f"{error_type} occurred: {context[:200]}"
        
        # Ensure we have something
        if not error_msg or len(error_msg.strip()) == 0:
            error_msg = f"An error of type {error_type} occurred during scan processing. Please check the traceback for details."
        
        print(f"\n{'=' * 80}")
        print(f"ERROR processing scan {scan_id}")
        print(f"Error Type: {error_type}")
        print(f"Error Message: {error_msg}")
        print(f"Error Repr: {repr(e)}")
        print(f"{'=' * 80}")
        print("Full Traceback:")
        print(error_trace)
        print(f"{'=' * 80}\n")
        
        # Store error - ALWAYS with a message
        error_data = {
            "error": error_msg,
            "error_type": error_type,
            "traceback": error_trace,
            "scan_id": scan_id
        }
        
        scan_status[scan_id] = "error"
        scan_results[scan_id] = error_data
        
        # Verify storage
        stored = scan_results.get(scan_id, {})
        print(f"VERIFICATION: Stored error data for {scan_id}")
        print(f"  - Has error key: {'error' in stored}")
        print(f"  - Error value: '{stored.get('error', 'MISSING')}'")
        print(f"  - Error value length: {len(stored.get('error', ''))}")
        print(f"  - Full stored data keys: {list(stored.keys())}")


async def safe_process_scan_wrapper(scan_id: str, url: str, max_pages: int, include_external: bool):
    """Wrapper to ensure all errors are caught and stored"""
    try:
        await process_scan(scan_id, url, max_pages, include_external)
    except Exception as outer_e:
        # Final safety net
        import traceback
        error_trace = traceback.format_exc()
        error_type = type(outer_e).__name__
        error_msg = str(outer_e) if str(outer_e) else f"{error_type} occurred"
        
        if not error_msg or error_msg.strip() == "":
            error_msg = f"An unexpected error occurred: {error_type}. Please check backend logs."
        
        print(f"\n[SAFETY NET] Unhandled exception in wrapper for {scan_id}")
        print(f"Error: {error_msg}")
        print(error_trace)
        
        scan_status[scan_id] = "error"
        scan_results[scan_id] = {
            "error": error_msg,
            "error_type": error_type,
            "traceback": error_trace,
            "scan_id": scan_id
        }

@app.post("/api/scan", response_model=ScanResponse)
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """Start a new website scan"""
    scan_id = str(uuid.uuid4())
    scan_status[scan_id] = "pending"
    scan_results[scan_id] = {}  # Initialize
    
    # Start background task with safety wrapper
    background_tasks.add_task(
        safe_process_scan_wrapper,
        scan_id,
        str(request.url),
        request.max_pages,
        request.include_external
    )
    
    return ScanResponse(
        scan_id=scan_id,
        status="pending",
        message="Scan started successfully"
    )


@app.get("/api/scan/{scan_id}/status")
async def get_scan_status(scan_id: str):
    """Get the status of a scan"""
    if scan_id not in scan_status:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return {
        "scan_id": scan_id,
        "status": scan_status[scan_id]
    }


@app.get("/api/scan/{scan_id}/results")
async def get_scan_results(scan_id: str):
    """Get the results of a completed scan"""
    if scan_id not in scan_status:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    current_status = scan_status[scan_id]
    
    # If error, return error details immediately
    if current_status == "error":
        error_data = scan_results.get(scan_id, {})
        
        # Debug logging
        print(f"\n[DEBUG] get_scan_results for {scan_id}")
        print(f"  - Status: {current_status}")
        print(f"  - Has results: {scan_id in scan_results}")
        print(f"  - Error data keys: {list(error_data.keys()) if error_data else 'None'}")
        print(f"  - Error value: '{error_data.get('error', 'MISSING')}'")
        
        # Ensure we have valid error data
        if not error_data:
            error_data = {}
        
        # Ensure error message exists and is not empty
        if "error" not in error_data or not error_data.get("error") or error_data.get("error").strip() == "":
            error_type = error_data.get("error_type", "UnknownError")
            error_data["error"] = f"An error occurred during the scan (Type: {error_type}). Check backend terminal logs for full details."
            error_data["error_type"] = error_type
            error_data["scan_id"] = scan_id
            print(f"  - [FIXED] Set default error message: {error_data['error'][:100]}")
        
        print(f"  - Returning error: '{error_data.get('error', 'MISSING')[:100]}...'")
        return error_data
    
    # If still processing, return 202
    if current_status != "completed":
        raise HTTPException(status_code=202, detail="Scan still in progress")
    
    # Return completed results
    return scan_results.get(scan_id, {})


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/api/debug/scan/{scan_id}")
async def debug_scan(scan_id: str):
    """Debug endpoint to see scan status and results"""
    if scan_id not in scan_status:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return {
        "scan_id": scan_id,
        "status": scan_status.get(scan_id, "not_found"),
        "has_results": scan_id in scan_results,
        "results_keys": list(scan_results.get(scan_id, {}).keys()) if scan_id in scan_results else [],
        "error_data": scan_results.get(scan_id, {}) if scan_status.get(scan_id) == "error" else None,
        "full_results": scan_results.get(scan_id, {})
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

