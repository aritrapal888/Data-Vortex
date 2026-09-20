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

DAILY_SENTIMENT_FILE = (
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
    "round3/notebooks/"
    "Round3_Analysis_Notebook.pdf"
)

os.makedirs("round3/notebooks", exist_ok=True)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(SENTIMENT_FILE)
daily = pd.read_csv(DAILY_SENTIMENT_FILE)
engagement = pd.read_csv(ENGAGEMENT_FILE)
topics = pd.read_csv(TOPIC_FILE)

# =========================================================
# BASIC VALUES
# =========================================================

total_comments = len(df)
unique_videos = df["video_id"].nunique()

sentiment_counts = (
    df["sentiment_label"]
    .value_counts()
    .to_dict()
)

negative = sentiment_counts.get("Negative", 0)
neutral = sentiment_counts.get("Neutral", 0)
positive = sentiment_counts.get("Positive", 0)

avg_confidence = df["sentiment_confidence"].mean()

df["comment_published_at"] = pd.to_datetime(
    df["comment_published_at"],
    utc=True
)

earliest = df["comment_published_at"].min()
latest = df["comment_published_at"].max()

mean_engagement = df["comment_engagement"].mean()
median_engagement = df["comment_engagement"].median()
max_engagement = df["comment_engagement"].max()

# =========================================================
# PDF SETUP
# =========================================================

doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontSize=20,
    leading=24,
    spaceAfter=15,
)

heading_style = ParagraphStyle(
    "HeadingCustom",
    parent=styles["Heading2"],
    fontSize=14,
    leading=18,
    spaceBefore=12,
    spaceAfter=8,
)

body_style = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontSize=9.5,
    leading=14,
    spaceAfter=7,
)

small_style = ParagraphStyle(
    "SmallCustom",
    parent=styles["BodyText"],
    fontSize=8,
    leading=11,
)

story = []

# =========================================================
# TITLE
# =========================================================

story.append(
    Paragraph(
        "DATA VORTEX A'26 — ROUND 3",
        title_style
    )
)

story.append(
    Paragraph(
        "Real-Time Social Reaction Analysis Notebook",
        title_style
    )
)

story.append(
    Paragraph(
        "<b>Assigned Topic:</b> Public Reaction to a Platform "
        "Monetisation Change",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Platform/Event Focus:</b> X (Twitter) monetisation "
        "and the transition toward Original Content Rewards",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Analysis Dataset:</b> 40 manually reviewed public "
        "comments collected from YouTube videos discussing "
        "X monetisation changes.",
        body_style,
    )
)

story.append(Spacer(1, 10))

# =========================================================
# 1. DATASET OVERVIEW
# =========================================================

story.append(
    Paragraph(
        "1. Dataset Overview",
        heading_style
    )
)

overview_data = [
    ["Metric", "Value"],
    ["Final comments", str(total_comments)],
    ["Unique videos", str(unique_videos)],
    ["Duplicate comments", "0"],
    ["Earliest comment", str(earliest)],
    ["Latest comment", str(latest)],
    ["Total comment engagement", str(df["comment_engagement"].sum())],
    ["Maximum comment engagement", str(max_engagement)],
]

table = Table(overview_data, colWidths=[2.8 * inch, 3.6 * inch])

table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ])
)

story.append(table)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "The raw collection contained 326 comments. After "
        "platform/topic filtering, comment-quality review, and "
        "manual relevance review, 40 comments were retained for "
        "the final analytical dataset. The original raw dataset "
        "was preserved separately.",
        body_style,
    )
)

# =========================================================
# 2. DATA COLLECTION
# =========================================================

story.append(
    Paragraph(
        "2. Data Collection Method",
        heading_style
    )
)

story.append(
    Paragraph(
        "Public YouTube comments were collected using the "
        "YouTube Data API v3. Search queries focused on X "
        "monetisation, X creator monetisation, X creator revenue "
        "sharing, X monetisation in 2026, and Original Content "
        "Rewards. Video statistics and public comment metadata "
        "were collected together with timestamps and engagement "
        "counts.",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Raw collection:</b> 326 comments from 39 videos.",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Final analytical dataset:</b> 40 comments from 12 "
        "videos.",
        body_style,
    )
)

# =========================================================
# 3. PREPROCESSING
# =========================================================

story.append(
    Paragraph(
        "3. Preprocessing and Quality Control",
        heading_style
    )
)

preprocessing_points = [
    "Missing-value audit was performed.",
    "Duplicate comment IDs were checked.",
    "Clearly unrelated YouTube/Facebook and other unrelated videos were removed.",
    "Comments unrelated to the monetisation discussion were excluded during manual review.",
    "Extremely low-information and purely generic comments were reviewed.",
    "The raw collection was preserved and filtering was performed on derived datasets.",
    "The final dataset was sorted chronologically for time-based analysis.",
]

