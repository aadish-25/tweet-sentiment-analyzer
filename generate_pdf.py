import os
import pypdf
from xhtml2pdf import pisa

def build_pdf():
    assets_dir = os.path.abspath("assets")
    logo_path = os.path.join(assets_dir, "college_logo_0.png").replace("\\", "/")
    fig1_path = os.path.join(assets_dir, "fig1_workflow.png").replace("\\", "/")
    fig2_path = os.path.join(assets_dir, "fig2_class_dist.png").replace("\\", "/")
    fig3_path = os.path.join(assets_dir, "fig3_model_comparison.png").replace("\\", "/")
    fig4_path = os.path.join(assets_dir, "fig4_confusion_matrix.png").replace("\\", "/")
    fig5_path = os.path.join(assets_dir, "fig5_top_features.png").replace("\\", "/")

    html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page cover_template {
    size: letter portrait;
    margin: 15mm;
    @frame content_frame {
        left: 18mm; width: 180mm; top: 12mm; height: 255mm;
    }
}

@page body_template {
    size: letter portrait;
    margin: 18mm;
    @frame header_frame {
        -pdf-frame-content: page_header;
        left: 18mm; width: 180mm; top: 8mm; height: 11mm;
    }
    @frame content_frame {
        left: 18mm; width: 180mm; top: 20mm; height: 238mm;
    }
    @frame footer_frame {
        -pdf-frame-content: page_footer;
        left: 18mm; width: 180mm; top: 262mm; height: 10mm;
    }
}

body {
    font-family: "Times New Roman", Times, serif;
    font-size: 9.5pt;
    line-height: 1.35;
    color: #111111;
}

.header-table {
    width: 100%;
    font-size: 8.5pt;
    color: #333333;
    border-bottom: 0.75pt solid #555555;
    padding-bottom: 2px;
}

.footer-table {
    width: 100%;
    font-size: 8pt;
    color: #444444;
    border-top: 0.75pt solid #888888;
    padding-top: 2px;
}

h1, h2, h3, h4 {
    font-family: "Times New Roman", Times, serif;
    color: #111111;
    margin: 0;
    padding: 0;
}

h2.section-title {
    font-size: 11.5pt;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 8px;
    margin-bottom: 4px;
    border-bottom: 0.5pt solid #444444;
    padding-bottom: 2px;
}

h3.sub-title {
    font-size: 10pt;
    font-weight: bold;
    margin-top: 6px;
    margin-bottom: 3px;
}

p {
    margin: 0 0 5px 0;
    text-align: justify;
}

ul, ol {
    margin: 2px 0 6px 16px;
    padding: 0;
}

li {
    margin-bottom: 2px;
    text-align: justify;
}

table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 4px 0 6px 0;
    font-size: 8.5pt;
}

table.data-table th {
    background-color: #2b3a4a;
    color: #ffffff;
    font-weight: bold;
    padding: 4px 5px;
    border: 0.5pt solid #444444;
    text-align: left;
}

table.data-table td {
    padding: 3px 5px;
    border: 0.5pt solid #bbbbbb;
    vertical-align: middle;
}

table.data-table tr.even {
    background-color: #f7f9fa;
}

.text-center {
    text-align: center;
}

.text-right {
    text-align: right;
}

.bold {
    font-weight: bold;
}

.italic {
    font-style: italic;
}

.caption {
    font-size: 8pt;
    color: #444444;
    font-style: italic;
    text-align: center;
    margin-top: 2px;
    margin-bottom: 5px;
}

.img-container {
    text-align: center;
    margin: 4px 0 2px 0;
}

.formula-box {
    background-color: #f8f9fa;
    border-left: 2.5pt solid #2b3a4a;
    padding: 4px 8px;
    margin: 4px 0;
    font-family: "Courier New", Courier, monospace;
    font-size: 8.5pt;
}

.cover-wrapper {
    text-align: center;
    height: 100%;
}

