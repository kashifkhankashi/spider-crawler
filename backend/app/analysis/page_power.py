from typing import Dict, List, Any
from urllib.parse import urlparse
from collections import defaultdict


class PagePowerAnalyzer:
    def __init__(self, crawl_results: Dict[str, Any]):
        self.crawl_results = crawl_results
        self.pages = crawl_results.get("pages", [])
        self.backlinks_map = crawl_results.get("backlinks_map", {})
        
    def analyze(self) -> Dict[str, Any]:
        """Calculate page power/authority for each page"""
        page_scores = {}
        
        for page in self.pages:
            url = page.get("url", "")
            score = self._calculate_page_power(page, url)
            page_scores[url] = score
        
        # Sort by power score
        sorted_pages = sorted(
            page_scores.items(),
            key=lambda x: x[1]["total_score"],
            reverse=True
        )
        
        return {
            "page_power": {url: score for url, score in sorted_pages},
            "top_pages": [
                {
                    "url": url,
                    **score
                }
                for url, score in sorted_pages[:20]  # Top 20
            ],
            "average_power": sum(s["total_score"] for s in page_scores.values()) / len(page_scores) if page_scores else 0
        }
    
    def _calculate_page_power(self, page: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Calculate power score for a single page"""
        score = 0
        factors = {}
        
        # Factor 1: Backlinks (most important)
        backlinks_count = page.get("backlinks_count", 0)
        backlink_score = min(backlinks_count * 10, 100)  # Max 100 points
        score += backlink_score
        factors["backlinks"] = {
            "count": backlinks_count,
            "score": backlink_score,
            "weight": "High - Internal links boost page authority"
        }
        
        # Factor 2: Internal links (outgoing)
        internal_links = len(page.get("internal_links", []))
        internal_link_score = min(internal_links * 2, 50)  # Max 50 points
        score += internal_link_score
        factors["internal_links"] = {
            "count": internal_links,
            "score": internal_link_score,
            "weight": "Medium - Shows page is well-connected"
        }
        
        # Factor 3: Word count (content depth)
        word_count = page.get("word_count", 0)
        if word_count >= 1000:
            content_score = 30
        elif word_count >= 500:
            content_score = 20
        elif word_count >= 300:
            content_score = 10
        else:
            content_score = 5
        score += content_score
        factors["content_depth"] = {
            "word_count": word_count,
            "score": content_score,
            "weight": "Medium - More content = more authority"
        }
        
        # Factor 4: Crawl depth (homepage and shallow pages are more powerful)
        depth = page.get("crawl_depth", 0)
        if depth == 0:
            depth_score = 30  # Homepage
        elif depth == 1:
            depth_score = 20
        elif depth == 2:
            depth_score = 10
        else:
            depth_score = 5
        score += depth_score
        factors["crawl_depth"] = {
            "depth": depth,
            "score": depth_score,
            "weight": "Medium - Shallow pages are easier to find"
        }
        
        # Factor 5: SEO elements
        seo_score = 0
        if page.get("title"):
            seo_score += 5
        if page.get("meta_description"):
            seo_score += 5
        if page.get("h1"):
            seo_score += 5
        if page.get("canonical"):
            seo_score += 5
        score += seo_score
        factors["seo_elements"] = {
            "has_title": bool(page.get("title")),
            "has_meta": bool(page.get("meta_description")),
            "has_h1": bool(page.get("h1")),
            "has_canonical": bool(page.get("canonical")),
            "score": seo_score,
            "weight": "Low - Basic SEO elements"
        }
        
        # Factor 6: Images (engagement)
        images_count = len(page.get("images", []))
        image_score = min(images_count // 5, 10)  # Max 10 points
        score += image_score
        factors["images"] = {
            "count": images_count,
            "score": image_score,
            "weight": "Low - Visual content improves engagement"
        }
        
        # Normalize to 0-100 scale
        total_score = min(score, 100)
        
        # Determine power level
        if total_score >= 80:
            power_level = "Very High"
        elif total_score >= 60:
            power_level = "High"
        elif total_score >= 40:
            power_level = "Medium"
        elif total_score >= 20:
            power_level = "Low"
        else:
            power_level = "Very Low"
        
        return {
            "total_score": round(total_score, 1),
            "power_level": power_level,
            "factors": factors,
            "recommendations": self._get_recommendations(factors, total_score)
        }
    
    def _get_recommendations(self, factors: Dict, score: float) -> List[str]:
        """Get recommendations to improve page power"""
        recommendations = []
        
        if factors.get("backlinks", {}).get("count", 0) < 5:
            recommendations.append("Increase internal backlinks - Get more pages to link to this page")
        
        if factors.get("internal_links", {}).get("count", 0) < 10:
            recommendations.append("Add more internal links to other relevant pages")
        
        if factors.get("content_depth", {}).get("word_count", 0) < 500:
            recommendations.append("Expand content - Aim for at least 500 words")
        
        if not factors.get("seo_elements", {}).get("has_title"):
            recommendations.append("Add a title tag")
        
        if not factors.get("seo_elements", {}).get("has_meta"):
            recommendations.append("Add a meta description")
        
        if score < 50:
            recommendations.append("Overall: Focus on getting more internal backlinks and expanding content")
        
        return recommendations



