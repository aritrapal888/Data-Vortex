import os
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

# =========================================================
# FILES
# =========================================================

SENTIMENT_FILE = (
    "round3/data/processed/"
    "platform_monetisation_reaction_sentiment.csv"
)

DAILY_FILE = (
    "round3/outputs/sentiment/"
    "daily_sentiment_analysis.csv"
)

ENGAGEMENT_FILE = (
    "round3/outputs/engagement/"
    "engagement_spikes.csv"
)

TOPIC_FILE = (
    "round3/outputs/topics/"
    "topic_entity_analysis.csv"
)

OUTPUT_FILE = (
    "round3/reports/"
    "Round3_Analytical_Report.pdf"
)

os.makedirs("round3/reports", exist_ok=True)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(SENTIMENT_FILE)
daily = pd.read_csv(DAILY_FILE)
engagement = pd.read_csv(ENGAGEMENT_FILE)
topics = pd.read_csv(TOPIC_FILE)

df["comment_published_at"] = pd.to_datetime(
    df["comment_published_at"],
    utc=True
)

# =========================================================
# BASIC METRICS
# =========================================================

total_comments = len(df)
unique_videos = df["video_id"].nunique()

sentiment_counts = df["sentiment_label"].value_counts()

negative = int(sentiment_counts.get("Negative", 0))
neutral = int(sentiment_counts.get("Neutral", 0))
positive = int(sentiment_counts.get("Positive", 0))

avg_confidence = df["sentiment_confidence"].mean()

earliest = df["comment_published_at"].min()
latest = df["comment_published_at"].max()

mean_engagement = df["comment_engagement"].mean()
median_engagement = df["comment_engagement"].median()
std_engagement = df["comment_engagement"].std()

spike_threshold = mean_engagement + 2 * std_engagement

# =========================================================
# PDF SETUP
# =========================================================

doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    rightMargin=42,
    leftMargin=42,
    topMargin=42,
    bottomMargin=42,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "ReportTitle",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontSize=20,
    leading=24,
    spaceAfter=12,
)

subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    alignment=TA_CENTER,
    fontSize=10,
    leading=14,
    spaceAfter=16,
)

heading_style = ParagraphStyle(
    "ReportHeading",
    parent=styles["Heading2"],
    fontSize=14,
    leading=18,
    spaceBefore=12,
    spaceAfter=8,
)

subheading_style = ParagraphStyle(
    "ReportSubheading",
    parent=styles["Heading3"],
    fontSize=11,
    leading=14,
    spaceBefore=8,
    spaceAfter=5,
)

body_style = ParagraphStyle(
    "ReportBody",
    parent=styles["BodyText"],
    fontSize=9.5,
    leading=14,
    spaceAfter=7,
)

small_style = ParagraphStyle(
    "ReportSmall",
    parent=styles["BodyText"],
    fontSize=7.5,
    leading=10,
)

story = []

# =========================================================
# TITLE PAGE
# =========================================================

story.append(
    Paragraph(
        "DATA VORTEX A'26 — ROUND 3",
        title_style
    )
)

story.append(
    Paragraph(
        "Analytical Report",
        title_style
    )
)

story.append(
    Paragraph(
        "Public Reaction to a Platform Monetisation Change",
        subtitle_style
    )
)

story.append(
    Paragraph(
        "<b>Platform Focus:</b> X (Twitter)",
        body_style
    )
)

story.append(
    Paragraph(
        "<b>Data Source:</b> Public YouTube comments collected "
        "through YouTube Data API v3",
        body_style
    )
)

story.append(
    Paragraph(
        "<b>Final analytical sample:</b> 40 comments from 12 videos",
        body_style
    )
)

story.append(
    Paragraph(
        "<b>Analysis period:</b> "
        f"{earliest.strftime('%d %b %Y')} – "
        f"{latest.strftime('%d %b %Y')}",
        body_style
    )
)

story.append(Spacer(1, 20))

story.append(
    Paragraph(
        "This report analyzes the collected public reaction "
        "surrounding discussions of X monetisation changes. "
        "The analysis combines the sentiment model developed "
        "during Round 2 with time-based analysis, comment "
        "engagement analysis, and keyword-based topic/entity "
        "analysis.",
        body_style
    )
)

story.append(PageBreak())

# =========================================================
# 1. DATA COLLECTION METHOD
# =========================================================

story.append(
    Paragraph(
        "1. Data Collection Method",
        heading_style
    )
)

