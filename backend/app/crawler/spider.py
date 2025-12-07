import asyncio
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Set, Any, Optional
import time
from bs4 import BeautifulSoup
import httpx
import hashlib
import re

# Try to import Playwright, but make it optional
try:
    from playwright.async_api import async_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Browser = None
    Page = None
    async_playwright = None


class WebsiteCrawler:
    def __init__(self, max_pages: int = 100, include_external: bool = False):
        self.max_pages = max_pages
        self.include_external = include_external
        self.visited: Set[str] = set()
        self.pages: List[Dict[str, Any]] = []
        self.all_links: Set[str] = set()
        self.all_images: List[Dict[str, Any]] = []
        self.base_domain: Optional[str] = None
        self.browser: Optional[Browser] = None
        self.url_to_page: Dict[str, Dict[str, Any]] = {}  # Map URL to page data
        self.backlinks: Dict[str, List[Dict[str, Any]]] = {}  # Map URL to pages that link to it
        self.broken_links: List[Dict[str, Any]] = []  # List of broken links found
        
    async def crawl(self, start_url: str) -> Dict[str, Any]:
        """Main crawl method"""
        try:
            parsed = urlparse(start_url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(f"Invalid URL: {start_url}")
            self.base_domain = f"{parsed.scheme}://{parsed.netloc}"
        except Exception as e:
            print(f"Error parsing URL {start_url}: {e}")
            raise
        
        # Use HTTP-only mode (Playwright has issues on Windows/Python 3.13)
        # For most websites, HTTP-only works fine
        print("Using HTTP-only crawling mode (no JavaScript rendering)")
        self.browser = None
        
        try:
            await self._crawl_recursive(start_url, depth=0, max_depth=10)
        except Exception as e:
            error_msg = str(e) if str(e) else f"{type(e).__name__} occurred during crawling"
            print(f"Error during crawling: {error_msg}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            # Re-raise with a proper message if empty
            if not str(e):
                raise Exception(f"Crawl failed: {type(e).__name__} occurred. Check traceback for details.")
            raise
        
        # Calculate stats
        stats = self._calculate_stats()
        
        # Calculate link statistics
        all_internal_links = []
        all_external_links = []
        untitled_links = []
        
        for page in self.pages:
            for link in page.get("all_links", []):
                if link.get("internal"):
                    all_internal_links.append(link)
                else:
                    all_external_links.append(link)
                if link.get("is_untitled"):
                    untitled_links.append(link)
        
        return {
            "pages": self.pages,
            "links": list(self.all_links),
            "images": self.all_images,
            "stats": stats,
            "link_analysis": {
                "total_internal_links": len(all_internal_links),
                "total_external_links": len(all_external_links),
                "untitled_links": untitled_links,
                "broken_links": self.broken_links,
                "internal_links_detailed": all_internal_links,
                "external_links_detailed": all_external_links
            },
            "backlinks_map": {url: links for url, links in self.backlinks.items() if links}
        }
    
    async def _crawl_recursive(self, url: str, depth: int, max_depth: int):
        """Recursively crawl pages"""
        if len(self.visited) >= self.max_pages or depth > max_depth:
            return
        
        # Increased max_depth to support deeper crawling
        if max_depth < 15:
            max_depth = 15
        
        # Normalize URL
        normalized_url = self._normalize_url(url)
        if normalized_url in self.visited:
            return
        
        self.visited.add(normalized_url)
        
        try:
            page_data = await self._fetch_page(normalized_url, depth)
            if page_data:
                page_data["crawl_depth"] = depth
                self.pages.append(page_data)
                self.url_to_page[normalized_url] = page_data
                
                # Extract and follow internal links
                internal_links = page_data.get("internal_links", [])
                for link in internal_links[:20]:  # Increased limit
                    if len(self.visited) < self.max_pages:
                        await self._crawl_recursive(link, depth + 1, max_depth)
        except Exception as e:
            print(f"Error crawling {url}: {e}")
    
    async def _fetch_page(self, url: str, depth: int = 0) -> Optional[Dict[str, Any]]:
        """Fetch and parse a single page"""
        start_time = time.time()
        
        # Try with Playwright first (for JS-rendered pages) - but only if browser is available
        if self.browser:
            try:
                page_data = await self._fetch_with_playwright(url)
                if page_data:
                    load_time = time.time() - start_time
                    page_data["load_time"] = load_time
                    return page_data
            except Exception as e:
                # Silently fall through to HTTP request
                pass
        
        # Fallback to HTTP request (always used if Playwright unavailable)
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(url)
                if response.status_code < 400:  # Accept 2xx and 3xx status codes
                    load_time = time.time() - start_time
                    page_data = self._parse_html(url, response.text, response.status_code)
                    page_data["load_time"] = load_time
                    return page_data
                else:
                    # Still parse error pages to get basic info
                    load_time = time.time() - start_time
                    page_data = self._parse_html(url, response.text, response.status_code)
                    page_data["load_time"] = load_time
                    return page_data
        except Exception as e:
            print(f"HTTP fetch failed for {url}: {e}")
            return None
    
    async def _fetch_with_playwright(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetch page using Playwright for JS rendering"""
        if not self.browser:
            return None
        
        # Check if browser is still open
        try:
            if self.browser and hasattr(self.browser, 'is_connected'):
                if not self.browser.is_connected():
                    return None
        except:
            return None
        
        context = None
        page = None
        try:
            context = await self.browser.new_context()
            page = await context.new_page()
            
            response = await page.goto(url, wait_until="networkidle", timeout=30000)
            if not response:
                return None
            
            status_code = response.status
            html = await page.content()
            
            # Wait a bit for any lazy-loaded content
            await asyncio.sleep(1)
            
            page_data = self._parse_html(url, html, status_code)
            return page_data
            
        except Exception as e:
            error_msg = str(e) if str(e) else f"{type(e).__name__}"
            # Don't print if browser was closed (expected during shutdown)
            if "closed" not in error_msg.lower() and "disconnected" not in error_msg.lower():
                print(f"Playwright error for {url}: {error_msg}")
            return None
        finally:
            if page:
                try:
                    await page.close()
                except:
                    pass
            if context:
                try:
                    await context.close()
                except:
                    pass
    
    def _parse_html(self, url: str, html: str, status_code: int) -> Dict[str, Any]:
        """Parse HTML and extract data"""
        try:
            soup = BeautifulSoup(html, 'lxml')
        except Exception as e:
            print(f"Error parsing HTML for {url}: {e}")
            # Fallback to html.parser if lxml fails
            soup = BeautifulSoup(html, 'html.parser')
        
        # Basic metadata
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else ""
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_desc_text = meta_desc.get('content', '') if meta_desc else ""
        
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        canonical_url = canonical.get('href', '') if canonical else ""
        if canonical_url and not canonical_url.startswith('http'):
            canonical_url = urljoin(url, canonical_url)
        
        # Headings
        h1_tags = [h.get_text(strip=True) for h in soup.find_all('h1')]
        h2_tags = [h.get_text(strip=True) for h in soup.find_all('h2')]
        
        # Content extraction
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        text_content = soup.get_text(separator=' ', strip=True)
        word_count = len(text_content.split())
        
        # Links - Detailed collection
        all_links = []
        internal_links = []
        external_links = []
        broken_links = []
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            link_text = link.get_text(strip=True)
            link_title = link.get('title', '')
            absolute_url = urljoin(url, href)
            
            parsed_link = urlparse(absolute_url)
            is_internal = parsed_link.netloc == urlparse(self.base_domain).netloc or not parsed_link.netloc
            
            # Check if link has no text (untitled)
            is_untitled = not link_text or link_text.strip() == ""
            
            link_data = {
                "url": absolute_url,
                "href": href,
                "anchor_text": link_text,
                "title": link_title,
                "is_untitled": is_untitled,
                "internal": is_internal,
                "source_page": url,
                "location": self._get_element_location(link)  # Line number approximation
            }
            all_links.append(link_data)
            self.all_links.add(absolute_url)
            
            if is_internal:
                normalized = self._normalize_url(absolute_url)
                if normalized.startswith(self.base_domain):
                    if normalized not in self.visited:
                        internal_links.append(normalized)
                    # Track backlink for ALL internal pages (visited or not)
                    if normalized not in self.backlinks:
                        self.backlinks[normalized] = []
                    self.backlinks[normalized].append({
                        "from_url": url,
                        "anchor_text": link_text,
                        "title": link_title
                    })
            else:
                external_links.append(absolute_url)
            
            # Check for broken links (empty href, javascript:, mailto:, etc.)
            if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                if href and href.startswith('#'):
                    # Anchor link - check if target exists on page
                    target_id = href[1:]
                    if not soup.find(id=target_id) and not soup.find(attrs={'name': target_id}):
                        broken_links.append({
                            **link_data,
                            "issue": "Broken anchor link",
                            "reason": f"Target '{target_id}' not found on page"
                        })
                elif not href:
                    broken_links.append({
                        **link_data,
                        "issue": "Empty href",
                        "reason": "Link has no href attribute"
                    })
        
        # Store broken links
        for broken in broken_links:
            self.broken_links.append(broken)
        
        # Images
        images = []
        for img in soup.find_all('img'):
            img_src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if img_src:
                img_url = urljoin(url, img_src)
                alt_text = img.get('alt', '')
                
                img_data = {
                    "url": img_url,
                    "alt": alt_text,
                    "page_url": url
                }
                images.append(img_data)
                self.all_images.append(img_data)
        
        # Content hash for duplicate detection
        content_hash = hashlib.md5(text_content.encode()).hexdigest()
        
        return {
            "url": url,
            "status_code": status_code,
            "title": title_text,
            "meta_description": meta_desc_text,
            "canonical": canonical_url,
            "h1": h1_tags,
            "h2": h2_tags[:20],  # Increased limit
            "content": text_content[:10000],  # Increased content length
            "word_count": word_count,
            "content_hash": content_hash,
            "internal_links": list(set(internal_links)),
            "external_links": external_links[:50],  # Increased limit
            "images": images,
            "all_links": all_links,  # Keep all links for detailed analysis
            "internal_links_detailed": [l for l in all_links if l["internal"]],
            "external_links_detailed": [l for l in all_links if not l["internal"]],
            "broken_links_on_page": broken_links,
            "backlinks_count": len(self.backlinks.get(url, [])),
            "backlinks": self.backlinks.get(url, [])
        }
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL for comparison"""
        parsed = urlparse(url)
        # Remove fragment and trailing slash
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"
        if parsed.query:
            normalized += f"?{parsed.query}"
        return normalized
    
    def _get_element_location(self, element) -> str:
        """Get approximate location of element in HTML"""
        try:
            # Try to get line number from BeautifulSoup
            if hasattr(element, 'sourceline'):
                return f"Line {element.sourceline}"
            # Fallback: get parent tag info
            parent = element.parent
            if parent:
                return f"In <{parent.name}> tag"
            return "Unknown location"
        except:
            return "Unknown location"
    
    def _calculate_stats(self) -> Dict[str, Any]:
        """Calculate crawl statistics"""
        total_pages = len(self.pages)
        if total_pages == 0:
            return {}
        
        total_words = sum(p.get("word_count", 0) for p in self.pages)
        avg_load_time = sum(p.get("load_time", 0) for p in self.pages) / total_pages
        pages_with_title = sum(1 for p in self.pages if p.get("title"))
        pages_with_meta = sum(1 for p in self.pages if p.get("meta_description"))
        total_images = len(self.all_images)
        total_links = len(self.all_links)
        
        status_codes = {}
        for page in self.pages:
            code = page.get("status_code", 0)
            status_codes[code] = status_codes.get(code, 0) + 1
        
        return {
            "total_pages": total_pages,
            "total_words": total_words,
            "avg_word_count": total_words / total_pages if total_pages > 0 else 0,
            "avg_load_time": round(avg_load_time, 2),
            "pages_with_title": pages_with_title,
            "pages_with_meta": pages_with_meta,
            "total_images": total_images,
            "total_links": total_links,
            "status_codes": status_codes
        }

