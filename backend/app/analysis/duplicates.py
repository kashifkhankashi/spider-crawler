from typing import Dict, List, Any
from datasketch import MinHash, MinHashLSH
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from itertools import combinations


class DuplicateDetector:
    def __init__(self, crawl_results: Dict[str, Any]):
        self.crawl_results = crawl_results
        self.pages = crawl_results.get("pages", [])
        
    def detect(self) -> Dict[str, Any]:
        """Detect duplicate content using multiple methods"""
        if not self.pages or len(self.pages) < 2:
            return {
                "duplicates": [],
                "total_duplicates": 0,
                "methods_used": []
            }
        
        duplicates_minhash = self._detect_with_minhash()
        duplicates_cosine = self._detect_with_cosine()
        duplicates_jaccard = self._detect_with_jaccard()
        
        # Combine results (remove duplicates)
        all_duplicates = {}
        
        for dup in duplicates_minhash + duplicates_cosine + duplicates_jaccard:
            key = tuple(sorted([dup["page1"], dup["page2"]]))
            if key not in all_duplicates or dup["similarity"] > all_duplicates[key]["similarity"]:
                all_duplicates[key] = dup
        
        duplicates_list = list(all_duplicates.values())
        duplicates_list.sort(key=lambda x: x["similarity"], reverse=True)
        
        return {
            "duplicates": duplicates_list[:50],  # Top 50 duplicates
            "total_duplicates": len(duplicates_list),
            "methods_used": ["minhash", "cosine", "jaccard"]
        }
    
    def _detect_with_minhash(self) -> List[Dict[str, Any]]:
        """Detect duplicates using MinHash"""
        duplicates = []
        
        try:
            # Create MinHash for each page
            minhashes = []
            for page in self.pages:
                text = self._get_page_text(page)
                if not text:
                    continue
                
                m = MinHash(num_perm=128)
                # Add shingles (word sequences)
                words = text.split()
                for i in range(len(words) - 2):
                    shingle = " ".join(words[i:i+3])
                    m.update(shingle.encode('utf8'))
                
                minhashes.append({
                    "minhash": m,
                    "url": page.get("url"),
                    "text": text
                })
            
            # Compare all pairs
            for i in range(len(minhashes)):
                for j in range(i + 1, len(minhashes)):
                    similarity = minhashes[i]["minhash"].jaccard(minhashes[j]["minhash"])
                    if similarity > 0.7:  # Threshold
                        duplicates.append({
                            "page1": minhashes[i]["url"],
                            "page2": minhashes[j]["url"],
                            "similarity": round(similarity, 3),
                            "method": "minhash"
                        })
        except Exception as e:
            print(f"MinHash error: {e}")
        
        return duplicates
    
    def _detect_with_cosine(self) -> List[Dict[str, Any]]:
        """Detect duplicates using Cosine Similarity"""
        duplicates = []
        
        try:
            # Prepare texts
            texts = []
            urls = []
            for page in self.pages:
                text = self._get_page_text(page)
                if text and len(text) > 100:  # Minimum length
                    texts.append(text)
                    urls.append(page.get("url"))
            
            if len(texts) < 2:
                return duplicates
            
            # TF-IDF vectorization
            vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            # Find similar pairs
            for i in range(len(urls)):
                for j in range(i + 1, len(urls)):
                    similarity = similarity_matrix[i][j]
                    if similarity > 0.7:  # Threshold
                        duplicates.append({
                            "page1": urls[i],
                            "page2": urls[j],
                            "similarity": round(similarity, 3),
                            "method": "cosine"
                        })
        except Exception as e:
            print(f"Cosine similarity error: {e}")
        
        return duplicates
    
    def _detect_with_jaccard(self) -> List[Dict[str, Any]]:
        """Detect duplicates using Jaccard Similarity"""
        duplicates = []
        
        try:
            # Create word sets for each page
            page_sets = []
            for page in self.pages:
                text = self._get_page_text(page)
                if text:
                    words = set(text.lower().split())
                    if len(words) > 10:  # Minimum words
                        page_sets.append({
                            "words": words,
                            "url": page.get("url")
                        })
            
            # Compare all pairs
            for i in range(len(page_sets)):
                for j in range(i + 1, len(page_sets)):
                    set1 = page_sets[i]["words"]
                    set2 = page_sets[j]["words"]
                    
                    intersection = len(set1 & set2)
                    union = len(set1 | set2)
                    
                    if union > 0:
                        jaccard = intersection / union
                        if jaccard > 0.7:  # Threshold
                            duplicates.append({
                                "page1": page_sets[i]["url"],
                                "page2": page_sets[j]["url"],
                                "similarity": round(jaccard, 3),
                                "method": "jaccard"
                            })
        except Exception as e:
            print(f"Jaccard similarity error: {e}")
        
        return duplicates
    
    def _get_page_text(self, page: Dict[str, Any]) -> str:
        """Extract text content from page"""
        text_parts = []
        
        if page.get("title"):
            text_parts.append(page.get("title"))
        if page.get("h1"):
            text_parts.extend(page.get("h1", []))
        if page.get("h2"):
            text_parts.extend(page.get("h2", []))
        if page.get("content"):
            # Use first 2000 chars to avoid memory issues
            text_parts.append(page.get("content", "")[:2000])
        
        return " ".join(text_parts)

