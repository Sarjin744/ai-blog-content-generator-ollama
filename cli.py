"""
AI-Powered Blog Content Generator CLI
Course: 24CS2506 – Building Applications using GPT-4
Experiment 2: AI-Powered Blog Content Generator using Ollama
"""

import os
import sys

# Ensure UTF-8 output encoding across Windows consoles
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, IntPrompt

from engine import (
    BlogGenerator,
    PromptComponents,
    PromptBuilder,
    ContentAnalyzer,
    BlogExporter
)

console = Console(legacy_windows=False)


def print_banner(gen: BlogGenerator):
    title = Text("✍️  AI-POWERED BLOG CONTENT GENERATOR", style="bold cyan")
    subtitle = Text(
        "Course: 24CS2506 – Building Applications using GPT-4 | Experiment 2\n"
        "Department of Computer Science & Engineering | Karunya University",
        style="dim"
    )

    ollama_status = (
        f"[bold green]● Ollama Connected[/bold green] (Model: {gen.model})"
        if gen.ollama.is_connected
        else "[bold yellow]○ Ollama Offline[/bold yellow] (Using Local Semantic Synthesizer Fallback)"
    )

    banner_content = Text.from_markup(
        f"{title}\n{subtitle}\n\n"
        f"[bold white]Engine Status:[/bold white] {ollama_status}\n"
        f"[dim]Core Components: Topic, Writing Style, Tone, Word Count, Audience[/dim]"
    )
    console.print(Panel(banner_content, border_style="cyan"))


def display_analytics_table(analytics: dict, meta: dict):
    table = Table(title="📊 Blog Analytics & Linguistic Metrics", border_style="bright_blue")
    table.add_column("Metric", style="bold cyan")
    table.add_column("Value", style="bold white")
    table.add_column("Interpretation / Detail", style="dim")

    table.add_row("Total Word Count", str(analytics["word_count"]), f"Target: {meta['target_word_count']} words")
    table.add_row("Estimated Reading Time", f"{analytics['reading_time_min']} min", "Based on 200 WPM reading speed")
    table.add_row("Flesch Reading Ease", str(analytics["flesch_reading_ease"]), analytics["readability_label"])
    table.add_row("Flesch-Kincaid Grade", f"Grade {analytics['grade_level']}", "US School/College Grade Level")
    table.add_row("Sentences Count", str(analytics["sentence_count"]), "Structural sentence units")
    table.add_row("Generation Time", f"{meta['generation_time_sec']}s", f"Source: {meta['source']}")

    console.print(table)


