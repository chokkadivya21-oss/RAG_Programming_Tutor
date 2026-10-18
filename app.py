"""
RAG-Based Intelligent Programming Tutor with Step-by-Step Code Visualization
Streamlit Web Application
"""

import os
import sys
import time
import streamlit as st
import pandas as pd
from rag_engine import RAGKnowledgeEngine
from visualizer import StepExecutionTracer, generate_flowchart_mermaid

# Page Configuration
st.set_page_config(
    page_title="RAG Programming Tutor & Visualizer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling (CSS)
st.markdown("""
<style>
    /* Main Theme Polish */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #2563eb, #7c3aed, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .step-box {
        background-color: #f0fdf4;
        border-left: 5px solid #22c55e;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 12px;
        font-size: 1rem;
        color: #14532d;
    }
    .code-line-active {
        background-color: #fef08a !important;
        border-left: 4px solid #eab308;
        padding: 2px 8px;
        font-weight: bold;
        color: #1e293b;
    }
    .code-line-normal {
        padding: 2px 8px;
        color: #334155;
    }
    .terminal-box {
        background: #0f172a;
        color: #38bdf8;
        font-family: 'Consolas', 'Courier New', monospace;
        padding: 12px 16px;
        border-radius: 8px;
        min-height: 80px;
        white-space: pre-wrap;
    }
    .badge-rag {
        background: #e0e7ff;
        color: #3730a3;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 12px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_DIR = os.path.join(BASE_DIR, "knowledge_base")

# Initialize RAG Engine in Session State
@st.cache_resource
def get_rag_engine():
    return RAGKnowledgeEngine(KB_DIR)

rag_engine = get_rag_engine()

# Initialize Session State
if "tracer_code" not in st.session_state:
    st.session_state.tracer_code = "for i in range(1, 4):\n    print(i)"
if "tracer_results" not in st.session_state:
    tracer = StepExecutionTracer()
    st.session_state.tracer_results = tracer.trace_code(st.session_state.tracer_code)
if "current_step_idx" not in st.session_state:
    st.session_state.current_step_idx = 0
if "last_query" not in st.session_state:
    st.session_state.last_query = "Explain Python loops"
if "doubt_response" not in st.session_state:
    retrieved = rag_engine.retrieve(st.session_state.last_query, top_k=3)
    st.session_state.doubt_response = rag_engine.answer_doubt(st.session_state.last_query, retrieved)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=64)
    st.markdown("### 🎓 **AI Programming Tutor**")
    st.caption("RAG-Powered Q&A & Code Visualizer")

    st.markdown("---")
    st.markdown("#### ⚡ Quick Concept Doubts")
    preset_questions = [
        "Explain Python loops",
        "What is a Python function?",
        "Explain list comprehensions",
        "How do dictionaries work in Python?",
        "Explain recursion with factorial",
        "How to handle exceptions in Python?",
        "Difference between lists and tuples",
    ]

    selected_preset = st.selectbox("Select a Sample Doubt:", ["-- Choose a Question --"] + preset_questions)
    if selected_preset != "-- Choose a Question --":
        st.session_state.last_query = selected_preset
        retrieved = rag_engine.retrieve(selected_preset, top_k=3)
        st.session_state.doubt_response = rag_engine.answer_doubt(selected_preset, retrieved)

    st.markdown("---")
    st.markdown("#### 📊 Knowledge Base Stats")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Total Chunks", len(rag_engine.chunks))
    with col_s2:
        kb_files = [f for f in os.listdir(KB_DIR) if f.endswith((".md", ".txt"))] if os.path.exists(KB_DIR) else []
        st.metric("Documents", len(kb_files))

    st.markdown("---")
    st.info("💡 **Tip**: Ask any programming question, then click **'🚀 Send Code to Visualizer'** to watch it execute step by step!")

# Top Title Banner
st.markdown('<div class="main-title">RAG-Based Intelligent Programming Tutor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI Knowledge Retrieval & Interactive Step-by-Step Code Execution Visualizer</div>', unsafe_allow_html=True)

# Main Navigation Tabs
tab_doubt, tab_visualizer, tab_kb, tab_quiz, tab_arch = st.tabs([
    "💬 1. Doubt Solver (RAG)",
    "🔍 2. Visual Code Tracer",
    "📚 3. Knowledge Base Explorer",
    "🧪 4. Interactive Quiz",
    "🏛️ 5. System Architecture & Viva",
])

# ==========================================
# TAB 1: RAG DOUBT SOLVER
# ==========================================
with tab_doubt:
    st.markdown("### 🤖 Ask Any Programming Doubt")
    st.write("Type your question below. The RAG engine retrieves verified programming notes and synthesizes a complete explanation with code.")

    q_col1, q_col2 = st.columns([4, 1])
    with q_col1:
        user_query = st.text_input(
            "Enter your doubt:",
            value=st.session_state.last_query,
            placeholder="e.g. Explain Python loops or How do functions work?",
            label_visibility="collapsed",
        )
    with q_col2:
        search_btn = st.button("🔍 Resolve Doubt", use_container_width=True, type="primary")

    if search_btn and user_query:
        st.session_state.last_query = user_query
        retrieved = rag_engine.retrieve(user_query, top_k=3)
        st.session_state.doubt_response = rag_engine.answer_doubt(user_query, retrieved)

    resp = st.session_state.doubt_response

    # Display Answer Card
    st.markdown("---")
    st.markdown(f"## 📖 Concept: **{resp['concept_title']}**")

    # Sources & Relevance Badges
    if resp.get("sources"):
        st.markdown("**Retrieved Knowledge Sources:**")
        cols = st.columns(len(resp["sources"]))
        for i, src in enumerate(resp["sources"]):
            with cols[i]:
                st.markdown(f"""
                <div class="metric-card">
                    <span class="badge-rag">Relevance: {src['relevance']}</span><br/>
                    <b>📄 {src['file']}</b><br/>
                    <small style="color:#64748b;">Section: {src['section']}</small>
                </div>
                """, unsafe_allow_html=True)
        st.write("")

    col_exp, col_code = st.columns([1, 1])

    with col_exp:
        st.markdown("#### 💡 Explanation")
        st.markdown(resp["explanation"])

        if resp.get("step_summary"):
            st.markdown("#### 🪜 Key Execution Steps")
            for step in resp["step_summary"]:
                st.markdown(f"- {step}")

    with col_code:
        st.markdown("#### 💻 Example Program")
        st.code(resp["code_example"], language="python")

        col_c1, col_c2 = st.columns([1, 1])
        with col_c1:
            if st.button("🚀 Send to Visualizer", type="primary", use_container_width=True):
                st.session_state.tracer_code = resp["code_example"]
                tracer = StepExecutionTracer()
                st.session_state.tracer_results = tracer.trace_code(resp["code_example"])
                st.session_state.current_step_idx = 0
                st.success("✅ Code loaded into Visualizer! Switch to Tab 2 to trace.")
        with col_c2:
            st.download_button(
                "📥 Save Snippet (.py)",
                data=resp["code_example"],
                file_name="example_code.py",
                mime="text/x-python",
                use_container_width=True,
            )

        st.markdown("#### 🖥️ Expected Output")
        st.code(resp["expected_output"], language="text")

# ==========================================
# TAB 2: STEP-BY-STEP CODE VISUALIZER
# ==========================================
with tab_visualizer:
    st.markdown("### 🔍 Step-by-Step Code Execution Visualizer")
    st.write("Simulate and inspect Python code line-by-line. Observe variable mutations, standard output, and execution flow.")

    # Preset Codes
    preset_dict = {
        "For Loop Counting": "for i in range(1, 4):\n    print(i)",
        "Accumulator Sum Pattern": "total = 0\nfor num in [10, 20, 30]:\n    total += num\n    print(f'Added {num}, total={total}')\nprint(f'Final: {total}')",
        "While Loop Countdown": "count = 3\nwhile count > 0:\n    print(f'Countdown: {count}')\n    count -= 1\nprint('Blast off!')",
        "List Filtering & Squares": "numbers = [1, 2, 3, 4, 5]\nevens = []\nfor n in numbers:\n    if n % 2 == 0:\n        evens.append(n * n)\nprint('Even squares:', evens)",
        "Function Call & Return": "def square(n):\n    res = n * n\n    return res\n\nval = 5\nans = square(val)\nprint(f'Square of {val} is {ans}')",
    }

    col_p1, col_p2 = st.columns([3, 1])
    with col_p1:
        chosen_preset = st.selectbox("Load Sample Code Snippet:", ["-- Custom / Current Code --"] + list(preset_dict.keys()))
        if chosen_preset != "-- Custom / Current Code --":
            st.session_state.tracer_code = preset_dict[chosen_preset]
    with col_p2:
        st.write("")
        st.write("")
        if st.button("🔄 Reset Tracer", use_container_width=True):
            st.session_state.tracer_code = "for i in range(1, 4):\n    print(i)"
            st.session_state.current_step_idx = 0

    code_input = st.text_area(
        "Python Code to Trace:",
        value=st.session_state.tracer_code,
        height=140,
        help="Enter executable Python code to simulate step by step.",
    )

    if st.button("▶️ Execute & Trace Code", type="primary"):
        st.session_state.tracer_code = code_input
        tracer = StepExecutionTracer()
        st.session_state.tracer_results = tracer.trace_code(code_input)
        st.session_state.current_step_idx = 0

    trace_data = st.session_state.tracer_results

    if not trace_data.get("success"):
        st.error(f"❌ {trace_data.get('error')}")
    else:
        steps = trace_data["steps"]
        total_steps = len(steps)

        if total_steps == 0:
            st.warning("⚠️ No execution steps were recorded. Check if code has statements.")
        else:
            st.markdown("---")
            # Step Navigation Controls
            ctrl_c1, ctrl_c2, ctrl_c3, ctrl_c4 = st.columns([1, 4, 1, 1])

            with ctrl_c1:
                if st.button("⏮️ Prev Step", disabled=(st.session_state.current_step_idx <= 0), use_container_width=True):
                    st.session_state.current_step_idx -= 1
                    st.rerun()

            with ctrl_c2:
                selected_step = st.slider(
                    "Execution Step",
                    min_value=1,
                    max_value=total_steps,
                    value=st.session_state.current_step_idx + 1,
                    label_visibility="collapsed",
                )
                if selected_step - 1 != st.session_state.current_step_idx:
                    st.session_state.current_step_idx = selected_step - 1
                    st.rerun()

            with ctrl_c3:
                if st.button("⏭️ Next Step", disabled=(st.session_state.current_step_idx >= total_steps - 1), use_container_width=True):
                    st.session_state.current_step_idx += 1
                    st.rerun()

            with ctrl_c4:
                st.markdown(f"**Step {st.session_state.current_step_idx + 1} / {total_steps}**")

            # Current Step Details
            curr_step = steps[st.session_state.current_step_idx]

            # Step Explanation Box
            st.markdown(f"""
            <div class="step-box">
                <b>📌 Step {curr_step.step_num}:</b> {curr_step.explanation}
            </div>
            """, unsafe_allow_html=True)

            # Two Column Visualization: Code on Left, Live States on Right
            vis_c1, vis_c2 = st.columns([1, 1])

            with vis_c1:
                st.markdown("#### 📝 Code Trace (Line Pointer)")
                source_lines = trace_data["source_lines"]
                highlighted_html = ["<div style='background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:10px; font-family:monospace;'>"]
                for i, line in enumerate(source_lines, start=1):
                    line_escaped = line.replace("<", "&lt;").replace(">", "&gt;")
                    if i == curr_step.line_no and curr_step.event != "end":
                        highlighted_html.append(
                            f"<div class='code-line-active'>👉 Line {i:02d}: {line_escaped if line_escaped else ' '}</div>"
                        )
                    else:
                        highlighted_html.append(
                            f"<div class='code-line-normal'>&nbsp;&nbsp; Line {i:02d}: {line_escaped if line_escaped else ' '}</div>"
                        )
                highlighted_html.append("</div>")
                st.markdown("".join(highlighted_html), unsafe_allow_html=True)

                st.markdown("#### 🖨️ Terminal Stdout")
                out_text = curr_step.cumulative_stdout if curr_step.cumulative_stdout else "[No output emitted yet]"
                st.markdown(f'<div class="terminal-box">{out_text}</div>', unsafe_allow_html=True)

            with vis_c2:
                st.markdown("#### 📦 Variable State Watch")
                if curr_step.variables:
                    var_records = []
                    for k, v in curr_step.variables.items():
                        is_changed = k in curr_step.changed_vars
                        var_records.append({
                            "Variable": k,
                            "Type": curr_step.variable_types.get(k, type(v).__name__),
                            "Current Value": repr(v),
                            "Status": "🟢 Updated this step" if is_changed else "Unchanged",
                        })
                    df_vars = pd.DataFrame(var_records)
                    st.dataframe(df_vars, use_container_width=True, hide_index=True)
                else:
                    st.info("No local variables defined at this step.")

                st.markdown("#### 🗺️ Control Flow Diagram")
                mermaid_code = generate_flowchart_mermaid(st.session_state.tracer_code, curr_step.line_no)
                if mermaid_code:
                    st.components.v1.html(
                        f"""
                        <script type="module">
                            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                            mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
                        </script>
                        <div class="mermaid" style="text-align: center;">
                        {mermaid_code}
                        </div>
                        """,
                        height=280,
                        scrolling=True,
                    )

# ==========================================
# TAB 3: KNOWLEDGE BASE EXPLORER
# ==========================================
with tab_kb:
    st.markdown("### 📚 Knowledge Base Management & Explorer")
    st.write("Browse indexed notes, inspect chunks, or upload your own programming guides.")

    kb_c1, kb_c2 = st.columns([2, 1])

    with kb_c1:
        st.markdown("#### 🔍 Browse Existing Notes")
        files = [f for f in os.listdir(KB_DIR) if f.endswith((".md", ".txt"))] if os.path.exists(KB_DIR) else []
        selected_file = st.selectbox("Choose a Knowledge Document:", files)

        if selected_file:
            filepath = os.path.join(KB_DIR, selected_file)
            with open(filepath, "r", encoding="utf-8") as f:
                doc_text = f.read()
            st.text_area(f"Document Content ({selected_file})", value=doc_text, height=350, disabled=True)

    with kb_c2:
        st.markdown("#### ➕ Add Custom Notes")
        new_doc_name = st.text_input("File Name (e.g., custom_tuples.md):", value="custom_notes.md")
        new_doc_content = st.text_area(
            "Note Content (Markdown format):",
            value="# Custom Programming Notes\n\n## Concept Title\nExplanation goes here...\n\n```python\nprint('Hello World')\n```",
            height=240,
        )

        if st.button("📥 Save & Ingest into RAG Engine", type="primary", use_container_width=True):
            if new_doc_name and new_doc_content:
                rag_engine.add_custom_document(new_doc_name, new_doc_content)
                st.success(f"🎉 '{new_doc_name}' indexed successfully! Total chunks: {len(rag_engine.chunks)}")
                time.sleep(1)
                st.rerun()

# ==========================================
# TAB 4: INTERACTIVE PRACTICE QUIZ
# ==========================================
with tab_quiz:
    st.markdown("### 🧪 Practice & Conceptual Check")
    st.write("Test your programming understanding with these interactive conceptual questions.")

    q1 = st.radio(
        "1. What is the output of `for i in range(1, 4): print(i)`?",
        options=["A) 1, 2, 3, 4", "B) 1, 2, 3", "C) 0, 1, 2, 3", "D) 1, 3"],
    )
    if st.button("Check Question 1"):
        if "B) 1, 2, 3" in q1:
            st.success("✅ Correct! `range(start, stop)` stops at `stop - 1` (exclusive).")
        else:
            st.error("❌ Incorrect. In Python, `range(1, 4)` generates numbers 1, 2, 3.")

    st.markdown("---")
    q2 = st.radio(
        "2. What happens if a recursive function does not have a base case?",
        options=[
            "A) It compiles normally and executes once",
            "B) It returns None automatically",
            "C) It causes a `RecursionError: maximum recursion depth exceeded`",
            "D) Python converts it to an infinite loop without error",
        ],
    )
    if st.button("Check Question 2"):
        if "C)" in q2:
            st.success("✅ Correct! Without a base case, call stack overflows and triggers RecursionError.")
        else:
            st.error("❌ Incorrect. The correct answer is C: RecursionError due to stack overflow.")

    st.markdown("---")
    q3 = st.radio(
        "3. In Python's LEGB scope rule, what does 'E' stand for?",
        options=["A) External", "B) Enclosing", "C) Execution", "D) Environment"],
    )
    if st.button("Check Question 3"):
        if "B) Enclosing" in q3:
            st.success("✅ Correct! LEGB stands for Local, Enclosing, Global, Built-in.")
        else:
            st.error("❌ Incorrect. E stands for Enclosing scope.")

# ==========================================
# TAB 5: ARCHITECTURE & VIVA GUIDE
# ==========================================
with tab_arch:
    st.markdown("### 🏛️ System Architecture & Academic Viva Guide")

    st.markdown("""
    #### ⚙️ How the RAG Programming Tutor Works:
    1. **Knowledge Ingestion & Chunking**: Markdown notes stored in `knowledge_base/` are chunked into section-level passages with attached code blocks.
    2. **Vector Space & Hybrid Retrieval**: Queries are converted to TF-IDF n-gram vectors and matched using Cosine Similarity combined with keyword overlap ranking.
    3. **Pedagogic Synthesis**: The top retrieved context is synthesized into a definition, reproducible code example, expected output, and execution steps.
    4. **AST Code Tracer Sandbox**: Python's `sys.settrace` and `ast` parse user code in a safe execution sandbox to record line pointers, variable diffs, and console stdout at every clock cycle.
    5. **Streamlit Interactive UI**: Provides a clean visual interface with synchronized step navigation, variable watch tables, and dynamic flowcharts.
    """)

    st.markdown("---")
    st.markdown("#### 🎓 Common Viva Voce Questions & Answers")
    with st.expander("Q1: What is RAG and why is it used here?"):
        st.write(
            "**Answer:** RAG (Retrieval-Augmented Generation) combines information retrieval with generation. "
            "Instead of relying solely on general LLM memorization or static answers, RAG retrieves verified, "
            "domain-specific programming notes first and uses them to ground explanations and code examples accurately."
        )

    with st.expander("Q2: How does the step-by-step code tracer work?"):
        st.write(
            "**Answer:** The tracer uses Python's execution tracing hooks (`sys.settrace`) combined with an AST analyzer. "
            "At every line event, it captures local variables (`frame.f_locals`), compares them with the previous step to identify modified variables, "
            "captures stdout emissions, and constructs a state snapshot."
        )

    with st.expander("Q3: Can this system be connected to an online LLM API like OpenAI or Gemini?"):
        st.write(
            "**Answer:** Yes! The RAG retrieval pipeline extracts the context chunks and query, which can either be passed to an LLM prompt "
            "or processed by our built-in offline educational synthesis engine."
        )