story.append(
    Paragraph(
        "The data collection pipeline used the YouTube Data API "
        "v3 to identify public videos discussing X monetisation "
        "and related creator-reward changes. Search queries "
        "included X monetisation change, X monetisation 2026, "
        "X creator monetisation, X creator revenue sharing, and "
        "X Original Content Rewards.",
        body_style
    )
)

story.append(
    Paragraph(
        "For each relevant video, publicly available comment "
        "metadata was collected together with publication "
        "timestamps, comment likes, reply counts, video "
        "statistics, channel information, search query, source, "
        "and video URL.",
        body_style
    )
)

story.append(
    Paragraph(
        "<b>Initial collection:</b> 326 comments from 39 videos.",
        body_style
    )
)

story.append(
    Paragraph(
        "<b>Final analytical dataset:</b> 40 comments from "
        "12 videos.",
        body_style
    )
)

story.append(
    Paragraph(
        "The filtering process removed unrelated platform "
        "content, irrelevant comments, promotional material, "
        "generic low-information reactions, and other comments "
        "that did not contribute meaningfully to analysis of the "
        "assigned topic. The raw collection was retained "
        "separately to preserve traceability.",
        body_style
    )
)

# =========================================================
# 2. TIME WINDOW
# =========================================================

story.append(
    Paragraph(
        "2. Time Window",
        heading_style
    )
)

story.append(
    Paragraph(
        f"The final analytical comments span from "
        f"<b>{earliest.strftime('%d %B %Y, %H:%M UTC')}</b> "
        f"to <b>{latest.strftime('%d %B %Y, %H:%M UTC')}</b>.",
        body_style
    )
)

story.append(
    Paragraph(
        "The original API collection continued beyond the final "
        "analytical date, but comments collected later did not "
        "survive the relevance and manual-review process. "
        "Therefore, the report uses the final retained dataset's "
        "actual time window rather than claiming coverage of the "
        "entire raw collection period.",
        body_style
    )
)

# =========================================================
# 3. SENTIMENT ANALYSIS
# =========================================================

story.append(
    Paragraph(
        "3. Sentiment Analysis",
        heading_style
    )
)

story.append(
    Paragraph(
        "The Round 2 DistilBERT sentiment model was applied "
        "directly to the 40 final comments. The model produced "
        "three labels: Negative, Neutral, and Positive.",
        body_style
    )
)

sentiment_table = [
    ["Sentiment", "Comments", "Percentage"],
    [
        "Negative",
        str(negative),
        f"{negative / total_comments * 100:.1f}%"
    ],
    [
        "Neutral",
        str(neutral),
        f"{neutral / total_comments * 100:.1f}%"
    ],
    [
        "Positive",
        str(positive),
        f"{positive / total_comments * 100:.1f}%"
    ],
]

table = Table(
    sentiment_table,
    colWidths=[
        2.5 * inch,
        1.3 * inch,
        1.5 * inch
    ]
)

table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ])
)

story.append(table)

story.append(Spacer(1, 8))

story.append(
    Paragraph(
        f"The sample contains {neutral} Neutral, {positive} "
        f"Positive, and {negative} Negative predictions. The "
        f"average prediction confidence was {avg_confidence:.4f}. "
        "Neutral was the largest category, indicating that much "
        "of the collected discussion consisted of questions, "
        "requests for information, and informational reactions "
        "rather than explicitly positive or negative statements.",
        body_style
    )
)

story.append(
    Paragraph(
        "<b>Model limitation:</b> These labels are model "
        "predictions, not manually verified ground truth. "
        "Short, multilingual, slang-heavy, and context-dependent "
        "comments may be difficult for the model to classify "
        "reliably.",
        body_style
    )
)

# =========================================================
# SENTIMENT SHIFT 1
# =========================================================

story.append(
    Paragraph(
        "3.1 Observed Sentiment Shift — August",
        subheading_style
    )
)

story.append(
    Paragraph(
        "From Aug 8 to Aug 13, the collected comments move from "
        "a positive/mixed sentiment balance toward more "
        "negative or concern-oriented predictions. On Aug 8, "
        "the dataset contains 4 Positive and 5 Neutral comments "
        "with no Negative predictions. By Aug 11, one Negative "
        "and one Neutral prediction were recorded, and Aug 13 "
        "contains one Negative prediction.",
        body_style
    )
)

story.append(
    Paragraph(
        "The comments during this period include concerns from "
        "small creators, questions about the new requirements, "
        "and reactions to payout and eligibility changes. "
        "Because several later dates contain only one or two "
        "comments, this is reported as an observed shift in the "
        "collected sample rather than a population-level "
        "conclusion.",
        body_style
    )
)

