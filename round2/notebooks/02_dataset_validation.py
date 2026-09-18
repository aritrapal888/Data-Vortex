import pandas as pd
from pathlib import Path

# ============================================================
# DATA VORTEX A'26 — ROUND 2
# Dataset 2 Validation
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Labeled_Social_NLP_Training_Data.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("DATA VORTEX A'26 — ROUND 2 DATASET VALIDATION")
print("=" * 70)

# ------------------------------------------------------------
# 1. Duplicate text analysis
# ------------------------------------------------------------

print("\n[1] DUPLICATE TEXT ANALYSIS")
print("-" * 40)

duplicate_mask = df["post_text"].duplicated(keep=False)

duplicate_rows = df[duplicate_mask]

print(f"Rows belonging to duplicated texts: {len(duplicate_rows)}")
print(f"Unique duplicated texts: {duplicate_rows['post_text'].nunique()}")

# ------------------------------------------------------------
# 2. Check whether duplicate texts have conflicting labels
# ------------------------------------------------------------

print("\n[2] DUPLICATE LABEL CONSISTENCY")
print("-" * 40)

sentiment_conflicts = (
    duplicate_rows
    .groupby("post_text")["sentiment_label"]
    .nunique()
)

topic_conflicts = (
    duplicate_rows
    .groupby("post_text")["topic_category"]
    .nunique()
)

sentiment_conflicting_texts = (sentiment_conflicts > 1).sum()
topic_conflicting_texts = (topic_conflicts > 1).sum()

print(
    f"Duplicate texts with conflicting sentiment labels: "
    f"{sentiment_conflicting_texts}"
)

print(
    f"Duplicate texts with conflicting topic labels: "
    f"{topic_conflicting_texts}"
)

# ------------------------------------------------------------
# 3. Correct text pattern analysis
# ------------------------------------------------------------

print("\n[3] TEXT PATTERN ANALYSIS")
print("-" * 40)

text = df["post_text"].astype(str)

url_count = text.str.contains(
    r"https?://|www\.",
    regex=True,
    case=False,
    na=False
).sum()

mention_count = text.str.contains(
    r"@\w+",
    regex=True,
    na=False
).sum()

hashtag_count = text.str.contains(
    r"#\w+",
    regex=True,
    na=False
).sum()

number_count = text.str.contains(
    r"\d+",
    regex=True,
    na=False
).sum()

print(f"Texts containing URLs     : {url_count}")
print(f"Texts containing mentions : {mention_count}")
print(f"Texts containing hashtags : {hashtag_count}")
print(f"Texts containing numbers  : {number_count}")

# ------------------------------------------------------------
# 4. Case / punctuation / special characters
# ------------------------------------------------------------

print("\n[4] TEXT CHARACTERISTICS")
print("-" * 40)

uppercase_count = text.str.contains(
    r"[A-Z]",
    regex=True,
    na=False
).sum()

exclamation_count = text.str.contains(
    r"!",
    regex=True,
    na=False
).sum()

question_count = text.str.contains(
    r"\?",
    regex=True,
    na=False
).sum()

print(f"Texts containing uppercase letters : {uppercase_count}")
print(f"Texts containing !                : {exclamation_count}")
print(f"Texts containing ?                : {question_count}")

# ------------------------------------------------------------
# 5. Sample duplicated texts
# ------------------------------------------------------------

print("\n[5] SAMPLE DUPLICATED TEXTS")
print("-" * 40)

samples = (
    duplicate_rows
    .groupby("post_text")
    .filter(lambda x: len(x) > 1)
    .drop_duplicates("post_text")
    .head(10)
)

for _, row in samples.iterrows():
    print("\nText:")
    print(row["post_text"])
    print("Sentiment:", row["sentiment_label"])
    print("Topic:", row["topic_category"])

# ------------------------------------------------------------
# 6. Final validation summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)

if sentiment_conflicting_texts == 0:
    print("✓ Duplicate sentiment labels are consistent.")
else:
    print("⚠ Duplicate sentiment conflicts found.")

if topic_conflicting_texts == 0:
    print("✓ Duplicate topic labels are consistent.")
else:
    print("⚠ Duplicate topic conflicts found.")

print("\nNext step: preprocessing and train/test split.")