def run_generator_flow(gen: BlogGenerator):
    console.print("\n[bold yellow]Select a Topic from Lab Manual or enter custom:[/bold yellow]")
    for idx, t in enumerate(PromptBuilder.DEFAULT_TOPICS, 1):
        console.print(f"  [cyan]{idx}.[/cyan] {t}")
    console.print(f"  [cyan]7.[/cyan] Custom Topic")

    topic_choice = Prompt.ask("Choose option", choices=["1", "2", "3", "4", "5", "6", "7"], default="1")
    if topic_choice == "7":
        topic = Prompt.ask("[bold green]Enter custom topic[/bold green]")
    else:
        topic = PromptBuilder.DEFAULT_TOPICS[int(topic_choice) - 1]

    console.print("\n[bold yellow]Select Writing Style:[/bold yellow]")
    for idx, s in enumerate(PromptBuilder.STYLES, 1):
        console.print(f"  [cyan]{idx}.[/cyan] {s}")
    style_choice = Prompt.ask("Choose style", choices=[str(i) for i in range(1, len(PromptBuilder.STYLES) + 1)], default="1")
    writing_style = PromptBuilder.STYLES[int(style_choice) - 1]

    console.print("\n[bold yellow]Select Tone:[/bold yellow]")
    for idx, t in enumerate(PromptBuilder.TONES, 1):
        console.print(f"  [cyan]{idx}.[/cyan] {t}")
    tone_choice = Prompt.ask("Choose tone", choices=[str(i) for i in range(1, len(PromptBuilder.TONES) + 1)], default="1")
    tone = PromptBuilder.TONES[int(tone_choice) - 1]

    console.print("\n[bold yellow]Select Target Audience:[/bold yellow]")
    for idx, a in enumerate(PromptBuilder.AUDIENCES, 1):
        console.print(f"  [cyan]{idx}.[/cyan] {a}")
    aud_choice = Prompt.ask("Choose audience", choices=[str(i) for i in range(1, len(PromptBuilder.AUDIENCES) + 1)], default="1")
    audience = PromptBuilder.AUDIENCES[int(aud_choice) - 1]

    word_count = IntPrompt.ask("\n[bold yellow]Target Word Count (e.g. 300, 500, 800)[/bold yellow]", default=500)

    components = PromptComponents(
        topic=topic,
        writing_style=writing_style,
        tone=tone,
        word_count=word_count,
        audience=audience
    )

    console.print("\n[bold cyan]─── Constructed Engineered Prompt ───[/bold cyan]")
    prompt_text = PromptBuilder.build_engineered_prompt(components)
    console.print(Panel(prompt_text, border_style="dim"))

    with console.status("[bold green]Generating blog post with Llama 3.2...[/bold green]"):
        res = gen.generate_blog(components)

    console.print("\n" + "=" * 70)
    console.print(Panel(res["blog_text"], title=f"[bold green]Generated Article: {topic}[/bold green]", border_style="green"))
    console.print("=" * 70 + "\n")

    display_analytics_table(res["analytics"], res["metadata"])

    save_opt = Prompt.ask("\nSave article to disk? (markdown / html / none)", choices=["markdown", "html", "none"], default="markdown")
    if save_opt == "markdown":
        filename = f"blog_{topic.lower().replace(' ', '_')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(BlogExporter.to_markdown(res["blog_text"], res["metadata"]))
        console.print(f"[bold green]✓ Saved to {filename}[/bold green]")
    elif save_opt == "html":
        filename = f"blog_{topic.lower().replace(' ', '_')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(BlogExporter.to_html(res["blog_text"], res["metadata"]))
        console.print(f"[bold green]✓ Saved to {filename}[/bold green]")


def main():
    gen = BlogGenerator()
    print_banner(gen)

    while True:
        console.print("\n[bold white]Main Menu:[/bold white]")
        console.print("  [cyan]1.[/cyan] 📝 Generate Blog Post (Configure 5 Components)")
        console.print("  [cyan]2.[/cyan] ⚡ Quick Run Example from Manual (AI for Engineering Students, 500 words)")
        console.print("  [cyan]3.[/cyan] ⚖️ Compare Naïve Prompt vs Engineered Prompt")
        console.print("  [cyan]4.[/cyan] 🚪 Exit")

        choice = Prompt.ask("\nSelect option", choices=["1", "2", "3", "4"], default="1")

        if choice == "1":
            run_generator_flow(gen)
        elif choice == "2":
            comp = PromptComponents(
                topic="Artificial Intelligence",
                writing_style="Professional",
                tone="Friendly",
                word_count=500,
                audience="Engineering Students"
            )
            with console.status("[bold green]Generating manual sample blog...[/bold green]"):
                res = gen.generate_blog(comp)
            console.print(Panel(res["blog_text"], title="[bold green]Artificial Intelligence Blog[/bold green]"))
            display_analytics_table(res["analytics"], res["metadata"])
        elif choice == "3":
            topic = "Artificial Intelligence"
            naive = PromptBuilder.build_naive_prompt(topic)
            comp = PromptComponents(topic=topic, writing_style="Professional", tone="Friendly", word_count=500, audience="Engineering Students")
            eng = PromptBuilder.build_engineered_prompt(comp)

            t = Table(title="Prompt Engineering Comparison", border_style="magenta")
            t.add_column("Property", style="bold")
            t.add_column("Naïve Prompt", style="red")
            t.add_column("Engineered Prompt (5 Components)", style="green")

            t.add_row("Prompt Text", naive, eng)
            t.add_row("Topic Specified", "Yes (Basic)", "Yes (Specific Context)")
            t.add_row("Target Audience", "None (Generic)", "Engineering Students")
            t.add_row("Writing Style & Tone", "None", "Professional & Friendly")
            t.add_row("Length Constraint", "None", "500 words")
            t.add_row("Structural Directives", "None", "Intro, Body, Conclusion, Markdown Headers")
            console.print(t)
        elif choice == "4":
            console.print("[bold cyan]Exiting AI Blog Generator. Goodbye![/bold cyan]")
            break


if __name__ == "__main__":
    main()