# =========================================================
# SENTIMENT SHIFT 2
# =========================================================

story.append(
    Paragraph(
        "3.2 Observed Sentiment Shift — September",
        subheading_style
    )
)

story.append(
    Paragraph(
        "On Sep 6, the retained dataset contains one Neutral "
        "comment. By Sep 10, seven comments are present: six "
        "Neutral and one Negative. The resulting sentiment "
        "balance moves from 0 to -14.29 percentage points.",
        body_style
    )
)

story.append(
    Paragraph(
        "The Sep 10 discussion is dominated by questions about "
        "eligibility, impressions, account configuration, and "
        "monetisation access. This represents a weaker shift "
        "toward concern/question-oriented discussion rather than "
        "a large explicit negative reaction.",
        body_style
    )
)

# =========================================================
# 4. ACTIVITY ANALYSIS
# =========================================================

story.append(
    Paragraph(
        "4. Activity Analysis",
        heading_style
    )
)

story.append(
    Paragraph(
        f"Across the final sample, total comment engagement was "
        f"<b>{int(df['comment_engagement'].sum())}</b>. Mean "
        f"comment engagement was <b>{mean_engagement:.2f}</b>, "
        f"median engagement was <b>{median_engagement:.2f}</b>, "
        f"and the maximum was <b>{int(df['comment_engagement'].max())}</b>.",
        body_style
    )
)

story.append(
    Paragraph(
        f"An engagement spike was defined objectively as a "
        f"comment engagement value at or above mean + 2 standard "
        f"deviations. The calculated threshold was "
        f"<b>{spike_threshold:.2f}</b>.",
        body_style
    )
)

spike_table = [
    ["Date", "Engagement", "Video", "Observed Reaction"]
]

for _, row in engagement.iterrows():
    spike_table.append([
        str(row["comment_published_at"])[:16],
        str(int(row["comment_engagement"])),
        Paragraph(
            str(row["video_title"]),
            small_style
        ),
        Paragraph(
            str(row["comment_text"]),
            small_style
        ),
    ])

table = Table(
    spike_table,
    colWidths=[
        1.05 * inch,
        0.65 * inch,
        2.0 * inch,
        2.5 * inch
    ],
    repeatRows=1
)

table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ])
)

story.append(table)

story.append(Spacer(1, 8))

story.append(
    Paragraph(
        "Both detected spikes occurred on Aug 8 under the "
        "video \"X Monetization Just Changed... Again!\". "
        "One high-engagement comment expressed anticipation for "
        "information about the change, while another discussed "
        "potential payout effects. These comments indicate "
        "heightened interaction around the monetisation-change "
        "discussion.",
        body_style
    )
)

story.append(
    Paragraph(
        "The payout multiple mentioned in the second comment is "
        "treated only as a commenter claim. It is not independently "
        "verified by this analysis.",
        body_style
    )
)

# =========================================================
# 5. TOPIC / ENTITY ANALYSIS
# =========================================================

story.append(
    Paragraph(
        "5. Topic / Entity Analysis",
        heading_style
    )
)

story.append(
    Paragraph(
        "A transparent keyword-based approach was used to identify "
        "recurring topics and named entities in the final "
        "comments. Categories are not mutually exclusive; one "
        "comment can match multiple categories.",
        body_style
    )
)

topic_table = [
    ["Category", "Topic / Entity", "Comments", "Share"]
]

for _, row in topics.iterrows():
    topic_table.append([
        str(row["category"]),
        str(row["name"]),
        str(int(row["comment_count"])),
        f"{row['percentage_of_comments']:.1f}%"
    ])

table = Table(
    topic_table,
    colWidths=[
        1.0 * inch,
        3.0 * inch,
        0.8 * inch,
        0.8 * inch
    ],
    repeatRows=1
)

table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
    ])
)

story.append(table)

story.append(Spacer(1, 8))

story.append(
    Paragraph(
        "The most frequently detected topic was "
        "<b>Eligibility & Access</b> with 11 comments, followed "
        "by <b>Original Content & Reposts</b> with 10 comments. "
        "Monetisation Rules, Payouts & Earnings, Impressions & "
        "Reach, and Small Creators were also recurring themes.",
        body_style
    )
)

story.append(
    Paragraph(
        "Among named entities, Pakistan appeared in 6 comments, "
        "500K Impressions in 3 comments, Original Content Rewards "
        "in 2 comments, and Elon Musk in 1 comment. X/Twitter "
        "references were detected in 10 comments under the "
        "configured entity keyword rules.",
        body_style
    )
)

# =========================================================
# 6. TRIGGER EXPLANATIONS
# =========================================================

