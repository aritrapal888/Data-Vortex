import pandas as pd

FILE = "round3/data/raw/platform_monetisation_reaction.csv"

df = pd.read_csv(FILE)

print("=" * 60)
print("DATA VORTEX ROUND 3 - DATASET AUDIT")
print("=" * 60)

print("\nShape:")
print(df.shape)

print("\nColumns:")
for col in df.columns:
    print(" -", col)

print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicate comment IDs:")
print(df["comment_id"].duplicated().sum())

print("\nUnique videos:")
print(df["video_id"].nunique())

print("\nComments per search query:")
print(df["search_query"].value_counts())

print("\nVideo titles:")
for title in df["video_title"].drop_duplicates():
    print("-", title)

print("\nComment date range:")

dates = pd.to_datetime(
    df["comment_published_at"],
    errors="coerce",
    utc=True
)

print("Earliest:", dates.min())
print("Latest:  ", dates.max())

print("\nComment engagement:")
print(df["comment_engagement"].describe())

print("\nVideo engagement:")
print(df["video_engagement"].describe())

print("\n" + "=" * 60)
print("AUDIT COMPLETE")
print("=" * 60)