import pandas as pd
import re

INPUT_FILE = "round3/data/processed/platform_monetisation_reaction_clean.csv"
OUTPUT_FILE = "round3/data/processed/platform_monetisation_reaction_analysis.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("DATA VORTEX ROUND 3 - ANALYSIS DATASET FILTER")
print("=" * 70)

print("Input:", df.shape)

# ---------------------------------------------------------
# 1. Remove comments that are clearly unrelated to the
#    monetisation change / public reaction.
# ---------------------------------------------------------

exclude_patterns = [
    # Audio/video production issues
    r"\bvoice\b",
    r"\bmic\b",
    r"\bmicrophone\b",
    r"\bvoice over\b",

    # Generic creator-course promotion / unrelated service requests
    r"\bcourse\b",
    r"\bthumbnail\b",
    r"\bmail\b.*\bcheck\b",

    # Account recovery / suspension rather than monetisation reaction
    r"\bsuspend\b",
    r"\bunsuspend\b",
    r"\bappeal\b",

    # Purely technical/account setup questions
    r"\bpayment gateway\b",
    r"\bpaypal\b",
    r"\bpayoneer\b",
    r"\bVPN\b",

    # Generic reach/impression questions without discussion
    # of the monetisation change
    r"\breach nhi\b",
    r"\breach q\b",
]

def is_excluded(text):
    text = str(text).lower()

    for pattern in exclude_patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True

    return False


df["excluded"] = df["comment_text"].apply(is_excluded)

filtered = df[~df["excluded"]].copy()

# ---------------------------------------------------------
# 2. Remove extremely low-information comments.
# ---------------------------------------------------------

def is_low_information(text):
    text = str(text).strip()

    # Remove pure emoji / punctuation comments
    if not re.search(r"[A-Za-z\u0900-\u097F]", text):
        return True

    # One-word generic reactions
    generic = {
        "good",
        "great",
        "thanks",
        "thank you",
        "finally",
        "impossible",
        "kasay",
        "without vpn",
    }

    if text.lower() in generic:
        return True

    return False


filtered["low_information"] = filtered["comment_text"].apply(
    is_low_information
)

analysis_df = filtered[~filtered["low_information"]].copy()

# Remove helper columns
analysis_df.drop(
    columns=["excluded", "low_information"],
    inplace=True
)

# ---------------------------------------------------------
# 3. Final duplicate safety check
# ---------------------------------------------------------

analysis_df = analysis_df.drop_duplicates(
    subset=["comment_id"]
)

# ---------------------------------------------------------
# 4. Save
# ---------------------------------------------------------

analysis_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nFinal analysis dataset:", analysis_df.shape)

print("\nComments removed as unrelated:")
print(df["excluded"].sum())

print("\nLow-information comments removed:")
print(filtered["low_information"].sum())

print("\nFinal comments:", len(analysis_df))
print("Final videos:", analysis_df["video_id"].nunique())

print("\nFinal date range:")

dates = pd.to_datetime(
    analysis_df["comment_published_at"],
    errors="coerce",
    utc=True
)

print("Earliest:", dates.min())
print("Latest:  ", dates.max())

print("\nFinal comments:")
for i, row in analysis_df.iterrows():
    print(
        f"\n[{i + 1}] "
        f"{row['comment_published_at']} | "
        f"Engagement={row['comment_engagement']}"
    )
    print(row["comment_text"])

print("\nSaved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("ANALYSIS FILTER COMPLETE")
print("=" * 70)