for point in preprocessing_points:
    story.append(
        Paragraph(
            "• " + point,
            body_style
        )
    )

# =========================================================
# 4. ROUND 2 MODEL
# =========================================================

story.append(
    Paragraph(
        "4. NLP Model Application",
        heading_style
    )
)

story.append(
    Paragraph(
        "The sentiment predictions were generated using the "
        "DistilBERT model developed and evaluated during Round 2. "
        "The locally saved Round 2 model was loaded together with "
        "its tokenizer and applied to each final Round 3 comment.",
        body_style,
    )
)

model_data = [
    ["Model", "DistilBERT"],
    ["Task", "3-class sentiment classification"],
    ["Labels", "Negative / Neutral / Positive"],
    ["Maximum sequence length", "128 tokens"],
    ["Round 3 comments analyzed", str(total_comments)],
    ["Average prediction confidence", f"{avg_confidence:.4f}"],
]

table = Table(
    model_data,
    colWidths=[2.8 * inch, 3.6 * inch]
)

table.setStyle(
    TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ])
)

story.append(table)

story.append(Spacer(1, 8))

story.append(
    Paragraph(
        "<b>Important limitation:</b> Model predictions are "
        "treated as model outputs rather than manually verified "
        "ground truth. This is especially important for short, "
        "multilingual, slang-heavy, or context-dependent comments.",
        body_style,
    )
)

# =========================================================
# 5. SENTIMENT DISTRIBUTION
# =========================================================

story.append(
    Paragraph(
        "5. Sentiment Distribution",
        heading_style
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
    colWidths=[2.5 * inch, 1.5 * inch, 1.5 * inch]
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
        "Neutral predictions form the largest category in the "
        "collected sample. Positive and negative predictions are "
        "present in smaller numbers. This indicates that the "
        "observed discussion contains substantial informational "
        "and question-oriented content in addition to explicit "
        "positive or negative reactions.",
        body_style,
    )
)

# =========================================================
# 6. TIME-BASED SENTIMENT
# =========================================================

story.append(
    Paragraph(
        "6. Time-Based Sentiment Analysis",
        heading_style
    )
)

story.append(
    Paragraph(
        "Daily sentiment proportions were calculated from the "
        "timestamped comments. A sentiment balance was defined as "
        "Positive percentage minus Negative percentage.",
        body_style,
    )
)

daily_table = [
    [
        "Date",
        "Negative",
        "Neutral",
        "Positive",
        "Total",
        "Balance",
    ]
]

for _, row in daily.iterrows():
    daily_table.append([
        str(row["date"]),
        str(int(row["Negative"])),
        str(int(row["Neutral"])),
        str(int(row["Positive"])),
        str(int(row["Total"])),
        f"{row['sentiment_balance']:.2f}",
    ])

table = Table(
    daily_table,
    colWidths=[
        1.15 * inch,
        0.65 * inch,
        0.65 * inch,
        0.65 * inch,
        0.55 * inch,
        0.75 * inch,
    ],
    repeatRows=1,
)

table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ])
)

story.append(table)

story.append(Spacer(1, 8))

story.append(
    Paragraph(
        "<b>Observed Shift 1:</b> The Aug 8–Aug 13 period moves "
        "from a positive/mixed balance toward increasingly "
        "negative or concern-oriented observations. The later "
        "dates in this sequence have small sample sizes, so this "
        "should be interpreted as an observed shift in the "
        "collected comments rather than a population-level "
        "statistical conclusion.",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Observed Shift 2:</b> Between Sep 6 and Sep 10, the "
        "sample moves from one neutral comment to a larger Sep 10 "
        "sample dominated by neutral/question-oriented comments "
        "with one negative prediction. This represents a weaker "
        "shift toward concern/question-oriented discussion.",
        body_style,
    )
)

# =========================================================
# 7. ENGAGEMENT
# =========================================================

story.append(
    Paragraph(
        "7. Engagement Spike Analysis",
        heading_style
    )
)

story.append(
    Paragraph(
        f"Mean comment engagement was {mean_engagement:.2f}, "
        f"median engagement was {median_engagement:.2f}, and the "
        f"standard deviation was "
        f"{df['comment_engagement'].std():.2f}. "
        "An engagement spike was defined as engagement greater "
        "than or equal to mean + 2 standard deviations.",
        body_style,
    )
)

engagement_table = [
    ["Date", "Engagement", "Video", "Comment"]
]

