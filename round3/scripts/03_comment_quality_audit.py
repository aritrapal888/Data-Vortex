import pandas as pd

FILE = "round3/data/processed/platform_monetisation_reaction_clean.csv"

df = pd.read_csv(FILE)

print("=" * 70)
print("DATA VORTEX ROUND 3 - COMMENT QUALITY AUDIT")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)

print("\nUnique comments:")
print(df["comment_id"].nunique())

print("\nUnique videos:")
print(df["video_id"].nunique())

# Comment length
df["comment_length"] = df["comment_text"].astype(str).str.len()
df["word_count"] = df["comment_text"].astype(str).str.split().str.len()

print("\nComment length statistics:")
print(df["comment_length"].describe())

print("\nWord count statistics:")
print(df["word_count"].describe())

# Very short comments
short_comments = df[df["word_count"] <= 2]

print("\nVery short comments (2 words or fewer):")
print(len(short_comments))

# Exact duplicate comment text
print("\nDuplicate comment text:")
print(df["comment_text"].duplicated().sum())

# Print all comments with metadata
print("\n" + "=" * 70)
print("ALL COLLECTED COMMENTS")
print("=" * 70)

for i, row in df.iterrows():
    print("\n" + "-" * 70)
    print(f"Comment #{i + 1}")
    print("Video :", row["video_title"])
    print("Channel:", row["channel_title"])
    print("Date  :", row["comment_published_at"])
    print("Likes :", row["comment_like_count"])
    print("Replies:", row["comment_reply_count"])
    print("Engagement:", row["comment_engagement"])
    print("Comment:")
    print(row["comment_text"])

print("\n" + "=" * 70)
print("COMMENT QUALITY AUDIT COMPLETE")
print("=" * 70)