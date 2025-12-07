from typing import Dict, List, Any
from collections import Counter
import re
from rake_nltk import Rake
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class KeywordAnalyzer:
    def __init__(self, crawl_results: Dict[str, Any]):
        self.crawl_results = crawl_results
        self.pages = crawl_results.get("pages", [])
        
    def analyze(self) -> Dict[str, Any]:
        """Perform comprehensive keyword analysis"""
        if not self.pages:
            return {
                "keywords": {
                    "rake": [],
                    "ngrams": {"unigrams": [], "bigrams": [], "trigrams": []},
                    "tfidf": []
                },
                "keyword_clusters": [],
                "total_keywords": 0
            }
        
        # Combine all content
        all_text = self._extract_all_text()
        
        if not all_text or len(all_text.strip()) < 10:
            return {
                "keywords": {
                    "rake": [],
                    "ngrams": {"unigrams": [], "bigrams": [], "trigrams": []},
                    "tfidf": []
                },
                "keyword_clusters": [],
                "total_keywords": 0
            }
        
        # RAKE keywords
        rake_keywords = self._extract_rake_keywords(all_text)
        
        # N-gram analysis
        ngrams = self._extract_ngrams(all_text)
        
        # TF-IDF analysis
        tfidf_keywords = self._extract_tfidf_keywords()
        
        # Keyword clusters
        clusters = self._cluster_keywords(rake_keywords, tfidf_keywords)
        
        return {
            "keywords": {
                "rake": rake_keywords[:50],  # Top 50
                "ngrams": ngrams,
                "tfidf": tfidf_keywords[:50]  # Top 50
            },
            "keyword_clusters": clusters,
            "total_keywords": len(rake_keywords)
        }
    
    def _extract_all_text(self) -> str:
        """Extract all text content from pages"""
        texts = []
        for page in self.pages:
            # Combine title, headings, and content
            text_parts = []
            if page.get("title"):
                text_parts.append(page.get("title"))
            if page.get("h1"):
                text_parts.extend(page.get("h1", []))
            if page.get("h2"):
                text_parts.extend(page.get("h2", []))
            if page.get("content"):
                text_parts.append(page.get("content", "")[:2000])  # Limit content
            
            texts.append(" ".join(text_parts))
        
        return " ".join(texts)
    
    def _extract_rake_keywords(self, text: str) -> List[Dict[str, Any]]:
        """Extract keywords using RAKE"""
        try:
            r = Rake()
            r.extract_keywords_from_text(text)
            phrases = r.get_ranked_phrases_with_scores()
            
            keywords = []
            for score, phrase in phrases[:100]:  # Top 100
                keywords.append({
                    "phrase": phrase,
                    "score": round(score, 2),
                    "length": len(phrase.split())
                })
            
            return keywords
        except Exception as e:
            print(f"RAKE extraction error: {e}")
            return []
    
    def _extract_ngrams(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """Extract N-grams (1-gram, 2-gram, 3-gram)"""
        # Clean text
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        ngrams_result = {
            "unigrams": [],
            "bigrams": [],
            "trigrams": []
        }
        
        # Unigrams (single words)
        unigram_counter = Counter(words)
        for word, count in unigram_counter.most_common(50):
            if len(word) > 3:  # Filter short words
                ngrams_result["unigrams"].append({
                    "term": word,
                    "frequency": count
                })
        
        # Bigrams
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        bigram_counter = Counter(bigrams)
        for bigram, count in bigram_counter.most_common(30):
            ngrams_result["bigrams"].append({
                "term": bigram,
                "frequency": count
            })
        
        # Trigrams
        trigrams = [f"{words[i]} {words[i+1]} {words[i+2]}" for i in range(len(words)-2)]
        trigram_counter = Counter(trigrams)
        for trigram, count in trigram_counter.most_common(20):
            ngrams_result["trigrams"].append({
                "term": trigram,
                "frequency": count
            })
        
        return ngrams_result
    
    def _extract_tfidf_keywords(self) -> List[Dict[str, Any]]:
        """Extract keywords using TF-IDF"""
        try:
            # Prepare documents (one per page)
            documents = []
            for page in self.pages:
                doc_parts = []
                if page.get("title"):
                    doc_parts.append(page.get("title"))
                if page.get("h1"):
                    doc_parts.extend(page.get("h1", []))
                if page.get("content"):
                    doc_parts.append(page.get("content", "")[:1000])
                documents.append(" ".join(doc_parts))
            
            if len(documents) < 2:
                return []
            
            # TF-IDF vectorization
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english', ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform(documents)
            
            # Get feature names
            feature_names = vectorizer.get_feature_names_out()
            
            # Calculate average TF-IDF scores across all documents
            mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # Get top keywords
            top_indices = np.argsort(mean_scores)[::-1][:50]
            
            keywords = []
            for idx in top_indices:
                keywords.append({
                    "term": feature_names[idx],
                    "tfidf_score": round(float(mean_scores[idx]), 4)
                })
            
            return keywords
        except Exception as e:
            print(f"TF-IDF extraction error: {e}")
            return []
    
    def _cluster_keywords(self, rake_keywords: List[Dict], tfidf_keywords: List[Dict]) -> List[Dict[str, Any]]:
        """Group related keywords into clusters"""
        # Simple clustering based on word overlap
        clusters = []
        processed = set()
        
        # Combine keywords from both methods
        all_keywords = []
        for kw in rake_keywords[:30]:
            all_keywords.append(kw.get("phrase", "").lower())
        for kw in tfidf_keywords[:30]:
            all_keywords.append(kw.get("term", "").lower())
        
        for keyword in all_keywords:
            if keyword in processed or len(keyword.split()) < 2:
                continue
            
            # Find similar keywords
            cluster = [keyword]
            processed.add(keyword)
            
            words_in_keyword = set(keyword.split())
            
            for other_keyword in all_keywords:
                if other_keyword in processed:
                    continue
                
                words_in_other = set(other_keyword.split())
                overlap = len(words_in_keyword & words_in_other)
                
                if overlap > 0:
                    cluster.append(other_keyword)
                    processed.add(other_keyword)
            
            if len(cluster) > 1:
                clusters.append({
                    "theme": keyword,
                    "keywords": cluster[:10],  # Limit cluster size
                    "size": len(cluster)
                })
        
        return clusters[:10]  # Top 10 clusters

