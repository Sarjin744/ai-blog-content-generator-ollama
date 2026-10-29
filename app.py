"""
AI-Powered Blog Content Generator using Ollama
Course: 24CS2506 – Building Applications using GPT-4
Experiment 2: AI-Powered Blog Content Generator using Ollama
"""

import os
import streamlit as st
import pandas as pd
import altair as alt

from engine import (
    BlogGenerator,
    PromptComponents,
    PromptBuilder,
    ContentAnalyzer,
    BlogExporter,
    OllamaClient
)

st.set_page_config(
    page_title="AI Blog Content Generator | Lab Exp 2",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #0284c7;
        margin-bottom: 2px;
    }
    .sub-header {
        font-size: 0.98rem;
        color: #64748b;
        margin-bottom: 20px;
    }
    .component-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .badge-topic { background-color: #e0f2fe; color: #0369a1; }
    .badge-style { background-color: #fef3c7; color: #b45309; }
    .badge-tone { background-color: #f3e8ff; color: #7e22ce; }
    .badge-words { background-color: #dcfce7; color: #15803d; }
    .badge-aud { background-color: #ffe4e6; color: #be123c; }
    .prompt-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px;
        font-family: monospace;
        font-size: 0.88rem;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "generator" not in st.session_state:
    st.session_state.generator = BlogGenerator(model="llama3.2")

if "generated_blog" not in st.session_state:
    st.session_state.generated_blog = None

if "history" not in st.session_state:
    st.session_state.history = []

gen: BlogGenerator = st.session_state.generator

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/edit-property.png", width=100)
    st.markdown("### 🏛️ Karunya University")
    st.markdown("**24CS2506 – Building Applications using GPT-4**")
    st.markdown("**Experiment 2: AI-Powered Blog Content Generator**")
    st.markdown("---")

    # Connection Status
    st.subheader("⚙️ Ollama Status")
    is_connected = gen.ollama.check_connection()
    if is_connected:
        st.success("● Ollama Service Active (localhost:11434)")
        models = gen.ollama.list_models()
        if models:
            selected_model = st.selectbox("Available Models", models, index=0)
            gen.set_model(selected_model)
        else:
            st.info("No models currently loaded in Ollama.\nPull Llama 3.2: `ollama run llama3.2`")
    else:
        st.warning("○ Ollama Daemon Offline\n(Running in Semantic Fallback Mode)")
        st.caption("To run locally with Llama 3.2:\n1. Install Ollama\n2. Run: `ollama run llama3.2`")

    st.markdown("---")
    st.subheader("💡 Lab Manual Topic Presets")
    preset_topic = st.selectbox(
        "Choose standard example topic:",
        PromptBuilder.DEFAULT_TOPICS,
        index=0
    )

    st.markdown("---")
    st.caption("Meta Llama 3.2 • Local Inference • Zero API Cost • Offline Ready")

# Main Header
st.markdown('<div class="main-header">✍️ AI-Powered Blog Content Generator using Ollama</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Blog Creation & Prompt Engineering Suite Powered by Meta Llama 3.2</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Blog Generator (5 Components)",
    "⚖️ Naïve vs Engineered Prompt Comparator",
    "🧰 Llama 3.2 Multitask Suite",
    "📖 Lab Manual & Theoretical Concepts"
])

# ==========================================
# TAB 1: Blog Generator (5 Core Components)
# ==========================================
with tab1:
    st.markdown("#### 🎯 Configure Prompt Components")
    st.caption("A high quality prompt integrates Topic, Writing Style, Tone, Word Count, and Audience.")

    col1, col2 = st.columns(2)
    with col1:
        topic_input = st.text_input("1. Blog Topic:", value=preset_topic, help="Specific subject to write about")
        writing_style = st.selectbox("2. Writing Style:", PromptBuilder.STYLES, index=0)
        tone = st.selectbox("3. Tone:", PromptBuilder.TONES, index=0)

    with col2:
        word_count = st.select_slider(
            "4. Word Count Target:",
            options=[300, 500, 800, 1000],
            value=500
        )
        audience = st.selectbox("5. Target Audience:", PromptBuilder.AUDIENCES, index=0)
        language_simplicity = st.selectbox("Language Level:", ["Simple English", "Technical English", "Standard Academic"], index=0)

    with st.expander("🛠️ Advanced Prompt Options (SEO Keywords, Structure & CTA)"):
        col_adv1, col_adv2 = st.columns(2)
        with col_adv1:
            sections = st.multiselect(
                "Article Structure Sections:",
                ["Introduction", "Key Principles", "Practical Applications", "Case Studies", "Conclusion & Next Steps"],
                default=["Introduction", "Practical Applications", "Conclusion & Next Steps"]
            )
        with col_adv2:
            keywords_input = st.text_input("Focus SEO Keywords (comma separated):", value=f"{topic_input}, Innovation, Technology")
            call_to_action = st.text_input("Call to Action (CTA):", value="Start exploring this technology and build your own project today!")

    seo_keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    components = PromptComponents(
        topic=topic_input,
        writing_style=writing_style,
        tone=tone,
        word_count=word_count,
        audience=audience,
        language_simplicity=language_simplicity,
        include_sections=sections,
        seo_keywords=seo_keywords,
        call_to_action=call_to_action
    )

    engineered_prompt_preview = PromptBuilder.build_engineered_prompt(components)

    # Prompt Preview & Inspection
    with st.expander("🔍 Inspect Constructed Engineered Prompt & Quality Score", expanded=False):
        eval_res = PromptBuilder.evaluate_prompt_quality(engineered_prompt_preview, components)
        c_score, c_grade = st.columns([1, 3])
        with c_score:
            st.metric("Prompt Quality Score", f"{eval_res['score']}/100", eval_res['grade'])
        with c_grade:
            st.markdown("**Checklist Validation:**")
            badges = " ".join([f"`{k}: {'✅' if v else '❌'}`" for k, v in eval_res['checklist'].items()])
            st.markdown(badges)
        st.markdown(f'<div class="prompt-box">{engineered_prompt_preview}</div>', unsafe_allow_html=True)

    # Generate Button
    if st.button("🚀 Generate Blog with Llama 3.2", type="primary", use_container_width=True):
        with st.spinner("🤖 Prompting Llama 3.2 via Ollama to generate professional blog..."):
            result = gen.generate_blog(components)
            st.session_state.generated_blog = result
            st.session_state.history.append(result)

    # Display Result
    if st.session_state.generated_blog:
        res = st.session_state.generated_blog
        analytics = res["analytics"]
        meta = res["metadata"]

        st.markdown("---")
        st.subheader("📄 Generated Blog Article")

        # Metric Badges
        st.markdown(f"""
        <span class="component-badge badge-topic">📌 Topic: {meta['topic']}</span>
        <span class="component-badge badge-style">🎨 Style: {meta['writing_style']}</span>
        <span class="component-badge badge-tone">🗣️ Tone: {meta['tone']}</span>
        <span class="component-badge badge-words">📏 Target: {meta['target_word_count']} words</span>
        <span class="component-badge badge-aud">👥 Audience: {meta['audience']}</span>
        """, unsafe_allow_html=True)

        # Output Text Container
        st.markdown(res["blog_text"])

        st.markdown("---")
        st.markdown("#### 📊 Content Analytics & Readability Metrics")
        mcol1, mcol2, mcol3, mcol4, mcol5 = st.columns(5)
        mcol1.metric("Actual Word Count", analytics["word_count"], f"{analytics['word_count'] - meta['target_word_count']} diff")
        mcol2.metric("Reading Time", f"{analytics['reading_time_min']} min", "200 WPM speed")
        mcol3.metric("Flesch Reading Ease", analytics["flesch_reading_ease"], analytics["readability_label"])
        mcol4.metric("Grade Level", f"Grade {analytics['grade_level']}")
        mcol5.metric("Latency / Time", f"{meta['generation_time_sec']}s", meta["source"])

        # Keyword Density Chart
        if analytics["top_keywords"]:
            st.markdown("##### 🔑 Top Extracted Keywords")
            kw_df = pd.DataFrame(analytics["top_keywords"], columns=["Keyword", "Frequency"])
            chart = alt.Chart(kw_df).mark_bar(color="#0284c7").encode(
                x=alt.X("Frequency:Q", title="Occurrence Count"),
                y=alt.Y("Keyword:N", sort="-x", title="Keyword"),
                tooltip=["Keyword", "Frequency"]
            ).properties(height=220)
            st.altair_chart(chart, use_container_width=True)

        # Export Actions
        st.markdown("#### 💾 Export & Save Blog")
        col_exp1, col_exp2, col_exp3 = st.columns(3)

        md_content = BlogExporter.to_markdown(res["blog_text"], meta)
        html_content = BlogExporter.to_html(res["blog_text"], meta)
        json_content = BlogExporter.to_json(res["blog_text"], meta, analytics)

        col_exp1.download_button(
            "📥 Download as Markdown (.md)",
            data=md_content,
            file_name=f"blog_{meta['topic'].lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )
        col_exp2.download_button(
            "🌐 Download as HTML Webpage (.html)",
            data=html_content,
            file_name=f"blog_{meta['topic'].lower().replace(' ', '_')}.html",
            mime="text/html",
            use_container_width=True
        )
        col_exp3.download_button(
            "📋 Download Metadata & Metrics (.json)",
            data=json_content,
            file_name=f"blog_{meta['topic'].lower().replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True
        )


# ==========================================
# TAB 2: Naïve vs Engineered Comparator
# ==========================================
with tab2:
    st.subheader("⚖️ Naïve Prompt vs Engineered Prompt Comparison")
    st.markdown("""
    As highlighted in Section 5 and 6 of the lab manual:
    > *"The better the prompt, the better the output."*
    
    A **Naïve prompt** gives generic, unfocused instructions. An **Engineered prompt** provides explicit constraints
    on Topic, Writing Style, Tone, Word Count, and Target Audience.
    """)

    sample_topic = st.selectbox(
        "Select Topic to Compare:",
        PromptBuilder.DEFAULT_TOPICS,
        key="comp_topic"
    )

    col_n, col_e = st.columns(2)

    with col_n:
        st.markdown("### 🔴 Naïve Prompt (Unstructured)")
        naive_text = PromptBuilder.build_naive_prompt(sample_topic)
        st.code(naive_text, language="text")
        eval_n = PromptBuilder.evaluate_prompt_quality(naive_text)
        st.metric("Quality Score", f"{eval_n['score']}/100", eval_n['grade'])
        st.markdown("""
        **Characteristics:**
        - ❌ No designated audience
        - ❌ No word count constraint
        - ❌ No tone or style guidance
        - ⚠️ Leads to generic, unpredictable responses
        """)

    with col_e:
        st.markdown("### 🟢 Engineered Prompt (5 Components)")
        eng_comp = PromptComponents(
            topic=sample_topic,
            writing_style="Professional",
            tone="Friendly",
            word_count=500,
            audience="Engineering Students"
        )
        eng_text = PromptBuilder.build_engineered_prompt(eng_comp)
        st.code(eng_text, language="text")
        eval_e = PromptBuilder.evaluate_prompt_quality(eng_text, eng_comp)
        st.metric("Quality Score", f"{eval_e['score']}/100", eval_e['grade'])
        st.markdown("""
        **Characteristics:**
        - ✅ Explicit Target: Engineering Students
        - ✅ Target Word Count: 500 words
        - ✅ Style: Professional | Tone: Friendly
        - ✅ Strict structure: Intro, Body, Conclusion
        """)

    st.markdown("---")
    st.info("💡 **Key Learning:** Adding specific audience, style, tone, and length constraints in the prompt enables Llama 3.2 to generate tailored, publication-ready content.")


# ==========================================
# TAB 3: Llama 3.2 Multitask Suite
# ==========================================
with tab3:
    st.subheader("🧰 Llama 3.2 Multitask Capabilities")
    st.caption("Demonstrating Meta Llama 3.2 capabilities listed in Section 4 of Lab Manual 2: Summarize text, Translate languages, Rewrite articles.")

    task_mode = st.radio(
        "Choose Llama 3.2 Task:",
        ["Summarize Text", "Rewrite with Different Tone/Style", "Translate Language"],
        horizontal=True
    )

    default_sample = (
        st.session_state.generated_blog["blog_text"]
        if st.session_state.generated_blog
        else (
            "Artificial Intelligence is transforming industries by enabling machines to perform tasks that normally "
            "require human intelligence. Machine learning algorithms discover hidden patterns in data, while deep neural networks "
            "power voice recognition and autonomous driving. For engineering students, mastering these principles unlocks "
            "boundless career opportunities in software development, robotics, and cloud computing."
        )
    )

    input_text = st.text_area("Input Text to Process:", value=default_sample, height=180)

    if task_mode == "Summarize Text":
        summary_wc = st.slider("Summary Word Limit:", 50, 200, 80)
        if st.button("📑 Run Summarizer"):
            with st.spinner("Summarizing with Llama 3.2..."):
                output = gen.summarize_content(input_text, word_count=summary_wc)
                st.markdown("#### Summary Output:")
                st.markdown(output)

    elif task_mode == "Rewrite with Different Tone/Style":
        c_rw1, c_rw2 = st.columns(2)
        with c_rw1:
            target_style = st.selectbox("Target Style:", ["Conversational", "Technical & Analytical", "Persuasive Marketing"])
        with c_rw2:
            target_tone = st.selectbox("Target Tone:", ["Enthusiastic & Inspiring", "Formal & Authoritative", "Humorous & Casual"])

        if st.button("✏️ Run Article Rewriter"):
            with st.spinner("Rewriting with Llama 3.2..."):
                output = gen.rewrite_content(input_text, new_tone=target_tone, new_style=target_style)
                st.markdown("#### Rewritten Content:")
                st.markdown(output)

    elif task_mode == "Translate Language":
        lang = st.selectbox("Select Target Language:", ["Spanish", "French", "German", "Hindi", "Tamil"])
        if st.button("🌐 Translate Content"):
            with st.spinner(f"Translating to {lang} with Llama 3.2..."):
                output = gen.translate_content(input_text, target_language=lang)
                st.markdown(f"#### Translated Output ({lang}):")
                st.markdown(output)


# ==========================================
# TAB 4: Lab Manual & Theory
# ==========================================
with tab4:
    st.subheader("📖 Lab Manual: Theoretical Concepts & Formulations")
    st.markdown("""
    ### 1. What is a Blog?
    A blog is an article written to share information, opinions, tutorials, or news on a specific topic.
    - **Example Topics:** Artificial Intelligence, Climate Change, Cyber Security, Electric Vehicles, Healthy Living, Digital Marketing.

    ### 2. What is AI Content Generation?
    AI Content Generation is the process of automatically creating human-like text using Artificial Intelligence. Instead of writing manually, users provide a prompt, and the AI generates content.
    - **Example Input:** `Write a blog about Artificial Intelligence.`
    - **AI Output:** `Artificial Intelligence (AI) is transforming industries by enabling machines to perform tasks that normally require human intelligence...`

    ### 3. What is Ollama?
    Ollama is a software that allows users to run Large Language Models (LLMs) locally on their own computer without using cloud APIs.
    - **Key Advantages:**
      1. Free to use
      2. Runs offline
      3. Faster response
      4. No API cost
      5. Data remains completely on your computer

    ### 4. What is Llama 3.2?
    Llama 3.2 is an advanced Large Language Model developed by Meta. It can:
    - Answer questions
    - Generate blogs
    - Summarize text
    - Translate languages
    - Write code
    - Rewrite articles

    ### 5. Understanding Prompt Engineering
    A **Prompt** is the instruction given to the AI.
    > *"The better the prompt, the better the output."*

    ### 6. Components of a Good Prompt
    A comprehensive prompt contains:
    - **Topic:** e.g., Artificial Intelligence
    - **Writing Style:** e.g., Professional
    - **Tone:** e.g., Friendly
    - **Word Count:** e.g., 500 words
    - **Audience:** e.g., Engineering Students

    **Example Prompt:**
    ```text
    Write a 500-word professional blog on Artificial Intelligence for engineering students.
    Use simple English. Include Introduction, Main Content and Conclusion.
    ```
    """)
