<div align="center">

# 🌐 Data Vortex A'26

### Rebuilding the Social Engine

**From Raw Social Data → Machine Learning → NLP → Social Signals**

![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQL](https://img.shields.io/badge/SQL-SQLite-blue)
![NLP](https://img.shields.io/badge/NLP-DistilBERT-orange)
![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-green)

### Team `soumadipd43`

**Soumadip Das** · Team Head &nbsp; | &nbsp; **Aritra Pal** · CSE — AI & ML

**Haldia Institute Of Technology**

</div>

---

## 🚀 About the Project

**Data Vortex A'26** was a multi-round data science and AI challenge by **Aaruush** built around the theme **"Rebuilding the Social Engine."**

Across three rounds, we moved from structured social-media data and SQL analysis to NLP modelling and finally to independently collected public social-media data.

### Our Journey

| Round | Focus | What We Built |
|:---:|---|---|
| **01** | 📊 Data + SQL | Engagement, location & user-behaviour analysis |
| **02** | 🤖 ML + NLP | Sentiment & topic classification |
| **03** | 🌐 Social Signals | Sentiment shifts, engagement spikes & topic analysis |

---

# 📊 Round 1 — Data & SQL

### The Challenge

Analyse structured social-media data and uncover engagement patterns using SQL.

### What We Analysed

- **E3** — Platform engagement
- **M1** — Location-based engagement
- **H6** — Suspicious high-impact users

### Platform Engagement

![Platform Engagement](sql/outputs/E3_output.jpeg)

**Stack:** `Python` `Pandas` `SQLite` `SQL`

---

# 🤖 Round 2 — NLP & Machine Learning

### The Challenge

Build NLP models capable of understanding the **sentiment and topic** of social-media posts.

We experimented with:

`Logistic Regression` · `SVM` · `Naive Bayes` · `TF-IDF` · `DistilBERT`

### Results

| Task | Model | Accuracy | Macro F1 |
|---|---|---:|---:|
| Sentiment | DistilBERT | **68.33%** | **67.81%** |
| Topic | TF-IDF + Logistic Regression | **93.52%** | **65.52%** |

### Sentiment Classes

`Negative` · `Neutral` · `Positive`

### Model Evaluation

![Sentiment Confusion Matrix](round2/outputs/transformer_sentiment/confusion_matrix.png)

---

# 🌐 Round 3 — Real-World Social Signals

### The Challenge

Take our NLP pipeline beyond a prepared dataset and apply it to **independently collected public social-media data**.

We collected public YouTube comments around a platform monetisation change using the **YouTube Data API v3**.

### Pipeline

**YouTube API → Collection → Filtering → NLP → Time Analysis → Social Signals**

### Final Dataset

| Comments | Videos | Duplicates | Engagement Spikes |
|:---:|:---:|:---:|:---:|
| **40** | **12** | **0** | **2** |

### Sentiment Distribution

| Negative | Neutral | Positive |
|:---:|:---:|:---:|
| 🔴 **7** | ⚪ **26** | 🟢 **7** |

### Sentiment Over Time

![Sentiment Timeline](round4/outputs/round3_sentiment_timeline.png)

### Engagement Spikes

![Engagement Spikes](round4/outputs/round3_engagement_spikes.png)

---

## 🏷️ What People Were Discussing

| Topic | Share |
|---|---:|
| Eligibility & Access | **27.5%** |
| Original Content & Reposts | **25.0%** |
| Monetisation Rules | **15.0%** |
| Payouts & Earnings | **12.5%** |
| Impressions & Reach | **12.5%** |
| Small Creators | **10.0%** |

---

## 🛠️ Tech Stack

<div align="center">

**Python · SQL · Pandas · NumPy · SQLite · Scikit-learn · TF-IDF · DistilBERT · Hugging Face · YouTube Data API · Git · GitHub**

</div>

---

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
| **Soumadip Das** | Team Head |
| **Institute** | Haldia Institute Of Technology |
| **Team** | `soumadipd43` |

---

<div align="center">

### 🌐 Data Vortex A'26

**Rebuilding the Social Engine**

*No trophy this time. But definitely a lot of progress. 🚀*

</div>
