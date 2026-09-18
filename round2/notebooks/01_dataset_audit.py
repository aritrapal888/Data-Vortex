import pandas as pd
from pathlib import Path

# ============================================================
# DATA VORTEX A'26 — ROUND 2
# Dataset 2 Audit
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Labeled_Social_NLP_Training_Data.csv"

print("=" * 70)
print("DATA VORTEX A'26 — ROUND 2 DATASET AUDIT")
print("=" * 70)

# Load dataset
df = pd.read_csv(DATA_PATH)

# ------------------------------------------------------------
# 1. Basic information
# ------------------------------------------------------------

print("\n[1] BASIC DATASET INFORMATION")
print("-" * 40)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\nColumns:")
for col in df.columns:
    print(f"  - {col}")

# ------------------------------------------------------------
# 2. Data types
# ------------------------------------------------------------

print("\n[2] DATA TYPES")
print("-" * 40)
print(df.dtypes)

# ------------------------------------------------------------
# 3. Missing values
# ------------------------------------------------------------

print("\n[3] MISSING VALUES")
print("-" * 40)

missing = df.isnull().sum()
print(missing)

# ------------------------------------------------------------
# 4. Duplicate analysis
# ------------------------------------------------------------

print("\n[4] DUPLICATE ANALYSIS")
print("-" * 40)

print(f"Duplicate rows : {df.duplicated().sum()}")

if "text_id" in df.columns:
    print(f"Duplicate text_id : {df['text_id'].duplicated().sum()}")

if "post_text" in df.columns:
    print(f"Duplicate post_text : {df['post_text'].duplicated().sum()}")

# ------------------------------------------------------------
# 5. Sentiment distribution
# ------------------------------------------------------------

if "sentiment_label" in df.columns:

    print("\n[5] SENTIMENT DISTRIBUTION")
    print("-" * 40)

    sentiment_counts = df["sentiment_label"].value_counts()
    sentiment_percent = df["sentiment_label"].value_counts(normalize=True) * 100

    for label in sentiment_counts.index:
        print(
            f"{label}: {sentiment_counts[label]} "
            f"({sentiment_percent[label]:.2f}%)"
        )

# ------------------------------------------------------------
# 6. Topic distribution
# ------------------------------------------------------------

if "topic_category" in df.columns:

    print("\n[6] TOPIC DISTRIBUTION")
    print("-" * 40)

    topic_counts = df["topic_category"].value_counts()
    topic_percent = df["topic_category"].value_counts(normalize=True) * 100

    for label in topic_counts.index:
        print(
            f"{label}: {topic_counts[label]} "
            f"({topic_percent[label]:.2f}%)"
        )

# ------------------------------------------------------------
# 7. Text length analysis
# ------------------------------------------------------------

if "post_text" in df.columns:

    df["text_length_chars"] = df["post_text"].astype(str).str.len()
    df["text_length_words"] = (
        df["post_text"]
        .astype(str)
        .str.split()
        .str.len()
    )

    print("\n[7] TEXT LENGTH")
    print("-" * 40)

    print("Characters:")
    print(df["text_length_chars"].describe())

    print("\nWords:")
    print(df["text_length_words"].describe())

# ------------------------------------------------------------
# 8. Social-media pattern analysis
# ------------------------------------------------------------

if "post_text" in df.columns:

    text = df["post_text"].astype(str)

    print("\n[8] TEXT PATTERN ANALYSIS")
    print("-" * 40)

    print(f"Texts containing URLs     : {text.str.contains(r'https?://|www\\.', regex=True).sum()}")
    print(f"Texts containing mentions : {text.str.contains(r'@\\w+', regex=True).sum()}")
    print(f"Texts containing hashtags : {text.str.contains(r'#\\w+', regex=True).sum()}")
    print(f"Texts containing numbers  : {text.str.contains(r'\\d+', regex=True).sum()}")

# ------------------------------------------------------------
# 9. Sample records
# ------------------------------------------------------------

print("\n[9] SAMPLE RECORDS")
print("-" * 40)

print(df.head(10).to_string(index=False))

# ------------------------------------------------------------
# 10. Label relationship
# ------------------------------------------------------------

if "sentiment_label" in df.columns and "topic_category" in df.columns:

    print("\n[10] SENTIMENT × TOPIC")
    print("-" * 40)

    cross_tab = pd.crosstab(
        df["topic_category"],
        df["sentiment_label"]
    )

    print(cross_tab)

# ------------------------------------------------------------
# 11. Save audit report
# ------------------------------------------------------------

REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

output_path = REPORT_DIR / "dataset_audit.txt"

with open(output_path, "w", encoding="utf-8") as f:

    f.write("DATA VORTEX A'26 — ROUND 2 DATASET AUDIT\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Rows: {df.shape[0]}\n")
    f.write(f"Columns: {df.shape[1]}\n\n")

    f.write("Columns:\n")
    for col in df.columns:
        f.write(f"- {col}\n")

    f.write("\nMissing Values:\n")
    f.write(df.isnull().sum().to_string())

    f.write("\n\nDuplicate Rows:\n")
    f.write(str(df.duplicated().sum()))

    if "text_id" in df.columns:
        f.write("\nDuplicate text_id:\n")
        f.write(str(df["text_id"].duplicated().sum()))

    if "post_text" in df.columns:
        f.write("\nDuplicate post_text:\n")
        f.write(str(df["post_text"].duplicated().sum()))

    if "sentiment_label" in df.columns:
        f.write("\n\nSentiment Distribution:\n")
        f.write(df["sentiment_label"].value_counts().to_string())

    if "topic_category" in df.columns:
        f.write("\n\nTopic Distribution:\n")
        f.write(df["topic_category"].value_counts().to_string())

    if "post_text" in df.columns:
        f.write("\n\nText Length Statistics:\n")
        f.write(df["text_length_chars"].describe().to_string())

print("\n" + "=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)
print(f"Saved report: {output_path}")