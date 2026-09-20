import pandas as pd

INPUT_FILE = "round3/data/processed/platform_monetisation_reaction_sentiment.csv"
OUTPUT_FILE = "round3/outputs/engagement/engagement_spikes.csv"

df = pd.read_csv(INPUT_FILE)

df["comment_published_at"] = pd.to_datetime(
    df["comment_published_at"],
    utc=True
)

# Sort by comment engagement
top_comments = df.sort_values(
    "comment_engagement",
    ascending=False
).copy()

# Calculate engagement statistics
mean_engagement = df["comment_engagement"].mean()
median_engagement = df["comment_engagement"].median()
std_engagement = df["comment_engagement"].std()

# Define an objective spike threshold:
# engagement greater than mean + 2 standard deviations
spike_threshold = mean_engagement + (2 * std_engagement)

spikes = top_comments[
    top_comments["comment_engagement"] >= spike_threshold
].copy()

# Save
spikes.to_csv(
    OUTPUT_FILE,
    index=False
)

print("=" * 70)
print("DATA VORTEX ROUND 3 - ENGAGEMENT ANALYSIS")
print("=" * 70)

print("\nEngagement statistics:")
print(f"Mean   : {mean_engagement:.2f}")
print(f"Median : {median_engagement:.2f}")
print(f"Std    : {std_engagement:.2f}")
print(f"Spike threshold (mean + 2 SD): {spike_threshold:.2f}")

print("\nTop 10 comments by engagement:")
print("-" * 70)

for _, row in top_comments.head(10).iterrows():
    print(
        f"\nDate: {row['comment_published_at']}"
        f"\nEngagement: {row['comment_engagement']}"
        f"\nVideo: {row['video_title']}"
        f"\nComment: {row['comment_text']}"
    )

print("\n" + "=" * 70)
print("DETECTED ENGAGEMENT SPIKES")
print("=" * 70)

if len(spikes) == 0:
    print("No comments exceeded the mean + 2 SD threshold.")

else:
    print(f"Spike comments: {len(spikes)}")

    for _, row in spikes.iterrows():
        print(
            f"\nDate: {row['comment_published_at']}"
            f"\nEngagement: {row['comment_engagement']}"
            f"\nVideo: {row['video_title']}"
            f"\nComment: {row['comment_text']}"
        )

print("\nSaved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("ENGAGEMENT ANALYSIS COMPLETE")
print("=" * 70)