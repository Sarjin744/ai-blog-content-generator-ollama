"""
Prompt Engineering Module
Course: 24CS2506 – Building Applications using GPT-4
Experiment 2: AI-Powered Blog Content Generator using Ollama
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class PromptComponents:
    """The 5 Core Components of a Good Prompt as defined in Lab Manual 2."""
    topic: str
    writing_style: str = "Professional"
    tone: str = "Friendly"
    word_count: int = 500
    audience: str = "Engineering Students"
    language_simplicity: str = "Simple English"
    include_sections: List[str] = field(default_factory=lambda: ["Introduction", "Main Content", "Conclusion"])
    seo_keywords: List[str] = field(default_factory=list)
    call_to_action: Optional[str] = None


class PromptBuilder:
    """
    Constructs highly structured, optimized prompts for Llama 3.2 blog generation.
    Supports naïve vs engineered prompt comparisons and prompt scoring.
    """

    DEFAULT_TOPICS = [
        "Artificial Intelligence",
        "Climate Change",
        "Cyber Security",
        "Electric Vehicles",
        "Healthy Living",
        "Digital Marketing"
    ]

    STYLES = [
        "Professional",
        "Conversational",
        "Technical & Analytical",
        "Educational & Tutorial",
        "Inspirational & Thought Leadership",
        "Engaging & Storytelling"
    ]

    TONES = [
        "Friendly",
        "Informative & Clear",
        "Formal & Authoritative",
        "Enthusiastic & Inspiring",
        "Curious & Thought-Provoking",
        "Empathetic & Relatable"
    ]

    AUDIENCES = [
        "Engineering Students",
        "Tech Enthusiasts & Developers",
        "Beginners & General Public",
        "Industry Professionals & Leaders",
        "College Academics & Researchers"
    ]

    WORD_COUNTS = [300, 500, 800, 1000]

    @staticmethod
    def build_naive_prompt(topic: str) -> str:
        """Returns a basic, un-engineered prompt as shown in Section 2 of manual."""
        return f"Write a blog about {topic.strip()}."

    @classmethod
    def build_engineered_prompt(cls, c: PromptComponents) -> str:
        """
        Builds a comprehensive prompt strictly integrating the 5 core components
        from Section 6 of the lab manual.
        """
        sections_str = ", ".join(c.include_sections) if c.include_sections else "Introduction, Main Content and Conclusion"
        keywords_str = f"\n- Target Focus Keywords: {', '.join(c.seo_keywords)}" if c.seo_keywords else ""
        cta_str = f"\n- Concluding Call-to-Action: {c.call_to_action}" if c.call_to_action else ""

        prompt = (
            f"Write a {c.word_count}-word {c.writing_style.lower()} blog on {c.topic} for {c.audience}. "
            f"Maintain a {c.tone.lower()} tone and use {c.language_simplicity.lower()}.\n\n"
            f"Formatting and Structure Instructions:\n"
            f"1. Generate a catchy, click-worthy blog title starting with '# '.\n"
            f"2. Include structured sections: {sections_str}.\n"
            f"3. Use markdown headers ('## ', '### ') for clean reading hierarchy.\n"
            f"4. Incorporate real-world examples, bullet points for readability, and clear takeaways.\n"
            f"5. Maintain approximately {c.word_count} words total.{keywords_str}{cta_str}"
        )
        return prompt

    @staticmethod
    def build_system_prompt(writing_style: str = "Professional", tone: str = "Friendly") -> str:
        """Constructs system instruction for Llama 3.2."""
        return (
            f"You are an expert content writer and AI educator. "
            f"Your writing style is {writing_style.lower()} and your tone is {tone.lower()}. "
            f"You write accurate, engaging, highly structured markdown blog posts that directly address "
            f"the requested target audience without fluff."
        )

    @classmethod
    def evaluate_prompt_quality(cls, prompt_text: str, components: Optional[PromptComponents] = None) -> Dict[str, Any]:
        """
        Evaluates a prompt against the 5 key criteria in the manual:
        Topic, Writing Style, Tone, Word Count, Target Audience.
        """
        score = 0
        checks = {}

        # 1. Topic
        has_topic = len(prompt_text.strip()) > 10
        score += 20 if has_topic else 0
        checks["Has Clear Topic"] = has_topic

        # 2. Writing Style
        has_style = any(s.lower() in prompt_text.lower() for s in ["professional", "technical", "conversational", "tutorial", "style"])
        score += 20 if has_style else 0
        checks["Specifies Style"] = has_style

        # 3. Tone
        has_tone = any(t.lower() in prompt_text.lower() for t in ["friendly", "informative", "formal", "tone", "enthusiastic"])
        score += 20 if has_tone else 0
        checks["Specifies Tone"] = has_tone

        # 4. Word Count
        has_word_count = any(wc in prompt_text.lower() for wc in ["word", "300", "500", "800", "1000", "length"])
        score += 20 if has_word_count else 0
        checks["Specifies Word Count"] = has_word_count

        # 5. Target Audience
        has_audience = any(a.lower() in prompt_text.lower() for a in ["student", "engineer", "audience", "beginner", "public", "professional"])
        score += 20 if has_audience else 0
        checks["Specifies Audience"] = has_audience

        return {
            "score": score,
            "max_score": 100,
            "grade": "Excellent (Engineered)" if score >= 80 else ("Moderate" if score >= 40 else "Naïve / Basic"),
            "checklist": checks
        }
