# RAG-Based Intelligent Programming Tutor with Step-by-Step Code Visualization

An AI-powered programming learning assistant that answers programming doubts using **RAG (Retrieval-Augmented Generation)** and helps students understand Python code execution with interactive, **step-by-step visual explanations**.

---

## 🌟 Key Highlights & Features

1. **AI Programming Doubt Solver (RAG)**:
   - Ask any programming doubt (e.g., *"Explain Python loops"*, *"What is a Python function?"*, *"How does recursion work?"*).
   - Retrieves relevant knowledge chunks using **TF-IDF + Cosine Similarity hybrid semantic search**.
   - Generates structured answers containing conceptual definitions, clean runnable code examples, expected outputs, and execution breakdowns.

2. **Interactive Step-by-Step Code Visualizer**:
   - Traces any Python program line-by-line using Python's standard `sys.settrace` and AST parser.
   - Highlights the currently active line with an interactive step slider and Next/Previous navigation.
   - **Real-Time Variable State Watcher**: Inspects local variables, types, and highlights values that changed during that specific step.
   - **Terminal Stdout Stream**: Captures console output emitted in real time.
   - **Dynamic Control Flow Diagram**: Generates Mermaid flowcharts mapping out program flow.

3. **Knowledge Base Explorer & Note Ingestion**:
   - Browse pre-loaded programming modules (loops, functions, data structures, OOP, recursion, exceptions).
   - Upload and ingest custom markdown/text notes dynamically into the RAG vector index.

4. **Self-Assessment Quiz**:
   - Interactive multiple-choice conceptual quizzes with immediate feedback and explanations.

5. **Viva & Project Presentation Guide**:
   - Built-in architecture breakdown and Viva Voce questions & answers for academic evaluations.

---

## 🏗️ System Architecture

```text
+-------------------------------------------------------------+
|                     Student Interface                       |
|        (Streamlit Web App: Doubt Solver + Visualizer)       |
+------------------------------+------------------------------+
                               |
            +------------------+------------------+
            |                                     |
    [1. Ask Question]                     [2. Trace Code]
            |                                     |
            v                                     v
+-----------------------+             +-----------------------+
|      RAG Engine       |             | Execution Tracer      |
|  - TF-IDF Vectorizer  |             |  - sys.settrace       |
|  - Cosine Similarity  |             |  - AST Analyzer       |
|  - Hybrid Keyword BM25|             |  - Variable Diffing   |
+-----------+-----------+             +-----------+-----------+
            |                                     |
            v                                     v
+-----------------------+             +-----------------------+
| Indexed Knowledge     |             | Step-by-Step State    |
| Base (.md / .txt)     |             | & Flowchart Output    |
+-----------------------+             +-----------------------+
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit | Clean, modern interactive web interface |
| **Core Language** | Python 3 | Application logic, parsing, execution |
| **Vector Retrieval** | Scikit-learn (TF-IDF & Cosine Similarity) | Semantic retrieval over knowledge base |
| **Execution Tracer** | Python `sys.settrace` & `ast` | Line-by-line state recording & variable diffing |
| **Data Handling** | Pandas & NumPy | Variable tables and vector calculations |
| **Diagrams** | Mermaid.js | Control flow diagrams |

---

## 🚀 How to Run the Project

### Option 1: 1-Click Launch (Windows)
Double-click the included `run_tutor.bat` file in the project folder.

### Option 2: Command Line
1. Open PowerShell or Command Prompt in the project folder:
   ```bash
   cd c:\Users\SUMANTH\OneDrive\Desktop\RAG_Programming_Tutor
   ```
2. Run the Streamlit application:
   ```bash
   python -m streamlit run app.py
   ```
   *(Or using full Python path if `python` is not directly on PATH: `& "C:\Users\SUMANTH\AppData\Local\Python\bin\python.exe" -m streamlit run app.py`)*

3. Open your browser at:
   ```
   http://localhost:8501
   ```

---

## 📁 Project Directory Structure

```text
RAG_Programming_Tutor/
├── app.py                      # Main Streamlit web application
├── rag_engine.py               # RAG document chunking & vector search engine
├── visualizer.py               # Step-by-step AST code tracer & state diff engine
├── run_tutor.bat               # 1-click Windows runner script
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation
└── knowledge_base/             # Structured programming notes
    ├── loops_and_iteration.md
    ├── functions_and_scope.md
    ├── data_structures.md
    ├── oop_concepts.md
    ├── recursion_and_algorithms.md
    ├── exception_handling.md
    └── python_basics.md
```

---

## 🎓 Academic Viva Questions & Answers

1. **What is RAG (Retrieval-Augmented Generation)?**
   - RAG combines document retrieval with text generation. Instead of hallucinating answers, it retrieves relevant domain knowledge chunks first and provides grounded, factual answers.

2. **How does the step-by-step code visualization work?**
   - The visualizer executes student code using a tracing hook (`sys.settrace`). At every line event, it captures local variables from the current stack frame, compares them with previous snapshots to calculate diffs, records console output, and generates step-by-step explanations.

3. **Why is this project useful for beginners?**
   - Novice programmers often struggle with mental models of how variables change inside loops and functions. This tutor connects abstract doubt-clearing with concrete, animated visual execution.
