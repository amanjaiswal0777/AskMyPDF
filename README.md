<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AskMyPDF – RAG Question Answering over PDFs</title>
<style>
  :root {
    --bg: #f6f8fa;
    --paper: #ffffff;
    --ink: #14202b;
    --muted: #55636f;
    --line: #d9e0e6;
    --accent: #1f6f8b;
    --accent-soft: #e3f0f4;
    --code-bg: #0f1b26;
    --code-ink: #dbe7ef;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: Georgia, "Times New Roman", serif;
    font-size: 18px;
    line-height: 1.7;
  }
  .wrap { max-width: 860px; margin: 0 auto; padding: 48px 24px 80px; }
  header { padding-bottom: 28px; border-bottom: 2px solid var(--ink); margin-bottom: 36px; }
  h1 {
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    font-size: 3rem; line-height: 1.1; margin: 0 0 12px; letter-spacing: -0.02em;
  }
  .tagline { font-size: 1.2rem; color: var(--muted); margin: 0 0 18px; max-width: 60ch; }
  .badges { display: flex; flex-wrap: wrap; gap: 8px; }
  .badge {
    font-family: system-ui, sans-serif; font-size: 0.8rem; font-weight: 600;
    background: var(--accent-soft); color: var(--accent);
    padding: 4px 12px; border-radius: 999px;
  }
  h2 {
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    font-size: 1.6rem; margin: 48px 0 12px; padding-top: 8px; letter-spacing: -0.01em;
  }
  h3 { font-family: system-ui, sans-serif; font-size: 1.1rem; margin: 28px 0 6px; }
  p { margin: 0 0 14px; max-width: 70ch; }
  ul, ol { padding-left: 1.3em; max-width: 70ch; }
  li { margin-bottom: 6px; }
  a { color: var(--accent); }
  code {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 0.85em; background: var(--accent-soft); padding: 1px 6px; border-radius: 4px;
  }
  pre {
    background: var(--code-bg); color: var(--code-ink);
    padding: 16px 20px; border-radius: 8px; overflow-x: auto;
    font-size: 0.85rem; line-height: 1.6; margin: 12px 0 20px;
  }
  pre code { background: none; padding: 0; color: inherit; font-size: inherit; }

  /* The pipeline is a true sequence, so it is numbered */
  .pipeline {
    list-style: none; padding: 0; margin: 20px 0 8px; max-width: none;
    display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px;
    counter-reset: step;
  }
  .pipeline li {
    counter-increment: step; margin: 0; background: var(--paper);
    border: 1px solid var(--line); border-left: 4px solid var(--accent);
    padding: 10px 14px; font-family: system-ui, sans-serif; font-size: 0.92rem; line-height: 1.4;
  }
  .pipeline li::before {
    content: counter(step) ". "; font-weight: 700; color: var(--accent);
  }
  .pipeline small { display: block; color: var(--muted); margin-top: 2px; font-size: 0.8rem; }

  .table-scroll { overflow-x: auto; margin: 12px 0 20px; }
  table {
    border-collapse: collapse; width: 100%; background: var(--paper);
    font-family: system-ui, sans-serif; font-size: 0.92rem;
  }
  th, td { text-align: left; padding: 10px 14px; border-bottom: 1px solid var(--line); vertical-align: top; }
  th { background: var(--ink); color: #fff; font-weight: 600; }

  .note {
    background: var(--accent-soft); border-left: 4px solid var(--accent);
    padding: 12px 18px; margin: 16px 0; max-width: 70ch; font-size: 0.95rem;
  }
  details {
    background: var(--paper); border: 1px solid var(--line);
    padding: 12px 18px; margin-bottom: 10px; max-width: 70ch;
  }
  summary { cursor: pointer; font-family: system-ui, sans-serif; font-weight: 600; }
  summary:focus-visible, a:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
  details p { margin: 10px 0 0; }
  footer { margin-top: 60px; padding-top: 20px; border-top: 1px solid var(--line); color: var(--muted); font-size: 0.9rem; }
  @media (max-width: 560px) { h1 { font-size: 2.2rem; } body { font-size: 17px; } }
</style>
</head>
<body>
<div class="wrap">

<header>
  <h1>AskMyPDF</h1>
  <p class="tagline">Upload a PDF, ask questions in plain English, and get answers grounded in the document, with the source passages shown alongside.</p>
  <div class="badges">
    <span class="badge">Python</span>
    <span class="badge">LangChain</span>
    <span class="badge">Streamlit</span>
    <span class="badge">ChromaDB</span>
    <span class="badge">OpenAI</span>
  </div>
</header>

<h2 id="overview">Overview</h2>
<p>AskMyPDF is a Retrieval-Augmented Generation (RAG) application. Instead of asking a language model to answer from memory, the app first finds the passages of your PDF that are relevant to the question and gives only those passages to the model. This keeps answers tied to your document and reduces made-up facts.</p>
<p>If the document does not contain the answer, the app says so: <em>"The information is not available in the uploaded PDF."</em></p>

<h2 id="features">Features</h2>
<ul>
  <li>Upload any text-based PDF and process it with one click</li>
  <li>Ask questions in a text area and read the answer in a separate box</li>
  <li>View the exact chunks used for the answer, labelled with page number and chunk id</li>
  <li>Adjust chunk size, chunk overlap, number of retrieved chunks (k) and the LLM from the sidebar</li>
  <li>A fresh vector store for each upload, so answers never mix content from different PDFs</li>
</ul>

<h2 id="pipeline">How it works</h2>
<ol class="pipeline">
  <li>PDF upload<small>Streamlit file uploader</small></li>
  <li>Document loader<small>PyPDFLoader, one document per page</small></li>
  <li>Chunking<small>Recursive character splitter</small></li>
  <li>Embeddings<small>text-embedding-3-small</small></li>
  <li>Vector store<small>Chroma, text + vectors + metadata</small></li>
  <li>Retriever<small>Top-k similarity search</small></li>
  <li>Prompt<small>Question + retrieved context + rules</small></li>
  <li>LLM<small>ChatOpenAI, temperature 0</small></li>
  <li>Answer + context<small>Shown in the UI</small></li>
</ol>

<h3>Indexing (when you click Process PDF)</h3>
<p>The PDF is saved to a temporary file and loaded page by page. The text is split into overlapping chunks, each chunk is converted into an embedding vector, and the vectors are stored in Chroma together with the original text and page number.</p>

<h3>Querying (when you click Ask Question)</h3>
<p>Your question is embedded with the same model, Chroma returns the k closest chunks, and those chunks are placed in a prompt that instructs the model to answer only from the context. The answer and the retrieved chunks are then displayed.</p>

<h2 id="concepts">Key design decisions</h2>
<div class="table-scroll">
<table>
  <thead><tr><th>Decision</th><th>Why</th></tr></thead>
  <tbody>
    <tr><td>Chunk size 1000, overlap 200</td><td>Chunks are small enough for precise retrieval. Overlap keeps sentences that cross a boundary intact in at least one chunk.</td></tr>
    <tr><td>Same embedding model for chunks and questions</td><td>Vectors from different models are not comparable, so similarity search would be meaningless.</td></tr>
    <tr><td>Unique Chroma collection per upload</td><td>Prevents chunks from an earlier PDF from appearing in answers about a new one.</td></tr>
    <tr><td>Strict prompt with a fixed fallback sentence</td><td>Forces grounded answers and a clear "not available" response.</td></tr>
    <tr><td>Temperature 0</td><td>Keeps answers factual and repeatable.</td></tr>
    <tr><td>Page metadata kept on every chunk</td><td>Lets the UI show where each piece of context came from.</td></tr>
  </tbody>
</table>
</div>

<h2 id="structure">Project structure</h2>
<pre><code>askmypdf/
├── app.py              # Entire application (loader, splitter, embeddings,
│                       # vector store, retriever, prompt, LLM, Streamlit UI)
├── requirements.txt    # Python dependencies
├── .env.example        # Template for your API key
└── README.html         # This file</code></pre>

<p>Inside <code>app.py</code>, the code is divided into numbered sections, one per pipeline stage:</p>
<div class="table-scroll">
<table>
  <thead><tr><th>Section</th><th>Function</th><th>Responsibility</th></tr></thead>
  <tbody>
    <tr><td>1. PDF loading</td><td><code>load_pdf()</code></td><td>Save upload to a temp file, extract text per page</td></tr>
    <tr><td>2. Text splitting</td><td><code>split_documents()</code></td><td>Create overlapping chunks and assign chunk ids</td></tr>
    <tr><td>3. Embeddings</td><td><code>get_embedding_model()</code></td><td>Return the OpenAI embedding model</td></tr>
    <tr><td>4. Vector store</td><td><code>create_vector_store()</code></td><td>Embed and store chunks in Chroma</td></tr>
    <tr><td>5. Retrieval</td><td><code>retrieve_context()</code></td><td>Return the top-k similar chunks for a question</td></tr>
    <tr><td>6. Prompt</td><td><code>prompt_template</code>, <code>format_context()</code></td><td>Build the grounded prompt with page-labelled context</td></tr>
    <tr><td>7. LLM</td><td><code>generate_answer()</code></td><td>Run prompt, model and output parser as a chain</td></tr>
    <tr><td>8. UI</td><td>Streamlit code</td><td>Upload, buttons, answer box, context viewer</td></tr>
  </tbody>
</table>
</div>

<h2 id="setup">Setup</h2>
<h3>Requirements</h3>
<ul>
  <li>Python 3.10 or newer</li>
  <li>An OpenAI API key</li>
</ul>

<h3>Install and run</h3>
<pre><code># 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key
cp .env.example .env            # then edit .env and set OPENAI_API_KEY

# 4. Start the app
streamlit run app.py</code></pre>
<p>Streamlit opens the app in your browser, usually at <code>http://localhost:8501</code>.</p>

<h2 id="usage">Usage</h2>
<ol>
  <li>Click <strong>Browse files</strong> and choose a PDF.</li>
  <li>Click <strong>Process PDF</strong> and wait for the success message. The page and chunk counts appear.</li>
  <li>Type a question and click <strong>Ask Question</strong>.</li>
  <li>Read the answer in the answer box.</li>
  <li>Tick <strong>Show retrieved context / chunks</strong> to see the passages the answer was based on.</li>
</ol>

<h3>Settings</h3>
<div class="table-scroll">
<table>
  <thead><tr><th>Setting</th><th>Default</th><th>Effect</th></tr></thead>
  <tbody>
    <tr><td>Chunk size</td><td>1000</td><td>Larger chunks carry more context but retrieve less precisely. Applies on the next Process PDF.</td></tr>
    <tr><td>Chunk overlap</td><td>200</td><td>Higher overlap reduces cut-off sentences but increases the number of chunks.</td></tr>
    <tr><td>Chunks to retrieve (k)</td><td>4</td><td>More chunks give broader context at the cost of noise and token usage.</td></tr>
    <tr><td>LLM model</td><td>gpt-4o-mini</td><td>Choose a stronger model for harder questions.</td></tr>
  </tbody>
</table>
</div>

<h2 id="limits">Known limitations</h2>
<ul>
  <li><strong>Scanned PDFs:</strong> pages that are images have no extractable text and need OCR first.</li>
  <li><strong>Broad questions:</strong> a request such as "summarize the whole document" only sees the top-k chunks, not the full text.</li>
  <li><strong>In-memory store:</strong> the vector store is lost when the app restarts.</li>
  <li><strong>Error handling:</strong> the current version does not validate inputs or catch errors. For example, clicking Process PDF with no file raises an exception.</li>
  <li><strong>Single document, no chat memory:</strong> each question is answered independently.</li>
</ul>

<h2 id="roadmap">Possible improvements</h2>
<ul>
  <li>Input validation and friendly error messages</li>
  <li>Persistent Chroma storage (<code>persist_directory</code>)</li>
  <li>Map-reduce summarization for whole-document questions</li>
  <li>MMR or reranking for more diverse, relevant retrieval</li>
  <li>Hybrid search combining keyword (BM25) and vector search</li>
  <li>Conversation history for follow-up questions</li>
  <li>Streaming answers and support for multiple PDFs</li>
  <li>Automated evaluation with a framework such as RAGAS</li>
</ul>

<h2 id="faq">Common questions</h2>
<details>
  <summary>Why not send the whole PDF to the LLM?</summary>
  <p>Long documents may exceed the model's context window, cost more per question, and dilute the relevant information. Retrieval sends only the passages that matter.</p>
</details>
<details>
  <summary>What does overlap do?</summary>
  <p>It repeats the end of one chunk at the start of the next, so a sentence or idea that sits on a boundary is still complete in at least one chunk.</p>
</details>
<details>
  <summary>How does the app avoid hallucinations?</summary>
  <p>The prompt restricts the model to the retrieved context, requires a fixed "not available" reply when the answer is missing, and the model runs at temperature 0. No approach removes hallucination entirely, which is why the retrieved chunks are shown for verification.</p>
</details>
<details>
  <summary>Why does the app show page numbers?</summary>
  <p>Every chunk keeps its page metadata from the loader, so users can check the answer against the original document.</p>
</details>

<footer>AskMyPDF · Built with Python, LangChain, Streamlit and ChromaDB</footer>

</div>
</body>
</html>
