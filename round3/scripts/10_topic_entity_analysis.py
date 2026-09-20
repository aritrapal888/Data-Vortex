import pandas as pd
import re
from collections import Counter

INPUT_FILE = "round3/data/processed/platform_monetisation_reaction_sentiment.csv"
OUTPUT_FILE = "round3/outputs/topics/topic_entity_analysis.csv"

df = pd.read_csv(INPUT_FILE)

# ---------------------------------------------------------
# Topic keyword groups
# ---------------------------------------------------------

topic_keywords = {
    "Payouts & Earnings": [
        "payout",
        "payouts",
        "earning",
        "earn",
        "money",
        "payment",
        "paying",
        "paid",
        "revenue",
    ],

    "Eligibility & Access": [
        "eligible",
        "eligibility",
        "eligible",
        "pakistan",
        "account",
        "accounts",
        "country",
        "list",
        "verification",
        "verified",
    ],

    "Impressions & Reach": [
        "impression",
        "impressions",
        "reach",
        "500k",
        "5 lac",
        "target",
    ],

    "Original Content & Reposts": [
        "original",
        "repost",
        "reposts",
        "content",
        "creator",
        "creators",
        "engagement farming",
    ],

    "Small Creators": [
        "small creator",
        "small creators",
        "meme page",
        "big account",
    ],

    "Monetisation Rules": [
        "monetization",
        "monetisation",
        "rules",
        "change",
        "changed",
        "update",
        "program",
    ],
}

# ---------------------------------------------------------
# Entity keywords
# ---------------------------------------------------------

entity_keywords = {
    "X / Twitter": [
        "x",
        "twitter",
    ],

    "Original Content Rewards": [
        "original content rewards",
        "original content",
    ],

    "500K Impressions": [
        "500k",
        "500 k",
        "5 lac",
        "5 lakh",
    ],

    "Pakistan": [
        "pakistan",
        "pakistani",
    ],

    "Grok": [
        "grok",
    ],

    "Elon Musk": [
        "elon musk",
    ],
}

# ---------------------------------------------------------
# Count topic occurrences
# ---------------------------------------------------------

topic_counts = Counter()

for text in df["comment_text"].astype(str):

    text_lower = text.lower()

    for topic, keywords in topic_keywords.items():

        if any(
            keyword.lower() in text_lower
            for keyword in keywords
        ):
            topic_counts[topic] += 1

# ---------------------------------------------------------
# Count entity occurrences
# ---------------------------------------------------------

entity_counts = Counter()

for text in df["comment_text"].astype(str):

    text_lower = text.lower()

    for entity, keywords in entity_keywords.items():

        if any(
            keyword.lower() in text_lower
            for keyword in keywords
        ):
            entity_counts[entity] += 1

# ---------------------------------------------------------
# Create output
# ---------------------------------------------------------

rows = []

for topic, count in topic_counts.most_common():

    rows.append({
        "category": "Topic",
        "name": topic,
        "comment_count": count,
        "percentage_of_comments": round(
            count / len(df) * 100,
            2
        ),
    })

for entity, count in entity_counts.most_common():

    rows.append({
        "category": "Entity",
        "name": entity,
        "comment_count": count,
        "percentage_of_comments": round(
            count / len(df) * 100,
            2
        ),
    })

result = pd.DataFrame(rows)

result.to_csv(
    OUTPUT_FILE,
    index=False
)

# ---------------------------------------------------------
# Print results
# ---------------------------------------------------------

print("=" * 70)
print("DATA VORTEX ROUND 3 - TOPIC & ENTITY ANALYSIS")
print("=" * 70)

print("\nTOPICS")
print("-" * 70)

for topic, count in topic_counts.most_common():
    print(
        f"{topic:<30} "
        f"{count:>3} comments "
        f"({count / len(df) * 100:.1f}%)"
    )

print("\nENTITIES")
print("-" * 70)

for entity, count in entity_counts.most_common():
    print(
        f"{entity:<30} "
        f"{count:>3} comments "
        f"({count / len(df) * 100:.1f}%)"
    )

print("\nSaved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("TOPIC & ENTITY ANALYSIS COMPLETE")
print("=" * 70)