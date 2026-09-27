# Data Vortex A'26 — Rebuilding the Social Engine

**Team:** soumadipd43 ||
**Team Head:** Soumadip Das ||
**Team Member:** Aritra Pal ||
**Institute:** Haldia Institute Of Technology

Data Vortex A'26 was a multi-round data and AI challenge built around the theme "Rebuilding the Social Engine".

Our work progressed from structured social-media analysis and SQL to NLP, sentiment classification, and independent collection of public social-media data for real-world analysis.

# 🌐 Data Vortex A'26 — Rebuilding the Social Engine

> From raw social-media data to meaningful patterns, signals, and insights.

**Data Vortex A'26** was a multi-round data science and AI challenge by **Aaruush**, where we explored how a "Social Engine" could understand not only what people say, but how conversations evolve over time.

### 👥 Team `soumadipd43`

**Soumadip Das** · Team Head  
**Aritra Pal** · CSE — AI & ML

**Haldia Institute Of Technology**

---

## 🚀 Our Journey

The project evolved through three different layers of social-media analysis:

```text
        RAW SOCIAL DATA
              │
              ▼
       ┌──────────────┐
       │ Round 1      │
       │ Data + SQL   │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │ Round 2      │
       │ ML + NLP     │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │ Round 3      │
       │ Social       │
       │ Signals      │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │   INSIGHTS   │
       └──────────────┘

       📊 Round 1 — Data & SQL
🎯 Objective

Understand structured social-media data and uncover hidden engagement patterns using SQL and data analysis.

🔎 What We Explored
📈 Platform engagement
📍 Location-based engagement
👤 High-impact user behaviour
🔥 Engagement patterns
🧩 Key Challenges

E3 — Platform Engagement

Compared average:

Likes · Shares · Comments · Total Engagement

across platforms.

M1 — Location Engagement

Analysed locations generating higher engagement.

H6 — High-Impact Users

Investigated users with relatively low follower counts but unusually high engagement.

🛠️ Stack

Python · Pandas · SQLite · SQL

📌 Output

Structured SQL queries and visual outputs for engagement analysis.

🤖 Round 2 — NLP & Machine Learning
🎯 Objective

Move from structured social-media data to understanding the language behind the conversations.

🧠 Pipeline
Raw Text
   ↓
Preprocessing
   ↓
Train / Test Split
   ↓
TF-IDF + ML Models
   ↓
DistilBERT
   ↓
Sentiment + Topic Analysis
💬 Sentiment Classification

We experimented with:

Logistic Regression
Linear SVM
Naive Bayes
TF-IDF
DistilBERT
📊 Final Sentiment Model
Metric	Result
Accuracy	68.33%
Macro F1	67.81%
Weighted F1	67.77%

Classes

Negative · Neutral · Positive

🏷️ Topic Classification

Final model:

Word + Character TF-IDF → Logistic Regression

Metric	Result
Accuracy	93.52%
Macro Precision	92.92%
Macro Recall	56.30%
Macro F1	65.52%
Weighted F1	92.30%
📌 Output
NLP training pipeline
Sentiment model
Topic model
Confusion matrices
Evaluation reports
🌐 Round 3 — Real-World Social Signals
🎯 Objective

Take the NLP model into the real world by independently collecting public social-media data and analysing how conversations change over time.

📡 Data Source

YouTube public comments

Topic:

Public reaction to an X platform monetisation change

🔄 Data Pipeline
YouTube Data API
       ↓
Video Search
       ↓
Comment Collection
       ↓
Deduplication
       ↓
Relevance Filtering
       ↓
Manual Review
       ↓
Round 2 NLP Model
       ↓
┌────────────┬────────────┬────────────┐
│ Sentiment  │ Engagement │  Topics &   │
│   Shifts   │   Spikes   │  Entities  │
└────────────┴────────────┴────────────┘
       ↓
 SOCIAL SIGNALS
📊 Final Dataset
Metric	Result
Comments	40
Videos	12
Duplicate Comments	0
Sentiment Classes	3
Engagement Spikes	2

Analysis Window: 5 Aug 2026 → 10 Sep 2026

📈 Sentiment Over Time

The Round 2 DistilBERT model was applied to the collected comments.

Final Distribution
Sentiment	Count
🔴 Negative	7
⚪ Neutral	26
🟢 Positive	7

We analysed changes in sentiment across the observation period to identify potential shifts in discussion.

🔥 Engagement Spikes
Comment Engagement = Likes + Replies
Metric	Value
Mean	2.35
Median	1.50
Spike Threshold	8.32
Detected
🔥 15 Engagement
🔥 10 Engagement

Both spikes occurred on the same video discussing the monetisation change.

🏷️ Topics & Entities
Topics
Topic	Share
Eligibility & Access	27.5%
Original Content & Reposts	25.0%
Monetisation Rules	15.0%
Payouts & Earnings	12.5%
Impressions & Reach	12.5%
Small Creators	10.0%
Entities
Entity	Share
X / Twitter	25.0%
Pakistan	15.0%
500K Impressions	7.5%
Original Content Rewards	5.0%
Elon Musk	2.5%
📸 Visual Results
Round 1
Platform Engagement

Round 2
Sentiment Confusion Matrix

Round 3
Sentiment Over Time

Engagement Spikes

🛠️ Technology Stack
Category	Technologies
Language	Python, SQL
Data Analysis	Pandas, NumPy
Database	SQLite
Machine Learning	Scikit-learn
NLP	TF-IDF, DistilBERT
Transformers	Hugging Face
Data Collection	YouTube Data API v3
Development	VS Code
Version Control	Git, GitHub
📁 Repository Structure
DATA-VORTEX-STARTER/
│
├── sql/
│   └── outputs/
│
├── round2/
│   ├── data/
│   ├── models/
│   ├── notebooks/
│   ├── outputs/
│   └── reports/
│
├── round3/
│   ├── data/
│   ├── scripts/
│   ├── notebooks/
│   ├── outputs/
│   └── reports/
│
├── round4/
│   ├── data/
│   ├── dashboard/
│   ├── outputs/
│   └── reports/
│
├── .env.example
├── .gitignore
└── README.md
🔐 Security

API credentials are not stored in the repository.

Use .env.example:

YOUTUBE_API_KEY=your_youtube_api_key_here

The actual .env file is excluded using .gitignore.

⚡ Key Numbers
	
🧩 Rounds Completed	3
🤖 NLP Models	Multiple approaches + DistilBERT
💬 Final Round 3 Comments	40
🎥 Analysed Videos	12
📈 Engagement Spikes	2
🗃️ Duplicate Comments	0
🧠 Sentiment Accuracy	68.33%
🏷️ Topic Accuracy	93.52%
💡 What We Learned

Real-world data rarely behaves like a clean benchmark dataset.

The project taught us to work through:

Data Cleaning → SQL → ML → NLP → Real-World Data → Analysis

More importantly, we learned to question the output before trusting it.

🏁 Final Takeaway

We didn't make it to the final round.

But Data Vortex gave us the opportunity to build something that went from:

Raw Data
   ↓
SQL
   ↓
Machine Learning
   ↓
NLP
   ↓
Social Data
   ↓
Social Signals
   ↓
Insights

No trophy this time.
But definitely a lot of progress. 🚀

👥 Team
Aritra Pal

CSE — Artificial Intelligence & Machine Learning
Haldia Institute Of Technology

Soumadip Das

Team Head
Haldia Institute Of Technology

🔗 Project

GitHub:
https://github.com/aritrapal888/Data-Vortex

<div align="center">
🌐 Data Vortex A'26

Rebuilding the Social Engine

Team soumadipd43

Haldia Institute Of Technology

</div> ```