for _, row in engagement.iterrows():
    engagement_table.append([
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
    engagement_table,
    colWidths=[
        1.05 * inch,
        0.65 * inch,
        2.0 * inch,
        2.5 * inch,
    ],
    repeatRows=1,
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
        "Both detected spikes occurred on Aug 8 under the video "
        "\"X Monetization Just Changed... Again!\". The reactions "
        "focused on the newly discussed monetisation change, "
        "creator expectations, and payout implications. The "
        "payout multiple mentioned in one comment is treated as "
        "a commenter claim rather than independently verified "
        "fact.",
        body_style,
    )
)

# =========================================================
# 8. TOPICS AND ENTITIES
# =========================================================

story.append(
    Paragraph(
        "8. Topic and Entity Analysis",
        heading_style
    )
)

topic_rows = [
    ["Category", "Topic / Entity", "Comments", "Share"]
]

for _, row in topics.iterrows():
    topic_rows.append([
        row["category"],
        row["name"],
        str(int(row["comment_count"])),
        f"{row['percentage_of_comments']:.1f}%",
    ])

table = Table(
    topic_rows,
    colWidths=[
        1.0 * inch,
        3.0 * inch,
        0.8 * inch,
        0.8 * inch,
    ],
    repeatRows=1,
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
        "The most frequent detected topics were Eligibility & "
        "Access and Original Content & Reposts. Other recurring "
        "areas included monetisation rules, payouts/earnings, "
        "impressions/reach, and small creators.",
        body_style,
    )
)

story.append(
    Paragraph(
        "Topic percentages are keyword-based and are not "
        "mutually exclusive; one comment can contribute to more "
        "than one topic.",
        body_style,
    )
)

# =========================================================
# 9. TRIGGER INTERPRETATION
# =========================================================

story.append(
    Paragraph(
        "9. Trigger Explanations",
        heading_style
    )
)

triggers = [
    (
        "Monetisation-rule change",
        "The strongest concentration of engagement occurred "
        "around videos discussing the change to X monetisation."
    ),
    (
        "Eligibility and access",
        "Several comments focused on country eligibility, "
        "verification, account access, and whether particular "
        "creator/account types could participate."
    ),
    (
        "Original content and reposts",
        "Comments discussed original content, repost-related "
        "eligibility, and how creators should adapt their content."
    ),
    (
        "Impressions and creator thresholds",
        "Multiple comments asked how to reach or satisfy "
        "impression-related requirements."
    ),
]

for title, explanation in triggers:
    story.append(
        Paragraph(
            f"<b>{title}:</b> {explanation}",
            body_style,
        )
    )

# =========================================================
# 10. LIMITATIONS
# =========================================================

story.append(
    Paragraph(
        "10. Limitations",
        heading_style
    )
)

limitations = [
    "The dataset consists of public YouTube comments, not a complete sample of all X users.",
    "YouTube search results can contain videos with mixed or indirect relevance, requiring filtering.",
    "The final analytical sample contains only 40 comments.",
    "Several dates have very small numbers of comments, limiting the strength of daily sentiment comparisons.",
    "The Round 2 DistilBERT model was trained on a different labelled dataset and may be less reliable for multilingual slang-heavy comments.",
    "Keyword-based topic/entity analysis can miss implicit references and may assign multiple categories to one comment.",
    "Commenter statements about payouts, eligibility, or platform rules are observations or claims and were not independently treated as verified facts.",
]

for item in limitations:
    story.append(
        Paragraph(
            "• " + item,
            body_style
        )
    )

# =========================================================
# 11. CONCLUSION
# =========================================================

story.append(
    Paragraph(
        "11. Analytical Conclusion",
        heading_style
    )
)

story.append(
    Paragraph(
        "Within this collected sample, discussion around the X "
        "monetisation change was concentrated on eligibility and "
        "access, original-content/repost rules, monetisation "
        "requirements, payouts, and impressions. The largest "
        "engagement spikes occurred on Aug 8 around a video "
        "specifically discussing the monetisation change. "
        "Sentiment predictions were predominantly neutral, with "
        "smaller positive and negative groups. The observed "
        "temporal movements provide evidence of changing "
        "discussion patterns within the collected sample, while "
        "the small and platform-specific sample limits "
        "generalisation to the wider public.",
        body_style,
    )
)

# =========================================================
# BUILD PDF
# =========================================================

doc.build(story)

print("=" * 70)
print("ROUND 3 ANALYSIS NOTEBOOK PDF CREATED")
print("=" * 70)

print("\nOutput:")
print(OUTPUT_FILE)

print("\nDataset:")
print(f"Comments: {total_comments}")
print(f"Videos: {unique_videos}")
print(f"Sentiment confidence: {avg_confidence:.4f}")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)