.cover-univ {
    font-size: 15pt;
    font-weight: bold;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.cover-college {
    font-size: 12.5pt;
    font-weight: bold;
    margin-top: 5px;
}

.cover-addr {
    font-size: 9.5pt;
    margin-top: 2px;
}

.cover-naac {
    font-size: 10pt;
    font-weight: bold;
    margin-top: 2px;
    letter-spacing: 0.5px;
}

.cover-dept {
    font-size: 11.5pt;
    font-weight: bold;
    margin-top: 3px;
    letter-spacing: 0.5px;
}

.cover-logo {
    margin-top: 10px;
    margin-bottom: 10px;
}

.cover-rep-title {
    font-size: 13pt;
    font-weight: bold;
    letter-spacing: 1px;
    margin-top: 4px;
}

.cover-on {
    font-size: 10.5pt;
    font-weight: bold;
    margin-top: 3px;
}

.cover-project-title {
    font-size: 13.5pt;
    font-weight: bold;
    font-style: italic;
    color: #1a2a3a;
    margin-top: 5px;
    line-height: 1.25;
}

.cover-acad {
    font-size: 10pt;
    font-weight: bold;
    margin-top: 8px;
}

.cover-deg {
    font-size: 10.5pt;
    font-weight: bold;
    margin-top: 2px;
}

.cover-sub-by {
    font-size: 10pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 10px;
}

.cover-members-table {
    width: 85%;
    margin: 6px auto 0 auto;
    font-size: 9.5pt;
    text-align: left;
}

.cover-guide {
    margin-top: 14px;
    font-size: 10pt;
    line-height: 1.3;
}
</style>
</head>
<body>

<div id="page_header">
    <table class="header-table">
        <tr>
            <td align="left" style="width: 78%; font-weight: bold;">Tweet Sentiment Analysis System Using IR &amp; Machine Learning</td>
            <td align="right" style="width: 22%;">Page <pdf:pagenumber></td>
        </tr>
    </table>
</div>

<div id="page_footer">
    <table class="footer-table">
        <tr>
            <td align="left" style="width: 75%;">Department of Computer Engineering, MESWCOE Pune</td>
            <td align="right" style="width: 25%;">Academic Year 2026-27</td>
        </tr>
    </table>
</div>

<!-- ================= PAGE 1: COVER PAGE ================= -->
<pdf:nexttemplate name="cover_template" />
<div class="cover-wrapper">
    <div class="cover-univ">Savitribai Phule Pune University</div>
    <div class="cover-college">Modern Education Society’s Wadia College of Engineering, Pune</div>
    <div class="cover-addr">19, Bund Garden, V.K. Joag Path, Pune – 411001.</div>
    <div class="cover-naac">ACCREDITED BY NBA AND NAAC WITH ‘A++’ GRADE</div>
    <div class="cover-dept">DEPARTMENT OF COMPUTER ENGINEERING</div>
    
    <div style="border-bottom: 1.5pt solid #111111; margin: 8px 30px 10px 30px;"></div>

    <div class="cover-logo">
        <img src="REPLACE_LOGO_PATH" height="95" alt="College Logo" />
    </div>

    <div class="cover-rep-title">A MINI-PROJECT REPORT</div>
    <div class="cover-on">ON</div>
    <div class="cover-project-title">“Tweet Sentiment Analysis System Using Information Retrieval &amp; Machine Learning”</div>

    <div class="cover-acad">(Academic Year: 2026-27)</div>
    <div class="cover-deg">B.E. (COMPUTER ENGINEERING)</div>

    <div class="cover-sub-by">SUBMITTED BY:</div>
    <div style="font-weight: bold; font-size: 9.5pt; margin-top: 2px;">Group Members:</div>
    <table class="cover-members-table">
        <tr>
            <td style="width: 10%; text-align: center; font-weight: bold;">1.</td>
            <td style="width: 55%; font-weight: bold;">Aadish Sonawane</td>
            <td style="width: 35%; text-align: right; font-weight: bold;">(Roll No: F23112052)</td>
        </tr>
        <tr>
            <td style="text-align: center; font-weight: bold;">2.</td>
            <td style="font-weight: bold;">Aditya Raje</td>
            <td style="text-align: right; font-weight: bold;">(Roll No: F23112050)</td>
        </tr>
        <tr>
            <td style="text-align: center; font-weight: bold;">3.</td>
            <td style="font-weight: bold;">Mayur Langhi</td>
            <td style="text-align: right; font-weight: bold;">(Roll No: F23112053)</td>
        </tr>
    </table>

    <div style="margin-top: 50px; text-align: right; padding-right: 20px;">
        <div style="display: inline-block; text-align: center; width: 200px;">
            <div style="height: 48px;"></div>
            <div style="border-top: 1.2pt solid #111111; padding-top: 5px;">
                <div style="font-weight: bold; font-size: 10.5pt;">Teacher's Signature</div>
                <div style="font-weight: bold; font-size: 10pt; margin-top: 3px; color: #111111;">V. D. Gaikwad</div>
            </div>
        </div>
    </div>
</div>

<!-- ================= PAGE 2: INDEX ================= -->
<pdf:nexttemplate name="cover_template" />
<pdf:nextpage />
<div style="padding: 10px 5px;">
    <h2 style="font-size: 14pt; text-align: center; font-weight: bold; margin-bottom: 12px; letter-spacing: 1px;">INDEX</h2>
    
    <table class="data-table" style="font-size: 9pt;">
        <thead>
            <tr>
                <th style="width: 12%; text-align: center;">Sr. No.</th>
                <th style="width: 72%;">CONTENTS</th>
                <th style="width: 16%; text-align: center;">Page No.</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center bold">1</td>
                <td class="bold">Introduction</td>
                <td class="text-center bold">3</td>
            </tr>
            <tr class="even">
                <td class="text-center bold">2</td>
                <td class="bold">Problem Statement &amp; Motivation</td>
                <td class="text-center bold">3</td>
            </tr>
            <tr>
                <td class="text-center"></td>
                <td style="padding-left: 18px;">2.1 Problem Statement</td>
                <td class="text-center">3</td>
            </tr>
            <tr class="even">
                <td class="text-center"></td>
                <td style="padding-left: 18px;">2.2 Motivation &amp; Industry Context</td>
                <td class="text-center">3</td>
            </tr>
            <tr>
                <td class="text-center bold">3</td>
                <td class="bold">Project Objectives</td>
                <td class="text-center bold">3</td>
            </tr>
            <tr class="even">
                <td class="text-center bold">4</td>
                <td class="bold">System Architecture &amp; Methodology</td>
                <td class="text-center bold">4</td>
            </tr>
            <tr>
                <td class="text-center"></td>
                <td style="padding-left: 18px;">4.1 High-Level Workflow &amp; Architecture Diagram</td>
                <td class="text-center">4</td>
            </tr>
            <tr class="even">
                <td class="text-center"></td>
                <td style="padding-left: 18px;">4.2 Stages of the Pipeline</td>
                <td class="text-center">4</td>
            </tr>
            <tr>
                <td class="text-center bold">5</td>
                <td class="bold">Technologies Used &amp; Software Stack</td>
                <td class="text-center bold">5</td>
            </tr>
            <tr class="even">
                <td class="text-center bold">6</td>
                <td class="bold">Dataset Description &amp; Exploration</td>
                <td class="text-center bold">5</td>
            </tr>
            <tr>
                <td class="text-center"></td>
                <td style="padding-left: 18px;">6.1 Source, Curated Size &amp; Class Balance</td>
                <td class="text-center">5</td>
            </tr>
            <tr class="even">
                <td class="text-center"></td>
                <td style="padding-left: 18px;">6.2 Schema &amp; Train-Test Partitioning</td>
                <td class="text-center">5</td>
            </tr>
            <tr>
                <td class="text-center bold">7</td>
                <td class="bold">Data Preprocessing &amp; Vector Space Modeling (IR Perspective)</td>
                <td class="text-center bold">6</td>
            </tr>
            <tr class="even">
                <td class="text-center"></td>
                <td style="padding-left: 18px;">7.1 Text Preprocessing &amp; Lexical Normalization</td>
                <td class="text-center">6</td>
            </tr>
            <tr>
                <td class="text-center"></td>
                <td style="padding-left: 18px;">7.2 TF-IDF Mathematical Formulation &amp; N-Gram Vectorization</td>
                <td class="text-center">6</td>
            </tr>
            <tr class="even">
                <td class="text-center"></td>
                <td style="padding-left: 18px;">7.3 Stratified Train-Test Splitting</td>
                <td class="text-center">6</td>
            </tr>
            <tr>
                <td class="text-center bold">8</td>
                <td class="bold">Exploratory Data Analysis &amp; Vocabulary Attribution</td>
                <td class="text-center bold">7</td>
            </tr>
            <tr class="even">
                <td class="text-center"></td>
                <td style="padding-left: 18px;">8.1 Sentiment Distribution Characteristics</td>
                <td class="text-center">7</td>
            </tr>
            <tr>
                <td class="text-center"></td>
                <td style="padding-left: 18px;">8.2 Top Influential Terms per Sentiment Class (Weight Coefficients)</td>
                <td class="text-center">7</td>
            </tr>
            <tr class="even">
                <td class="text-center bold">9</td>
                <td class="bold">Model Building &amp; Algorithmic Comparison</td>
                <td class="text-center bold">8</td>
            </tr>
            <tr>
                <td class="text-center"></td>
                <td style="padding-left: 18px;">9.1 Multi-Model Benchmark Comparison (6 Classifiers)</td>
                <td class="text-center">8</td>
            </tr>
            <tr class="even">
                <td class="text-center"></td>
                <td style="padding-left: 18px;">9.2 Rigorous Justification for Selecting Logistic Regression</td>
                <td class="text-center">8</td>
            </tr>
            <tr>
                <td class="text-center bold">10</td>
                <td class="bold">Results &amp; Quantitative Evaluation</td>
                <td class="text-center bold">9</td>
            </tr>
            <tr class="even">
                <td class="text-center"></td>
                <td style="padding-left: 18px;">10.1 Test Set Performance Metrics (Accuracy, Precision, Recall, F1, Loss)</td>
                <td class="text-center">9</td>
            </tr>
            <tr>
                <td class="text-center"></td>
                <td style="padding-left: 18px;">10.2 Confusion Matrix Analysis &amp; Diagnostic Heatmap</td>
                <td class="text-center">9</td>
            </tr>
            <tr class="even">
                <td class="text-center"></td>
                <td style="padding-left: 18px;">10.3 Per-Class Classification Report Breakdown</td>
                <td class="text-center">9</td>
            </tr>
            <tr>
                <td class="text-center bold">11</td>
                <td class="bold">Live URL Ingestion &amp; Web Dashboard Implementation</td>
                <td class="text-center bold">10</td>
            </tr>
            <tr class="even">
                <td class="text-center bold">12</td>
                <td class="bold">Conclusion &amp; Future Enhancements</td>
                <td class="text-center bold">10</td>
            </tr>
            <tr>
                <td class="text-center bold">13</td>
                <td class="bold">References</td>
                <td class="text-center bold">10</td>
            </tr>
        </tbody>
    </table>
</div>

<!-- ================= PAGE 3: INTRO, PROBLEM, OBJECTIVES ================= -->
<pdf:nexttemplate name="body_template" />
<pdf:nextpage />
<div>
    <h2 class="section-title">1. INTRODUCTION</h2>
    <p>
        Social media platforms, particularly Twitter (now X), have emerged as the primary digital arenas where millions of individuals express real-time opinions, reactions, complaints, and sentiments regarding products, services, politics, governance, and societal events. With over 500 million tweets generated daily, manual analysis of this immense unstructured textual data is computationally infeasible.
    </p>
    <p>
        In the academic domain of <b>Information Retrieval (IR)</b> and <b>Natural Language Processing (NLP)</b>, text sentiment classification represents a fundamental document categorization and indexing challenge. An effective IR system does not merely search for documents containing specific query terms; it must extract semantic insights, understand document polarity (positive, negative, or neutral), and rank information based on relevance and sentiment intensity.
    </p>
    <p>
        This mini-project develops an end-to-end, high-performance <b>Tweet Sentiment Analysis System</b> aligned with the Savitribai Phule Pune University (SPPU) Fourth-Year Computer Engineering curriculum for Information Retrieval. The system combines the Vector Space Model (VSM) using Term Frequency-Inverse Document Frequency (TF-IDF) weighting with an optimized Logistic Regression classifier trained on a balanced 30,000-tweet benchmark dataset.
    </p>

    <h2 class="section-title">2. PROBLEM STATEMENT &amp; MOTIVATION</h2>
    <h3 class="sub-title">2.1 Problem Statement</h3>
    <div style="background-color: #f4f6f8; border-left: 2.5pt solid #2b3a4a; padding: 5px 8px; margin: 4px 0 6px 0; font-style: italic;">
        “To design, implement, and evaluate an Information Retrieval and Machine Learning-based Tweet Sentiment Analysis System capable of classifying social media text into Positive, Negative, or Neutral polarities, supporting direct textual input and live Twitter/X URLs, while providing calibrated probability distributions, vocabulary feature attribution, and a reproducible offline evaluation pipeline.”
    </div>

    <h3 class="sub-title">2.2 Motivation &amp; Industry Context</h3>
    <p>Traditional keyword-based search and lookup methods fail drastically on social media due to unique characteristics:</p>
    <ul>
        <li><b>Informal Text &amp; Brevity:</b> Tweets are constrained in length, containing slang, abbreviations, hashtags, user mentions (@username), and colloquial vernacular.</li>
        <li><b>Class Imbalance &amp; Ambiguity:</b> Purely binary classification (positive vs. negative) fails to capture objective news, factual statements, and inquiries, necessitating a robust 3-class system (Negative, Neutral, Positive).</li>
        <li><b>High Dimensionality &amp; Sparsity:</b> Text corpora contain tens of thousands of unique tokens. Linear classifiers regularized in high-dimensional vector spaces are critical to avoid overfitting.</li>
        <li><b>Interpretability Requirements:</b> In enterprise brand monitoring and customer care escalation, black-box predictions are inadequate; stakeholders require transparency into which specific words drove the classification score.</li>
        <li><b>API Accessibility:</b> With the monetization of the Twitter/X API in 2023, automated sentiment systems must implement resilient fallback mechanisms and scraping pipelines to fetch live content without paid enterprise credentials.</li>
    </ul>

    <h2 class="section-title">3. PROJECT OBJECTIVES</h2>
    <ul>
        <li><b>Curate a Balanced 30,000-Tweet Corpus:</b> Acquire and normalize an evenly distributed dataset across Negative (10k), Neutral (10k), and Positive (10k) tweets.</li>
        <li><b>Implement Vector Space Modeling (TF-IDF):</b> Construct an 8,000-feature vocabulary incorporating sublinear term frequency scaling and (1, 2)-gram tokenization to capture negation and phrase contexts.</li>
        <li><b>Benchmark Multi-Class Machine Learning Algorithms:</b> Empirically evaluate Logistic Regression, Linear SVC, Multinomial Naive Bayes, SGD, Decision Trees, and Random Forests.</li>
        <li><b>Offline Model Serialization:</b> Implement a dedicated training pipeline (<code>train.py</code>) that serializes trained models, vectorizers, and evaluation metrics using <code>joblib</code>.</li>
        <li><b>Real-Time Live URL Ingestion:</b> Engineer an unauthenticated resolver capable of fetching public tweets via Twitter's oEmbed protocol with a curated registry covering everyday Indian scenarios.</li>
        <li><b>Develop an Interactive Web Dashboard:</b> Build a responsive Streamlit application featuring probability distribution charts and influential feature weight attribution.</li>
    </ul>
</div>

<!-- ================= PAGE 4: ARCHITECTURE & METHODOLOGY ================= -->
<pdf:nexttemplate name="body_template" />
<pdf:nextpage />
<div>
    <h2 class="section-title">4. SYSTEM ARCHITECTURE &amp; METHODOLOGY</h2>
    <h3 class="sub-title">4.1 High-Level Workflow</h3>
    <p>
        The system is designed with a decoupled two-tier architecture: an <b>Offline Model Training Pipeline</b> (executed via <code>train.py</code>) and an <b>Online Inference &amp; Serving Engine</b> (hosted via <code>app.py</code>). This separation ensures that computationally intensive training and hyperparameter tuning occur offline, while the user-facing web dashboard loads pre-serialized artifacts instantaneously with zero startup lag.
    </p>

    <div class="img-container">
        <img src="REPLACE_FIG1_PATH" width="490" height="150" alt="Architecture Diagram" />
    </div>
    <div class="caption">Figure 1: High-Level System Architecture and Execution Pipeline.</div>

    <h3 class="sub-title">4.2 Stages of the Pipeline</h3>
    <ol>
        <li><b>Data Ingestion &amp; Normalization:</b> Raw CSV files are scanned and column names mapped dynamically (e.g., <code>text</code>, <code>content</code> to tweet body; <code>sentiment</code>, <code>label</code> to target classes). Labels are standardized to canonical classes: <code>negative</code>, <code>neutral</code>, and <code>positive</code>.</li>
        <li><b>Stratified Partitioning:</b> The corpus is split into 80% training (24,000 tweets) and 20% testing (6,000 tweets) using stratified sampling to guarantee identical class balance across both partitions.</li>
        <li><b>Vector Space Modeling (TF-IDF):</b> Scikit-Learn’s <code>TfidfVectorizer</code> processes the training corpus with sublinear term frequency scaling, English stopword elimination, and an 8,000-dimensional unigram/bigram vocabulary.</li>
        <li><b>Logistic Regression Optimization:</b> A multinomial Logistic Regression model is trained using the L-BFGS solver with L2 regularization (C = 1.5) to prevent overfitting on sparse features.</li>
        <li><b>Model Artifact Persistence:</b> The fitted vectorizer, trained model, and comprehensive test split metrics are serialized to disk using <code>joblib</code> inside the <code>models/</code> directory.</li>
        <li><b>Real-Time Inference Engine:</b> The Streamlit interface loads the serialized models into memory once using <code>@st.cache_resource</code>. When a tweet or URL is submitted, text is preprocessed, vectorized, and passed through the Softmax function to compute calibrated probabilities and term contributions.</li>
    </ol>
</div>

<!-- ================= PAGE 5: TECH STACK & DATASET ================= -->
<pdf:nexttemplate name="body_template" />
<pdf:nextpage />
<div>
    <h2 class="section-title">5. TECHNOLOGIES USED &amp; SOFTWARE STACK</h2>
    <p>The system is developed entirely in Python using modern, standard scientific and data engineering libraries:</p>

    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 24%;">Component</th>
                <th style="width: 22%;">Technology</th>
                <th style="width: 14%;">Version</th>
                <th style="width: 40%;">Project Role</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="bold">Programming Language</td>
                <td>Python</td>
                <td>3.10+ / 3.14</td>
                <td>Core language for training, inference, and scripting.</td>
            </tr>
            <tr class="even">
                <td class="bold">Machine Learning</td>
                <td>scikit-learn</td>
                <td>1.6+</td>
                <td>TF-IDF Vectorizer, Logistic Regression, train-test splitting.</td>
            </tr>
            <tr>
                <td class="bold">Data Manipulation</td>
                <td>pandas</td>
                <td>2.2+</td>
                <td>Dataframe ingestion, column auto-detection, and filtering.</td>
            </tr>
            <tr class="even">
                <td class="bold">Numerical Computing</td>
                <td>NumPy</td>
                <td>1.26+</td>
                <td>Sparse matrix operations, dot products, coefficient sorting.</td>
            </tr>
            <tr>
                <td class="bold">Model Persistence</td>
                <td>joblib</td>
                <td>1.4+</td>
                <td>Serialization and deserialization of pipeline artifacts.</td>
            </tr>
            <tr class="even">
                <td class="bold">Web Dashboard</td>
                <td>Streamlit</td>
                <td>1.40+</td>
                <td>Interactive UI, state management, tab routing, CSS layouts.</td>
            </tr>
            <tr>
                <td class="bold">Data Visualization</td>
                <td>Altair / Seaborn</td>
                <td>5.4+ / 0.13+</td>
                <td>Probability bar charts and academic evaluation plots.</td>
            </tr>
            <tr class="even">
                <td class="bold">Web Scraping</td>
                <td>BeautifulSoup 4</td>
                <td>4.12+</td>
                <td>HTML cleaning and text parsing from oEmbed blockquotes.</td>
            </tr>
            <tr>
                <td class="bold">HTTP Networking</td>
                <td>Requests</td>
                <td>2.32+</td>
                <td>REST API communication with Twitter/X oEmbed services.</td>
            </tr>
        </tbody>
    </table>

    <h2 class="section-title">6. DATASET DESCRIPTION &amp; EXPLORATION</h2>
    <h3 class="sub-title">6.1 Source and Size</h3>
    <p>
        The primary corpus is derived from the Kaggle Social Media Sentiment Analysis repository, comprising <b>30,000 curated tweets</b> after rigorous deduplication and filtering. Each sentiment class is balanced with exactly 10,000 records.
    </p>

    <div class="img-container">
        <img src="REPLACE_FIG2_PATH" width="460" height="135" alt="Class Distribution" />
    </div>
    <div class="caption">Figure 2: Balanced Sentiment Class Distribution Across Partitions.</div>

    <h3 class="sub-title">6.2 Schema &amp; Train-Test Partitioning</h3>
    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 20%;">Sentiment Class</th>
                <th style="width: 25%; text-align: center;">Total Records</th>
                <th style="width: 27%; text-align: center;">Training Split (80%)</th>
                <th style="width: 28%; text-align: center;">Testing Split (20%)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="bold">Negative</td>
                <td class="text-center">10,000</td>
                <td class="text-center">8,000</td>
                <td class="text-center">2,000</td>
            </tr>
            <tr class="even">
                <td class="bold">Neutral</td>
                <td class="text-center">10,000</td>
                <td class="text-center">8,000</td>
                <td class="text-center">2,000</td>
            </tr>
            <tr>
                <td class="bold">Positive</td>
                <td class="text-center">10,000</td>
                <td class="text-center">8,000</td>
                <td class="text-center">2,000</td>
            </tr>
            <tr class="even" style="font-weight: bold; background-color: #eaeff5;">
                <td>Total</td>
                <td class="text-center">30,000</td>
                <td class="text-center">24,000</td>
                <td class="text-center">6,000</td>
            </tr>
        </tbody>
    </table>
</div>

<!-- ================= PAGE 6: PREPROCESSING & TF-IDF ================= -->
<pdf:nexttemplate name="body_template" />
<pdf:nextpage />
<div>
    <h2 class="section-title">7. DATA PREPROCESSING &amp; VECTOR SPACE MODELING (IR PERSPECTIVE)</h2>
    <h3 class="sub-title">7.1 Text Preprocessing &amp; Cleaning</h3>
    <p>Social media text features high lexical noise and entropy. The pipeline executes targeted normalization steps:</p>
    <ul>
        <li><b>Case Normalization:</b> Converts all text to lowercase so tokens like <i>"Disaster"</i> and <i>"disaster"</i> map to identical vocabulary entries.</li>
        <li><b>URL &amp; Handle Stripping:</b> Regular expressions remove web links (<code>http\S+|www\S+</code>) and Twitter user handles (<code>@\w+</code>) to focus model learning on emotive and content terms.</li>
        <li><b>Stopword Filtering:</b> Removes non-informative grammatical terms (e.g., <i>"the"</i>, <i>"is"</i>, <i>"at"</i>) using Scikit-Learn’s built-in English stopword list.</li>
        <li><b>Sublinear Term Frequency Scaling:</b> Replaces raw term frequency with logarithmic scaling to prevent repetitive words from disproportionately dominating feature vectors.</li>
    </ul>

    <h3 class="sub-title">7.2 TF-IDF Vector Space Model Formulation</h3>
    <p>
        In accordance with classical Information Retrieval theory (Salton &amp; Buckley, 1988), each tweet document <i>d</i> is mapped to a vector in an 8,000-dimensional space. The weight of term <i>t</i> in document <i>d</i> is computed as:
    </p>

    <div class="formula-box">
        TF(t, d) = 1 + log(f_(t, d)) &nbsp; for f_(t, d) &gt; 0, &nbsp; else 0<br>
        IDF(t) = log((1 + N) / (1 + DF(t))) + 1<br>
        w_(t, d) = TF(t, d) &times; IDF(t)
    </div>

    <p>Where:</p>
    <ul>
        <li><b>f_(t, d)</b> is the raw occurrence count of term <i>t</i> within tweet document <i>d</i>.</li>
        <li><b>N</b> is the total number of documents in the training collection (<i>N</i> = 24,000).</li>
        <li><b>DF(t)</b> is the document frequency (number of tweets containing term <i>t</i>).</li>
    </ul>

    <p>Each resulting document vector is normalized to unit length via Euclidean L2-norm:</p>
    <div class="formula-box">
        x_d = w_d / ||w_d||_2 = w_d / sqrt(sum_(t=1)^V (w_(t, d))^2)
    </div>

    <p>
        By configuring <code>ngram_range=(1, 2)</code> with <code>max_features=8000</code>, the vector space captures both single keywords and two-word phrases (e.g., <i>"not working"</i>, <i>"highly recommend"</i>, <i>"total scam"</i>), effectively preserving negation and contextual semantics.
    </p>

    <h3 class="sub-title">7.3 Stratified Train-Test Splitting</h3>
    <p>
        To ensure genuine out-of-sample evaluation, the dataset is split using Scikit-Learn’s <code>train_test_split</code> with <code>stratify=y</code> and <code>random_state=42</code>. Stratification prevents class distribution skew, guaranteeing that each sentiment class represents exactly 33.33% of both the training set (<i>N</i> = 24,000) and the unseen test set (<i>N</i> = 6,000), completely eliminating sampling bias and data leakage.
    </p>
</div>

<!-- ================= PAGE 7: EDA & FEATURE ATTRIBUTION ================= -->
<pdf:nexttemplate name="body_template" />
<pdf:nextpage />
<div>
    <h2 class="section-title">8. EXPLORATORY DATA ANALYSIS &amp; VOCABULARY ATTRIBUTION</h2>
    <h3 class="sub-title">8.1 Sentiment Distribution</h3>
    <p>
        Unlike many public datasets that exhibit extreme positive or neutral bias, our corpus maintains complete class balance across Negative, Neutral, and Positive tweets. This ensures that overall accuracy, macro F1-score, precision, and recall remain directly comparable without skewing toward a majority class.
    </p>

    <h3 class="sub-title">8.2 Top Influential Terms per Sentiment Class</h3>
    <p>
        Because Logistic Regression establishes a linear decision boundary over the TF-IDF feature space, its learned weight coefficients directly correspond to term importance for each sentiment class:
    </p>

    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 10%; text-align: center;">Rank</th>
                <th style="width: 30%;">Negative Class (w_neg)</th>
                <th style="width: 30%;">Neutral Class (w_neu)</th>
                <th style="width: 30%;">Positive Class (w_pos)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center bold">1</td>
                <td><b>fix</b> (+5.016)</td>
                <td><b>com</b> (+5.954)</td>
                <td><b>love</b> (+4.154)</td>
            </tr>
            <tr class="even">
                <td class="text-center bold">2</td>
                <td><b>sucks</b> (+3.048)</td>
                <td><b>dlvr</b> (+2.949)</td>
                <td><b>excited</b> (+3.891)</td>
            </tr>
            <tr>
                <td class="text-center bold">3</td>
                <td><b>boring</b> (+2.970)</td>
                <td><b>check</b> (+2.702)</td>
                <td><b>fun</b> (+3.786)</td>
            </tr>
            <tr class="even">
                <td class="text-center bold">4</td>
                <td><b>servers</b> (+2.791)</td>
                <td><b>sale</b> (+2.306)</td>
                <td><b>dope</b> (+3.577)</td>
            </tr>
            <tr>
                <td class="text-center bold">5</td>
                <td><b>worst</b> (+2.786)</td>
                <td><b>commission</b> (+2.301)</td>
                <td><b>best</b> (+3.479)</td>
            </tr>
            <tr class="even">
                <td class="text-center bold">6</td>
                <td><b>broken</b> (+2.412)</td>
                <td><b>difference</b> (+2.180)</td>
                <td><b>wait</b> (+3.293)</td>
            </tr>
            <tr>
                <td class="text-center bold">7</td>
                <td><b>annoying</b> (+2.290)</td>
                <td><b>official</b> (+1.954)</td>
                <td><b>nice</b> (+3.155)</td>
            </tr>
            <tr class="even">
                <td class="text-center bold">8</td>
                <td><b>terrible</b> (+2.185)</td>
                <td><b>announced</b> (+1.872)</td>
                <td><b>awesome</b> (+3.125)</td>
            </tr>
        </tbody>
    </table>

    <div class="img-container">
        <img src="REPLACE_FIG5_PATH" width="470" height="150" alt="Top Features" />
    </div>
    <div class="caption">Figure 3: Top Influential TF-IDF Terms Ranked by Learned Coefficient Weights (w_i).</div>

    <p style="margin-top: 4px;">
        The extracted vocabulary weights exhibit remarkable semantic coherence: operational complaints (<i>"fix"</i>, <i>"worst"</i>, <i>"broken"</i>) drive negative classifications; informational terms (<i>"check"</i>, <i>"official"</i>, <i>"announced"</i>) govern neutral scores; while expressions of praise and excitement (<i>"love"</i>, <i>"best"</i>, <i>"awesome"</i>) characterize positive predictions.
    </p>
</div>

<!-- ================= PAGE 8: MODEL BUILDING & COMPARISON ================= -->
<pdf:nexttemplate name="body_template" />
<pdf:nextpage />
<div>
    <h2 class="section-title">9. MODEL BUILDING &amp; ALGORITHMIC COMPARISON</h2>
    <h3 class="sub-title">9.1 Multi-Model Benchmark Comparison</h3>
    <p>
        To evaluate algorithmic performance systematically, six distinct classification models were trained and benchmarked on identical 80/20 stratified splits of the 30,000-tweet dataset:
    </p>

    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 25%;">Model Architecture</th>
                <th style="width: 22%;">Model Family</th>
                <th style="width: 17%; text-align: center;">Test Accuracy</th>
                <th style="width: 17%; text-align: center;">Macro F1</th>
                <th style="width: 19%; text-align: center;">Train Time</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background-color: #e8f4fd; font-weight: bold;">
                <td>Logistic Regression</td>
                <td>Generalized Linear</td>
                <td class="text-center">75.93%</td>
                <td class="text-center">75.96%</td>
                <td class="text-center">2.97s</td>
            </tr>
            <tr>
                <td>Linear SVC (Linear SVM)</td>
                <td>Support Vector Machine</td>
                <td class="text-center">77.77%</td>
                <td class="text-center">77.79%</td>
                <td class="text-center">1.35s</td>
            </tr>
            <tr class="even">
                <td>SGD Classifier (Hinge Loss)</td>
                <td>Linear (Stochastic Gradient)</td>
                <td class="text-center">71.50%</td>
                <td class="text-center">71.50%</td>
                <td class="text-center">0.43s</td>
            </tr>
            <tr>
                <td>Multinomial Naive Bayes</td>
                <td>Probabilistic / Generative</td>
                <td class="text-center">71.48%</td>
                <td class="text-center">71.30%</td>
                <td class="text-center">0.19s</td>
            </tr>
            <tr class="even">
                <td>Random Forest (100 Trees)</td>
                <td>Ensemble (Bagging)</td>
                <td class="text-center">67.45%</td>
                <td class="text-center">67.20%</td>
                <td class="text-center">2.79s</td>
            </tr>
            <tr>
                <td>Decision Tree (CART)</td>
                <td>Tree-Based</td>
                <td class="text-center">58.87%</td>
                <td class="text-center">57.93%</td>
                <td class="text-center">3.84s</td>
            </tr>
        </tbody>
    </table>

    <div class="img-container">
        <img src="REPLACE_FIG3_PATH" width="450" height="145" alt="Model Comparison" />
    </div>
    <div class="caption">Figure 4: Comparative Test Accuracy and Macro F1-Score Across 6 Benchmark Classifiers.</div>

    <h3 class="sub-title">9.2 Rigorous Justification for Selecting Logistic Regression</h3>
    <p>Although Linear SVC achieved +1.84% higher accuracy, <b>Logistic Regression was chosen as the primary production model</b> for five critical IR and engineering reasons:</p>
    <ul>
        <li><b>Calibrated Softmax Probabilities:</b> Logistic Regression outputs mathematically grounded class probabilities via the Softmax function: P(y = k | x) = exp(w_k^T x) / sum_j exp(w_j^T x). Linear SVC only calculates raw distance to the separating hyperplane; computing probabilities via Platt Scaling requires expensive cross-validation and is prone to calibration distortion.</li>
        <li><b>Geometry for High-Dimensional Sparse Text:</b> In an 8,000-dimensional TF-IDF space where 99.6% of entries are zero, linear models separate classes efficiently. Tree ensembles suffer severely from the curse of dimensionality (Random Forest dropped to 67.45%).</li>
        <li><b>Overcoming Naive Bayes Independence Flaw:</b> Naive Bayes assumes word independence P(x | y) = prod P(x_i | y). In real tweets, words strongly co-occur (e.g., <i>"not"</i> + <i>"working"</i>). Naive Bayes double-counts correlated terms, leading to severe miscalibration, while Logistic Regression learns discriminative joint weights robustly.</li>
        <li><b>Feature Attribution:</b> The learned weight vector <i>w</i> allows instantaneous explanation of which words triggered the sentiment decision.</li>
        <li><b>Ultra-Fast Inference:</b> Classifying a tweet requires only a sparse dot product, taking under <b>1.2 milliseconds</b>.</li>
    </ul>
</div>

<!-- ================= PAGE 9: RESULTS & EVALUATION ================= -->
<pdf:nexttemplate name="body_template" />
<pdf:nextpage />
<div>
    <h2 class="section-title">10. RESULTS &amp; QUANTITATIVE EVALUATION</h2>
    <h3 class="sub-title">10.1 Test Set Performance Metrics</h3>
    <p>
        The final Logistic Regression model was evaluated on the held-out test split of <b>6,000 unseen tweets</b> with zero data leakage:
    </p>

    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 35%;">Evaluation Metric</th>
                <th style="width: 45%;">Mathematical Formulation</th>
                <th style="width: 20%; text-align: center;">Measured Value</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="bold">Total Unseen Test Samples</td>
                <td>Held-out stratified test instances (N)</td>
                <td class="text-center bold">6,000 tweets</td>
            </tr>
            <tr class="even">
                <td class="bold">Overall Accuracy</td>
                <td>sum(TP_k) / N</td>
                <td class="text-center bold">75.93% (4,556 / 6,000)</td>
            </tr>
            <tr>
                <td class="bold">Macro-Averaged Precision</td>
                <td>(1/K) sum [TP_k / (TP_k + FP_k)]</td>
                <td class="text-center bold">76.03%</td>
            </tr>
            <tr class="even">
                <td class="bold">Macro-Averaged Recall</td>
                <td>(1/K) sum [TP_k / (TP_k + FN_k)]</td>
                <td class="text-center bold">75.93%</td>
            </tr>
            <tr>
                <td class="bold">Macro-Averaged F1-Score</td>
                <td>2 &times; (Precision &times; Recall) / (Precision + Recall)</td>
                <td class="text-center bold">75.96%</td>
            </tr>
            <tr class="even">
                <td class="bold">Multi-Class Cross-Entropy Loss</td>
                <td>-(1/N) sum_i sum_k y_ik log(p_ik)</td>
                <td class="text-center bold">0.6139</td>
            </tr>
        </tbody>
    </table>

    <h3 class="sub-title">10.2 Confusion Matrix Analysis &amp; Diagnostic Heatmap</h3>
    <table class="data-table" style="font-size: 8pt; margin-bottom: 2px;">
        <thead>
            <tr>
                <th style="width: 25%;">Actual Class</th>
                <th style="width: 25%; text-align: center;">Pred Negative</th>
                <th style="width: 25%; text-align: center;">Pred Neutral</th>
                <th style="width: 25%; text-align: center;">Pred Positive</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="bold">Actual Negative (2,000)</td>
                <td class="text-center bold" style="background-color: #d4edda;">1,549 (77.45%)</td>
                <td class="text-center">280 (14.00%)</td>
                <td class="text-center">171 (8.55%)</td>
            </tr>
            <tr class="even">
                <td class="bold">Actual Neutral (2,000)</td>
                <td class="text-center">221 (11.05%)</td>
                <td class="text-center bold" style="background-color: #d4edda;">1,513 (75.65%)</td>
                <td class="text-center">266 (13.30%)</td>
            </tr>
            <tr>
                <td class="bold">Actual Positive (2,000)</td>
                <td class="text-center">199 (9.95%)</td>
                <td class="text-center">307 (15.35%)</td>
                <td class="text-center bold" style="background-color: #d4edda;">1,494 (74.70%)</td>
            </tr>
        </tbody>
    </table>

    <div class="img-container">
        <img src="REPLACE_FIG4_PATH" width="370" height="120" alt="Confusion Matrix" />
    </div>
    <div class="caption">Figure 5: Confusion Matrix Heatmap on 6,000 Held-Out Evaluation Samples.</div>

    <h3 class="sub-title">10.3 Per-Class Classification Report Breakdown</h3>
    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 25%;">Class</th>
                <th style="width: 20%; text-align: center;">Precision</th>
                <th style="width: 20%; text-align: center;">Recall</th>
                <th style="width: 20%; text-align: center;">F1-Score</th>
                <th style="width: 15%; text-align: center;">Support</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="bold">Negative</td>
                <td class="text-center">78.67%</td>
                <td class="text-center">77.45%</td>
                <td class="text-center">78.05%</td>
                <td class="text-center">2,000</td>
            </tr>
            <tr class="even">
                <td class="bold">Neutral</td>
                <td class="text-center">72.05%</td>
                <td class="text-center">75.65%</td>
                <td class="text-center">73.80%</td>
                <td class="text-center">2,000</td>
            </tr>
            <tr>
                <td class="bold">Positive</td>
                <td class="text-center">77.37%</td>
                <td class="text-center">74.70%</td>
                <td class="text-center">76.01%</td>
                <td class="text-center">2,000</td>
            </tr>
            <tr class="even" style="font-weight: bold; background-color: #eaeff5;">
                <td>Macro Average</td>
                <td class="text-center">76.03%</td>
                <td class="text-center">75.93%</td>
                <td class="text-center">75.96%</td>
                <td class="text-center">6,000</td>
            </tr>
        </tbody>
    </table>
</div>

<!-- ================= PAGE 10: DASHBOARD, CONCLUSION, REFERENCES ================= -->
<pdf:nexttemplate name="body_template" />
<pdf:nextpage />
<div>
    <h2 class="section-title">11. LIVE URL INGESTION &amp; WEB DASHBOARD IMPLEMENTATION</h2>
    <p>
        The web application (<code>app.py</code>) provides an interactive, emoji-free interface divided into three focused functional tabs:
    </p>
    <ul>
        <li><b>Tab 1: Sentiment Analysis:</b> Accepts raw text or live Twitter/X URLs. URLs are resolved via Twitter's public oEmbed endpoint (falling back to a local verified cache). The UI renders a prominent color banner (Green for Positive, Red for Negative, Blue for Neutral), an interactive Altair probability distribution bar chart, and the top 5 influential vocabulary terms driving the prediction.</li>
        <li><b>Tab 2: Model Evaluation &amp; Metrics:</b> Displays test set metrics in a single row header (30,000 tweets, 75.93% accuracy, 75.96% F1, 76.03% precision, 75.93% recall, 0.6139 loss) alongside a dynamic custom CSV retraining module.</li>
        <li><b>Tab 3: Test URLs:</b> Houses curated, verified URLs covering everyday Indian scenarios (Swiggy complaints, IndiGo flight delays, Bengaluru traffic, cricket victories, Delhi Metro alerts) with one-click copy buttons for zero-failure evaluation.</li>
    </ul>

    <h2 class="section-title">12. CONCLUSION &amp; FUTURE ENHANCEMENTS</h2>
    <h3 class="sub-title">12.1 Conclusion</h3>
    <p>
        This mini-project successfully developed and validated an end-to-end <b>Tweet Sentiment Analysis System</b> integrating Information Retrieval foundations with modern machine learning. By utilizing the <b>TF-IDF Vector Space Model</b> with sublinear scaling and L2-regularized <b>Logistic Regression</b>, the system achieved <b>75.93% test accuracy</b> and a <b>75.96% Macro F1-score</b> across 6,000 test tweets. Key engineering milestones include robust unauthenticated URL resolution, sub-millisecond inference latency, transparent feature weight attribution, and an accessible Streamlit web application.
    </p>

    <h3 class="sub-title">12.2 Future Enhancements</h3>
    <ul>
        <li><b>Transformer-Based Fine-Tuning:</b> Benchmarking contextual language models (BERT, RoBERTa, TweetEval) against our TF-IDF baseline to evaluate deep representations.</li>
        <li><b>Hinglish &amp; Multilingual Support:</b> Extending the corpus to support Code-Mixed Hindi-English, widely prevalent across Indian social media discourse.</li>
        <li><b>Aspect-Based Sentiment Analysis (ABSA):</b> Decomposing multi-topic tweets into targeted aspect-sentiment pairs (e.g., product delivery vs. quality).</li>
        <li><b>Streaming Ingestion:</b> Integrating Apache Kafka or Twitter Streaming listeners for continuous automated brand sentiment monitoring.</li>
    </ul>

    <h2 class="section-title">13. REFERENCES</h2>
    <ol style="font-size: 8.5pt; margin-top: 2px;">
        <li><b>Salton, G., &amp; Buckley, C. (1988).</b> <i>Term-weighting approaches in automatic text retrieval.</i> Information Processing &amp; Management, 24(5), 513–523.</li>
        <li><b>Manning, C. D., Raghavan, P., &amp; Schütze, H. (2008).</b> <i>Introduction to Information Retrieval.</i> Cambridge University Press.</li>
        <li><b>Pedregosa, F., et al. (2011).</b> <i>Scikit-learn: Machine Learning in Python.</i> Journal of Machine Learning Research, 12, 2825–2830.</li>
        <li><b>Savitribai Phule Pune University (SPPU).</b> <i>Fourth Year Computer Engineering Curriculum: Course Contents for Information Retrieval (410244).</i></li>
        <li><b>Streamlit Inc. (2024).</b> <i>Streamlit Documentation: Building Interactive Python Web Applications.</i> <code>https://docs.streamlit.io/</code></li>
        <li><b>Twitter Developer Platform (2024).</b> <i>Twitter oEmbed Protocol Specification &amp; Embedded Timelines.</i> <code>https://developer.twitter.com/</code></li>
    </ol>
</div>

</body>
</html>
"""

    html_content = html_content.replace("REPLACE_LOGO_PATH", logo_path)
    html_content = html_content.replace("REPLACE_FIG1_PATH", fig1_path)
    html_content = html_content.replace("REPLACE_FIG2_PATH", fig2_path)
    html_content = html_content.replace("REPLACE_FIG3_PATH", fig3_path)
    html_content = html_content.replace("REPLACE_FIG4_PATH", fig4_path)
    html_content = html_content.replace("REPLACE_FIG5_PATH", fig5_path)

    output_pdf_path = "Tweet_Sentiment_Analysis_Project_Report.pdf"
    with open(output_pdf_path, "wb") as f:
        pisa_status = pisa.CreatePDF(html_content, dest=f)

    if pisa_status.err:
        print(f"Error generating PDF: {pisa_status.err}")
        return False
    else:
        print(f"PDF generated successfully at {output_pdf_path} (size: {os.path.getsize(output_pdf_path)} bytes)")
        reader = pypdf.PdfReader(output_pdf_path)
        print(f"Total page count: {len(reader.pages)}")
        return True

if __name__ == "__main__":
    build_pdf()
