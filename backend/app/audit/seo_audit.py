from typing import Dict, List, Any
from urllib.parse import urlparse
from collections import Counter


class SEOAuditor:
    def __init__(self, crawl_results: Dict[str, Any]):
        self.crawl_results = crawl_results
        self.pages = crawl_results.get("pages", [])
        self.issues: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        # Store crawl_results for access in methods
        self.crawl_results = crawl_results
        
    def audit(self) -> Dict[str, Any]:
        """Run complete SEO audit"""
        self._check_missing_titles()
        self._check_missing_meta_descriptions()
        self._check_short_content()
        self._check_duplicate_h1()
        self._check_broken_links()
        self._check_redirect_chains()
        self._check_canonical_issues()
        self._check_sitemap()
        self._check_robots_txt()
        self._check_page_depth()
        self._check_duplicate_titles()
        self._check_duplicate_meta_descriptions()
        self._check_untitled_links()
        self._check_image_alt_text()
        
        # Calculate score
        total_checks = len(self.pages) * 10  # Approximate
        issues_count = len(self.issues)
        warnings_count = len(self.warnings)
        
        score = max(0, 100 - (issues_count * 5) - (warnings_count * 2))
        score = min(100, score)
        
        return {
            "score": round(score, 1),
            "issues": self.issues,
            "warnings": self.warnings,
            "summary": {
                "total_issues": len(self.issues),
                "total_warnings": len(self.warnings),
                "total_pages": len(self.pages)
            }
        }
    
    def _check_missing_titles(self):
        """Check for pages without titles"""
        for page in self.pages:
            if not page.get("title") or not page.get("title").strip():
                self.issues.append({
                    "type": "missing_title",
                    "severity": "high",
                    "page": page.get("url"),
                    "message": "Page is missing a title tag",
                    "fix": "Add a <title> tag in the <head> section of your HTML",
                    "example": "<title>Your Page Title Here</title>",
                    "location": "HTML <head> section",
                    "impact": "Titles are crucial for SEO and appear in search results"
                })
    
    def _check_missing_meta_descriptions(self):
        """Check for pages without meta descriptions"""
        for page in self.pages:
            if not page.get("meta_description") or not page.get("meta_description").strip():
                self.warnings.append({
                    "type": "missing_meta_description",
                    "severity": "medium",
                    "page": page.get("url"),
                    "message": "Page is missing a meta description",
                    "fix": "Add a meta description tag in the <head> section",
                    "example": '<meta name="description" content="Your page description here (150-160 characters)">',
                    "location": "HTML <head> section",
                    "impact": "Meta descriptions appear in search results and can improve click-through rates"
                })
    
    def _check_short_content(self):
        """Check for pages with very short content"""
        for page in self.pages:
            word_count = page.get("word_count", 0)
            if word_count < 300:
                self.warnings.append({
                    "type": "short_content",
                    "severity": "medium",
                    "page": page.get("url"),
                    "message": f"Page has only {word_count} words (recommended: 300+)",
                    "word_count": word_count,
                    "fix": "Add more relevant content to the page. Aim for at least 300 words",
                    "location": page.get("url"),
                    "impact": "Short content may not rank well in search engines"
                })
    
    def _check_duplicate_h1(self):
        """Check for pages with multiple H1 tags"""
        for page in self.pages:
            h1_tags = page.get("h1", [])
            if len(h1_tags) > 1:
                self.issues.append({
                    "type": "multiple_h1",
                    "severity": "high",
                    "page": page.get("url"),
                    "message": f"Page has {len(h1_tags)} H1 tags (should be 1)",
                    "h1_count": len(h1_tags),
                    "h1_tags": h1_tags,
                    "fix": "Keep only one H1 tag per page. Use H2-H6 for other headings",
                    "example": "<h1>Main Page Title</h1>\n<h2>Section Title</h2>",
                    "location": "Page body content",
                    "impact": "Multiple H1 tags can confuse search engines about page hierarchy"
                })
            elif len(h1_tags) == 0:
                self.warnings.append({
                    "type": "missing_h1",
                    "severity": "medium",
                    "page": page.get("url"),
                    "message": "Page is missing an H1 tag",
                    "fix": "Add a single H1 tag with your main page heading",
                    "example": "<h1>Your Main Heading</h1>",
                    "location": "Page body content",
                    "impact": "H1 tags help search engines understand page structure"
                })
    
    def _check_broken_links(self):
        """Check for broken internal links (4xx, 5xx status codes)"""
        broken_status_codes = [404, 500, 502, 503, 504]
        for page in self.pages:
            status_code = page.get("status_code", 200)
            if status_code in broken_status_codes:
                status_messages = {
                    404: "Page Not Found",
                    500: "Internal Server Error",
                    502: "Bad Gateway",
                    503: "Service Unavailable",
                    504: "Gateway Timeout"
                }
                self.issues.append({
                    "type": "broken_link",
                    "severity": "high",
                    "page": page.get("url"),
                    "message": f"Page returns status code {status_code} ({status_messages.get(status_code, 'Error')})",
                    "status_code": status_code,
                    "fix": f"Fix the {status_messages.get(status_code, 'server error')}. Check if the page exists, server configuration, or hosting issues",
                    "location": page.get("url"),
                    "impact": "Broken pages harm user experience and SEO rankings"
                })
        
        # Check broken links found during crawling
        crawl_results = getattr(self, 'crawl_results', {})
        link_analysis = crawl_results.get('link_analysis', {})
        broken_links = link_analysis.get('broken_links', [])
        
        for broken_link in broken_links:
            self.issues.append({
                "type": "broken_link_detected",
                "severity": "high",
                "page": broken_link.get("source_page"),
                "message": f"Broken link found: {broken_link.get('issue', 'Unknown issue')}",
                "broken_url": broken_link.get("url"),
                "anchor_text": broken_link.get("anchor_text", "No text"),
                "location": broken_link.get("location", "Unknown"),
                "fix": broken_link.get("reason", "Fix or remove this link"),
                "impact": "Broken links create poor user experience"
            })
    
    def _check_redirect_chains(self):
        """Check for redirect chains (3xx status codes)"""
        redirect_codes = [301, 302, 307, 308]
        for page in self.pages:
            status_code = page.get("status_code", 200)
            if status_code in redirect_codes:
                self.warnings.append({
                    "type": "redirect",
                    "severity": "medium",
                    "page": page.get("url"),
                    "message": f"Page redirects with status {status_code}",
                    "status_code": status_code
                })
    
    def _check_canonical_issues(self):
        """Check for canonical tag issues"""
        for page in self.pages:
            canonical = page.get("canonical", "")
            page_url = page.get("url", "")
            
            if canonical and canonical != page_url:
                # Check if canonical points to different page
                parsed_canonical = urlparse(canonical)
                parsed_page = urlparse(page_url)
                
                if parsed_canonical.path != parsed_page.path:
                    self.warnings.append({
                        "type": "canonical_mismatch",
                        "severity": "low",
                        "page": page_url,
                        "message": f"Canonical URL differs from page URL",
                        "canonical": canonical
                    })
    
    def _check_sitemap(self):
        """Check if sitemap exists"""
        # This would require additional HTTP request, simplified for now
        # In production, you'd check robots.txt and common sitemap locations
        pass
    
    def _check_robots_txt(self):
        """Check if robots.txt exists"""
        # This would require additional HTTP request, simplified for now
        pass
    
    def _check_page_depth(self):
        """Analyze page depth (how many clicks from homepage)"""
        # Simplified depth analysis
        base_domain = None
        for page in self.pages:
            parsed = urlparse(page.get("url", ""))
            if not base_domain:
                base_domain = parsed.netloc
                break
        
        # Count path depth
        depth_distribution = {}
        for page in self.pages:
            parsed = urlparse(page.get("url", ""))
            depth = len([p for p in parsed.path.split('/') if p])
            depth_distribution[depth] = depth_distribution.get(depth, 0) + 1
        
        # Warn if many deep pages
        deep_pages = sum(count for depth, count in depth_distribution.items() if depth > 3)
        if deep_pages > len(self.pages) * 0.3:
            self.warnings.append({
                "type": "deep_pages",
                "severity": "low",
                "message": f"{deep_pages} pages are more than 3 levels deep",
                "depth_distribution": depth_distribution
            })
    
    def _check_duplicate_titles(self):
        """Check for duplicate page titles"""
        title_counter = Counter(page.get("title", "") for page in self.pages)
        duplicates = {title: count for title, count in title_counter.items() if count > 1 and title}
        
        if duplicates:
            for title, count in duplicates.items():
                pages_with_title = [p.get("url") for p in self.pages if p.get("title") == title]
                self.issues.append({
                    "type": "duplicate_title",
                    "severity": "high",
                    "message": f"Title '{title[:50]}...' is used on {count} pages",
                    "pages": pages_with_title[:5]  # Limit to first 5
                })
    
    def _check_duplicate_meta_descriptions(self):
        """Check for duplicate meta descriptions"""
        meta_counter = Counter(page.get("meta_description", "") for page in self.pages)
        duplicates = {meta: count for meta, count in meta_counter.items() if count > 1 and meta}
        
        if duplicates:
            for meta, count in duplicates.items():
                pages_with_meta = [p.get("url") for p in self.pages if p.get("meta_description") == meta]
                self.warnings.append({
                    "type": "duplicate_meta_description",
                    "severity": "medium",
                    "message": f"Meta description is duplicated on {count} pages",
                    "pages": pages_with_meta[:5]  # Limit to first 5
                })
    
    def _check_untitled_links(self):
        """Check for links without anchor text"""
        link_analysis = self.crawl_results.get("link_analysis", {})
        untitled_links = link_analysis.get("untitled_links", [])
        
        if untitled_links:
            # Group by source page
            by_page = {}
            for link in untitled_links[:50]:  # Limit to 50
                page = link.get("source_page", "Unknown")
                if page not in by_page:
                    by_page[page] = []
                by_page[page].append(link)
            
            for page_url, links in list(by_page.items())[:10]:  # Top 10 pages
                self.warnings.append({
                    "type": "untitled_links",
                    "severity": "low",
                    "page": page_url,
                    "message": f"Found {len(links)} links without anchor text on this page",
                    "untitled_count": len(links),
                    "fix": "Add descriptive anchor text to all links. Avoid 'click here' or empty links",
                    "example": '<a href="/page">Descriptive Link Text</a>',
                    "location": page_url,
                    "impact": "Links without text are not accessible and provide no context"
                })
    
    def _check_image_alt_text(self):
        """Check for images without alt text"""
        for page in self.pages:
            images = page.get("images", [])
            images_without_alt = [img for img in images if not img.get("alt") or not img.get("alt").strip()]
            
            if images_without_alt:
                self.warnings.append({
                    "type": "missing_image_alt",
                    "severity": "medium",
                    "page": page.get("url"),
                    "message": f"Found {len(images_without_alt)} images without alt text",
                    "missing_alt_count": len(images_without_alt),
                    "fix": "Add alt attributes to all images for accessibility and SEO",
                    "example": '<img src="image.jpg" alt="Description of image">',
                    "location": page.get("url"),
                    "impact": "Images without alt text are not accessible and miss SEO opportunities"
                })

