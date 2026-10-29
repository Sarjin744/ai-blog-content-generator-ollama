"""
Content Analytics Module
Course: 24CS2506 – Building Applications using GPT-4
Experiment 2: AI-Powered Blog Content Generator using Ollama
"""

import re
from typing import Dict, Any, List
from collections import Counter


class ContentAnalyzer:
    """
    Computes readability metrics, reading time, heading hierarchy, and keyword density
    for AI-generated blog posts.
    """

    STOPWORDS = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
        "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can",
        "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
        "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having",
        "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how",
        "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its",
        "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on",
        "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't",
        "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's",
        "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd",
        "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very",
        "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when",
        "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't",
        "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
    }

    @staticmethod
    def _count_syllables(word: str) -> int:
        """Estimate syllable count in an English word accurately using vowel transition groups."""
        word = word.lower().strip(".:;?!,'\"-()")
        if not word or len(word) <= 3:
            return 1
        # Strip common silent endings
        if word.endswith("e") and not word.endswith("le") and not word.endswith("ee"):
            word = word[:-1]
        elif word.endswith("ed") and not word.endswith("ted") and not word.endswith("ded"):
            word = word[:-2]
        elif word.endswith("es") and not word.endswith("ses") and not word.endswith("zes") and not word.endswith("ches") and not word.endswith("shes"):
            word = word[:-1]

        vowels = "aeiouy"
        count = 0
        prev_is_vowel = False
        for ch in word:
            is_v = ch in vowels
            if is_v and not prev_is_vowel:
                count += 1
            prev_is_vowel = is_v
        return max(1, count)

    @classmethod
    def analyze(cls, text: str) -> Dict[str, Any]:
        """Performs comprehensive linguistic and readability analysis."""
        if not text or not text.strip():
            return {
                "word_count": 0,
                "char_count": 0,
                "sentence_count": 0,
                "syllable_count": 0,
                "reading_time_min": 0.0,
                "flesch_reading_ease": 0.0,
                "readability_label": "N/A",
                "grade_level": 0.0,
                "top_keywords": [],
                "headings": []
            }

        # Clean markdown formatting for statistical accuracy
        clean_text = re.sub(r'[#*`_~\[\]\(\)>]', ' ', text)
        clean_sentences_text = re.sub(r'[\r\n]+', '. ', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()

        words = re.findall(r'\b[a-zA-Z]{2,}\b', clean_text)
        total_words = len(words)
        total_chars = len(clean_text)

        # Sentence counting (treating markdown breaks and periods as sentence boundaries)
        sentences = [s.strip() for s in re.split(r'[.!?]+', clean_sentences_text) if len(s.strip()) > 3]
        total_sentences = max(1, len(sentences))

        # Syllables
        total_syllables = sum(cls._count_syllables(w) for w in words)

        # Reading Time (Average reading speed: 200 words per minute)
        reading_time_min = round(total_words / 200.0, 1)

        # Flesch Reading Ease Formula
        # 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
        if total_words > 0:
            asl = total_words / total_sentences
            asw = total_syllables / total_words
            fre = 206.835 - (1.015 * asl) - (84.6 * asw)
            fre = max(0.0, min(100.0, round(fre, 1)))

            # Flesch-Kincaid Grade Level
            fkgl = 0.39 * asl + 11.8 * asw - 15.59
            fkgl = max(0.0, round(fkgl, 1))
        else:
            fre = 0.0
            fkgl = 0.0

        if fre >= 90:
            readability_label = "Very Easy (5th Grade)"
        elif fre >= 80:
            readability_label = "Easy (6th Grade)"
        elif fre >= 70:
            readability_label = "Fairly Easy (7th Grade)"
        elif fre >= 60:
            readability_label = "Standard / Conversational (8th-9th Grade)"
        elif fre >= 50:
            readability_label = "Fairly Difficult (10th-12th Grade)"
        elif fre >= 30:
            readability_label = "Difficult (College Student)"
        else:
            readability_label = "Very Difficult (Academic / Graduate)"

        # Keyword frequency analysis
        filtered_words = [w.lower() for w in words if w.lower() not in cls.STOPWORDS and len(w) > 3]
        top_keywords = Counter(filtered_words).most_common(8)

        # Headings extraction
        headings = []
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("#"):
                level = len(line) - len(line.lstrip("#"))
                title = line.lstrip("#").strip()
                headings.append({"level": level, "title": title})

        return {
            "word_count": total_words,
            "char_count": total_chars,
            "sentence_count": total_sentences,
            "syllable_count": total_syllables,
            "reading_time_min": reading_time_min,
            "flesch_reading_ease": fre,
            "readability_label": readability_label,
            "grade_level": fkgl,
            "top_keywords": top_keywords,
            "headings": headings
        }
