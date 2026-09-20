import pandas as pd

INPUT_FILE = "round3/data/processed/platform_monetisation_reaction_review.csv"
OUTPUT_FILE = "round3/data/processed/platform_monetisation_reaction_final.csv"

df = pd.read_csv(INPUT_FILE)

# Keep only manually approved comments.
final_df = df[df["review_status"] == "KEEP"].copy()

# Remove the review helper column from the final analytical dataset.
final_df.drop(columns=["review_status"], inplace=True)

# Final duplicate safety check.
before = len(final_df)

final_df = final_df.drop_duplicates(
    subset=["comment_id"]
)

duplicates_removed = before - len(final_df)

# Sort chronologically for time-based analysis.
final_df["comment_published_at"] = pd.to_datetime(
    final_df["comment_published_at"],
    utc=True
)

final_df = final_df.sort_values(
    "comment_published_at"
).reset_index(drop=True)

# Save final dataset.
final_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("=" * 70)
print("DATA VORTEX ROUND 3 - FINAL DATASET")
print("=" * 70)

print("\nFinal shape:")
print(final_df.shape)

print("\nUnique comments:")
print(final_df["comment_id"].nunique())

print("\nUnique videos:")
print(final_df["video_id"].nunique())

print("\nDuplicate comments removed:")
print(duplicates_removed)

print("\nDate range:")
print("Earliest:", final_df["comment_published_at"].min())
print("Latest:  ", final_df["comment_published_at"].max())

print("\nComments by search query:")
print(final_df["search_query"].value_counts())

print("\nTop videos by number of comments:")
print(
    final_df["video_title"]
    .value_counts()
    .head(10)
)

print("\nTotal comment engagement:")
print(final_df["comment_engagement"].sum())

print("\nMaximum comment engagement:")
print(final_df["comment_engagement"].max())

print("\nSaved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("FINAL DATASET CREATED")
print("=" * 70)