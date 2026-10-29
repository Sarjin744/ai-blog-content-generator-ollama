"""
Export Utility Module
Course: 24CS2506 – Building Applications using GPT-4
Experiment 2: AI-Powered Blog Content Generator using Ollama
"""

import json
from typing import Dict, Any


class BlogExporter:
    """Exports generated blog posts into various formats: Markdown, HTML, and JSON."""

    @staticmethod
    def to_markdown(blog_text: str, metadata: Dict[str, Any]) -> str:
        """Exports blog with YAML frontmatter."""
        frontmatter = [
            "---",
            f"title: \"{metadata.get('topic', 'AI Generated Blog')}\"",
            f"model: \"{metadata.get('model', 'llama3.2')}\"",
            f"word_count: {metadata.get('word_count', 0)}",
            f"audience: \"{metadata.get('audience', 'General')}\"",
            f"tone: \"{metadata.get('tone', 'Friendly')}\"",
            f"style: \"{metadata.get('style', 'Professional')}\"",
            f"generated_by: \"Ollama Llama 3.2 Generator\"",
            "---\n\n"
        ]
        return "\n".join(frontmatter) + blog_text

    @staticmethod
    def to_html(blog_text: str, metadata: Dict[str, Any]) -> str:
        """Converts markdown blog into a standalone, styled HTML document."""
        # Simple markdown to HTML converter
        html_lines = []
        in_list = False

        for line in blog_text.split("\n"):
            line = line.strip()
            if not line:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                continue

            if line.startswith("# "):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h1>{line[2:].strip()}</h1>")
            elif line.startswith("## "):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h2>{line[3:].strip()}</h2>")
            elif line.startswith("### "):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h3>{line[4:].strip()}</h3>")
            elif line.startswith("- ") or line.startswith("• ") or line.startswith("* "):
                if not in_list:
                    html_lines.append("<ul>")
                    in_list = True
                content = line[2:].strip()
                html_lines.append(f"  <li>{content}</li>")
            else:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<p>{line}</p>")

        if in_list:
            html_lines.append("</ul>")

        body_content = "\n".join(html_lines)
        topic = metadata.get("topic", "AI Generated Blog")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.7;
            color: #24292e;
            max-width: 820px;
            margin: 40px auto;
            padding: 0 24px;
            background-color: #fdfdfd;
        }}
        h1 {{ color: #1a365d; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 0; }}
        h2 {{ color: #2b6cb0; margin-top: 32px; border-bottom: 1px solid #edf2f7; padding-bottom: 6px; }}
        h3 {{ color: #4a5568; margin-top: 24px; }}
        p {{ margin-bottom: 18px; font-size: 1.05rem; }}
        ul {{ margin-bottom: 20px; padding-left: 28px; }}
        li {{ margin-bottom: 8px; }}
        .badge-box {{
            background: #ebf8ff;
            border-left: 4px solid #3182ce;
            padding: 12px 18px;
            margin-bottom: 24px;
            border-radius: 4px;
            font-size: 0.9rem;
            color: #2b6cb0;
        }}
        footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
            font-size: 0.85rem;
            color: #718096;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="badge-box">
        <strong>Course:</strong> 24CS2506 – Building Applications using GPT-4 | <strong>Model:</strong> {metadata.get('model', 'llama3.2')} | <strong>Audience:</strong> {metadata.get('audience', 'Engineering Students')}
    </div>
    {body_content}
    <footer>Generated via AI-Powered Blog Content Generator using Ollama &amp; Llama 3.2</footer>
</body>
</html>
"""

    @staticmethod
    def to_json(blog_text: str, metadata: Dict[str, Any], analytics: Dict[str, Any]) -> str:
        """Exports blog, generation settings, and analytical metrics as structured JSON."""
        data = {
            "metadata": metadata,
            "analytics": analytics,
            "content": blog_text
        }
        return json.dumps(data, indent=2)
