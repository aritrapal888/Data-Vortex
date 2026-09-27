# 🌐 Data Vortex A'26

### Rebuilding the Social Engine

> **From raw social-media data to social signals and insights.**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![SQL](https://img.shields.io/badge/SQL-SQLite-blue?logo=sqlite)
![NLP](https://img.shields.io/badge/NLP-DistilBERT-orange)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange)

---

## 👥 Team

**Team soumadipd43** · Haldia Institute Of Technology

**Soumadip Das** — Team Head  
**Aritra Pal** — CSE, AI & ML

---

## 💡 About the Project

**Data Vortex A'26** was a multi-round data science and AI challenge by **Aaruush** built around the theme **"Rebuilding the Social Engine."**

Across three rounds, we moved from structured social-media data and SQL analysis to machine learning, NLP, and finally independently collected public social-media data.

### Our Journey

**📊 Data & SQL → 🤖 Machine Learning & NLP → 🌐 Real-World Social Signals**

---

## 📊 Round 1 — Data & SQL

We analysed structured social-media data using **SQL and Python** to uncover engagement patterns and unusual user behaviour.

### What we analysed

- **Platform Engagement** — average likes, shares, comments and total engagement
- **Location Engagement** — locations generating the highest engagement
- **High-Impact Users** — users showing unusually high engagement relative to follower count

**Tech:** `Python` `Pandas` `SQLite` `SQL`

---

## 🤖 Round 2 — Machine Learning & NLP

Round 2 moved from analysing numbers to understanding **what people were actually saying**.

We built NLP pipelines for:

- Sentiment Classification
- Topic Classification
- Text Preprocessing
- Feature Engineering
- Model Evaluation
- Error Analysis

### Sentiment Model

After experimenting with Logistic Regression, SVM, Naive Bayes and TF-IDF approaches, we trained a **DistilBERT** sentiment classifier.

| Metric | Result |
| :--- | ---: |
| Accuracy | **68.33%** |
| Macro F1 | **67.81%** |
| Weighted F1 | **67.77%** |

**Classes:** `Negative` · `Neutral` · `Positive`

### Topic Model

Our final topic classifier combined **word + character TF-IDF** features with Logistic Regression.

| Metric | Result |
| :--- | ---: |
| Accuracy | **93.52%** |
| Macro F1 | **65.52%** |
| Weighted F1 | **92.30%** |

---

## 🌐 Round 3 — Real-World Social Signals

For Round 3, we moved outside the provided datasets.

We independently collected **public YouTube comments** around a platform monetisation change and applied our Round 2 NLP model to the discussion.

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

---

## 🔥 Engagement Analysis

Comment engagement was calculated as:

**Engagement = Likes + Replies**

| Metric | Value |
| :--- | ---: |
| Mean Engagement | **2.35** |
| Median Engagement | **1.50** |
| Spike Threshold | **8.32** |
| Highest Engagement | **15** |
| Second Highest | **10** |

Two comments crossed the engagement-spike threshold.

---

## 🏷️ Discussion Topics

| Topic | Share |
| :--- | ---: |
| Eligibility & Access | **27.5%** |
| Original Content & Reposts | **25.0%** |
| Monetisation Rules | **15.0%** |
| Payouts & Earnings | **12.5%** |
| Impressions & Reach | **12.5%** |
| Small Creators | **10.0%** |

---

## 🛠️ Tech Stack

`Python` · `SQL` · `Pandas` · `NumPy` · `SQLite` · `Scikit-learn` · `TF-IDF` · `DistilBERT` · `Hugging Face Transformers` · `YouTube Data API` · `Git` · `GitHub`

---

## 📁 Project Structure

```text
Data-Vortex/
├── sql/                 # Round 1 SQL analysis
├── round2/              # NLP & ML pipeline
│   ├── models/
│   ├── outputs/
│   └── reports/
├── round3/              # Real-world social analysis
│   ├── scripts/
│   ├── notebooks/
│   ├── outputs/
│   └── reports/
├── round4/              # Round 4 preparation
├── .env.example
└── README.md
