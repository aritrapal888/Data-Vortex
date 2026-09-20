import pandas as pd
import re

INPUT_FILE = "round3/data/raw/platform_monetisation_reaction.csv"
OUTPUT_FILE = "round3/data/processed/platform_monetisation_reaction_clean.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("DATA VORTEX ROUND 3 - DATASET FILTERING")
print("=" * 60)

print("\nOriginal dataset:", df.shape)

# Keywords indicating that the video is actually about X/Twitter
x_keywords = [
    "x monetization",
    "x monetisation",
    "x (twitter)",
    "twitter monetization",
    "twitter monetisation",
    "x creator",
    "twitter creator",
    "x revenue sharing",
    "twitter revenue sharing",
    "original content rewards",
    "x platform changes",
    "x changed",
    "x just changed",
    "x new update",
    "twitter new update",
    "earn money on x",
    "make money on x",
    "monetize x",
    "monetise x"
]

# Explicitly exclude unrelated platforms/topics
exclude_keywords = [
    "youtube monetization",
    "youtube monetisation",
    "youtube partner program",
    "youtube update",
    "facebook reels",
    "facebook monetization",
    "facebook monetisation",
    "facebook story",
    "type beat",
    "osamason",
    "ken carson"
]

def is_relevant(title):
    title_lower = str(title).lower()

    # Remove clearly unrelated content first
    for keyword in exclude_keywords:
        if keyword in title_lower:
            return False

    # Keep videos containing relevant X/Twitter monetization terms
    for keyword in x_keywords:
        if keyword in title_lower:
            return True

    return False


df["is_relevant"] = df["video_title"].apply(is_relevant)

clean_df = df[df["is_relevant"]].copy()

# Remove helper column
clean_df.drop(columns=["is_relevant"], inplace=True)

# Remove duplicate comments just in case
clean_df = clean_df.drop_duplicates(subset=["comment_id"])

# Save cleaned dataset
clean_df.to_csv(OUTPUT_FILE, index=False)

print("\nRelevant comments:", len(clean_df))
print("Relevant videos:", clean_df["video_id"].nunique())

print("\nRemoved comments:", len(df) - len(clean_df))
print("Removed videos:", df["video_id"].nunique() - clean_df["video_id"].nunique())

print("\nRemaining video titles:")
for title in clean_df["video_title"].drop_duplicates():
    print("-", title)

print("\nComments by search query:")
print(clean_df["search_query"].value_counts())

print("\nSaved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 60)
print("FILTERING COMPLETE")
print("=" * 60)