story.append(
    Paragraph(
        "6. Trigger Explanations",
        heading_style
    )
)

story.append(
    Paragraph(
        "<b>Trigger 1 — Monetisation-change announcement:</b> "
        "The highest-engagement comments were concentrated on "
        "Aug 8 under a video specifically discussing the "
        "monetisation change. The comments show strong interest "
        "in understanding the new system and its implications.",
        body_style
    )
)

story.append(
    Paragraph(
        "<b>Trigger 2 — Eligibility and access:</b> "
        "Repeated comments discussed whether particular countries, "
        "accounts, or creator types could participate. Pakistan "
        "was a recurring entity in this discussion.",
        body_style
    )
)

story.append(
    Paragraph(
        "<b>Trigger 3 — Original content and reposts:</b> "
        "Several comments focused on what content would qualify "
        "and how reposting or engagement-oriented behaviour would "
        "be treated.",
        body_style
    )
)

story.append(
    Paragraph(
        "<b>Trigger 4 — Creator thresholds:</b> "
        "Comments repeatedly asked about impressions, verified "
        "followers, reach, and other requirements, indicating "
        "that creators were trying to understand how to meet the "
        "new or discussed monetisation conditions.",
        body_style
    )
)

# =========================================================
# 7. KEY FINDINGS
# =========================================================

story.append(
    Paragraph(
        "7. Key Findings",
        heading_style
    )
)

findings = [
    "Neutral sentiment was the largest model-predicted sentiment category.",
    "Eligibility & Access was the most frequent detected topic.",
    "Original Content & Reposts was the second most frequent detected topic.",
    "The strongest engagement concentration occurred on Aug 8.",
    "Both detected engagement spikes were associated with a video discussing the monetisation change.",
    "The collected discussion contained substantial questions about eligibility, impressions, payouts, reposts, and small-creator participation.",
    "The temporal analysis shows observable changes in the composition of the collected comments, but the small daily sample sizes limit generalisation.",
]

for finding in findings:
    story.append(
        Paragraph(
            "• " + finding,
            body_style
        )
    )

# =========================================================
# 8. LIMITATIONS
# =========================================================

story.append(
    Paragraph(
        "8. Limitations",
        heading_style
    )
)

limitations = [
    "The dataset represents public YouTube commenters discussing X monetisation and is not a representative sample of all X users.",
    "The final analytical dataset contains only 40 comments.",
    "Some dates contain very few comments, making daily sentiment percentages unstable.",
    "The Round 2 model was trained on a separate labelled dataset and may have reduced reliability on multilingual or slang-heavy comments.",
    "Keyword-based topic detection is transparent but may miss implicit topics and can assign multiple categories to one comment.",
    "Comments containing claims about payouts, eligibility, or platform rules were not independently verified.",
    "Search-result based collection can introduce source-selection bias because the available videos influence which public comments are observed.",
]

for limitation in limitations:
    story.append(
        Paragraph(
            "• " + limitation,
            body_style
        )
    )

# =========================================================
# 9. CONCLUSION
# =========================================================

story.append(
    Paragraph(
        "9. Conclusion",
        heading_style
    )
)

story.append(
    Paragraph(
        "The collected sample shows that public discussion around "
        "the X monetisation change was primarily concerned with "
        "eligibility and access, original-content and repost rules, "
        "monetisation requirements, payouts, impressions, and "
        "small-creator participation. The highest engagement "
        "occurred around Aug 8 in comments responding to a video "
        "focused specifically on the monetisation change.",
        body_style
    )
)

story.append(
    Paragraph(
        "The Round 2 DistilBERT model provided a consistent "
        "sentiment classification framework, while time-based "
        "analysis showed observable shifts in the composition of "
        "the collected discussion. Because the final dataset is "
        "small and source-specific, the findings should be "
        "interpreted as patterns in the collected public comments "
        "rather than as estimates of the sentiment of all X users.",
        body_style
    )
)

# =========================================================
# BUILD
# =========================================================

doc.build(story)

print("=" * 70)
print("ROUND 3 ANALYTICAL REPORT CREATED")
print("=" * 70)

print("\nOutput:")
print(OUTPUT_FILE)

print("\nFinal dataset:")
print(f"Comments: {total_comments}")
print(f"Videos: {unique_videos}")

print("\nSentiment:")
print(f"Negative: {negative}")
print(f"Neutral: {neutral}")
print(f"Positive: {positive}")

print("\nEngagement:")
print(f"Mean: {mean_engagement:.2f}")
print(f"Spike threshold: {spike_threshold:.2f}")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)