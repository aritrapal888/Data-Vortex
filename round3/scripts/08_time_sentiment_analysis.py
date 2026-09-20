import pandas as pd

INPUT_FILE = "round3/data/processed/platform_monetisation_reaction_sentiment.csv"
OUTPUT_FILE = "round3/outputs/sentiment/daily_sentiment_analysis.csv"

df = pd.read_csv(INPUT_FILE)

# Convert timestamps
df["comment_published_at"] = pd.to_datetime(
    df["comment_published_at"],
    utc=True
)

# Create date column
df["date"] = df["comment_published_at"].dt.date

# Count comments by day and sentiment
daily = (
    df.groupby(["date", "sentiment_label"])
    .size()
    .unstack(fill_value=0)
)

# Ensure all sentiment columns exist
for sentiment in ["Negative", "Neutral", "Positive"]:
    if sentiment not in daily.columns:
        daily[sentiment] = 0

# Keep consistent order
daily = daily[
    ["Negative", "Neutral", "Positive"]
]

# Total comments
daily["Total"] = daily.sum(axis=1)

# Sentiment percentages
daily["Negative_pct"] = (
    daily["Negative"] / daily["Total"] * 100
)

daily["Neutral_pct"] = (
    daily["Neutral"] / daily["Total"] * 100
)

daily["Positive_pct"] = (
    daily["Positive"] / daily["Total"] * 100
)

# Sentiment balance:
# Positive proportion - Negative proportion
daily["sentiment_balance"] = (
    daily["Positive_pct"] - daily["Negative_pct"]
)

# Save
daily.to_csv(OUTPUT_FILE)

print("=" * 70)
print("DATA VORTEX ROUND 3 - DAILY SENTIMENT ANALYSIS")
print("=" * 70)

print("\nDaily sentiment:")
print(daily.round(2).to_string())

print("\n" + "=" * 70)
print("LARGEST DAILY SHIFTS")
print("=" * 70)

# Calculate change in sentiment balance
daily["balance_change"] = daily["sentiment_balance"].diff()

print(
    daily[
        [
            "sentiment_balance",
            "balance_change"
        ]
    ]
    .round(2)
    .sort_values(
        "balance_change",
        key=lambda x: x.abs(),
        ascending=False
    )
    .head(10)
    .to_string()
)

print("\nSaved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("DAILY SENTIMENT ANALYSIS COMPLETE")
print("=" * 70)