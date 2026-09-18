import pandas as pd
from pathlib import Path
from sklearn.model_selection import GroupShuffleSplit

# ============================================================
# DATA VORTEX A'26 — ROUND 2
# Leakage-Safe Preprocessing & Train/Test Split
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Labeled_Social_NLP_Training_Data.csv"
OUTPUT_DIR = BASE_DIR / "data"

print("=" * 70)
print("DATA VORTEX A'26 — ROUND 2 PREPROCESSING & SPLIT")
print("=" * 70)

# ------------------------------------------------------------
# 1. Load data
# ------------------------------------------------------------

df = pd.read_csv(DATA_PATH)

print(f"\nOriginal rows: {len(df)}")

# ------------------------------------------------------------
# 2. Basic text normalization
# ------------------------------------------------------------
# We deliberately keep punctuation, numbers, hashtags and
# sentiment-bearing words because they may contain useful
# semantic information.

df["post_text"] = (
    df["post_text"]
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# ------------------------------------------------------------
# 3. Remove empty text if any
# ------------------------------------------------------------

before = len(df)

df = df[df["post_text"].str.len() > 0].copy()

removed = before - len(df)

print(f"Empty texts removed: {removed}")

# ------------------------------------------------------------
# 4. Leakage-safe grouped split
# ------------------------------------------------------------
# All identical post_text values stay in the same split.

gss = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)

train_idx, test_idx = next(
    gss.split(
        df,
        groups=df["post_text"]
    )
)

train_df = df.iloc[train_idx].copy()
test_df = df.iloc[test_idx].copy()

# ------------------------------------------------------------
# 5. Validate no text leakage
# ------------------------------------------------------------

train_texts = set(train_df["post_text"])
test_texts = set(test_df["post_text"])

overlap = train_texts.intersection(test_texts)

print("\n[1] SPLIT")
print("-" * 40)

print(f"Training rows : {len(train_df)}")
print(f"Testing rows  : {len(test_df)}")

print(f"\nUnique training texts: {train_df['post_text'].nunique()}")
print(f"Unique testing texts : {test_df['post_text'].nunique()}")

print(f"\nExact text overlap between train/test: {len(overlap)}")

# ------------------------------------------------------------
# 6. Label distributions
# ------------------------------------------------------------

print("\n[2] SENTIMENT DISTRIBUTION")
print("-" * 40)

print("Training:")
print(train_df["sentiment_label"].value_counts())

print("\nTesting:")
print(test_df["sentiment_label"].value_counts())

print("\n[3] TOPIC DISTRIBUTION")
print("-" * 40)

print("Training:")
print(train_df["topic_category"].value_counts())

print("\nTesting:")
print(test_df["topic_category"].value_counts())

# ------------------------------------------------------------
# 7. Save splits
# ------------------------------------------------------------

train_path = OUTPUT_DIR / "train.csv"
test_path = OUTPUT_DIR / "test.csv"

train_df.to_csv(train_path, index=False)
test_df.to_csv(test_path, index=False)

print("\n[4] FILES CREATED")
print("-" * 40)

print(f"Training dataset: {train_path}")
print(f"Testing dataset : {test_path}")

# ------------------------------------------------------------
# 8. Final validation
# ------------------------------------------------------------

print("\n" + "=" * 70)

if len(overlap) == 0:
    print("✓ NO DUPLICATE TEXT LEAKAGE")
else:
    print("⚠ TEXT LEAKAGE DETECTED")

print("✓ PREPROCESSING & SPLIT COMPLETE")
print("=" * 70)