import pandas as pd

INPUT_FILE = "round3/data/processed/platform_monetisation_reaction_analysis.csv"
OUTPUT_FILE = "round3/data/processed/platform_monetisation_reaction_review.csv"

df = pd.read_csv(INPUT_FILE)

# Default every comment to KEEP.
df["review_status"] = "KEEP"

# Clearly irrelevant comments identified from the quality audit.
remove_texts = [
    # Promotional links
    "Join 1,500+ creators in my community: https://skool.com/smallcreators\n\nWant to work with me? Apply here: https://calendly.com/jacob-jacobcedmunds/x-growth-call-yt",

    # Account verification / recovery
    "Sir mera I'd verification under review poda hai 🫢 kaise solve Karu",
    "Bhai Jan ap id verification aor strip k bato.\nMra criteria complete hua h",
    "Recovery kesa koraa",

    # Generic praise
    "Masha Allah ❤\nGood work bro❤",
    "Good work brother 🎉",
    "Great Very Informative",

    # Unrelated discussion
    "Doing same with grok and it's really help full",

    # Unrelated Jensen/Nvidia discussion
    "haha no wonder Jensen say AGI has arrived when the money from OpenAI to Nvidia also has arrived! They are all boosting eachother at the same time they all do business with eachother! It's one big circus!",

    # Voice-quality discussion
    "Vice clear nhi ha",

    # Unclear/unrelated comments
    "Vi bhaiya Apne subscriber Kori then",
    "El nuevo xol  la roots.  Camouflage. Don cultura pantera  pro rebelde   videos   la ceiba Atlántida and los angeles California.",
    "hey bro what do you think of gainworkers video coming soon maybe",
]

# Remove only exact matching comments.
for text in remove_texts:
    mask = df["comment_text"].astype(str).str.strip() == text.strip()
    df.loc[mask, "review_status"] = "REMOVE"

# IMPORTANT:
# "Repost count hoga ?" is intentionally KEPT because
# it is directly related to the monetisation-rule discussion.

# Save review dataset.
df.to_csv(OUTPUT_FILE, index=False)

print("=" * 70)
print("DATA VORTEX ROUND 3 - MANUAL REVIEW PREPARATION")
print("=" * 70)

print("\nInput comments:", len(df))
print("Marked KEEP:", (df["review_status"] == "KEEP").sum())
print("Marked REMOVE:", (df["review_status"] == "REMOVE").sum())

print("\nCOMMENTS MARKED FOR REMOVAL:")
print("-" * 70)

for _, row in df[df["review_status"] == "REMOVE"].iterrows():
    print(f"\n{row['comment_text']}")

print("\n" + "=" * 70)
print("REVIEW FILE SAVED")
print("=" * 70)

print(OUTPUT_FILE)