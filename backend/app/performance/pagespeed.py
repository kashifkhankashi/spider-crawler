from typing import Dict, List, Any, Optional
import httpx
import os
from urllib.parse import urlparse
import random


class PageSpeedAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_PAGESPEED_API_KEY", "")
        self.api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        
    async def analyze_sample(self, crawl_results: Dict[str, Any], sample_size: int = 5) -> Dict[str, Any]:
        """Analyze a sample of pages using PageSpeed API"""
        pages = crawl_results.get("pages", [])
        
        if not pages:
            return {
                "error": "No pages to analyze",
                "results": []
            }
        
        # Sample pages (prioritize homepage and important pages)
        sample_pages = self._select_sample_pages(pages, sample_size)
        
        results = []
        for page in sample_pages:
            page_result = await self._analyze_page(page.get("url"))
            if page_result:
                results.append(page_result)
        
        # Aggregate metrics
        if results:
            aggregated = self._aggregate_metrics(results)
            return {
                "results": results,
                "aggregated": aggregated,
                "sample_size": len(results)
            }
        else:
            return {
                "error": "No results from PageSpeed API",
                "results": [],
                "note": "API key may be required. Set GOOGLE_PAGESPEED_API_KEY environment variable."
            }
    
    def _select_sample_pages(self, pages: List[Dict], sample_size: int) -> List[Dict]:
        """Select representative sample of pages"""
        # Prioritize homepage
        homepage = None
        for page in pages:
            parsed = urlparse(page.get("url", ""))
            if parsed.path == "/" or parsed.path == "":
                homepage = page
                break
        
        sample = []
        if homepage:
            sample.append(homepage)
        
        # Add random pages
        remaining = [p for p in pages if p != homepage]
        random.shuffle(remaining)
        sample.extend(remaining[:sample_size - len(sample)])
        
        return sample
    
    async def _analyze_page(self, url: str) -> Optional[Dict[str, Any]]:
        """Analyze a single page with PageSpeed API"""
        if not self.api_key:
            # Return mock data if no API key
            return {
                "url": url,
                "LCP": "2.5s",
                "CLS": "0.1",
                "FID": "50ms",
                "FCP": "1.2s",
                "TTI": "3.0s",
                "score": 85,
                "note": "Mock data - API key required for real analysis"
            }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                params = {
                    "url": url,
                    "key": self.api_key,
                    "strategy": "mobile"  # or "desktop"
                }
                
                response = await client.get(self.api_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_pagespeed_response(url, data)
                else:
                    print(f"PageSpeed API error for {url}: {response.status_code}")
                    return None
        except Exception as e:
            print(f"PageSpeed API exception for {url}: {e}")
            return None
    
    def _parse_pagespeed_response(self, url: str, data: Dict) -> Dict[str, Any]:
        """Parse PageSpeed API response"""
        try:
            lighthouse_result = data.get("lighthouseResult", {})
            audits = lighthouse_result.get("audits", {})
            categories = lighthouse_result.get("categories", {})
            
            # Extract Core Web Vitals
            lcp = audits.get("largest-contentful-paint", {})
            cls = audits.get("cumulative-layout-shift", {})
            fid = audits.get("max-potential-fid", {})
            fcp = audits.get("first-contentful-paint", {})
            tti = audits.get("interactive", {})
            
            # Performance score
            performance = categories.get("performance", {})
            score = performance.get("score", 0) * 100
            
            # Recommendations
            recommendations = []
            for audit_key, audit_data in audits.items():
                if audit_data.get("score") is not None and audit_data.get("score") < 0.9:
                    recommendations.append({
                        "id": audit_key,
                        "title": audit_data.get("title", ""),
                        "description": audit_data.get("description", ""),
                        "score": audit_data.get("score", 0)
                    })
            
            return {
                "url": url,
                "LCP": self._format_metric(lcp.get("numericValue", 0)),
                "CLS": round(cls.get("numericValue", 0), 3),
                "FID": self._format_metric(fid.get("numericValue", 0)),
                "FCP": self._format_metric(fcp.get("numericValue", 0)),
                "TTI": self._format_metric(tti.get("numericValue", 0)),
                "score": round(score, 1),
                "recommendations": recommendations[:10]  # Top 10
            }
        except Exception as e:
            print(f"Error parsing PageSpeed response: {e}")
            return {
                "url": url,
                "error": str(e)
            }
    
    def _format_metric(self, value: float) -> str:
        """Format metric value"""
        if value < 1000:
            return f"{value:.0f}ms"
        else:
            return f"{value/1000:.2f}s"
    
    def _aggregate_metrics(self, results: List[Dict]) -> Dict[str, Any]:
        """Aggregate metrics across all analyzed pages"""
        if not results:
            return {}
        
        scores = [r.get("score", 0) for r in results if r.get("score")]
        lcp_values = [self._parse_metric(r.get("LCP", "0ms")) for r in results if r.get("LCP")]
        cls_values = [r.get("CLS", 0) for r in results if isinstance(r.get("CLS"), (int, float))]
        
        return {
            "avg_score": round(sum(scores) / len(scores), 1) if scores else 0,
            "avg_LCP": self._format_metric(sum(lcp_values) / len(lcp_values)) if lcp_values else "N/A",
            "avg_CLS": round(sum(cls_values) / len(cls_values), 3) if cls_values else 0,
            "pages_analyzed": len(results)
        }
    
    def _parse_metric(self, value: str) -> float:
        """Parse metric string to float (ms)"""
        try:
            if value.endswith("s"):
                return float(value[:-1]) * 1000
            elif value.endswith("ms"):
                return float(value[:-2])
            else:
                return float(value)
        except:
            return 0.0

