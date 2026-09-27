<div align="center">

# 🌐 Data Vortex A'26

### Rebuilding the Social Engine

> **From raw social-media data to social signals and insights.**
**From Raw Social Data → Machine Learning → NLP → Social Signals**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![SQL](https://img.shields.io/badge/SQL-SQLite-blue?logo=sqlite)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQL](https://img.shields.io/badge/SQL-SQLite-blue)
![NLP](https://img.shields.io/badge/NLP-DistilBERT-orange)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange)
![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-green)

---
### Team `soumadipd43`

## 👥 Team
**Soumadip Das** · IT · Team Head &nbsp; | &nbsp; **Aritra Pal** · CSE — AI & ML

**Team soumadipd43** · Haldia Institute Of Technology
**Haldia Institute Of Technology**

**Soumadip Das** — Team Head  
**Aritra Pal** — CSE, AI & ML
</div>

---

## 🚀 About the Project

**Data Vortex A'26** was a multi-round data science and AI challenge by **Aaruush** built around the theme **"Rebuilding the Social Engine."**

Across three rounds, we moved from structured social-media data and SQL analysis to machine learning, NLP, and finally independently collected public social-media data.
Across three rounds, we moved from structured social-media data and SQL analysis to NLP modelling and finally to independently collected public social-media data.

### Our Journey

**📊 Data & SQL → 🤖 Machine Learning & NLP → 🌐 Real-World Social Signals**
| Round | Focus | What We Built |
|:---:|---|---|
| **01** | 📊 Data + SQL | Engagement, location & user-behaviour analysis |
| **02** | 🤖 ML + NLP | Sentiment & topic classification |
| **03** | 🌐 Social Signals | Sentiment shifts, engagement spikes & topic analysis |

---

# 📊 Round 1 — Data & SQL

### The Challenge

We analysed structured social-media data using **SQL and Python** to uncover engagement patterns and unusual user behaviour.
Analyse structured social-media data and uncover engagement patterns using SQL.

### What we analysed
### What We Analysed

- **Platform Engagement** — average likes, shares, comments and total engagement
- **Location Engagement** — locations generating the highest engagement
- **High-Impact Users** — users showing unusually high engagement relative to follower count
- **E3** — Platform engagement
- **M1** — Location-based engagement
- **H6** — Suspicious high-impact users

**Tech:** `Python` `Pandas` `SQLite` `SQL`
### Platform Engagement

![Platform Engagement](sql/outputs/E3_output.jpeg)

**Stack:** `Python` `Pandas` `SQLite` `SQL`

---

# 🤖 Round 2 — NLP & Machine Learning

Round 2 moved from analysing numbers to understanding **what people were actually saying**.
### The Challenge

We built NLP pipelines for:
Build NLP models capable of understanding the **sentiment and topic** of social-media posts.

- Sentiment Classification
- Topic Classification
- Text Preprocessing
- Feature Engineering
- Model Evaluation
- Error Analysis
We experimented with:

### Sentiment Model
`Logistic Regression` · `SVM` · `Naive Bayes` · `TF-IDF` · `DistilBERT`

After experimenting with Logistic Regression, SVM, Naive Bayes and TF-IDF approaches, we trained a **DistilBERT** sentiment classifier.
### Results

| Metric | Result |
| :--- | ---: |
| Accuracy | **68.33%** |
| Macro F1 | **67.81%** |
| Weighted F1 | **67.77%** |
| Task | Model | Accuracy | Macro F1 |
|---|---|---:|---:|
| Sentiment | DistilBERT | **68.33%** | **67.81%** |
| Topic | TF-IDF + Logistic Regression | **93.52%** | **65.52%** |

**Classes:** `Negative` · `Neutral` · `Positive`
### Sentiment Classes

### Topic Model
`Negative` · `Neutral` · `Positive`

Our final topic classifier combined **word + character TF-IDF** features with Logistic Regression.
### Model Evaluation

| Metric | Result |
| :--- | ---: |
| Accuracy | **93.52%** |
| Macro F1 | **65.52%** |
| Weighted F1 | **92.30%** |
![Sentiment Confusion Matrix](round2/outputs/transformer_sentiment/confusion_matrix.png)

---

# 🌐 Round 3 — Real-World Social Signals

For Round 3, we moved outside the provided datasets.
### The Challenge

We independently collected **public YouTube comments** around a platform monetisation change and applied our Round 2 NLP model to the discussion.
Take our NLP pipeline beyond a prepared dataset and apply it to **independently collected public social-media data**.

We collected public YouTube comments around a platform monetisation change using the **YouTube Data API v3**.

### Pipeline

**YouTube API → Collection → Filtering → NLP → Time Analysis → Social Signals**

We analysed:

- 💬 Sentiment
- 📈 Sentiment shifts over time
- 🔥 Engagement spikes
- 🏷️ Topics
- 🔎 Entities
- ⚡ Possible discussion triggers

### Final Dataset

| Metric | Result |
| :--- | ---: |
| Comments | **40** |
| Videos | **12** |
| Duplicate Comments | **0** |
| Negative | **7** |
| Neutral | **26** |
| Positive | **7** |
| Engagement Spikes | **2** |

**Analysis period:** 5 August 2026 – 10 September 2026
| Comments | Videos | Duplicates | Engagement Spikes |
|:---:|:---:|:---:|:---:|
| **40** | **12** | **0** | **2** |

---
### Sentiment Distribution

## 🔥 Engagement Analysis
| Negative | Neutral | Positive |
|:---:|:---:|:---:|
| 🔴 **7** | ⚪ **26** | 🟢 **7** |

Comment engagement was calculated as:
### Sentiment Over Time

**Engagement = Likes + Replies**
![Sentiment Timeline](round4/outputs/round3_sentiment_timeline.png)

| Metric | Value |
| :--- | ---: |
| Mean Engagement | **2.35** |
| Median Engagement | **1.50** |
| Spike Threshold | **8.32** |
| Highest Engagement | **15** |
| Second Highest | **10** |
### Engagement Spikes

Two comments crossed the engagement-spike threshold.
![Engagement Spikes](round4/outputs/round3_engagement_spikes.png)

---

## 🏷️ Discussion Topics
## 🏷️ What People Were Discussing

| Topic | Share |
| :--- | ---: |
|---|---:|
| Eligibility & Access | **27.5%** |
| Original Content & Reposts | **25.0%** |
| Monetisation Rules | **15.0%** |
@@ -151,24 +133,47 @@ Two comments crossed the engagement-spike threshold.

## 🛠️ Tech Stack

`Python` · `SQL` · `Pandas` · `NumPy` · `SQLite` · `Scikit-learn` · `TF-IDF` · `DistilBERT` · `Hugging Face Transformers` · `YouTube Data API` · `Git` · `GitHub`
<div align="center">

**Python · SQL · Pandas · NumPy · SQLite · Scikit-learn · TF-IDF · DistilBERT · Hugging Face · YouTube Data API · Git · GitHub**

</div>

---

## 📁 Project Structure

```text
Data-Vortex/
├── sql/                  # Round 1 SQL analysis
├── round2/               # NLP & ML pipeline
│   ├── models/
│   ├── outputs/
│   └── reports/
├── round3/               # Real-world social analysis
│   ├── scripts/
│   ├── notebooks/
│   ├── outputs/
│   └── reports/
├── round4/               # Round 4 preparation
├── .env.example
└── README.md
```

## 💡 What We Learned

> **Real-world data rarely behaves like a clean benchmark dataset.**

Working through Data Vortex meant dealing with noisy data, class imbalance, irrelevant search results, model uncertainty and small samples.

The biggest lesson wasn't simply how to train another model — it was learning to **question what the data actually supports before trusting the result.**

<div align="center">

### Raw Data → SQL → ML → NLP → Social Signals → Insights

</div>

---

## 👥 Team

| | |
|---|---|
| **Aritra Pal** | CSE — Artificial Intelligence & Machine Learning |
| **Soumadip Das** | IT — Information Technology \| Team Head |
| **Institute** | Haldia Institute Of Technology |
| **Team** | `soumadipd43` |

---

<div align="center">

### 🌐 Data Vortex A'26

**Rebuilding the Social Engine**

*No trophy this time. But definitely a lot of progress. *

</div>
