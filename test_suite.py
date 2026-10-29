"""
Comprehensive Verification and Test Suite for Experiment 2
Course: 24CS2506 – Building Applications using GPT-4
Experiment 2: AI-Powered Blog Content Generator using Ollama
"""

import sys
import os
import json

from engine import (
    OllamaClient,
    PromptComponents,
    PromptBuilder,
    ContentAnalyzer,
    BlogGenerator,
    BlogExporter
)


def run_tests():
    passed = 0
    total = 0

    def assert_test(condition, name, details=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"  [PASS] Test {total}: {name}")
        else:
            print(f"  [FAIL] Test {total}: {name} - Details: {details}")

    print("=" * 60)
    print("RUNNING EXPERIMENT 2 AUTOMATED TEST SUITE")
    print("=" * 60)

    # 1. Ollama Client Tests
    print("\n--- 1. Ollama Client Tests ---")
    client = OllamaClient()
    assert_test(isinstance(client.is_connected, bool), "Ollama connection check returns boolean")
    models = client.list_models()
    assert_test(isinstance(models, list), "Ollama list_models returns a list")
    best_m = client.get_best_available_model()
    assert_test(isinstance(best_m, str) and len(best_m) > 0, "Ollama get_best_available_model returns valid model name")

    # 2. Prompt Builder Tests
    print("\n--- 2. Prompt Engineering & 5 Components Tests ---")
    naive = PromptBuilder.build_naive_prompt("Cyber Security")
    assert_test(naive == "Write a blog about Cyber Security.", "Naive prompt generation matches expected structure")

    comp = PromptComponents(
        topic="Cyber Security",
        writing_style="Professional",
        tone="Friendly",
        word_count=500,
        audience="Engineering Students",
        language_simplicity="Simple English",
        include_sections=["Introduction", "Main Content", "Conclusion"],
        seo_keywords=["Zero Trust", "Firewall"],
        call_to_action="Stay vigilant and patch your systems."
    )
    eng_prompt = PromptBuilder.build_engineered_prompt(comp)
    assert_test("Cyber Security" in eng_prompt, "Engineered prompt contains Topic")
    assert_test("professional" in eng_prompt.lower(), "Engineered prompt contains Writing Style")
    assert_test("friendly" in eng_prompt.lower(), "Engineered prompt contains Tone")
    assert_test("500" in eng_prompt, "Engineered prompt contains Word Count")
    assert_test("Engineering Students" in eng_prompt, "Engineered prompt contains Audience")
    assert_test("Zero Trust" in eng_prompt, "Engineered prompt includes SEO Focus Keywords")
    assert_test("Stay vigilant" in eng_prompt, "Engineered prompt includes Call to Action")

    eval_eng = PromptBuilder.evaluate_prompt_quality(eng_prompt, comp)
    assert_test(eval_eng["score"] == 100, f"Engineered prompt quality score is 100/100 (got {eval_eng['score']})")
    assert_test(eval_eng["grade"] == "Excellent (Engineered)", "Engineered prompt grade is Excellent")

    eval_naive = PromptBuilder.evaluate_prompt_quality(naive)
    assert_test(eval_naive["score"] < 50, f"Naive prompt quality score correctly flagged as low (got {eval_naive['score']})")

    # 3. Content Analytics Tests
    print("\n--- 3. Content Analytics & Linguistic Metrics Tests ---")
    sample_text = (
        "# Artificial Intelligence in Modern Engineering\n\n"
        "Artificial intelligence is transforming industries worldwide. "
        "Engineers build smart software that analyzes data with remarkable precision.\n\n"
        "## Practical Applications\n"
        "Here are three practical use cases for students:\n"
        "- Smart robotics and automated assembly.\n"
        "- Predictive maintenance in civil structures.\n"
        "- Fast computer code generation and debugging.\n\n"
        "## Conclusion\n"
        "Learning these foundational principles will prepare you for a bright technical career."
    )
    analytics = ContentAnalyzer.analyze(sample_text)
    assert_test(analytics["word_count"] > 30, f"Word count computed correctly (got {analytics['word_count']})")
    assert_test(analytics["sentence_count"] >= 4, f"Sentence count computed correctly (got {analytics['sentence_count']})")
    assert_test(analytics["syllable_count"] > 30, f"Syllable count computed correctly (got {analytics['syllable_count']})")
    assert_test(analytics["flesch_reading_ease"] >= 0, f"Flesch Reading Ease is within valid scale: {analytics['flesch_reading_ease']}")
    assert_test(analytics["reading_time_min"] > 0, f"Reading time estimated: {analytics['reading_time_min']} min")
    assert_test(len(analytics["headings"]) == 3, f"Extracted 3 headings accurately (got {len(analytics['headings'])})")
    assert_test(len(analytics["top_keywords"]) > 0, f"Top keywords extracted: {analytics['top_keywords'][:3]}")

    # 4. Blog Generator & Multitask Suite Tests
    print("\n--- 4. Blog Generator Pipeline Tests ---")
    gen = BlogGenerator()
    res = gen.generate_blog(comp)
    assert_test("blog_text" in res and len(res["blog_text"]) > 100, "Blog generated with content")
    assert_test("analytics" in res and res["analytics"]["word_count"] > 50, "Blog includes valid analytics")
    assert_test("metadata" in res and res["metadata"]["topic"] == "Cyber Security", "Metadata correctly attached")
    assert_test("prompt_evaluation" in res and res["prompt_evaluation"]["score"] >= 80, "Prompt quality evaluated")

    # Multitask features from Section 4 of manual
    print("\n--- 5. Llama 3.2 Multitask Suite Tests (Summarize, Rewrite, Translate) ---")
    summary = gen.summarize_content(sample_text, word_count=50)
    assert_test(len(summary) > 20, "Summarize content returns concise summary")

    rewritten = gen.rewrite_content(sample_text, new_tone="Formal", new_style="Academic")
    assert_test(len(rewritten) > 20, "Rewrite content returns transformed article")

    translated = gen.translate_content(sample_text, target_language="Spanish")
    assert_test(len(translated) > 20, "Translate content returns translation structure")

    # 6. Blog Exporter Tests
    print("\n--- 6. Blog Exporter Tests ---")
    md_output = BlogExporter.to_markdown(res["blog_text"], res["metadata"])
    assert_test(md_output.startswith("---") and "title:" in md_output, "Export to Markdown includes valid YAML frontmatter")

    html_output = BlogExporter.to_html(res["blog_text"], res["metadata"])
    assert_test("<!DOCTYPE html>" in html_output and "<h1>" in html_output, "Export to HTML generates full valid HTML webpage")

    json_output = BlogExporter.to_json(res["blog_text"], res["metadata"], res["analytics"])
    parsed_json = json.loads(json_output)
    assert_test("metadata" in parsed_json and "analytics" in parsed_json and "content" in parsed_json, "Export to JSON produces valid JSON structure")

    print("\n" + "=" * 60)
    print(f"TEST RESULTS SUMMARY: {passed} / {total} TESTS PASSED ({(passed/total)*100:.1f}%)")
    print("=" * 60)

    if passed == total:
        print("ALL TESTS PASSED SUCCESSFULLY! The application is verified and operational.")
        return 0
    else:
        print("SOME TESTS FAILED! Review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
